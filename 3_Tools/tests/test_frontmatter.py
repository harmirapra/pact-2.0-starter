"""L1 -- unit testy: parser frontmatteru/scope.yml, validace, cisté funkce."""

import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path

PACT_PATH = Path(__file__).resolve().parents[1] / "bin" / "pact"


def load_pact_module():
    loader = importlib.machinery.SourceFileLoader("pact_cli_under_test", str(PACT_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


pact = load_pact_module()


class TestYamlLite(unittest.TestCase):
    def test_flat_scalars(self):
        self.assertEqual(
            pact.parse_yaml_lite("name: foo\ntype: bar\n"),
            {"name": "foo", "type": "bar"},
        )

    def test_list_of_strings(self):
        self.assertEqual(
            pact.parse_yaml_lite("items:\n  - a\n  - b\n"),
            {"items": ["a", "b"]},
        )

    def test_nested_mapping_one_level(self):
        text = "code:\n  path: ../x\n  remote: git@x\n"
        self.assertEqual(
            pact.parse_yaml_lite(text),
            {"code": {"path": "../x", "remote": "git@x"}},
        )

    def test_two_level_mapping_with_lists(self):
        text = "user_level:\n  context:\n    - a.md\n    - b/\n  skills: []\n"
        self.assertEqual(
            pact.parse_yaml_lite(text),
            {"user_level": {"context": ["a.md", "b/"], "skills": []}},
        )

    def test_folded_scalar_joins_lines(self):
        text = "description: >\n  hello\n  world\n"
        self.assertEqual(pact.parse_yaml_lite(text)["description"], "hello world")

    def test_literal_scalar_keeps_newlines(self):
        text = "description: |\n  line1\n  line2\n"
        self.assertEqual(pact.parse_yaml_lite(text)["description"], "line1\nline2")

    def test_empty_list_marker(self):
        self.assertEqual(pact.parse_yaml_lite("skills: []\n"), {"skills": []})

    def test_trailing_comment_stripped(self):
        self.assertEqual(pact.parse_yaml_lite("skills: []   # poznamka\n"), {"skills": []})

    def test_quoted_scalar_unquoted(self):
        self.assertEqual(pact.parse_yaml_lite('name: "foo bar"\n'), {"name": "foo bar"})

    def test_invalid_line_raises(self):
        with self.assertRaises(pact.PactError):
            pact.parse_yaml_lite("not a valid line\n")


class TestSplitFrontmatter(unittest.TestCase):
    def test_no_frontmatter(self):
        fm, body = pact.split_frontmatter("jen obycejny text\n")
        self.assertIsNone(fm)

    def test_with_frontmatter(self):
        text = "---\nname: x\n---\ntelo\n"
        fm, body = pact.split_frontmatter(text)
        self.assertEqual(fm.strip(), "name: x")
        self.assertEqual(body, "telo\n")

    def test_unterminated_frontmatter(self):
        fm, body = pact.split_frontmatter("---\nname: x\n")
        self.assertIsNone(fm)


class TestValidateSkills(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmp.name)
        self._orig_skills_dir = pact.SKILLS_DIR
        pact.SKILLS_DIR = self.tmp_path

    def tearDown(self):
        pact.SKILLS_DIR = self._orig_skills_dir
        self._tmp.cleanup()

    def _write_skill(self, name, content):
        skill_dir = self.tmp_path / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        return skill_dir

    def test_valid_skill(self):
        self._write_skill("foo", "---\nname: foo\ndescription: Use when testing.\n---\nbody\n")
        result = pact.validate_skills()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "foo")

    def test_missing_skill_md_raises(self):
        (self.tmp_path / "foo").mkdir()
        with self.assertRaises(pact.PactError):
            pact.validate_skills()

    def test_missing_frontmatter_raises(self):
        self._write_skill("foo", "zadny frontmatter\n")
        with self.assertRaises(pact.PactError):
            pact.validate_skills()

    def test_missing_description_raises(self):
        self._write_skill("foo", "---\nname: foo\n---\nbody\n")
        with self.assertRaises(pact.PactError):
            pact.validate_skills()

    def test_name_mismatch_raises(self):
        self._write_skill("foo", "---\nname: bar\ndescription: x\n---\n")
        with self.assertRaises(pact.PactError):
            pact.validate_skills()

    def test_empty_skills_dir_ok(self):
        self.assertEqual(pact.validate_skills(), [])


class TestNameRegex(unittest.TestCase):
    def test_valid_kebab_case(self):
        for name in ("foo", "foo-bar", "foo-bar-2"):
            self.assertTrue(pact.NAME_RE.match(name), name)

    def test_invalid_names(self):
        for name in ("Foo", "foo_bar", "-foo", "foo-", "foo--bar", ""):
            self.assertFalse(pact.NAME_RE.match(name), name)


class TestTemplateExtraction(unittest.TestCase):
    def test_extract_known_block(self):
        block = pact._extract_template_block(pact.FALLBACK_PROJECT_TEMPLATE, "single-root")
        self.assertIn("type: single-root", block)
        self.assertNotIn("dual-root", block)

    def test_extract_unknown_block_raises(self):
        with self.assertRaises(pact.PactError):
            pact._extract_template_block(pact.FALLBACK_PROJECT_TEMPLATE, "nope")


if __name__ == "__main__":
    unittest.main()
