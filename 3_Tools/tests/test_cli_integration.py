"""L2 -- integracni testy: kazdy test bezi nad izolovanym piskovistem
(docasny adresar, prepsany $HOME), pact se vola jako podproces."""

import json
import tempfile
import unittest
from pathlib import Path

from helpers import make_sandbox, add_skill, run_pact, tree_signature, git_init_repo, git_add_commit


class BaseSandboxTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self.repo = make_sandbox(self.tmp_path)
        self.home = self.tmp_path / "home"
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()


class TestSyncBasics(BaseSandboxTest):
    def test_help_exits_zero(self):
        result = run_pact(self.repo, "--help", home=self.home)
        self.assertEqual(result.returncode, 0)

    def test_sync_dry_run_writes_nothing(self):
        add_skill(self.repo, "example-skill")
        result = run_pact(self.repo, "sync", "--dry-run", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Plánované operace", result.stdout)
        self.assertFalse((self.repo / ".agents").exists())
        self.assertFalse((self.repo / ".claude").exists())
        self.assertFalse((self.repo / ".github").exists())

    def test_sync_is_idempotent(self):
        add_skill(self.repo, "example-skill", extra_body="obsah dovednosti\n")
        r1 = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(r1.returncode, 0, r1.stderr)
        sig1 = tree_signature(self.repo / ".agents")
        r2 = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(r2.returncode, 0, r2.stderr)
        sig2 = tree_signature(self.repo / ".agents")
        self.assertEqual(sig1, sig2)
        self.assertEqual(
            (self.repo / ".github" / "copilot-instructions.md").read_bytes(),
            (self.repo / ".github" / "copilot-instructions.md").read_bytes(),
        )

    def test_sync_copies_skill_into_all_three_adapters(self):
        add_skill(self.repo, "example-skill")
        run_pact(self.repo, "sync", home=self.home)
        for adapter in (".agents", ".claude", ".github"):
            self.assertTrue(
                (self.repo / adapter / "skills" / "example-skill" / "SKILL.md").is_file(),
                adapter,
            )

    def test_sync_missing_description_exits_1(self):
        skill_dir = self.repo / "1_Abilities" / "skills" / "broken"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("---\nname: broken\n---\n", encoding="utf-8")
        result = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("broken", result.stderr)

    def test_sync_name_mismatch_exits_1(self):
        skill_dir = self.repo / "1_Abilities" / "skills" / "foo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: bar\ndescription: x\n---\n", encoding="utf-8"
        )
        result = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(result.returncode, 1)


