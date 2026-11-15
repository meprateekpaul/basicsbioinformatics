"""
unit09.py - Builder for Unit 09: Predictive Methods using Protein Sequence
Notebooks:
- U09_C1_Protein_Properties_and_Motifs.ipynb
- U09_C2_Secondary_Structure_Prediction_Scoring.ipynb
- U09_P_Protein_Prediction.ipynb
- solutions/U09_P_Protein_Prediction_Solutions.ipynb
- U09_Q_Predictive_Protein.ipynb
- solutions/U09_Q_Predictive_Protein_Key.ipynb
"""

import sys
from pathlib import Path
import nbformat as nbf

from .common import (
    REPO_ROOT,
    NOTEBOOKS_DIR,
    digest_answer,
    make_header_cell,
    make_setup_cell,
    make_quiz_checker_cell,
    save_notebook,
    PracticeExercise,
    QuizQuestion
)

UNIT_DIR = NOTEBOOKS_DIR / "U09_Predictive_Protein"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u09_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U09_C1",
        title="Protein Properties and Motifs",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L23–L24, Practical S10 (ProtParam & PROSITE)",
        before_this="U08_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Compute** fundamental physicochemical properties (molecular weight, pI, GRAVY hydropathy) using Biopython's `Bio.SeqUtils.ProtParam` [LO6].
