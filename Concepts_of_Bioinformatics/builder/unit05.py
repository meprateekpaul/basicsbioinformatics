"""
unit05.py - Builder for Unit 05: Sequence Alignment and Database Searching
Notebooks:
- U05_C1_Dot_Plots_and_Global_Alignment.ipynb
- U05_C2_Local_Alignment_and_Scoring.ipynb
- U05_C3_Reading_BLAST_Results.ipynb
- U05_P_Sequence_Alignment.ipynb
- solutions/U05_P_Sequence_Alignment_Solutions.ipynb
- U05_Q_Sequence_Alignment.ipynb
- solutions/U05_Q_Sequence_Alignment_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U05_Sequence_Alignment"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u05_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U05_C1",
        title="Dot Plots and Global Alignment",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L10–L11, Practical S6 (BLAST)",
        before_this="U04_C2"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Construct** and interpret 2D dot plots to visualize sequence identity, insertions, and tandem repeats [LO3].
- **Explain** dynamic programming and the Needleman–Wunsch global alignment recurrence relation [LO3].
- **Fill** a global alignment scoring matrix and perform traceback by hand and in Python [LO3].
- **Compare** normal hemoglobin A (HbA) against sickle-cell hemoglobin (HbS) globally [LO3].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Sickle-cell disease is caused by a single point mutation in human *HBB* substituting valine for glutamic acid at codon 6 (E6V). In globin evolution, how do we systematically compare two protein sequences across their entire length to align corresponding functional residues, score identical and mismatched amino acids, and prove that two sequences are homologous?
"""))

    nb.cells.append(make_setup_cell("U05_C1"))

    # Concept 1: Dot Plots
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Visualizing Alignments with Dot Plots
### Theory
A **dot plot** is a 2D matrix where Sequence 1 is plotted along the x-axis and Sequence 2 along the y-axis. A dot is placed at $(i, j)$ whenever sequence character $x_i$ equals $y_j$.
- **Continuous diagonal**: Regions of uninterrupted sequence identity.
- **Shifted diagonal**: An insertion or deletion (indel) introduced a coordinate offset.
- **Parallel diagonal lines**: Tandem or interspersed sequence repeats.
- **Noise reduction**: A sliding window of size $W$ with match threshold $T$ filters random single-character background noise.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Generating a Dot Plot in Python
import numpy as np
import matplotlib.pyplot as plt

seq1 = "VHLTPEEKSAVTALWGKVNV"  # Normal HbA N-terminus
seq2 = "VHLTPVEKSAVTALWGKVNV"  # Sickle-cell HbS N-terminus (E6V)

