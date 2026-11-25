#!/usr/bin/env python3
"""Build a self-contained engineering interview workbook for a local Git commit."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def git(repo, *args):
    command = ["git", "--no-pager", "--no-replace-objects", "-C", str(repo), *args]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Git could not read this commit.")
    return result.stdout


def display(raw):
    return "".join(c if c.isprintable() else ascii(c)[1:-1]
                   for c in raw.decode("utf-8", errors="backslashreplace"))


def changes(raw):
    """Decode --numstat -z, including binary files and rename path pairs."""
    fields = iter(raw.split(b"\0"))
    files = []
    for entry in fields:
        if not entry:
            break
        added, removed, name = entry.split(b"\t", 2)
        previous = None
        if not name:
            previous, name = display(next(fields)), next(fields)
        files.append(dict(path=display(name), previous=previous,
                          added=None if added == b"-" else int(added),
                          removed=None if removed == b"-" else int(removed)))
    return files


def inspect(repo, ref):
    sha = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()
    # Read real parents from the object. A shallow boundary must not look like a root.
    headers = git(repo, "cat-file", "-p", sha).split(b"\n\n", 1)[0]
    parents = [line[7:].decode() for line in headers.splitlines() if line.startswith(b"parent ")]
    base = parents[:1]
    if base:
        try:
            git(repo, "cat-file", "-e", base[0] + "^{commit}")
        except ValueError as error:
            raise ValueError("The parent commit is unavailable. Fetch more history and retry.") from error
    raw = git(repo, "diff-tree", "--root", "-r", "--no-commit-id", "--numstat", "-z",
              "--find-renames", "--no-ext-diff", "--no-textconv", *base, sha, "--")
    title = display(git(repo, "show", "-s", "--no-show-signature", "--format=%s", sha).rstrip(b"\n"))
    return dict(sha=sha, subject=title, parents=parents, files=changes(raw))


def role(path):
    parts = path.lower().split("/")
    name = parts[-1]
    if (any(x in {"test", "tests", "__tests__", "spec", "specs"} for x in parts)
            or name.startswith("test_") or any(x in name for x in (".spec.", ".test.", "_test."))):
        return "test"
    if "migrations" in parts or name.endswith(".sql"):
        return "data"
    if "docs" in parts or name.endswith((".md", ".rst", ".adoc")):
        return "docs"
    if ".github" in parts or name in {"dockerfile", "makefile"} or name.endswith((".yml", ".yaml", ".toml")):
        return "config"
    return "implementation"


def questions(files):
    ranked = sorted(files, key=lambda f: -(sum((f["added"] or 0, f["removed"] or 0))))
    groups = {}
    for file in ranked:
        groups.setdefault(role(file["path"]), file["path"])
    focus = next((groups[k] for k in ("data", "implementation", "config", "docs", "test") if k in groups), None)
    test = groups.get("test")
    if not focus:
        decision = "This commit has no file changes against its base. What did recording it communicate?"
    elif "data" in groups:
        decision = f"What transition does {focus} introduce? Compare it with a staged migration."
    elif "implementation" in groups:
        decision = f"Why put this change in {focus}? Describe one other place or layer you considered."
    elif "config" in groups:
        decision = f"Which environment picks up {focus}, and what happens during a partial rollout?"
    elif "docs" in groups:
        decision = f"Which reader decision changes because of {focus}? How could you test that with a reader?"
    else:
        decision = f"What behavior does {focus} pin down? Describe an implementation it should still allow."
    verification = (f"Walk through one case in {test}. What nearby failure could still pass that check?"
                    if test else "Which observation would distinguish success from a silent regression? Describe how to reproduce it.")
    return [
        ["Context", "What problem was worth changing?", "Describe the previous behavior, who experienced it and your part in the work.", "Name one concrete before-state."],
        ["Decision", decision, "Compare two plausible choices under a constraint you actually faced.", "Name the trade-off and who bears its cost."],
        ["Verification", verification, "Describe an input, an expected observation and a counterexample. Inspect the commit locally if needed.", "Distinguish a test you ran from one you would add."],
        ["Outcome", "What happened after this change reached users?", "Give an observed result and its source, or state what remains unknown and how you would measure it.", "Credit collaborators and label estimates."],
    ]


def render(data):
    payload = json.dumps({**data, "questions": questions(data["files"])}, ensure_ascii=True)
    # A commit subject or path can contain an HTML closing tag.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return (ROOT / "workbook.html").read_text(encoding="utf-8").replace("__COMMIT_JSON__", payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ref", nargs="?", default="HEAD", help="commit, branch, or tag (default HEAD)")
    parser.add_argument("--repo", default=".", type=Path, help="local Git working tree or bare repository")
    parser.add_argument("-o", "--output", type=Path, default=Path("rehearsal.html"))
    args = parser.parse_args()
    try:
        content = render(inspect(args.repo, args.ref))
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except FileExistsError:
        parser.exit(1, f"{args.output} already exists. Choose another path with -o.\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not build workbook: {error}\n")
    print(f"Open {os.path.abspath(args.output)} in your browser.")


if __name__ == "__main__":
    main()
