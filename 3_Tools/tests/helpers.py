"""Sdilene pomucky pro testy CLI 'pact'. Neni to test soubor sam o sobe."""

import os
import shutil
import subprocess
import sys
import hashlib
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PACT_BIN = TESTS_DIR.parent / "bin" / "pact"
FIXTURES_DIR = TESTS_DIR / "fixtures"


def make_sandbox(tmp_path, fixture_name=None):
    """Vytvori kopii kostry PACT (nebo pojmenovane fixtury) v tmp_path."""
    dest = Path(tmp_path) / "repo"
    if fixture_name:
        shutil.copytree(FIXTURES_DIR / fixture_name, dest)
    else:
        dest.mkdir()
        (dest / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
        for sub in (
            "1_Abilities/skills",
            "2_Context/identity/tone-of-voice",
            "2_Context/goals",
            "2_Context/expertise",
            "0_Projects/_TEMPLATE",
        ):
            (dest / sub).mkdir(parents=True, exist_ok=True)
    bin_dir = dest / "3_Tools" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PACT_BIN, bin_dir / "pact")
    (bin_dir / "pact").chmod(0o755)
    return dest


def add_skill(repo, name, description="Testovací dovednost. Use when: test.", extra_body=""):
    skill_dir = repo / "1_Abilities" / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n{extra_body}",
        encoding="utf-8",
    )
    return skill_dir


def run_pact(repo, *args, home=None, input_text=None, cwd=None, timeout=30):
    env = dict(os.environ)
    if home is not None:
        env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(repo / "3_Tools" / "bin" / "pact"), *args],
        cwd=str(cwd or repo),
        env=env,
        capture_output=True,
        text=True,
        input=input_text,
        timeout=timeout,
    )


def tree_signature(path):
    path = Path(path)
    if not path.exists():
        return None
    sig = []
    for f in sorted(path.rglob("*")):
        if f.is_file():
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            sig.append((str(f.relative_to(path)), h))
    return tuple(sig)


def git_init_repo(path):
    subprocess.run(["git", "init", "-q"], cwd=str(path), check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=str(path), check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=str(path), check=True)


def git_add_commit(path, message="test commit"):
    subprocess.run(["git", "add", "-A"], cwd=str(path), check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=str(path), check=True)
