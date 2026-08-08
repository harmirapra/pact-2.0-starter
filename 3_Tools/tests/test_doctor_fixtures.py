"""L3 -- pact doctor jako jediny kontrolor, overovany nad fixturami
fixtures/fresh/ (nedotcena sablona) a fixtures/filled/ (fiktivne vyplnena)."""

import tempfile
import unittest
from pathlib import Path

from helpers import make_sandbox, run_pact, git_init_repo, git_add_commit


class TestFreshFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="fresh")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        sync = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_warns_on_placeholders_and_exits_0(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN", result.stdout)
        self.assertIn("pact-setup", result.stdout)
        self.assertNotIn("FAIL", result.stdout)


class TestFilledFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="filled")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        sync = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_reports_no_fail_when_filled(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("FAIL", result.stdout)
        self.assertNotIn("[DOPLNIT", result.stdout)


class TestSecretDetection(unittest.TestCase):
    """A7 / A9 FAIL vetev: tajemstvi v trackovanem souboru musi doctor odhalit."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="filled")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        run_pact(self.repo, "sync", home=self.home)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_fails_on_tracked_secret(self):
        secret_file = self.repo / "3_Tools" / "api" / "leaked.txt"
        secret_file.parent.mkdir(parents=True, exist_ok=True)
        secret_file.write_text("sk-" + "x" * 32 + "\n", encoding="utf-8")

        git_init_repo(self.repo)
        git_add_commit(self.repo, "add fixture with secret (test only)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("tajemství", result.stdout)


if __name__ == "__main__":
    unittest.main()
