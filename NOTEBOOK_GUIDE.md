# Notebook Guide — Python `.ipynb` notebooks for the B.Tech. Bioinformatics courses

Instructions for adding Jupyter notebooks to any course folder under `btech/`. Each course's `COURSE_PLAN.md` lists *which* notebooks to build (its section 11); this file says *how* to build them so every course looks the same.

---

## 1. The three notebook types

| Type | Code | Purpose | Who writes code | Graded? |
|---|---|---|---|---|
| **Course** | `C` | Teaches one idea from the unit with explanation and worked examples. Used in the lecture or at the start of the practical. | Mostly the instructor; students run cells and change inputs | No |
| **Practice** | `P` | Exercises on the same idea, easy to hard, each with a self-check. Used in the practical or as homework. | Students fill `TODO` cells | No, or as part of the lab record |
| **Quiz** | `Q` | 8–12 short questions with instant right/wrong feedback and a score. Used at the end of a unit. | Students type answers into answer cells | Formative only (see §7) |

Every unit gets at least one `C`, one `P` and one `Q` notebook. A unit with several distinct ideas gets several `C` notebooks (`C1`, `C2`, …) and still one `P` and one `Q`.

**Relation to the official practicals.** The syllabus practicals use web servers and standalone tools (NCBI, BLAST, ClustalW, GLIMMER, VMD). Those stay as the recorded practicals. Notebooks sit beside them: they open up the tool and show what it computes, on small inputs.

**How much Python to assume.** Python for Bioinformatics (CBBI-511) is a Semester V course, so:

- Semester II–IV courses: students cannot be assumed to know Python. Course notebooks are *run and modify*: change a sequence, an accession, a parameter, then re-run. Practice `TODO`s are one to five lines with the pattern shown directly above. No task should need a student to design a function from nothing.
- Semester V onwards: practice notebooks may ask for whole functions.

---

## 2. Where notebooks go and how they are named

```
<Course_Folder>/
├── notebooks/
│   ├── U01_<Unit_Title>/
│   │   ├── U01_C1_<Topic>.ipynb
│   │   ├── U01_P_<Topic>.ipynb
│   │   ├── U01_Q_<Topic>.ipynb
│   │   └── solutions/
│   │       ├── U01_P_<Topic>_Solutions.ipynb
│   │       └── U01_Q_<Topic>_Key.ipynb
│   └── U02_<Unit_Title>/ ...
├── data/            read-only inputs (already in each course plan)
└── outputs/         everything notebooks write; git-ignored
```

| Thing | Convention | Example |
|---|---|---|
| Unit folder | `U<2-digit>_<Title>` matching the unit numbers in `COURSE_PLAN.md` | `U05_Sequence_Alignment` |
| Notebook | `U<unit>_<C/P/Q><n>_<Topic>.ipynb`; the number is only needed for multiple `C` notebooks | `U05_C2_Local_Alignment_and_Scoring.ipynb` |
| Solutions | same name + `_Solutions` (practice) or `_Key` (quiz), inside `solutions/` | `solutions/U05_P_Alignment_Solutions.ipynb` |
| Exercise IDs | `Ex <unit>.<n>` | `Ex 5.3` |
| Quiz question IDs | `q1`, `q2`, … | |
| Data files | lowercase, underscores, organism and gene in the name | `hbb_human_mrna.fasta` |
| Outputs | `outputs/<notebook id>/` | `outputs/U05_C2/` |

---

## 3. Environment

One environment for all courses: `btech/requirements.txt`.

```text
jupyterlab
biopython>=1.83
numpy
pandas
matplotlib
seaborn
scipy
requests
nbformat
nbval
pytest
```

Add a package only when a notebook needs it, and add it to this file in the same change. Every notebook must also run on Google Colab, because lab machines and student laptops vary: the setup cell (§4) installs anything Colab lacks.

---

## 4. Rules that apply to all three types

