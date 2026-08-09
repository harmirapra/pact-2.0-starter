"""L3 -- pact doctor jako jediny kontrolor, overovany nad fixturami
fixtures/fresh/ (nedotcena sablona) a fixtures/filled/ (fiktivne vyplnena),
a nad skutecnym 'git clone' tohoto repa -- kotva ve skutecnosti, kterou
zastupne fixtury nemohou nahradit (vada E, fix-brief-02)."""

import subprocess
import tempfile
import unittest
from pathlib import Path

from helpers import make_sandbox, add_skill, run_pact, git_init_repo, git_add_commit

# Koren tohoto repa (PACT-2.0), ne sandboxu -- pro test proti skutecnemu klonu.
REAL_REPO_ROOT = Path(__file__).resolve().parents[2]


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
        sync = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)

    def tearDown(self):
        self._tmp.cleanup()

    def test_doctor_reports_no_fail_when_filled(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("FAIL", result.stdout)
        self.assertNotIn("[DOPLNIT", result.stdout)

    def test_doctor_warns_when_source_note_is_missing(self):
        about_me = self.repo / "2_Context" / "identity" / "about-me.md"
        about_me.write_text(
            "# O mně\n\nVyplněný kontext bez provenance.\n",
            encoding="utf-8",
        )

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN  chybí poznámka o zdroji", result.stdout)
        self.assertIn("2_Context/identity/about-me.md", result.stdout)
        self.assertNotIn("FAIL", result.stdout)

    def test_doctor_ignores_context_files_without_provenance_requirement(self):
        context = self.repo / "2_Context"
        (context / "stack.md").write_text("Provozní manifest.\n", encoding="utf-8")
        (context / "quality-criteria.md").write_text("Pravidla kvality.\n", encoding="utf-8")
        (context / "expertise" / "README.md").write_text("Rozcestník.\n", encoding="utf-8")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK    poznámky o zdroji jsou doplněné", result.stdout)
        self.assertNotIn("chybí poznámka o zdroji", result.stdout)


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


class TestDoctorChecklistCompleteness(unittest.TestCase):
    """F9 -- doctor musi implementovat vsech osm aktualnich kontrol
    (kontrola $HOME byla zrusena fix-brief-03 a FIX04 pridava provenance),
    a kazda z nich musi v realnem behu skutecne vyprodukovat radek vystupu
    (ne jen existovat nekde v kodu)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path, fixture_name="filled")
        self.home = self.tmp_path / "home"
        self.home.mkdir()
        sync = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(sync.returncode, 0, sync.stderr)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pocatecni stav (test)")
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "main"],
            cwd=str(self.repo), check=True,
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_all_eight_checks_produce_output(self):
        result = run_pact(self.repo, "doctor", home=self.home)
        markers = {
            "nezacommitované změny": ("nezacommitované", "pracovní strom je čistý"),
            "nepushnuté commity": ("nepushnutých", "synchronizovaný s origin/main"),
            "placeholdery": ("kontext je vyplněný", "chybí soubory kontextu", "placeholdery"),
            "poznámky o zdroji": ("poznámky o zdroji jsou doplněné", "chybí poznámka o zdroji"),
            "tajemství": ("tajemství",),
            "adaptéry v PACT": ("adaptéry odpovídají", "neodpovídá kanonickému zdroji"),
            "osiřelé projekty (code.path)": ("code.path", "žádné projekty"),
            "rozbité odkazy": ("odkazy na neexistující soubory", "rozbitý odkaz"),
        }
        for label, options in markers.items():
            with self.subTest(kontrola=label):
                self.assertTrue(
                    any(opt in result.stdout for opt in options),
                    f"chybí výstup pro kontrolu '{label}' (3.7): {result.stdout}",
                )


class TestNeverSynced(unittest.TestCase):
    """Vada D -- adaptery, ktere jeste nikdy neexistovaly (pred prvnim
    'pact sync'), musi hlasit WARN, ne FAIL. Na rozdil od TestFreshFixture
    tenhle sandbox 'sync' v setUp vubec nespousti."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path)
        add_skill(self.repo, "example-skill")
        self.home = self.tmp_path / "home"
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_adapters_before_first_sync_warn_not_fail(self):
        self.assertFalse((self.repo / ".agents").exists())
        self.assertFalse((self.repo / ".claude").exists())
        self.assertFalse((self.repo / ".github").exists())

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("FAIL", result.stdout)
        self.assertIn("adaptéry ještě nebyly vygenerovány", result.stdout)

    def test_partially_synced_adapters_are_fail_not_warn(self):
        """Castecny/rozjety stav (nekonzistence) neni totez jako 'nenastaveno'."""
        run_pact(self.repo, "sync", home=self.home)
        import shutil

        shutil.rmtree(self.repo / ".claude")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)
        self.assertIn(".claude/skills", result.stdout)


class TestRealGitClone(unittest.TestCase):
    """Vada E -- kotva ve skutecnosti. Fixtura fresh/ nema 1_Abilities/skills/,
    takze kontrola adapteru nema co porovnavat a projde i nad produktem,
    ktery ve skutecnem klonu pada (N-11). 'git clone' zaruci, ze se
    gitignorovane adaptery neprenesou -- presne ta podminka, kterou
    fixtura postrada."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.clone = self.tmp_path / "clone"
        subprocess.run(
            ["git", "clone", "-q", str(REAL_REPO_ROOT), str(self.clone)],
            check=True, timeout=60,
        )
        self.home = self.tmp_path / "home"
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_fresh_clone_doctor_has_no_fail(self):
        result = run_pact(self.clone, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
