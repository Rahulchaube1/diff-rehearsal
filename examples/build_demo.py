"""Regenerate the public workbook from a tiny, fictional two-commit repository."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    with tempfile.TemporaryDirectory() as temp:
        repo = Path(temp)
        env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
               "GIT_AUTHOR_NAME": "Example Engineer", "GIT_COMMITTER_NAME": "Example Engineer",
               "GIT_AUTHOR_EMAIL": "dev@example.invalid", "GIT_COMMITTER_EMAIL": "dev@example.invalid",
               "GIT_AUTHOR_DATE": "2025-02-10T12:00:00Z", "GIT_COMMITTER_DATE": "2025-02-10T12:00:00Z"}

        def git(*args):
            subprocess.run(["git", *args], cwd=repo, env=env, check=True, stdout=subprocess.DEVNULL)

        git("init", "-q", "--object-format=sha1", "-b", "main")
        (repo / "reservations.py").write_bytes(b"def reserve(stock, units):\n    return stock - units\n")
        git("add", ".")
        git("commit", "-qm", "Record inventory reservations")
        (repo / "reservations.py").write_bytes(
            b"def reserve(stock, units):\n    if units > stock:\n"
            b'        raise ValueError("insufficient stock")\n    return stock - units\n')
        (repo / "tests").mkdir()
        (repo / "tests/test_reservations.py").write_bytes(
            b"import unittest\n\nfrom reservations import reserve\n\n\n"
            b"class ReservationTests(unittest.TestCase):\n    def test_overbooking(self):\n"
            b"        with self.assertRaises(ValueError):\n            reserve(2, 3)\n")
        git("add", ".")
        git("commit", "-qm", "Reject orders that exceed available stock")
        subprocess.run([sys.executable, str(ROOT / "rehearse.py"), "--repo", str(repo),
                        "-o", str(destination)], check=True)


if __name__ == "__main__":
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "examples" / "rehearsal.html")
