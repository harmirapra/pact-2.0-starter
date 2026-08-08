"""L3 -- pact doctor jako jediny kontrolor, overovany nad fixturami
fixtures/fresh/ (nedotcena sablona) a fixtures/filled/ (fiktivne vyplnena)."""

import subprocess
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
        sync = run_pact(self.repo, "sync", "--yes", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_warns_on_placeholders_and_exits_0(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN", result.stdout)
        self.assertIn("pact-setup", result.stdout)
        self.assertNotIn("FAIL", result.stdout)

    def test_doctor_reports_home_ok_after_confirmed_sync(self):
        """setUp synchronizuje s --yes -- $HOME musi souhlasit s kanonickym zdrojem."""
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertIn("$HOME odpovídá kanonickému zdroji", result.stdout)

    def test_doctor_warns_when_context_files_are_missing(self):
        """Prazdna slozka drive prosla jako 'kontext je vyplneny'."""
        for f in (self.repo / "2_Context" / "identity").rglob("*"):
            if f.is_file():
                f.unlink()

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chybí soubory kontextu", result.stdout)
        self.assertIn("2_Context/identity", result.stdout)
        self.assertNotIn("kontext je vyplněný", result.stdout)
        self.assertNotIn("FAIL", result.stdout)

    def test_doctor_warns_when_context_directory_does_not_exist(self):
        import shutil

        shutil.rmtree(self.repo / "2_Context" / "goals")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chybí soubory kontextu", result.stdout)
        self.assertIn("2_Context/goals", result.stdout)
        self.assertNotIn("FAIL", result.stdout)


class TestFilledFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="filled")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        sync = run_pact(self.repo, "sync", "--yes", home=self.home)
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
        run_pact(self.repo, "sync", "--yes", home=self.home)

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


class TestDoctorChecklistCompleteness(unittest.TestCase):
    """F9 -- doctor musi implementovat vsech osm kontrol ze sekce 3.7
    rozhodovaciho dokumentu, a kazda z nich musi v realnem behu skutecne
    vyprodukovat radek vystupu (ne jen existovat nekde v kodu)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="filled")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        sync = run_pact(self.repo, "sync", "--yes", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pocatecni stav (test)")
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "main"],
            cwd=str(self.repo), check=True,
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_all_eight_checks_from_section_3_7_produce_output(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        markers = {
            "nezacommitované změny": ("nezacommitované", "pracovní strom je čistý"),
            "nepushnuté commity": ("nepushnutých", "synchronizovaný s origin/main"),
            "placeholdery": ("kontext je vyplněný", "chybí soubory kontextu", "placeholdery"),
            "tajemství": ("tajemství",),
            "adaptéry v PACT": ("adaptéry odpovídají", "neodpovídá kanonickému zdroji"),
            "instalace v $HOME": (
                "$HOME odpovídá kanonickému zdroji", "$HOME neodpovídá", "$HOME: nic k instalaci",
            ),
            "osiřelé projekty (code.path)": ("code.path", "žádné projekty"),
            "rozbité odkazy": ("odkazy na neexistující soubory", "rozbitý odkaz"),
        }
        for label, options in markers.items():
            with self.subTest(kontrola=label):
                self.assertTrue(
                    any(opt in result.stdout for opt in options),
                    f"chybí výstup pro kontrolu '{label}' (3.7): {result.stdout}",
                )


if __name__ == "__main__":
    unittest.main()