# Create boolean identity matrix
dot_matrix = np.zeros((len(seq2), len(seq1)), dtype=int)
for i in range(len(seq2)):
    for j in range(len(seq1)):
        if seq2[i] == seq1[j]:
            dot_matrix[i, j] = 1

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(dot_matrix, cmap="binary", origin="upper")
ax.set_xticks(range(len(seq1)))
ax.set_xticklabels(list(seq1))
ax.set_yticks(range(len(seq2)))
ax.set_yticklabels(list(seq2))
ax.set_xlabel("Seq 1: HbA (Normal)")
ax.set_ylabel("Seq 2: HbS (Sickle-cell)")
ax.set_title("Dot Plot: HbA vs HbS N-terminus")
plt.tight_layout()
plt.savefig(OUT_DIR / "dotplot_hba_hbs.png", dpi=100)
plt.show()
'''))

    # Concept 2: Needleman-Wunsch Dynamic Programming
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Needleman–Wunsch Global Alignment
### Theory
Needleman and Wunsch (1970) introduced dynamic programming to guarantee finding the mathematically optimal global alignment across the entire length of two sequences.

Given sequences $X$ of length $M$ and $Y$ of length $N$:
1. **Matrix Initialization**:
   $$F(0, 0) = 0$$
   $$F(i, 0) = i \\times d \\quad (i = 1 \\dots M)$$
   $$F(0, j) = j \\times d \\quad (j = 1 \\dots N)$$
   where $d$ is the linear gap penalty (negative score).

2. **Recurrence Relation**:
   $$F(i, j) = \\max \\begin{cases}
   F(i-1, j-1) + s(x_i, y_j) & \\text{(Diagonal: match/mismatch)} \\\\
   F(i-1, j) + d & \\text{(Up: gap in sequence } Y) \\\\
   F(i, j-1) + d & \\text{(Left: gap in sequence } X)
   \\end{cases}$$

3. **Traceback**: Begins at bottom-right cell $(M, N)$ and traces path pointers back to $(0, 0)$.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Hand-sized Needleman-Wunsch Matrix in Python
def needleman_wunsch(seq_x, seq_y, match_score=2, mismatch_score=-1, gap_penalty=-2):
    m, n = len(seq_x), len(seq_y)
    F = np.zeros((m + 1, n + 1), dtype=int)
    
    # Initialize margins
    for i in range(1, m + 1):
        F[i, 0] = i * gap_penalty
    for j in range(1, n + 1):
        F[0, j] = j * gap_penalty
        
    # Fill DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = match_score if seq_x[i-1] == seq_y[j-1] else mismatch_score
            diag = F[i-1, j-1] + s
            up = F[i-1, j] + gap_penalty
            left = F[i, j-1] + gap_penalty
            F[i, j] = max(diag, up, left)
            
    return F

s_x = "HEAGAWG"
s_y = "PAWHEAE"
dp_matrix = needleman_wunsch(s_x, s_y)

print(f"Aligning {s_x} vs {s_y}")
print("Final Global Alignment Optimal Score F(M, N):", dp_matrix[-1, -1])
print("\\nDynamic Programming Matrix:\\n", dp_matrix)
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Align the first 6 residues of HbA ('VHLTPE') and HbS ('VHLTPV')
hba_sub = "VHLTPE"
hbs_sub = "VHLTPV"
dp_hb = needleman_wunsch(hba_sub, hbs_sub, match_score=2, mismatch_score=-1, gap_penalty=-2)
print("HbA vs HbS (6-mer) optimal global score:", dp_hb[-1, -1])
'''))

    # Compare with Biopython
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Compare with Biopython PairwiseAligner
Biopython provides high-performance pairwise alignment using the `Bio.Align.PairwiseAligner` class.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Align using Biopython PairwiseAligner
from Bio.Align import PairwiseAligner

aligner = PairwiseAligner()
aligner.mode = "global"
aligner.match_score = 2
aligner.mismatch_score = -1
aligner.open_gap_score = -2
aligner.extend_gap_score = -2

score = aligner.score(hba_sub, hbs_sub)
print("Biopython computed score:", score)
print("Matches our manual DP matrix score?", score == dp_hb[-1, -1])

alignments = aligner.align(hba_sub, hbs_sub)
print("\\nOptimal Global Alignment:")
print(alignments[0])
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- Dot plots provide an immediate visual representation of sequence relationships and structural rearrangements.
- Needleman–Wunsch guarantees the optimal global alignment over full sequence lengths.
- Initialization fills boundaries with cumulative gap penalties; traceback starts at bottom-right $(M, N)$.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Learn about local alignment and substitution matrices in `U05_C2_Local_Alignment_and_Scoring.ipynb`.
- Explore database search heuristics in `U05_C3_Reading_BLAST_Results.ipynb`.
"""))

    return nb


def build_u05_c2():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U05_C2",
        title="Local Alignment and Scoring",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L12–L13, Practical S6 (BLAST)",
        before_this="U05_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Implement** Smith–Waterman local alignment and understand why the zero-floor condition is biologically essential [LO3].
- **Choose** appropriate substitution matrices (BLOSUM62 vs PAM250) based on evolutionary divergence [LO3].
- **Apply** affine gap penalties (gap opening vs gap extension) to model biological indel events [LO3].
- **Compare** global vs local alignment scores when aligning full-length globins against short functional motifs [LO3].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Proteins frequently share isolated conserved domains (e.g. haem-binding pocket, kinase domain, zinc finger) surrounded by divergent, unalignable flanking sequences. If you force an alignment across the entire sequence with global alignment, the score is penalized heavily by non-homologous regions. How does local alignment find the highest-scoring matching sub-region?
"""))

    nb.cells.append(make_setup_cell("U05_C2"))

    # Concept 1: Smith-Waterman
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Smith–Waterman Local Alignment
### Theory
Smith and Waterman (1981) modified Needleman–Wunsch with two crucial differences:
1. **Zero floor**: If all paths leading to a cell yield negative scores, the cell resets to zero:
   $$H(i, j) = \\max \\begin{cases}
   0 & \\text{(Reset / Start new local alignment)} \\\\
   H(i-1, j-1) + s(x_i, y_j) \\\\
   H(i-1, j) + d \\\\
   H(i, j-1) + d
   \\end{cases}$$