class TestRegistry(BaseSandboxTest):
    def test_registry_row_count_matches_skill_count(self):
        add_skill(self.repo, "aaa-skill")
        add_skill(self.repo, "bbb-skill")
        result = run_pact(self.repo, "registry", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        registry = (self.repo / "1_Abilities" / "REGISTRY.md").read_text(encoding="utf-8")
        self.assertIn("aaa-skill", registry)
        self.assertIn("bbb-skill", registry)
        self.assertIn("Generováno", registry)

    def test_registry_dry_run_writes_nothing(self):
        add_skill(self.repo, "aaa-skill")
        result = run_pact(self.repo, "registry", "--dry-run", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Plánované operace", result.stdout)
        self.assertFalse((self.repo / "1_Abilities" / "REGISTRY.md").exists())

    def test_registry_invalid_frontmatter_exits_1(self):
        skill_dir = self.repo / "1_Abilities" / "skills" / "broken"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
        result = run_pact(self.repo, "registry", home=self.home)
        self.assertEqual(result.returncode, 1)


class TestProjectLifecycle(BaseSandboxTest):
    def test_new_single_root(self):
        result = run_pact(self.repo, "new", "muj-projekt", "--type", "single-root", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        project_md = self.repo / "0_Projects" / "muj-projekt" / "PROJECT.md"
        self.assertTrue(project_md.is_file())
        self.assertIn("type: single-root", project_md.read_text(encoding="utf-8"))

    def test_new_duplicate_exits_1(self):
        run_pact(self.repo, "new", "p", "--type", "single-root", home=self.home)
        result = run_pact(self.repo, "new", "p", "--type", "single-root", home=self.home)
        self.assertEqual(result.returncode, 1)

    def test_new_invalid_name_exits_2(self):
        result = run_pact(self.repo, "new", "Not_Valid", "--type", "single-root", home=self.home)
        self.assertEqual(result.returncode, 2)

    def test_new_missing_type_noninteractive_exits_2(self):
        result = run_pact(self.repo, "new", "p2", home=self.home)
        self.assertEqual(result.returncode, 2)

    def test_promote_then_doctor_then_cleanup(self):
        code_dir = self.tmp_path / "kod"
        code_dir.mkdir()
        git_init_repo(code_dir)
        (code_dir / "README.md").write_text("kod\n", encoding="utf-8")

        r_new = run_pact(self.repo, "new", "t", "--type", "single-root", home=self.home)
        self.assertEqual(r_new.returncode, 0, r_new.stderr)

        r_promote = run_pact(self.repo, "promote", "t", "--code-path", str(code_dir), home=self.home)
        self.assertEqual(r_promote.returncode, 0, r_promote.stderr)

        content = (self.repo / "0_Projects" / "t" / "PROJECT.md").read_text(encoding="utf-8")
        self.assertIn("type: dual-root", content)
        self.assertIn(str(code_dir), content)

        r_sync = run_pact(self.repo, "sync", home=self.home)
        self.assertEqual(r_sync.returncode, 0, r_sync.stderr)

        r_doctor = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(r_doctor.returncode, 0, r_doctor.stdout + r_doctor.stderr)
        self.assertNotIn("FAIL", r_doctor.stdout)

    def test_promote_already_dual_root_exits_0_noop(self):
        code_dir = self.tmp_path / "kod2"
        code_dir.mkdir()
        run_pact(self.repo, "new", "t2", "--type", "dual-root", "--code-path", str(code_dir), home=self.home)
        result = run_pact(self.repo, "promote", "t2", "--code-path", str(code_dir), home=self.home)
        self.assertEqual(result.returncode, 0)
        self.assertIn("není co dělat", result.stdout)

    def test_link_on_single_root_recommends_promote(self):
        run_pact(self.repo, "new", "t3", "--type", "single-root", home=self.home)
        result = run_pact(self.repo, "link", "t3", "--code-path", "/tmp/nope", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("promote", result.stderr)

    def test_link_nonexistent_path_exits_1(self):
        code_dir = self.tmp_path / "kod3"
        code_dir.mkdir()
        run_pact(self.repo, "new", "t4", "--type", "dual-root", "--code-path", str(code_dir), home=self.home)
        missing = self.tmp_path / "does-not-exist"
        result = run_pact(self.repo, "link", "t4", "--code-path", str(missing), home=self.home)
        self.assertEqual(result.returncode, 1)

    def test_link_non_git_path_exits_1(self):
        code_dir = self.tmp_path / "kod4"
        code_dir.mkdir()
        not_git = self.tmp_path / "not-git"
        not_git.mkdir()
        run_pact(self.repo, "new", "t5", "--type", "dual-root", "--code-path", str(code_dir), home=self.home)
        result = run_pact(self.repo, "link", "t5", "--code-path", str(not_git), home=self.home)
        self.assertEqual(result.returncode, 1)

    def test_link_generates_workspace_file(self):
        code_dir = self.tmp_path / "kod5"
        code_dir.mkdir()
        git_init_repo(code_dir)
        run_pact(self.repo, "new", "t6", "--type", "dual-root", "--code-path", str(code_dir), home=self.home)
        result = run_pact(self.repo, "link", "t6", "--code-path", str(code_dir), "--workspace", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        ws_path = self.repo.parent / "workspaces" / "t6.code-workspace"
        self.assertTrue(ws_path.is_file())
        data = json.loads(ws_path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["folders"]), 2)

    def test_link_workspace_warns_about_writing_outside_repo(self):
        # C4: --workspace zapisuje mimo repo (REPO_ROOT.parent), uzivatel
        # o tom musi byt informovan.
        code_dir = self.tmp_path / "kod5b"
        code_dir.mkdir()
        git_init_repo(code_dir)
        run_pact(self.repo, "new", "t6b", "--type", "dual-root", "--code-path", str(code_dir), home=self.home)
        result = run_pact(self.repo, "link", "t6b", "--code-path", str(code_dir), "--workspace", home=self.home)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("POZOR", result.stdout)
        self.assertIn("mimo", result.stdout)


class TestDoctorBasics(BaseSandboxTest):
    def test_doctor_fails_on_invalid_frontmatter(self):
        skill_dir = self.repo / "1_Abilities" / "skills" / "broken"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)

    def test_doctor_fails_when_adapters_stale(self):
        add_skill(self.repo, "example-skill")
        run_pact(self.repo, "sync", home=self.home)
        add_skill(self.repo, "example-skill", extra_body="ZMENENO\n")
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("pact sync", result.stdout)

    def test_doctor_reports_no_broken_links_by_default(self):
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "init (test)")
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("žádné odkazy na neexistující soubory", result.stdout)
        self.assertIn("žádné tajemství v trackovaných souborech", result.stdout)

    def test_doctor_warns_instead_of_false_ok_outside_git_repo(self):
        """C1: mimo git repozitar nelze zjistit trackovane soubory -- kontroly
        tajemstvi a rozbitych odkazu musi na to upozornit (WARN), ne tise
        nahlasit OK, jako by bylo vsechno zkontrolovano."""
        run_pact(self.repo, "sync", home=self.home)
        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN  nelze zkontrolovat tajemství", result.stdout)
        self.assertIn("WARN  nelze zkontrolovat odkazy", result.stdout)
        self.assertNotIn("žádné tajemství v trackovaných souborech", result.stdout)
        self.assertNotIn("žádné odkazy na neexistující soubory", result.stdout)

    def test_doctor_fails_on_broken_markdown_link(self):
        readme = self.repo / "2_Context" / "expertise" / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text("## Oblasti\n\n[neexistujici](neexistujici.md)\n", encoding="utf-8")
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pridat rozbity odkaz (test)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("rozbitý odkaz", result.stdout)

    def test_doctor_fails_on_broken_bullet_file_reference(self):
        """Presne vzor z N-5: '- soubor.md — popis' na neexistujici soubor."""
        readme = self.repo / "2_Context" / "expertise" / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text("## Oblasti\n\n- pojistovnictvi.md — popis oblasti.\n", encoding="utf-8")
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pridat vymysleny odkaz (test)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 1)
        self.assertIn("pojistovnictvi.md", result.stdout)

    def test_doctor_ignores_placeholder_and_prose_filenames(self):
        """Falesne poplachy: [DOPLNIT: ...] a jmeno souboru zminene v bezne vete nejsou odkazy."""
        readme = self.repo / "2_Context" / "expertise" / "README.md"
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            "## Oblasti\n\n"
            "[DOPLNIT: seznam souboru v teto slozce, napr. procesy.md]\n\n"
            "V textu zminuji soubor nastroje.md, ale neni to odkaz.\n",
            encoding="utf-8",
        )
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "placeholder a proza (test)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("FAIL", result.stdout)

    def test_doctor_warns_on_unqualified_vendor_mention_in_skill(self):
        add_skill(
            self.repo, "vendor-locked",
            extra_body="Po dokoncenych krocich spust `/clear` a pokracuj.\n",
        )
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pridat vendor-specifickou dovednost (test)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("WARN", result.stdout)
        self.assertIn("vendor-locked", result.stdout)

    def test_doctor_does_not_warn_on_qualified_vendor_example(self):
        add_skill(
            self.repo, "vendor-example",
            extra_body="U Claude Code typicky spustis `/clear`; jiny nastroj ma vlastni ekvivalent.\n",
        )
        run_pact(self.repo, "sync", home=self.home)
        git_init_repo(self.repo)
        git_add_commit(self.repo, "pridat kvalifikovany priklad (test)")

        result = run_pact(self.repo, "doctor", home=self.home)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("vendor-example", result.stdout)


if __name__ == "__main__":
    unittest.main()