- **Generate** Kyte–Doolittle hydropathy plots to contrast soluble globular proteins with hydrophobic transmembrane helices [LO6].
- **Translate** PROSITE regular expression syntax (`[LIVM]`, `x(2,4)`, `{C}`) into standard Python regex [LO6].
- **Quantify** how a single pathogenic amino acid substitution (HbS Glu6Val) shifts molecular weight, isoelectric point, and surface hydrophobicity [LO6].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Sickle-cell hemoglobin (HbS) polymerizes into rigid fibers under low oxygen tension, causing erythrocyte sickling and vaso-occlusive crises. Biochemically, why does substituting a single residue (glutamic acid to valine at position 6) produce such catastrophic polymerization? How do computational sequence analysis tools quantify the change in molecular weight, net charge (pI), and hydrophobicity?
"""))

    nb.cells.append(make_setup_cell("U09_C1"))

    # Concept 1: ProtParam
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Physicochemical Properties with ProtParam
### Theory
Expasy ProtParam computes physical and chemical parameters based on primary sequence:
1. **Molecular Weight ($M_r$)**: Sum of isotopic average masses of amino acids minus $(N-1) \\times 18.015$ Da (water lost in peptide bond formation).
2. **Isoelectric Point (pI)**: The pH at which the protein carries net zero electrical charge. Acidic residues (Asp, Glu) lower the pI; basic residues (Lys, Arg, His) raise the pI.
3. **GRAVY (Grand Average of Hydropathy)**: Average of Kyte–Doolittle hydropathy values across all residues. Negative values indicate hydrophilic/globular proteins; positive values indicate hydrophobic/transmembrane proteins.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Comparing Normal HbA vs Sickle-Cell HbS with ProtParam
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

hbb_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq)
hbs_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbs_human_protein.fasta", "fasta").seq)

pa_hbb = ProteinAnalysis(hbb_seq)
pa_hbs = ProteinAnalysis(hbs_seq)

print("=== Normal Adult Hemoglobin Beta (HbA) ===")
print(f"Length:           {len(hbb_seq)} amino acids")
print(f"Molecular Weight: {pa_hbb.molecular_weight():.2f} Da")
print(f"Isoelectric (pI): {pa_hbb.isoelectric_point():.2f}")
print(f"GRAVY Score:      {pa_hbb.gravy():.3f} (Globular/Soluble)")

print("\\n=== Sickle-Cell Hemoglobin (HbS Glu6Val) ===")
print(f"Length:           {len(hbs_seq)} amino acids")
print(f"Molecular Weight: {pa_hbs.molecular_weight():.2f} Da")
print(f"Isoelectric (pI): {pa_hbs.isoelectric_point():.2f}")
print(f"GRAVY Score:      {pa_hbs.gravy():.3f} (Shifted more hydrophobic)")

mw_diff = pa_hbs.molecular_weight() - pa_hbb.molecular_weight()
pi_diff = pa_hbs.isoelectric_point() - pa_hbb.isoelectric_point()
print(f"\\nNet effect of Glu6Val: MW shift = {mw_diff:.2f} Da | pI shift = {pi_diff:+.2f} pH units")
'''))

    # Concept 2: Hydropathy Plot
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Kyte–Doolittle Hydropathy Profiles
### Theory
Kyte and Doolittle (1982) assigned an empirical hydropathy value to each of the 20 amino acids (from Isoleucine $+4.5$ to Arginine $-4.5$).
A sliding window computes local hydrophobicity along the peptide chain:
- Peaks $> +1.6$ (over a 19–21 residue window) indicate **transmembrane alpha-helices**.
- Mostly negative regions ($< 0$) indicate **water-exposed, hydrophilic loops**.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Plotting Kyte-Doolittle Hydropathy Profile for HBB
import matplotlib.pyplot as plt
from Bio.SeqUtils.ProtParam import ProtParamData

window_size = 9
# ProteinAnalysis.protein_scale returns a list of window averages
kd_scores = pa_hbb.protein_scale(ProtParamData.kd, window=window_size)
positions = list(range(window_size // 2, window_size // 2 + len(kd_scores)))

fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(positions, kd_scores, color="navy", lw=1.5)
ax.axhline(0, color="gray", linestyle="--", alpha=0.7)
ax.axhline(1.6, color="red", linestyle=":", alpha=0.7, label="Transmembrane threshold (>1.6)")
ax.set_xlabel("Amino Acid Position")
ax.set_ylabel("Hydropathy Score (Kyte-Doolittle)")
ax.set_title("HBB Hydropathy Profile (Soluble Globular Protein)")
ax.set_ylim(-3.5, 3.5)
ax.legend(loc="upper right")
plt.tight_layout()
plt.savefig(OUT_DIR / "hbb_hydropathy.png", dpi=100)
plt.show()
'''))

    # Concept 3: PROSITE Motifs
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: PROSITE Motifs and Regular Expressions
### Theory
PROSITE defines biological sequence motifs using a standard pattern grammar:
- `[ALT]`: Any of Ala, Leu, or Thr.
- `{P}`: Any amino acid *except* Proline.
- `x`: Any amino acid.
- `x(3)`: Exactly 3 of any amino acid (`.{3}` in regex).
- `x(2,4)`: Between 2 and 4 of any amino acid (`.{2,4}` in regex).
- `<` and `>`: Sequence N-terminus and C-terminus.

**Globin Family Signature (PS00017):**
`[LIVMFY]-[A-Z]-H-[A-Z]-[A-Z]-[LIVMFY]` matches the proximal histidine region.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Scanning for PROSITE motifs using Python re
import re

# PROSITE globin distal histidine pattern: [LIVMF]-x(2)-H-x(2)-[KR]
# Convert to Python regular expression:
regex_pattern = r"[LIVMF].{2}H.{2}[KR]"

matches = list(re.finditer(regex_pattern, hbb_seq))
print(f"Scanning HBB for globin motif pattern '{regex_pattern}':")
for m in matches:
    print(f"  Match at 0-based indices {m.start()}:{m.end()} (1-based {m.start()+1}..{m.end()}): '{m.group()}'")
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- `Bio.SeqUtils.ProtParam.ProteinAnalysis` calculates molecular weight, pI, and GRAVY hydropathy.
- The sickle-cell mutation (E6V) eliminates an acidic charge, shifting the pI from 6.74 to 7.13 and increasing hydrophobicity.
- Kyte–Doolittle hydropathy profiles identify transmembrane helices and surface loops.
- PROSITE patterns map directly to Python regular expressions (`[LIVM]`, `.{N}`).
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Learn how secondary structure is predicted and scored with $Q_3$ in `U09_C2_Secondary_Structure_Prediction_Scoring.ipynb`.
- Solve protein property and motif exercises in `U09_P_Protein_Prediction.ipynb`.
"""))

    return nb