2. **Traceback**: Starts at the **maximum score cell** anywhere in the matrix (not bottom-right) and terminates as soon as a cell with score `0` is reached.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Smith-Waterman Local Alignment implementation
import numpy as np

def smith_waterman(seq_x, seq_y, match_score=3, mismatch_score=-2, gap_penalty=-2):
    m, n = len(seq_x), len(seq_y)
    H = np.zeros((m + 1, n + 1), dtype=int)
    max_score = 0
    max_pos = (0, 0)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = match_score if seq_x[i-1] == seq_y[j-1] else mismatch_score
            score = max(0, H[i-1, j-1] + s, H[i-1, j] + gap_penalty, H[i, j-1] + gap_penalty)
            H[i, j] = score
            if score > max_score:
                max_score = score
                max_pos = (i, j)
                
    return H, max_score, max_pos

seq_a = "TGTTACGG"
seq_b = "GGTTGACTA"
H_mat, best_score, best_coord = smith_waterman(seq_a, seq_b)

print("Best Local Alignment Score:", best_score)
print("Best Score Located at Matrix Cell:", best_coord)
'''))

    # Concept 2: Substitution Matrices
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Substitution Matrices (BLOSUM and PAM)
### Theory
Amino acids have distinct physicochemical properties; substituting a Leucine with Isoleucine is far more conservative than substituting with a Proline.
- **PAM (Point Accepted Mutation)**: Margaret Dayhoff (1978). Derived from global alignments of closely related proteins ($>85\\%$ identity). **Higher PAM number = greater evolutionary divergence** (e.g. PAM250 for distant relatives).
- **BLOSUM (Blocks Substitution Matrix)**: Henikoff & Henikoff (1992). Derived from local ungapped blocks of conserved protein families. **Higher BLOSUM number = closer evolutionary relatedness** (e.g. BLOSUM80 for close, BLOSUM62 standard default, BLOSUM45 for distant).
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Inspecting BLOSUM62 log-odds scores in Biopython
from Bio.Align import substitution_matrices

blosum62 = substitution_matrices.load("BLOSUM62")

# Check identical match scores
print("Trp self-match (W-W):", blosum62["W", "W"])  # Rare, structurally rigid -> high score (+11)
print("Ala self-match (A-A):", blosum62["A", "A"])  # Common, simple (+4)

# Check conservative vs radical substitutions
print("Glu -> Asp (E-D, both negative acidic):", blosum62["E", "D"])  # Conservative (+2)
print("Glu -> Val (E-V, sickle-cell mutation): ", blosum62["E", "V"])  # Non-conservative (-2)
print("Trp -> Cys (W-C, radical mismatch):    ", blosum62["W", "C"])  # Disruptive (-2)
'''))

    # Concept 3: Affine Gap Penalties
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Affine Gap Penalties
### Theory
Biologically, introducing a single insertion of length $k$ typically arises from one mutational event (e.g. replication slippage), rather than $k$ independent 1-bp insertions.
Therefore, biological alignments use **affine gap penalties**:
$$\\text{Penalty}(k) = \\text{open\\_gap\\_score} + (k - 1) \\times \\text{extend\\_gap\\_score}$$
where opening a gap is penalized heavily (e.g. $-10$), but extending an existing gap is penalized lightly (e.g. $-1$).
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Comparing Linear vs Affine Gaps on HBB vs Myoglobin
from Bio import SeqIO
from Bio.Align import PairwiseAligner