1. **Self-contained.** A notebook runs top to bottom on a fresh kernel with only `requirements.txt` installed. No imports from other notebooks.
2. **Offline first.** Read inputs from `data/`. A cell that calls a web service (Entrez, UniProt, RCSB) must be wrapped so that on failure it loads a saved copy from `data/` and prints that it did so. A dead network must never stop a class.
3. **Small and fast.** Whole notebook under two minutes to run; inputs small enough to print and inspect.
4. **Same molecules as the lectures.** Use the course's running examples (named in each course plan), so the notebook result can be compared with the web-tool result from the practical.
5. **No personal details or keys.** `Entrez.email` is set from a variable the student fills in; never commit a real address or an API key.
6. **Biology in every exercise.** Each task states the biological question first, the coding step second.
7. **Outputs.** Write files only to `outputs/`. Student copies are committed with outputs cleared; solution copies are committed with outputs kept.
8. **One idea per notebook.** 30–45 minutes for a course notebook, 45–60 for practice, 15–20 for a quiz.

### Header cell (markdown, first cell of every notebook)

```markdown
# U05 · C2 — Local Alignment and Scoring
**Course:** Concepts of Bioinformatics (CBBI-501) · **Unit 5:** Sequence Alignment and Database Searching
**Type:** Course notebook · **Time:** 40 min · **Difficulty:** ★★☆
**Goes with:** Lectures L12–L13, Practical S6 (BLAST)
**Before this:** U05_C1
```

### Setup cell (code, second cell of every notebook)

```python
import sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "biopython"], check=True)

NOTEBOOK_ID = "U05_C2"
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data").is_dir())
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs" / NOTEBOOK_ID
OUT_DIR.mkdir(parents=True, exist_ok=True)

import Bio
print("Python", sys.version.split()[0], "| Biopython", Bio.__version__)
```

On Colab the `data/` folder is not present by default. Add one cell above the setup cell that downloads the course `data/` folder once the repository location is fixed; until then, upload the needed files through the Colab file panel.

---

## 5. Course notebook (`C`) template

| # | Section | Content |
|---|---|---|
| 0 | Header | As above |
| 1 | What you will learn | 3–4 outcomes, each starting with a verb, each tagged with the course learning outcome (LO) it serves |
| 2 | Biological question | Two or three sentences: the problem this method solves, on the running example |
| 3 | Setup | Setup cell |
| 4 | Concept sections × 2–4 | For each: short theory (under 150 words, one figure or table if it helps) → worked example (commented code, small output) → **Try it** (change one input and predict the result before running) → **Common mistakes** (2–3 bullets) |
| 5 | Compare with the tool | Run or load the web-tool result for the same input and line it up with the notebook's result |
| 6 | Summary | Five-line recap and a small table of the functions used |
| 7 | Next | Link to the practice and quiz notebooks for the unit |

"Try it" cells must work unmodified, so a student who changes nothing still gets a correct run.

---

## 6. Practice notebook (`P`) template

| # | Section | Content |
|---|---|---|
| 0–1 | Header, setup | As above |
| 2 | Warm-up (★) | 3–4 exercises: direct use of one thing from the course notebook |
| 3 | Core (★★) | 3–4 exercises: combine two or three steps |
| 4 | Challenge (★★★) | 1–2 open exercises on real data from `data/`; optional for Semester II–IV |
| 5 | Reflection | 2–3 written questions answered in markdown ("why is the local score higher than the global score here?") |

Each exercise is three cells:

```markdown
### Ex 5.3 ★★ — Does the sickle-cell mutation change the alignment score?
**Biology:** HbS differs from HbA at one residue (E6V).
**Task:** Align the first 20 residues of each with BLOSUM62 and store the score in `score`.
**Expected:** a single number, a little lower than the self-alignment score.
```

```python
# TODO: replace the ... with your code
hba = "VHLTPEEKSAVTALWGKVNV"
hbs = ...
score = ...
```

```python
# Check — do not edit
assert isinstance(score, (int, float)), "score should be a number"
assert score < aligner.score(hba, hba), "a mismatch cannot score as high as identity"
print("Ex 5.3 passed")
```

Rules for practice notebooks:

- Check cells test the *result*, not the method, and give a message that says what is wrong.
- Never put the answer in the check cell. Compare against a property, or against a hash as in §7.
- The matching `_Solutions` notebook has every `TODO` filled in and must pass all its own checks when run from a fresh kernel.