def build_u09_c2():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U09_C2",
        title="Secondary Structure Prediction and Scoring",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L25, Practical S11 (GOR IV & PSIPRED)",
        before_this="U09_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** 3-state secondary structure prediction ($H = \\text{alpha-helix}, E = \\text{beta-strand}, C = \\text{coil}$) [LO6].
- **Compare** statistical propensity methods (Chou–Fasman, GOR IV) with modern machine-learning models (PSIPRED) [LO6].
- **Calculate** the standard $Q_3$ accuracy score against experimentally determined crystallographic structures (DSSP) [LO6].
- **Construct** a $3 \\times 3$ confusion matrix to measure per-state prediction sensitivity and specificity [LO6].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Before AlphaFold, determining protein structure required predicting local secondary structure from sequence alone. How accurate are algorithms like GOR IV (information theory) and PSIPRED (neural networks)? By comparing predicted secondary structure strings for human *HBB* with the true crystallographic secondary structure derived from the 2.0 Å crystal structure (PDB `1A3N`), how do we quantify prediction accuracy ($Q_3$)?
"""))

    nb.cells.append(make_setup_cell("U09_C2"))

    # Concept 1: 3-State Secondary Structure
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The Three Secondary Structure States
### Theory
Although crystallography assigns secondary structure into 8 DSSP states ($H, G, I, E, B, T, S, C$), secondary structure prediction simplifies this into a **3-state classification**:
- **`H` (Helix)**: $\\alpha$-helices (DSSP $H$) and $3_{10}$-helices ($G$).
- **`E` (Strand)**: Extended $\\beta$-strands ($E$) and isolated $\\beta$-bridges ($B$).
- **`C` (Coil / Loop)**: Turns ($T$), bends ($S$), and unstructured coils ($C$).

Hemoglobin beta is an **all-$\\alpha$** protein consisting of 8 classic helices (A through H) connected by short coils.
"""))

    # Concept 2: Loading Expected Predictions
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Inspecting GOR IV, PSIPRED, and Real DSSP Strings
### Theory
- **GOR IV**: Uses statistical information theory based on amino acid propensities in a 17-residue local window (accuracy $\\approx 64\\%$).
- **PSIPRED**: Uses position-specific scoring matrices (PSSMs from PSI-BLAST) fed into a two-stage feedforward neural network (accuracy $\\approx 80\\%$).
- **DSSP**: Definitive secondary structure assigned from atomic 3D coordinates by identifying hydrogen bonds in PDB crystal structures.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading prediction strings from data/expected/
def load_sec_str(filename):
    with open(DATA_DIR / "expected" / filename) as f:
        for line in f:
            line = line.strip()
            # If line is only letters H, E, C
            if line and set(line).issubset(set("HECT ")):
                return line.replace(" ", "")
    return ""

gor_pred = load_sec_str("gor4_hbb_secondary_structure.txt")
psi_pred = load_sec_str("psipred_hbb_secondary_structure.txt")
dssp_raw = load_sec_str("dssp_hbb_1a3n.txt")

# Standardize DSSP 8-state to 3-state (H=H, E=E, else C)
dssp_true = "".join("H" if c in "HG" else ("E" if c == "E" else "C") for c in dssp_raw)