hbb_prot = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq
globin_seqs = {rec.id: rec.seq for rec in SeqIO.parse(DATA_DIR / "sequences" / "globin_family_proteins.fasta", "fasta")}
mb_prot = globin_seqs.get("MB_HUMAN", hbb_prot)

aligner = PairwiseAligner()
aligner.substitution_matrix = blosum62

# Linear gap penalty: open = -10, extend = -10
aligner.open_gap_score = -10
aligner.extend_gap_score = -10
linear_score = aligner.score(hbb_prot, mb_prot)

# Affine gap penalty: open = -10, extend = -1
aligner.open_gap_score = -10
aligner.extend_gap_score = -1
affine_score = aligner.score(hbb_prot, mb_prot)

print(f"HBB vs Myoglobin (BLOSUM62):")
print(f"  Score with Linear Gap (-10 / -10): {linear_score:.1f}")
print(f"  Score with Affine Gap (-10 / -1):   {affine_score:.1f}")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Compare with Web-Tool Practical
In Practical S6 (NCBI BLAST), the default scoring parameters are:
- Matrix: `BLOSUM62`
- Gap Costs: `Existence: 11, Extension: 1` (affine)
Notice that Biopython's `PairwiseAligner` uses negative numbers for penalties (`open_gap_score = -11`, `extend_gap_score = -1`), which matches NCBI's underlying score system.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Summary
- Smith–Waterman sets negative scores to zero, identifying localized regions of high similarity.
- BLOSUM62 is the general default; higher BLOSUM numbers correspond to closer sequences, whereas higher PAM numbers correspond to more distant sequences.
- Affine gap penalties penalize gap opening more than gap extension, reflecting evolutionary mechanisms.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Next Steps
- Read about database searching heuristics and E-values in `U05_C3_Reading_BLAST_Results.ipynb`.
- Practice aligning protein pairs with different scoring parameters in `U05_P_Sequence_Alignment.ipynb`.
"""))

    return nb


def build_u05_c3():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U05_C3",
        title="Reading BLAST Results",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L14–L15, Practical S6 (BLAST)",
        before_this="U05_C2"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** why heuristic search algorithms (BLAST and FASTA) are required for querying massive sequence databases [LO4].
- **Describe** the core algorithmic phases of BLAST: word matching ($W$), neighborhood threshold ($T$), and extension into High-Scoring Segment Pairs (HSPs) [LO4].
- **Differentiate** raw score, bit score ($S'$), and Expectation value ($E$-value) [LO4].
- **Parse** and filter tabular BLAST results (`-outfmt 6`) to detect true homologues and identify low-complexity artifacts [LO4].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
The NCBI RefSeq database contains hundreds of millions of protein sequences. Searching this entire database with exact Smith–Waterman dynamic programming would take hours per query. BLAST (Basic Local Alignment Search Tool) finds hits in seconds by indexing short 'words' and extending seeds. When BLAST returns a table of hits, how do we distinguish genuine evolutionary orthologues from chance statistical matches or repetitive sequence artifacts?
"""))

    nb.cells.append(make_setup_cell("U05_C3"))

    # Concept 1: The BLAST Heuristic
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The BLAST Algorithmic Strategy
### Theory
BLAST replaces the full $O(M \\times N)$ matrix search with an indexed heuristic:
1. **Seeding**: Break query into words of length $W$ (default $W=3$ for blastp, $W=11$ for blastn).
2. **Neighborhood Evaluation**: For each query word, list all possible words whose substitution score with the query word is $\\ge T$ (threshold).
3. **Database Scanning**: Rapidly scan the database index for exact matches to the neighborhood words.
4. **Extension**: Extend matches in both directions without gaps, then with dynamic programming, forming **High-Scoring Segment Pairs (HSPs)** until score falls below threshold $X$.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Generating 3-letter words from HBB peptide
hbb_peptide = "MVHLTPEEKSAV"
W = 3
words = [hbb_peptide[i:i+W] for i in range(len(hbb_peptide) - W + 1)]