---

## 7. Quiz notebook (`Q`) template

A quiz notebook is for self-testing. The answer check below stops a student from reading the answers by accident; it does not stop a determined one, since four options can simply be tried in turn. **Graded quizzes stay on paper or on the institute's LMS.**

| # | Section | Content |
|---|---|---|
| 0–1 | Header, setup | As above, plus the checker cell below |
| 2 | Section A — concept MCQs | 5–6 questions, one correct option each |
| 3 | Section B — read the output | 2–3 questions: a printed alignment, BLAST table, tree or plot is shown and the student answers from it |
| 4 | Section C — compute it | 2–3 questions: a short calculation in a code cell, numeric answer |
| 5 | Score | Score cell, then feedback on which course notebook section to revisit for each wrong answer |

Question mix: about half recall and understanding, half application. Every question is tagged with a learning outcome in a comment, so wrong answers point somewhere.

### Checker cell (code, directly after the setup cell)

```python
import hashlib

SALT = "U05_Q"                      # use the notebook ID
KEY = {                             # filled in by the instructor with make_key() below
    "q1": "3f1c9a0d2b7e",
    "q2": "a94e0c5512fd",
}
REVISIT = {"q1": "U05_C1 §4.1", "q2": "U05_C2 §4.3"}
results = {}

def _digest(answer):
    text = str(answer).strip().lower()
    return hashlib.sha256((SALT + text).encode()).hexdigest()[:12]

def check(qid, answer):
    """Record and report whether the answer to question qid is correct."""
    results[qid] = _digest(answer) == KEY[qid]
    print(f"{qid}: {'correct' if results[qid] else 'not yet — try again'}")

def show_score():
    done = sum(results.values())
    print(f"Score: {done} / {len(KEY)}")
    for qid in KEY:
        if not results.get(qid, False):
            print(f"  revisit {REVISIT[qid]} for {qid}")
```

### Question cells

```markdown
**q1.** Which alignment method is guaranteed to find the best *local* alignment?
(a) BLAST  (b) FASTA  (c) Smith–Waterman  (d) Needleman–Wunsch
```

```python
check("q1", "")     # type a, b, c or d between the quotes
```

Numeric answers are rounded before checking, and the question states the rounding:

```python
gc = ...                     # GC percentage of the sequence above
check("q7", round(gc, 1))    # one decimal place
```

### Making the key

The instructor keeps a `_Key` notebook in `solutions/` holding the plain answers and this cell, and pastes the printed dictionary into the student notebook:

```python
answers = {"q1": "c", "q2": "b", "q7": 52.4}
print({q: _digest(a) for q, a in answers.items()})
```

Changing `SALT` or any answer means regenerating the key.

---

## 8. Adding a notebook, step by step

1. Find the notebook in section 11 of the course's `COURSE_PLAN.md`. If it is new, add a row there first.
2. Put the input files in `data/` and record their source and accession in `data/README.md`.
3. Write the **solution** version first, start to finish, on a fresh kernel.
4. Copy it to the student name. For practice: replace answers with `TODO` stubs. For quiz: replace answers with empty `check()` calls and paste in the hashed key.
5. Restart and run all on both copies. The solution passes every check; the student copy runs without errors up to the first `TODO`.
6. Clear outputs in the student copy. Keep outputs in the solution copy.
7. Open the student copy in Colab and run the setup cell.
8. Go through the checklist below, then tick the notebook off in the course plan.

---

## 9. Checklist for every notebook

- [ ] File name and folder follow §2
- [ ] Header cell complete: course, unit, type, time, lectures and practical it goes with
- [ ] Runs top to bottom on a fresh kernel in under two minutes
- [ ] Works with the network unplugged (falls back to `data/`)
- [ ] Uses the course's running example molecules
- [ ] Every exercise or question states a biological question
- [ ] Every exercise has a check cell with a helpful failure message; no answers visible in student copies
- [ ] No real email address, API key or absolute path
- [ ] Writes only to `outputs/`
- [ ] Student copy has outputs cleared; solution or key copy exists and passes
- [ ] Opens and runs its setup cell on Colab
- [ ] Ticked off in section 11 of the course plan