print(f"GOR IV Length:  {len(gor_pred)} | Start: {gor_pred[:30]}")
print(f"PSIPRED Length: {len(psi_pred)} | Start: {psi_pred[:30]}")
print(f"DSSP True Length: {len(dssp_true)} | Start: {dssp_true[:30]}")
'''))

    # Concept 3: Q3 Metric
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Computing Q3 Accuracy
### Theory
The standard evaluation metric in secondary structure prediction is the **three-state overall accuracy ($Q_3$)**:
$$Q_3 = \\frac{\\text{Number of correctly predicted residues}}{\\text{Total number of residues}} \\times 100 = \\frac{N_H + N_E + N_C}{N_{\\text{total}}} \\times 100$$
where $N_H, N_E, N_C$ are the counts of residues where prediction matches the true DSSP state.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Calculating Q3 Accuracy
min_len = min(len(gor_pred), len(psi_pred), len(dssp_true))

gor_matches = sum(1 for i in range(min_len) if gor_pred[i] == dssp_true[i])
psi_matches = sum(1 for i in range(min_len) if psi_pred[i] == dssp_true[i])

q3_gor = (gor_matches / min_len) * 100
q3_psi = (psi_matches / min_len) * 100

print(f"=== Three-State Accuracy (Q3) for Human HBB ===")
print(f"Total residues evaluated: {min_len}")
print(f"GOR IV Correct:  {gor_matches:3} / {min_len} -> Q3 = {q3_gor:.2f}%")
print(f"PSIPRED Correct: {psi_matches:3} / {min_len} -> Q3 = {q3_psi:.2f}%")
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Confusion Matrix for PSIPRED
states = ["H", "E", "C"]
confusion = {s_true: {s_pred: 0 for s_pred in states} for s_true in states}

for i in range(min_len):
    t = dssp_true[i]
    p = psi_pred[i]
    if t in confusion and p in confusion[t]:
        confusion[t][p] += 1

print("=== Confusion Matrix (Rows = Actual DSSP, Columns = PSIPRED Predicted) ===")
print(f"{'Actual':8} | {'Pred H':8} | {'Pred E':8} | {'Pred C':8}")
print("-" * 42)
for s_true in states:
    print(f"{s_true:8} | {confusion[s_true]['H']:8} | {confusion[s_true]['E']:8} | {confusion[s_true]['C']:8}")
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- Secondary structure prediction standardizes local conformations into 3 states: Helix ($H$), Sheet ($E$), Coil ($C$).
- Experimental validation compares predictions with crystallographic DSSP assignments.
- $Q_3$ accuracy measures overall percentage concordance.
- Neural network methods incorporating evolutionary PSSMs (PSIPRED) outperform single-sequence propensity models (GOR).
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Complete protein prediction tasks in `U09_P_Protein_Prediction.ipynb`.
- Self-test secondary structure concepts in `U09_Q_Predictive_Protein.ipynb`.
"""))

    return nb


def build_u09_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 9.1",
            stars="★☆☆",
            title="Compute molecular weight and isoelectric point for human HBB",
            biology="Beta-globin is the 147-aa subunit of adult hemoglobin.",
            task="Load `hbb_human_protein.fasta`. Use `ProteinAnalysis` to calculate molecular weight `hbb_mw` and isoelectric point `hbb_pi` as floats rounded to 2 decimal places.",
            expected="`hbb_mw` ~15998 Da, `hbb_pi` ~6.74.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

hbb_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq)
pa = ProteinAnalysis(hbb_seq)
hbb_mw = ...
hbb_pi = ...
""",
            solution_code="""from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

hbb_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq)
pa = ProteinAnalysis(hbb_seq)
hbb_mw = round(pa.molecular_weight(), 2)
hbb_pi = round(pa.isoelectric_point(), 2)
""",
            check_code="""# Check — do not edit
assert 15900 < hbb_mw < 16100, f"Expected MW ~16000 Da, got {hbb_mw}"
assert 6.5 < hbb_pi < 7.0, f"Expected pI ~6.74, got {hbb_pi}"
print("Ex 9.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.2",
            stars="★☆☆",
            title="Measure the pI shift caused by the sickle-cell mutation",
            biology="Replacing negatively charged Glutamic acid with non-polar Valine shifts the isoelectric point more basic.",
            task="Load `hbs_human_protein.fasta`. Calculate `hbs_pi`. Store the difference `hbs_pi - hbb_pi` in `pi_shift`.",
            expected="`pi_shift` as a positive float between 0.3 and 0.5.",
            student_code="""# TODO: replace the ... with your code
hbs_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbs_human_protein.fasta", "fasta").seq)
pa_s = ProteinAnalysis(hbs_seq)
hbs_pi = round(pa_s.isoelectric_point(), 2)
pi_shift = ...
""",
            solution_code="""hbs_seq = str(SeqIO.read(DATA_DIR / "sequences" / "hbs_human_protein.fasta", "fasta").seq)
pa_s = ProteinAnalysis(hbs_seq)
hbs_pi = round(pa_s.isoelectric_point(), 2)
pi_shift = round(hbs_pi - hbb_pi, 2)
""",
            check_code="""# Check — do not edit
assert pi_shift > 0, "HbS pI must be higher than HbA pI due to loss of negative glutamate"
assert 0.3 <= pi_shift <= 0.5, f"Expected pI shift ~0.39, got {pi_shift}"
print("Ex 9.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.3",
            stars="★☆☆",
            title="Calculate GRAVY hydropathy score for human insulin",
            biology="The GRAVY score reflects the hydrophobic/hydrophilic balance of preproinsulin.",
            task="Load `ins_human_protein.fasta`. Use `ProteinAnalysis` to calculate its GRAVY hydropathy score in `ins_gravy` rounded to 3 decimal places.",
            expected="`ins_gravy` as float.",
            student_code="""# TODO: replace the ... with your code
ins_seq = str(SeqIO.read(DATA_DIR / "sequences" / "ins_human_protein.fasta", "fasta").seq)
pa_ins = ProteinAnalysis(ins_seq)
ins_gravy = ...
""",
            solution_code="""ins_seq = str(SeqIO.read(DATA_DIR / "sequences" / "ins_human_protein.fasta", "fasta").seq)
pa_ins = ProteinAnalysis(ins_seq)
ins_gravy = round(pa_ins.gravy(), 3)
""",
            check_code="""# Check — do not edit
assert isinstance(ins_gravy, float)
assert -0.5 <= ins_gravy <= 0.5, f"Unexpected GRAVY value: {ins_gravy}"
print("Ex 9.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.4",
            stars="★★☆",
            title="Translate a PROSITE pattern into a Python regular expression",
            biology="PROSITE syntax uses brackets `[ABC]`, excludes `{D}`, and wildcard counts `x(N)`.",
            task="Translate the PROSITE pattern `'[LIVM]-x(2)-[DE]'` into a Python regex string stored in `my_regex`. Verify it matches test peptide `'LAAEE'`.",
            expected="`my_regex` equals `'[LIVM].{2}[DE]'`.",
            student_code="""# TODO: replace the ... with your code
my_regex = ...
""",
            solution_code="""my_regex = "[LIVM].{2}[DE]"
""",
            check_code="""# Check — do not edit
import re
assert re.search(my_regex, "LAAEE") is not None, "Regex must match test peptide"
print("Ex 9.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.5",
            stars="★★☆",
            title="Scan human beta-globin for the distal histidine motif",
            biology="The haem pocket in hemoglobin is stabilized by the distal Histidine (His63 in HBB).",
            task="Using regex pattern `r'[LIVMF].{2}H.{2}[KR]'`, search `hbb_seq`. Extract the matching peptide substring into `matched_subseq`.",
            expected="`matched_subseq` of length 7 containing 'H'.",
            student_code="""# TODO: replace the ... with your code
import re

motif_regex = r"[LIVMF].{2}H.{2}[KR]"
match = re.search(motif_regex, hbb_seq)
matched_subseq = ...
""",
            solution_code="""import re

motif_regex = r"[LIVMF].{2}H.{2}[KR]"
match = re.search(motif_regex, hbb_seq)
matched_subseq = match.group() if match else ""
""",
            check_code="""# Check — do not edit
assert len(matched_subseq) == 7, f"Expected 7 aa motif match, got {len(matched_subseq)}"
assert "H" in matched_subseq, "Motif must contain coordinating Histidine"
print("Ex 9.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.6",
            stars="★★☆",
            title="Compute Q3 accuracy for PSIPRED against DSSP ground truth",
            biology="Benchmarking secondary structure prediction accuracy against experimental X-ray structures.",
            task="Given two 3-state strings `pred_str = 'CCHHHHHHCCCCCCCC'` and `true_str = 'CCHHHHHHCCCCHHHH'`, write a function `calc_q3(pred, true)` returning accuracy percentage rounded to 1 decimal place. Compute for `pred_str` and `true_str` in `test_q3`.",
            expected="`test_q3` = 75.0% (12/16 correct).",
            student_code="""# TODO: replace the ... with your code
def calc_q3(pred, true):
    ...

pred_str = "CCHHHHHHCCCCCCCC"
true_str = "CCHHHHHHCCCCHHHH"
test_q3 = calc_q3(pred_str, true_str)
""",
            solution_code="""def calc_q3(pred, true):
    n = min(len(pred), len(true))
    matches = sum(1 for i in range(n) if pred[i] == true[i])
    return round((matches / n) * 100, 1)

pred_str = "CCHHHHHHCCCCCCCC"
true_str = "CCHHHHHHCCCCHHHH"
test_q3 = calc_q3(pred_str, true_str)
""",
            check_code="""# Check — do not edit
assert test_q3 == 75.0, f"Expected 75.0%, got {test_q3}"
print("Ex 9.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 9.7",
            stars="★★★",
            title="Compare PSIPRED vs GOR IV accuracy on full HBB sequence",
            biology="Evolutionary profile neural networks (PSIPRED) outperform single-sequence propensity statistics (GOR IV).",
            task="Load `psipred_hbb_secondary_structure.txt`, `gor4_hbb_secondary_structure.txt`, and `dssp_hbb_1a3n.txt` from `data/expected/`. Calculate `q3_psipred` and `q3_gor4`. Verify both exceed 70.0%.",
            expected="Both `q3_psipred` and `q3_gor4` > 70.0.",
            student_code="""# TODO: replace the ... with your code
# Helper to extract H/E/C string
def get_string(p):
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line and set(line).issubset(set("HECT ")):
                return line.replace(" ", "")
    return ""

exp_dir = DATA_DIR / "expected"
psi_s = get_string(exp_dir / "psipred_hbb_secondary_structure.txt")
gor_s = get_string(exp_dir / "gor4_hbb_secondary_structure.txt")
dssp_s = get_string(exp_dir / "dssp_hbb_1a3n.txt")
dssp_3 = "".join("H" if c in "HG" else ("E" if c == "E" else "C") for c in dssp_s)

q3_psipred = ...
q3_gor4 = ...
""",
            solution_code="""def get_string(p):
    with open(p) as f:
        for line in f:
            line = line.strip()
            if line and set(line).issubset(set("HECT ")):
                return line.replace(" ", "")
    return ""

exp_dir = DATA_DIR / "expected"
psi_s = get_string(exp_dir / "psipred_hbb_secondary_structure.txt")
gor_s = get_string(exp_dir / "gor4_hbb_secondary_structure.txt")
dssp_s = get_string(exp_dir / "dssp_hbb_1a3n.txt")
dssp_3 = "".join("H" if c in "HG" else ("E" if c == "E" else "C") for c in dssp_s)

q3_psipred = calc_q3(psi_s, dssp_3)
q3_gor4 = calc_q3(gor_s, dssp_3)
""",
            check_code="""# Check — do not edit
assert q3_psipred > 70.0, f"Expected PSIPRED Q3 > 70%, got {q3_psipred}"
assert q3_gor4 > 70.0, f"Expected GOR4 Q3 > 70%, got {q3_gor4}"
print("Ex 9.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U09_P",
        title="Protein Prediction — Exercises",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L23–L25, Practicals S10–S11",
        before_this="U09_C1, U09_C2"
    ))
    nb_student.cells.append(make_setup_cell("U09_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U09_P",
        title="Protein Prediction — Solutions",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L23–L25, Practicals S10–S11",
        before_this="U09_C1, U09_C2"
    ))
    nb_sol.cells.append(make_setup_cell("U09_P"))
    
    for ex in exercises:
        md = f"""### {ex.ex_id} {ex.stars} — {ex.title}
**Biology:** {ex.biology}  
**Task:** {ex.task}  
**Expected:** {ex.expected}
"""
        nb_student.cells.append(nbf.v4.new_markdown_cell(md.strip()))
        nb_student.cells.append(nbf.v4.new_code_cell(ex.student_code.strip()))
        nb_student.cells.append(nbf.v4.new_code_cell(ex.check_code.strip()))
        
        nb_sol.cells.append(nbf.v4.new_markdown_cell(md.strip()))
        nb_sol.cells.append(nbf.v4.new_code_cell(ex.solution_code.strip()))
        nb_sol.cells.append(nbf.v4.new_code_cell(ex.check_code.strip()))
        
    reflection_md = """## 5. Reflection Questions
1. Why does replacing a charged amino acid with a hydrophobic one on a protein surface promote pathological fiber assembly in sickle-cell anemia?
2. What are the three states in $Q_3$ accuracy scoring, and why is $Q_3$ considered a better evaluation standard than per-residue root mean square deviation (RMSD) for primary sequence prediction?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u09_q():
    salt = "U09_Q"
    questions = [
        QuizQuestion("q1", "What is the isoelectric point (pI) of a protein?",
                     ["(a) The pH at which the protein has maximum enzymatic activity", "(b) The pH at which the protein carries zero net electrical charge", "(c) The temperature at which the protein denatures", "(d) The molecular weight in kDa"],
                     "b", "U09_C1 §3"),
        QuizQuestion("q2", "In the Kyte–Doolittle hydropathy scale, what does a positive score indicate?",
                     ["(a) Hydrophilic / polar character", "(b) Hydrophobic / non-polar character", "(c) Acidic charge", "(d) Disulfide bond"],
                     "b", "U09_C1 §4"),
        QuizQuestion("q3", "What does a negative GRAVY (Grand Average of Hydropathy) score indicate about a protein?",
                     ["(a) The protein is an integral membrane channel", "(b) The protein is generally hydrophilic and likely globular/soluble", "(c) The protein is completely unstructured", "(d) The protein has no basic residues"],
                     "b", "U09_C1 §3"),
        QuizQuestion("q4", "In PROSITE motif pattern syntax, what does `{C}` represent?",
                     ["(a) Cysteine only", "(b) Any amino acid EXCEPT Cysteine", "(c) Exactly 2 Cysteines", "(d) C-terminus"],
                     "b", "U09_C1 §5"),
        QuizQuestion("q5", "In PROSITE syntax, how is a variable gap of 2 to 4 residues of any amino acid written?",
                     ["(a) x(2,4)", "(b) [2-4]", "(c) *2..4*", "(d) (x)2-4"],
                     "a", "U09_C1 §5"),
        QuizQuestion("q6", "What are the three conformational states evaluated in standard Q3 secondary structure prediction accuracy?",
                     ["(a) Alpha, Beta, Gamma", "(b) Helix (H), Strand (E), Coil (C)", "(c) Parallel, Antiparallel, Mixed", "(d) Core, Surface, Loop"],
                     "b", "U09_C2 §3"),
        QuizQuestion("q7", "Which secondary structure prediction algorithm was the first to use evolutionary information from PSI-BLAST PSSMs in a neural network?",
                     ["(a) Chou–Fasman", "(b) GOR I", "(c) PSIPRED", "(d) ProtParam"],
                     "c", "U09_C2 §4"),
        QuizQuestion("q8", "What experimental resource serves as the gold-standard reference for secondary structure assignment derived from atomic coordinates?",
                     ["(a) GenBank", "(b) DSSP", "(c) PROSITE", "(d) PubMed"],
                     "b", "U09_C2 §4"),
        QuizQuestion("q9", "How does the sickle-cell mutation (Glu6Val) change the net charge of the beta-globin chain at physiological pH (7.4)?",
                     ["(a) It adds a negative charge", "(b) It removes a negative charge, making the protein more positively/neutrally charged", "(c) It changes the charge from +2 to -2", "(d) It has no effect on charge"],
                     "b", "U09_C1 §3"),
        QuizQuestion("q10", "Into which structural fold class does hemoglobin belong in the SCOP / CATH databases?",
                     ["(a) All-beta", "(b) All-alpha", "(c) Alpha/Beta alternating", "(d) Membrane-only"],
                     "b", "U09_C2 §3")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U09_Q",
        title="Predictive Protein — Quiz",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L23–L25, Practicals S10–S11",
        before_this="U09_C1, U09_C2, U09_P"
    ))
    nb_student.cells.append(make_setup_cell("U09_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U09_Q",
        title="Predictive Protein — Quiz Key",
        unit_num=9,
        unit_title="Predictive Methods using Protein Sequence",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L23–L25, Practicals S10–S11",
        before_this="U09_C1, U09_C2, U09_P"
    ))
    nb_key.cells.append(make_setup_cell("U09_Q"))
    nb_key.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_student.cells.append(nbf.v4.new_markdown_cell("## Section A — Concept MCQs\nSelect the single best option for each question."))
    nb_key.cells.append(nbf.v4.new_markdown_cell("## Section A — Concept MCQs\nSelect the single best option for each question."))
    
    for q in questions:
        q_md = f"**{q.qid}.** {q.prompt}\n"
        if q.options:
            q_md += "  ".join(q.options)
        
        nb_student.cells.append(nbf.v4.new_markdown_cell(q_md.strip()))
        nb_student.cells.append(nbf.v4.new_code_cell(f'check("{q.qid}", "")'))
        
        nb_key.cells.append(nbf.v4.new_markdown_cell(q_md.strip()))
        nb_key.cells.append(nbf.v4.new_code_cell(f'check("{q.qid}", "{q.answer}")'))
            
    nb_student.cells.append(nbf.v4.new_code_cell("show_score()"))
    nb_key.cells.append(nbf.v4.new_code_cell("show_score()"))
    
    answers_repr = {q.qid: q.answer for q in questions}
    nb_key.cells.append(nbf.v4.new_code_cell(f'''# Verification of answers dictionary and generated keys
answers = {answers_repr!r}
print("Keys:", {{q: _digest(a) for q, a in answers.items()}})
'''))

    return nb_student, nb_key


def generate_unit09():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 09 notebooks...")
    c1 = build_u09_c1()
    save_notebook(c1, UNIT_DIR / "U09_C1_Protein_Properties_and_Motifs.ipynb", clear=True)
    
    c2 = build_u09_c2()
    save_notebook(c2, UNIT_DIR / "U09_C2_Secondary_Structure_Prediction_Scoring.ipynb", clear=True)
    
    p_student, p_sol = build_u09_p()
    save_notebook(p_student, UNIT_DIR / "U09_P_Protein_Prediction.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U09_P_Protein_Prediction_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u09_q()
    save_notebook(q_student, UNIT_DIR / "U09_Q_Predictive_Protein.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U09_Q_Predictive_Protein_Key.ipynb", clear=False)
    
    print("  ✓ Unit 09 files written successfully.")