print(f"Peptide: {hbb_peptide}")
print(f"Generated {len(words)} query words of length W={W}:")
print(words)
'''))

    # Concept 2: Statistical Significance
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Bit Score and E-Value
### Theory
The raw alignment score $S$ depends on the scoring matrix and gap penalties used. To compare alignments across different search setups:
1. **Bit Score ($S'$)**: Normalized score independent of matrix units and database size:
   $$S' = \\frac{\\lambda S - \\ln K}{\\ln 2}$$
   Higher bit score always means a better alignment.
2. **Expectation Value ($E$-value)**: The number of distinct alignments with score $\\ge S$ expected to occur purely by chance in a database of size $N$ with query length $m$:
   $$E = K \\cdot m \\cdot N \\cdot e^{-\\lambda S} = m \\cdot N \\cdot 2^{-S'}$$
- $E \\le 10^{-5}$: Strong statistical evidence of biological homology.
- If database size $N$ doubles, $E$-value **doubles** for the exact same alignment!
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Computing E-value relationship
import math

# Suppose query length m = 147 aa, database size N = 10^8 residues, bit score S_prime = 50
m = 147
N = 10**8
S_prime = 50

# E = m * N * 2^(-S_prime)
e_val = m * N * (2 ** (-S_prime))
print(f"Query length: {m} aa, DB size: {N:.1e} residues")
print(f"Bit score: {S_prime} bits -> Expected random hits (E-value): {e_val:.3e}")

# What if database size increases 10-fold?
e_val_large_db = m * (10 * N) * (2 ** (-S_prime))
print(f"Same alignment in 10x larger database -> E-value: {e_val_large_db:.3e}")
'''))

    # Concept 3: Reading Tabular BLAST Results
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Reading Tabular BLAST Output (-outfmt 6)
### Theory
Standard tabular BLAST output (`-outfmt 6`) contains 12 tab-separated columns:
1. `qseqid`: Query Seq-id
2. `sseqid`: Subject (database hit) Seq-id
3. `pident`: Percentage of identical matches
4. `length`: Alignment length
5. `mismatch`: Number of mismatches
6. `gapopen`: Number of gap openings
7. `qstart`: Start of alignment in query
8. `qend`: End of alignment in query
9. `sstart`: Start of alignment in subject
10. `send`: End of alignment in subject
11. `evalue`: Expect value
12. `bitscore`: Bit score
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading and filtering saved BLAST results for HBB
import pandas as pd

blast_file = DATA_DIR / "expected" / "blast_hbb_vs_refseq.tsv"
df_blast = pd.read_csv(blast_file, sep="\\t")

print("=== Tabular BLAST Results for Human HBB ===")
print(df_blast[["subject_id", "identity", "evalue", "bit_score", "subject_title"]])
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Filter hits with evalue < 1e-10 and print their titles
significant_hits = df_blast[df_blast["evalue"] < 1e-10]
print(f"\\nNumber of statistically significant hits (E < 1e-10): {len(significant_hits)}")
for idx, row in significant_hits.iterrows():
    print(f"  {row['subject_id']:12} | {row['identity']:6.1f}% id | E={row['evalue']} | {row['subject_title']}")
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- BLAST uses word seeds ($W$) and neighborhood scoring thresholds ($T$) to accelerate searching by orders of magnitude over full dynamic programming.
- Bit score $S'$ is matrix-independent; $E$-value scales proportionally with database size $N$.
- Tabular format (`-outfmt 6`) allows filtering by percent identity, coverage, and E-value in Pandas.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Complete alignment exercises in `U05_P_Sequence_Alignment.ipynb`.
- Test your sequence alignment and BLAST knowledge in `U05_Q_Sequence_Alignment.ipynb`.
"""))

    return nb


def build_u05_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 5.1",
            stars="★☆☆",
            title="Confirm Needleman-Wunsch initialization row and column",
            biology="In global alignment, the margins represent end-gaps from aligning against leading insertions.",
            task="Given gap penalty $d = -3$, calculate the value of cell $F(4, 0)$ in the initialization column. Store in `col_val`.",
            expected="`col_val` as integer equal to $-12$.",
            student_code="""# TODO: replace the ... with your code
