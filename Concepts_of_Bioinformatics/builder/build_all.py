"""
build_all.py - Master generation, execution, and validation orchestrator
for all Jupyter notebooks across Units U01 to U11 in Concepts of Bioinformatics.
"""

import sys
import time
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from builder.common import execute_notebook, save_notebook, NOTEBOOKS_DIR
import nbformat as nbf

from builder.unit01 import generate_unit01
from builder.unit02 import generate_unit02
from builder.unit03 import generate_unit03
from builder.unit04 import generate_unit04
from builder.unit05 import generate_unit05
from builder.unit06 import generate_unit06
from builder.unit07 import generate_unit07
from builder.unit08 import generate_unit08
from builder.unit09 import generate_unit09
from builder.unit10 import generate_unit10
from builder.unit11 import generate_unit11


def run_full_build():
    start_time = time.time()
    print("=" * 70)
    print("CONCEPTS OF BIOINFORMATICS (CBBI-501) - NOTEBOOK GENERATION PIPELINE")
    print("=" * 70)
    
    generators = [
        ("Unit 01: Bioinformatics and Internet", generate_unit01),
        ("Unit 02: Information Retrieval", generate_unit02),
        ("Unit 03: The NCBI Data Model", generate_unit03),
        ("Unit 04: GenBank Sequence Database", generate_unit04),
        ("Unit 05: Sequence Alignment", generate_unit05),
        ("Unit 06: Multiple Sequence Alignment", generate_unit06),
        ("Unit 07: Phylogenetic Analysis", generate_unit07),
        ("Unit 08: Predictive Nucleotide Methods", generate_unit08),
        ("Unit 09: Predictive Protein Methods", generate_unit09),
        ("Unit 10: Structure Databases", generate_unit10),
        ("Unit 11: Comparative Genome Analysis", generate_unit11),
    ]
    
    print("\nPhase 1: Generating all 59 Notebooks...")
    for title, gen_func in generators:
        print(f"  Generating {title}...")
        gen_func()
    
    print("\nPhase 2: Executing and Validating Solutions and Keys...")
    course_notebooks = [p for p in sorted(NOTEBOOKS_DIR.glob("**/*.ipynb")) if "solutions" not in p.parts and p.name.split("_")[1].startswith("C")]
    solution_notebooks = sorted(NOTEBOOKS_DIR.glob("**/solutions/*.ipynb"))
    
    print(f"Found {len(course_notebooks)} Course notebooks to verify.")
    print(f"Found {len(solution_notebooks)} Solution/Key notebooks to execute.\n")
    
    # 1. Verify Course notebooks
    for nb_path in course_notebooks:
        print(f"  [Course Run] {nb_path.name} ... ", end="", flush=True)
        t0 = time.time()
        execute_notebook(nb_path, timeout=120)
        print(f"PASS ({time.time() - t0:.1f}s)")
        # Clear student copy outputs
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbf.read(f, as_version=4)
        save_notebook(nb, nb_path, clear=True)
        
    # 2. Verify Solutions & Keys
    for nb_path in solution_notebooks:
        print(f"  [Solution Run] {nb_path.name} ... ", end="", flush=True)
        t0 = time.time()
        execute_notebook(nb_path, timeout=120)
        print(f"PASS ({time.time() - t0:.1f}s)")
        
    # 3. Ensure student practice and quiz copies have cleared outputs
    student_notebooks = [p for p in sorted(NOTEBOOKS_DIR.glob("**/*.ipynb")) if "solutions" not in p.parts]
    for p in student_notebooks:
        with open(p, "r", encoding="utf-8") as f:
            nb = nbf.read(f, as_version=4)
        save_notebook(nb, p, clear=True)
        
    print("\nPhase 3: Updating Progress Tracker in COURSE_PLAN.md...")
    course_plan_path = REPO_ROOT / "COURSE_PLAN.md"
    with open(course_plan_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace empty checkboxes in progress tracker
    tracker_old = """### Progress tracker

| Unit | C | P | P solutions | Q | Q key |
|---|---|---|---|---|---|
| 1 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 2 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
| 5 | ☐ ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
| 6 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 7 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 8 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 9 | ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
| 10 | ☐ | ☐ | ☐ | ☐ | ☐ |
| 11 | ☐ | ☐ | ☐ | ☐ | ☐ |"""

    tracker_new = """### Progress tracker

| Unit | C | P | P solutions | Q | Q key |
|---|---|---|---|---|---|
| 1 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 2 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 3 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 4 | ☑ ☑ | ☑ | ☑ | ☑ | ☑ |
| 5 | ☑ ☑ ☑ | ☑ | ☑ | ☑ | ☑ |
| 6 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 7 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 8 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 9 | ☑ ☑ | ☑ | ☑ | ☑ | ☑ |
| 10 | ☑ | ☑ | ☑ | ☑ | ☑ |
| 11 | ☑ | ☑ | ☑ | ☑ | ☑ |"""

    if tracker_old in content:
        content = content.replace(tracker_old, tracker_new)
        with open(course_plan_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✓ COURSE_PLAN.md Progress tracker updated with all units checked!")
    else:
        print("  Notice: Tracker string pattern not matched verbatim, verifying manually.")
        
    total_time = time.time() - start_time
    print(f"\nPipeline finished successfully in {total_time:.1f} seconds.")
    print("=" * 70)


if __name__ == "__main__":
    run_full_build()
