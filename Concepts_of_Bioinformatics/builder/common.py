"""
common.py - Common utilities for generating, formatting, executing,
and validating Jupyter notebooks for Concepts of Bioinformatics (CBBI-501).
"""

import sys
import os
import hashlib
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import nbformat as nbf
from nbclient import NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"


def digest_answer(salt: str, answer: Any) -> str:
    """Generate SHA-256 salted hash for quiz answers matching NOTEBOOK_GUIDE.md."""
    text = str(answer).strip().lower()
    return hashlib.sha256((salt + text).encode()).hexdigest()[:12]


def make_header_cell(
    notebook_id: str,
    title: str,
    unit_num: int,
    unit_title: str,
    nb_type: str,  # 'Course', 'Practice', 'Quiz', 'Practice Solutions', 'Quiz Key'
    time_min: int,
    difficulty: str,  # '★☆☆', '★★☆', '★★★'
    goes_with: str,
    before_this: str = "None"
) -> Any:
    """Construct standard markdown header cell according to NOTEBOOK_GUIDE.md §4."""
    md = f"""# {notebook_id} — {title}
**Course:** Concepts of Bioinformatics (CBBI-501) · **Unit {unit_num}:** {unit_title}
**Type:** {nb_type} notebook · **Time:** {time_min} min · **Difficulty:** {difficulty}
**Goes with:** {goes_with}
**Before this:** {before_this}
"""
    return nbf.v4.new_markdown_cell(md.strip())


def make_setup_cell(notebook_id: str) -> Any:
    """Construct standard setup code cell according to NOTEBOOK_GUIDE.md §4."""
    code = f'''import sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "biopython"], check=True)

NOTEBOOK_ID = "{notebook_id}"
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data").is_dir())
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs" / NOTEBOOK_ID
OUT_DIR.mkdir(parents=True, exist_ok=True)

import Bio
print("Python", sys.version.split()[0], "| Biopython", Bio.__version__)
'''
    return nbf.v4.new_code_cell(code.strip())


def make_quiz_checker_cell(salt: str, key_dict: Dict[str, str], revisit_dict: Dict[str, str]) -> Any:
    """Construct quiz answer verification cell according to NOTEBOOK_GUIDE.md §7."""
    code = f'''import hashlib

SALT = "{salt}"
KEY = {key_dict!r}
REVISIT = {revisit_dict!r}
results = {{}}

def _digest(answer):
    text = str(answer).strip().lower()
    return hashlib.sha256((SALT + text).encode()).hexdigest()[:12]

def check(qid, answer):
    """Record and report whether the answer to question qid is correct."""
    results[qid] = _digest(answer) == KEY[qid]
    print(f"{{qid}}: {{'correct' if results[qid] else 'not yet — try again'}}")

def show_score():
    done = sum(results.values())
    print(f"Score: {{done}} / {{len(KEY)}}")
    for qid in KEY:
        if not results.get(qid, False):
            print(f"  revisit {{REVISIT[qid]}} for {{qid}}")
'''
    return nbf.v4.new_code_cell(code.strip())


@dataclass
class PracticeExercise:
    ex_id: str          # e.g. "Ex 1.1"
    stars: str          # e.g. "★☆☆"
    title: str          # e.g. "Counting base composition"
    biology: str        # Biological rationale / context
    task: str           # What the student must compute
    expected: str       # Type and description of expected output
    student_code: str   # Code stub with # TODO and ...
    solution_code: str  # Fully completed working code
    check_code: str     # Assertions and print("Ex X.Y passed")


@dataclass
class QuizQuestion:
    qid: str            # e.g. "q1"
    prompt: str         # Question text
    options: List[str]  # e.g. ["(a) BLAST", "(b) FASTA", ...]
    answer: Any         # e.g. "c" or 52.4
    revisit: str        # e.g. "U05_C1 §4.1"
    is_code: bool = False
    code_setup: str = "" # If question has code to inspect / compute


def clear_outputs(nb: Any) -> None:
    """Strip all cell execution counts and outputs."""
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None


def save_notebook(nb: Any, path: Path, clear: bool = False) -> None:
    """Save notebook to file, optionally clearing outputs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if clear:
        clear_outputs(nb)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)


def execute_notebook(path: Path, timeout: int = 180) -> bool:
    """Execute a notebook in its own directory and save it back with outputs."""
    with open(path, "r", encoding="utf-8") as f:
        nb = nbf.read(f, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    try:
        client.execute()
        with open(path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        return True
    except Exception as e:
        print(f"Error executing {path.name}: {e}")
        raise e