gap_penalty = -3
col_val = ...
""",
            solution_code="""gap_penalty = -3
col_val = 4 * gap_penalty
""",
            check_code="""# Check — do not edit
assert col_val == -12, f"Expected -12, got {col_val}"
print("Ex 5.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 5.2",
            stars="★☆☆",
            title="Inspect BLOSUM62 score for sickle-cell substitution",
            biology="The sickle-cell mutation replaces glutamic acid (E) with valine (V) at position 6.",
            task="Load `BLOSUM62` from `Bio.Align.substitution_matrices`. Extract the score for pair `('E', 'V')` into `e_v_score`, and self-score `('E', 'E')` into `e_e_score`.",
            expected="`e_v_score` is negative, `e_e_score` is positive.",
            student_code="""# TODO: replace the ... with your code
from Bio.Align import substitution_matrices

blosum62 = substitution_matrices.load("BLOSUM62")
e_v_score = ...
e_e_score = ...
""",
            solution_code="""from Bio.Align import substitution_matrices

blosum62 = substitution_matrices.load("BLOSUM62")
e_v_score = blosum62["E", "V"]
e_e_score = blosum62["E", "E"]
""",
            check_code="""# Check — do not edit
assert e_v_score == -2, f"Expected -2, got {e_v_score}"
assert e_e_score == 5, f"Expected 5, got {e_e_score}"
print("Ex 5.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 5.3",
            stars="★★☆",
            title="Does the sickle-cell mutation change the pairwise alignment score?",
            biology="HbS differs from HbA at residue 6 (E6V).",
            task="Align the first 20 residues of HbA (`hba_pep`) and HbS (`hbs_pep`) using `PairwiseAligner` with `BLOSUM62`, `open_gap_score=-10`, `extend_gap_score=-1`. Store the score in `score_diff` as `aligner.score(hba_pep, hba_pep) - aligner.score(hba_pep, hbs_pep)`.",
            expected="`score_diff` as a positive float.",
            student_code="""# TODO: replace the ... with your code
from Bio.Align import PairwiseAligner

hba_pep = "VHLTPEEKSAVTALWGKVNV"
hbs_pep = "VHLTPVEKSAVTALWGKVNV"

aligner = PairwiseAligner()
aligner.substitution_matrix = blosum62
aligner.open_gap_score = -10
aligner.extend_gap_score = -1

self_score = ...
variant_score = ...
score_diff = ...
""",
            solution_code="""from Bio.Align import PairwiseAligner

hba_pep = "VHLTPEEKSAVTALWGKVNV"
hbs_pep = "VHLTPVEKSAVTALWGKVNV"

aligner = PairwiseAligner()
aligner.substitution_matrix = blosum62
aligner.open_gap_score = -10
aligner.extend_gap_score = -1

self_score = aligner.score(hba_pep, hba_pep)
variant_score = aligner.score(hba_pep, hbs_pep)
score_diff = self_score - variant_score
""",
            check_code="""# Check — do not edit
assert score_diff > 0, "Self score must be strictly greater than mismatch score"
assert score_diff == 7.0, f"Expected score difference of 7.0 (5 - (-2)), got {score_diff}"
print("Ex 5.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 5.4",
            stars="★★☆",
            title="Local vs Global alignment of a truncated peptide against full HBB",
            biology="A 15-aa peptide fragment aligned globally against a 147-aa protein is heavily penalized by end-gaps.",
            task="Align `fragment = 'TALWGKVNVDEVGGE'` against full `hbb_prot`. Compute global alignment score in `glob_score` and local alignment score in `loc_score`.",
            expected="`loc_score` is significantly higher than `glob_score`.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

hbb_prot = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq)
fragment = "TALWGKVNVDEVGGE"

aligner.mode = "global"
glob_score = ...

aligner.mode = "local"
loc_score = ...
""",
            solution_code="""from Bio import SeqIO

hbb_prot = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_protein.fasta", "fasta").seq)
fragment = "TALWGKVNVDEVGGE"

aligner.mode = "global"
glob_score = aligner.score(hbb_prot, fragment)

aligner.mode = "local"
loc_score = aligner.score(hbb_prot, fragment)
""",
            check_code="""# Check — do not edit
assert loc_score > glob_score, "Local alignment score must exceed global score for a short fragment"
assert loc_score > 60.0, f"Expected local score > 60, got {loc_score}"
print("Ex 5.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 5.5",
            stars="★★☆",
            title="Filter BLAST hits by E-value and identity",
            biology="Distinguishing paralogues (e.g. alpha-globin vs beta-globin) from close orthologues.",
            task="Load `data/expected/blast_hbb_vs_refseq.tsv` with pandas. Filter hits having `identity >= 70.0` and `evalue < 1e-50`. Store the count of filtered hits in `num_close_hits`.",
            expected="`num_close_hits` as integer >= 2.",
            student_code="""# TODO: replace the ... with your code
import pandas as pd

blast_df = pd.read_csv(DATA_DIR / "expected" / "blast_hbb_vs_refseq.tsv", sep="\\t")
filtered_df = ...
num_close_hits = len(filtered_df)
""",
            solution_code="""import pandas as pd

blast_df = pd.read_csv(DATA_DIR / "expected" / "blast_hbb_vs_refseq.tsv", sep="\\t")
filtered_df = blast_df[(blast_df["identity"] >= 70.0) & (blast_df["evalue"] < 1e-50)]
num_close_hits = len(filtered_df)
""",
            check_code="""# Check — do not edit
assert num_close_hits >= 2, f"Expected at least 2 close globin hits, got {num_close_hits}"
print("Ex 5.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 5.6",
            stars="★★★",
            title="Calculate E-value for an observed bit score",
            biology="Understanding how database expansion changes alignment statistical confidence.",
            task="Write a function `compute_evalue(m, n, bit_score)` using the formula $E = m \\cdot n \\cdot 2^{-S'}$. Calculate $E$ for $m=147$, $n=5 \\times 10^7$, and $S'=80$. Store in `my_evalue`.",
            expected="`my_evalue` as a very small float ($< 10^{-13}$).",
            student_code="""# TODO: replace the ... with your code
def compute_evalue(m, n, bit_score):
    ...

my_evalue = compute_evalue(147, 50000000, 80)
""",
            solution_code="""def compute_evalue(m, n, bit_score):
    return m * n * (2 ** (-bit_score))

my_evalue = compute_evalue(147, 50000000, 80)
""",
            check_code="""# Check — do not edit
assert isinstance(my_evalue, float)
assert my_evalue < 1e-13, f"Expected < 1e-13, got {my_evalue}"
print("Ex 5.6 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U05_P",
        title="Sequence Alignment — Exercises",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L10–L15, Practicals S6–S7",
        before_this="U05_C1, U05_C2, U05_C3"
    ))
    nb_student.cells.append(make_setup_cell("U05_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U05_P",
        title="Sequence Alignment — Solutions",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L10–L15, Practicals S6–S7",
        before_this="U05_C1, U05_C2, U05_C3"
    ))
    nb_sol.cells.append(make_setup_cell("U05_P"))
    
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
1. Why does the Smith–Waterman recurrence include a zero floor ($H(i, j) = \\max(0, ...)$), and what biological problem does this solve?
2. If the size of GenBank doubles over the next five years, what happens to the Bit Score and the E-value of an identical BLAST hit?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u05_q():
    salt = "U05_Q"
    questions = [
        QuizQuestion("q1", "Which alignment algorithm is guaranteed to find the mathematically optimal LOCAL alignment?",
                     ["(a) Needleman–Wunsch", "(b) FASTA", "(c) Smith–Waterman", "(d) BLAST"],
                     "c", "U05_C2 §3"),
        QuizQuestion("q2", "In global alignment dynamic programming, where does the traceback path always begin?",
                     ["(a) The cell with the highest score anywhere", "(b) Bottom-right corner (M, N)", "(c) Top-left corner (0, 0)", "(d) The center cell"],
                     "b", "U05_C1 §4"),
        QuizQuestion("q3", "Which substitution matrix is calibrated for more distantly related protein sequences?",
                     ["(a) BLOSUM80", "(b) BLOSUM62", "(c) BLOSUM45", "(d) PAM30"],
                     "c", "U05_C2 §4"),
        QuizQuestion("q4", "What does an Expectation value (E-value) of 0.05 mean in a BLAST search?",
                     ["(a) There is a 5% chance the sequences are homologous", "(b) 0.05 alignments with this score or higher are expected purely by chance in this database", "(c) The sequences are 95% identical", "(d) The query was rejected by 5% of database sequences"],
                     "b", "U05_C3 §4"),
        QuizQuestion("q5", "If the sequence database size doubles, what happens to the E-value for the same alignment score?",
                     ["(a) It is halved", "(b) It doubles", "(c) It remains unchanged", "(d) It squares"],
                     "b", "U05_C3 §4"),
        QuizQuestion("q6", "Why are affine gap penalties biologically preferred over linear gap penalties?",
                     ["(a) They run faster in dynamic programming", "(b) Extending an existing indel is more probable than creating a new one", "(c) They prevent mismatch scores from being negative", "(d) They eliminate the need for substitution matrices"],
                     "b", "U05_C2 §5"),
        QuizQuestion("q7", "What is the default word size (W) for standard protein BLAST (blastp)?",
                     ["(a) 3", "(b) 6", "(c) 11", "(d) 28"],
                     "a", "U05_C3 §3"),
        QuizQuestion("q8", "What feature appears on a dot plot when comparing a sequence against itself that contains tandem repeats?",
                     ["(a) A single main diagonal", "(b) Multiple parallel diagonals offset from the main diagonal", "(c) An isolated perpendicular cross", "(d) A completely blank matrix"],
                     "b", "U05_C1 §3"),
        QuizQuestion("q9", "Which BLAST program translates a nucleotide query in six frames to search against a protein database?",
                     ["(a) blastn", "(b) blastp", "(c) blastx", "(d) tblastn"],
                     "c", "U05_C3 §3"),
        QuizQuestion("q10", "What is the term for an alignment segment that has been extended without gaps or with gaps to maximize local score in BLAST?",
                     ["(a) PSSM", "(b) HSP (High-Scoring Segment Pair)", "(c) Seed word", "(d) Ortholog group"],
                     "b", "U05_C3 §3")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U05_Q",
        title="Sequence Alignment — Quiz",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L10–L15, Practicals S6–S7",
        before_this="U05_C1, U05_C2, U05_C3, U05_P"
    ))
    nb_student.cells.append(make_setup_cell("U05_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U05_Q",
        title="Sequence Alignment — Quiz Key",
        unit_num=5,
        unit_title="Sequence Alignment and Database Searching",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L10–L15, Practicals S6–S7",
        before_this="U05_C1, U05_C2, U05_C3, U05_P"
    ))
    nb_key.cells.append(make_setup_cell("U05_Q"))
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


def generate_unit05():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 05 notebooks...")
    c1 = build_u05_c1()
    save_notebook(c1, UNIT_DIR / "U05_C1_Dot_Plots_and_Global_Alignment.ipynb", clear=True)
    
    c2 = build_u05_c2()
    save_notebook(c2, UNIT_DIR / "U05_C2_Local_Alignment_and_Scoring.ipynb", clear=True)
    
    c3 = build_u05_c3()
    save_notebook(c3, UNIT_DIR / "U05_C3_Reading_BLAST_Results.ipynb", clear=True)
    
    p_student, p_sol = build_u05_p()
    save_notebook(p_student, UNIT_DIR / "U05_P_Sequence_Alignment.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U05_P_Sequence_Alignment_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u05_q()
    save_notebook(q_student, UNIT_DIR / "U05_Q_Sequence_Alignment.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U05_Q_Sequence_Alignment_Key.ipynb", clear=False)
    
    print("  ✓ Unit 05 files written successfully.")
