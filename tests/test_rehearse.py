import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import rehearse


class WorkbookTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.repo = Path(directory.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args])

    def commit(self, message="change"):
        self.git("add", ".")
        self.git("commit", "-qm", message, "--allow-empty")
        return rehearse.inspect(self.repo, "HEAD")

    def test_root_binary_rename_and_special_names(self):
        (self.repo / "a file").write_bytes(b"x\x00y")
        root = self.commit()
        self.assertEqual(root["parents"], [])
        self.assertIsNone(root["files"][0]["added"])
        (self.repo / "a file").rename(self.repo / "new file")
        data = self.commit()
        self.assertEqual(data["files"][0]["previous"], "a file")
        self.assertEqual(data["files"][0]["path"], "new file")
        if os.name != "nt":
            (self.repo / "new file").rename(self.repo / "tab\there\n")
            self.assertEqual(self.commit()["files"][0]["path"], r"tab\there\n")

    def test_empty_and_untrusted_subject(self):
        title = "</script><script>alert(1)</script>"
        data = self.commit(title)
        self.assertEqual(data["files"], [])
        html = rehearse.render(data)
        self.assertNotIn(title, html)
        block = re.search(r'<script type="application/json" id="data">(.*?)</script>', html)
        self.assertEqual(json.loads(block[1])["subject"], title)

    def test_merge_against_first_parent(self):
        self.commit()
        self.git("checkout", "-qb", "feature")
        (self.repo / "feature").touch()
        self.commit()
        self.git("checkout", "-q", "main")
        (self.repo / "main").touch()
        self.commit()
        self.git("merge", "-q", "--no-ff", "-m", "merge", "feature")
        merge = rehearse.inspect(self.repo, "HEAD")
        self.assertEqual(len(merge["parents"]), 2)
        self.assertEqual([f["path"] for f in merge["files"]], ["feature"])

    def test_shallow_boundary(self):
        self.commit()
        self.commit()
        with tempfile.TemporaryDirectory() as target:
            self.git("clone", "-q", "--depth=1", self.repo.as_uri(), target)
            with self.assertRaisesRegex(ValueError, "Fetch more history"):
                rehearse.inspect(target, "HEAD")

    def test_existing_file_and_invalid_ref(self):
        self.commit()
        out = self.repo / "out.html"
        out.write_text("keep")
        cmd = [sys.executable, str(rehearse.ROOT / "rehearse.py"), "--repo", str(self.repo), "-o", str(out)]
        run = subprocess.run(cmd, capture_output=True)
        self.assertEqual(run.returncode, 1)
        self.assertEqual(out.read_text(), "keep")
        with self.assertRaises(ValueError):
            rehearse.inspect(self.repo, "--help")

    def test_data_and_test_questions(self):
        paths = ["migrations/add-index.sql", "spec/users.rb"]
        files = [dict(path=p, added=2, removed=0) for p in paths]
        questions = rehearse.questions(files)
        self.assertIn(paths[0], questions[1][1])
        self.assertIn(paths[1], questions[2][1])


if __name__ == "__main__":
    unittest.main()
