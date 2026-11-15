"""
unit06.py - Builder for Unit 06: Multiple Sequence Alignment
Notebooks:
- U06_C1_Multiple_Alignment_and_Conservation.ipynb
- U06_P_Multiple_Alignment.ipynb
- solutions/U06_P_Multiple_Alignment_Solutions.ipynb
- U06_Q_Multiple_Alignment.ipynb
- solutions/U06_Q_Multiple_Alignment_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U06_Multiple_Sequence_Alignment"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u06_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U06_C1",
        title="Multiple Alignment and Conservation",
        unit_num=6,
        unit_title="Multiple Sequence Alignment",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L16–L17, Practical S8 (Clustal & Jalview)",
        before_this="U05_C3"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** what a Multiple Sequence Alignment (MSA) reveals that pairwise alignments cannot (conserved motifs, functional active sites) [LO5].
- **Describe** the progressive alignment strategy (guide tree, profile-profile alignment, "once a gap, always a gap") [LO5].
- **Load** and slice Clustal format alignments using Biopython's `Bio.AlignIO` [LO5].
- **Calculate** per-column conservation and plot a conservation profile along the globin family [LO5].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
The human genome encodes multiple distinct globin proteins: hemoglobin alpha (*HBA1*), beta (*HBB*), delta (*HBD*), gamma (*HBG1*), myoglobin (*MB*), neuroglobin (*NGB*), and cytoglobin (*CYGB*). Despite millions of years of evolutionary divergence, all of them bind a haem group and transport oxygen. How do we align all 7 proteins simultaneously to identify the invariant catalytic residues that coordinate the haem iron atom?
"""))

    nb.cells.append(make_setup_cell("U06_C1"))

    # Concept 1: MSA vs Pairwise
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The Power of Multiple Sequence Alignment
### Theory
Pairwise alignment can only reveal similarity between two sequences. When three or more homologous sequences are aligned:
1. **Conserved columns** pinpoint essential catalytic residues, structural disulfides, or ligand-binding contacts.
2. **Variable columns** indicate neutral, surface-exposed positions tolerant of substitution.
3. **Indel patterns** delineate structural loops connecting conserved secondary structure elements.

Finding the mathematically optimal MSA with dynamic programming across $N$ sequences of length $L$ requires $O(L^N)$ computational time and space, which is **NP-hard** and computationally impossible for more than a few sequences.
"""))

    # Concept 2: Progressive Alignment
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Progressive Alignment Heuristics
### Theory
Algorithms like **ClustalW**, **Clustal Omega**, and **MUSCLE** use the **progressive alignment** heuristic:
1. **All-against-all pairwise alignment**: Calculate distance matrix between all pairs.
2. **Guide tree construction**: Cluster sequences (using UPGMA or Neighbor Joining) into a binary guide tree.
3. **Profile-profile alignment**: Progressively align the most closely related pairs first, then align alignments (profiles) following the guide tree.

**Rule:** *"Once a gap, always a gap."* If an early pairwise step introduces a gap, subsequent steps cannot undo it, potentially propagating early alignment errors.
"""))

    # Concept 3: AlignIO
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Reading and Slicing MSAs with Bio.AlignIO
### Theory
Biopython provides `Bio.AlignIO` to read standard MSA formats (`clustal`, `fasta`, `phylip`):
- `AlignIO.read(path, "clustal")`: Reads a single multiple alignment object (`MultipleSeqAlignment`).
- `len(alignment)`: Number of sequences (rows).
- `alignment.get_alignment_length()`: Number of alignment columns.
- Slicing: `alignment[:, 50]` extracts column 50 across all sequences; `alignment[:, 10:20]` extracts a block of columns.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading the Human Globin Family MSA
from Bio import AlignIO

aln_file = DATA_DIR / "alignments" / "globin_family.aln"
alignment = AlignIO.read(aln_file, "clustal")

num_seqs = len(alignment)
aln_len = alignment.get_alignment_length()

print(f"Loaded Multiple Alignment with {num_seqs} sequences across {aln_len} columns.\\n")
for record in alignment:
    print(f"  {record.id:15} | Length: {len(record.seq)} | Start: {record.seq[:25]}...")
'''))

    # Concept 4: Conservation and Consensus
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Column Conservation and Consensus Profile
### Theory
For each alignment column $j$, the fractional identity is the frequency of the most abundant amino acid in that column:
$$\\text{Identity}(j) = \\frac{\\max_{aa} \\text{Count}(aa, j)}{\\text{Total Sequences}}$$
Columns with $\\text{Identity} = 1.0$ (100%) represent invariant residues across all members.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Calculating per-column conservation and consensus
import matplotlib.pyplot as plt
from collections import Counter

conservation_scores = []
consensus_seq = []

for col_idx in range(aln_len):
    col_chars = alignment[:, col_idx].upper()
    # Exclude gaps when determining dominant residue
    valid_chars = [c for c in col_chars if c != "-"]
    if valid_chars:
        counts = Counter(valid_chars)
        most_common_aa, count = counts.most_common(1)[0]
        score = count / num_seqs
        consensus_seq.append(most_common_aa)
    else:
        score = 0.0
        consensus_seq.append("-")
    conservation_scores.append(score)

print(f"Consensus sequence length: {len(consensus_seq)}")
print(f"First 40 residues of consensus: {''.join(consensus_seq[:40])}")

# Plot conservation profile
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.plot(conservation_scores, color="darkblue", lw=1.2)
ax.axhline(1.0, color="red", linestyle="--", alpha=0.7, label="100% Invariant")
ax.set_xlabel("Alignment Column Index")
ax.set_ylabel("Fractional Conservation")
ax.set_title("Conservation Profile across 7 Human Globins")
ax.set_ylim(-0.05, 1.1)
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(OUT_DIR / "globin_conservation_profile.png", dpi=100)
plt.show()

# Find conserved positions
conserved_cols = [i for i, s in enumerate(conservation_scores) if s >= 0.7]
print(f"\\nFound {len(conserved_cols)} conserved columns (>=70% identity) across all 7 globins:")
for c in conserved_cols:
    print(f"  Column {c:3}: Dominant {consensus_seq[c]} (Score: {conservation_scores[c]:.2f})")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Compare with the Web Tool
In Practical S8 (Jalview / Clustal Omega):
- Invariant columns are marked with an asterisk (`*`) beneath the alignment.
- Conserved substitutions within strongly similar properties are marked with a colon (`:`).
- Weakly similar substitutions are marked with a period (`.`).
Our Python calculation identifies the same invariant columns, notably the proximal Histidine (coordinating the haem iron) and distal Histidine.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Summary
- Progressive alignment builds an MSA step-by-step from pairwise distances and a guide tree.
- `Bio.AlignIO.read()` parses alignments into `MultipleSeqAlignment` objects.
- Slicing `alignment[:, col]` accesses column slices across all sequences.
- Invariant columns identify core functional residues essential for protein mechanism.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 9. Next Steps
- Analyze globin conservation in `U06_P_Multiple_Alignment.ipynb`.
- Self-test multiple sequence alignment concepts in `U06_Q_Multiple_Alignment.ipynb`.
"""))

    return nb


def build_u06_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 6.1",
            stars="★☆☆",
            title="Load globin alignment and report dimensions",
            biology="The globin family MSA contains representative human globin chains.",
            task="Load `data/alignments/globin_family.aln` using `AlignIO.read`. Store the number of sequences in `num_globins` and the alignment length in `num_columns`.",
            expected="`num_globins` = 7, `num_columns` = 150.",
            student_code="""# TODO: replace the ... with your code
from Bio import AlignIO

aln_path = DATA_DIR / "alignments" / "globin_family.aln"
alignment = ...
num_globins = ...
num_columns = ...
""",
            solution_code="""from Bio import AlignIO

aln_path = DATA_DIR / "alignments" / "globin_family.aln"
alignment = AlignIO.read(aln_path, "clustal")
num_globins = len(alignment)
num_columns = alignment.get_alignment_length()
""",
            check_code="""# Check — do not edit
assert num_globins == 7, f"Expected 7 globin sequences, got {num_globins}"
assert num_columns == 150, f"Expected 150 alignment columns, got {num_columns}"
print("Ex 6.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.2",
            stars="★☆☆",
            title="Extract a specific alignment column across all sequences",
            biology="Alignment columns show which amino acid occupies homologous structural positions in each protein.",
            task="Extract the characters in column index `0` across all sequences as a list or string into `first_col`.",
            expected="`first_col` has length 7 and starts with 'M' (methionine start codon).",
            student_code="""# TODO: replace the ... with your code
first_col = ...
""",
            solution_code="""first_col = alignment[:, 0]
""",
            check_code="""# Check — do not edit
assert len(first_col) == 7, f"Expected 7 residues, got {len(first_col)}"
assert all(c == "M" for c in first_col), "All globin sequences should start with Methionine (M)"
print("Ex 6.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.3",
            stars="★☆☆",
            title="Calculate percentage identity for a single column",
            biology="High identity indicates evolutionary pressure to maintain that specific side chain.",
            task="Write a helper expression that calculates the fraction of sequences that share the most common amino acid in column index 0, and assign to `col0_identity`.",
            expected="`col0_identity` equals 1.0 (100% identity).",
            student_code="""# TODO: replace the ... with your code
from collections import Counter

col0_chars = alignment[:, 0]
col0_identity = ...
""",
            solution_code="""from collections import Counter

col0_chars = alignment[:, 0]
counts = Counter(col0_chars)
most_common, count = counts.most_common(1)[0]
col0_identity = count / len(col0_chars)
""",
            check_code="""# Check — do not edit
assert col0_identity == 1.0, f"Expected 1.0, got {col0_identity}"
print("Ex 6.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.4",
            stars="★★☆",
            title="Find conserved columns across globin chains",
            biology="Conserved columns across globin chains highlight residues required for folding stability and oxygen binding.",
            task="Compute the identity fraction for all columns $0 \\dots \\text{aln\\_len}-1$. Collect the indices of all columns with identity fraction >= 0.70 into a list `conserved_indices`.",
            expected="`conserved_indices` as a non-empty list of integers containing column 0.",
            student_code="""# TODO: replace the ... with your code
conserved_indices = []

for j in range(alignment.get_alignment_length()):
    col = alignment[:, j]
    ...
""",
            solution_code="""conserved_indices = []

for j in range(alignment.get_alignment_length()):
    col = alignment[:, j]
    counts = Counter(col)
    most_common, count = counts.most_common(1)[0]
    if count / len(col) >= 0.70:
        conserved_indices.append(j)
""",
            check_code="""# Check — do not edit
assert isinstance(conserved_indices, list) and len(conserved_indices) >= 2, "Expected at least 2 conserved columns"
assert 0 in conserved_indices, "Column 0 (initial Met) should be conserved"
print("Ex 6.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.5",
            stars="★★☆",
            title="Identify haem-coordinating histidine positions",
            biology="The distal (His63) and proximal (His92) histidines coordinate the haem iron atom.",
            task="Search across all columns in `alignment` for positions where Histidine ('H') is present in at least 3 globin chains. Store the column indices in `his_columns`.",
            expected="`his_columns` list of integers containing columns 63 and 92.",
            student_code="""# TODO: replace the ... with your code
his_columns = []
for j in range(alignment.get_alignment_length()):
    ...
""",
            solution_code="""his_columns = []
for j in range(alignment.get_alignment_length()):
    col = alignment[:, j]
    if col.count("H") >= 3:
        his_columns.append(j)
""",
            check_code="""# Check — do not edit
assert isinstance(his_columns, list)
assert 63 in his_columns and 92 in his_columns, f"Expected columns 63 and 92, got {his_columns}"
print("Ex 6.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.6",
            stars="★★☆",
            title="Calculate gap percentage for each sequence in the alignment",
            biology="Shorter globin chains (like HBA, 142 aa) contain terminal or loop deletions relative to longer globins (CYGB, 167 aa).",
            task="For each sequence in `alignment`, compute the percentage of characters that are gaps (`'-'`). Store in dictionary `gap_percentages` mapping sequence ID to float percentage.",
            expected="`gap_percentages` dict with 7 entries.",
            student_code="""# TODO: replace the ... with your code
gap_percentages = {}
for rec in alignment:
    ...
""",
            solution_code="""gap_percentages = {}
for rec in alignment:
    gap_count = rec.seq.count("-")
    gap_percentages[rec.id] = round((gap_count / len(rec.seq)) * 100, 2)
""",
            check_code="""# Check — do not edit
assert len(gap_percentages) == 7
assert all(0.0 <= v <= 30.0 for v in gap_percentages.values())
print("Ex 6.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 6.7",
            stars="★★★",
            title="Generate a 50% majority-rule consensus sequence",
            biology="Consensus sequences summarize the dominant amino acid at each evolutionary position.",
            task="Construct a consensus string `consensus_50` where each position is the most frequent amino acid if its frequency is $\\ge 0.5$, else `'X'`. (Ignore gaps when computing frequency).",
            expected="`consensus_50` string with length equal to alignment length.",
            student_code="""# TODO: replace the ... with your code
consensus_50 = []
for j in range(alignment.get_alignment_length()):
    col = [c for c in alignment[:, j] if c != "-"]
    ...
consensus_50 = "".join(consensus_50)
""",
            solution_code="""consensus_50 = []
for j in range(alignment.get_alignment_length()):
    col = [c for c in alignment[:, j] if c != "-"]
    if col:
        counts = Counter(col)
        aa, count = counts.most_common(1)[0]
        if count / len(alignment) >= 0.5:
            consensus_50.append(aa)
        else:
            consensus_50.append("X")
    else:
        consensus_50.append("X")
consensus_50 = "".join(consensus_50)
""",
            check_code="""# Check — do not edit
assert len(consensus_50) == alignment.get_alignment_length()
assert consensus_50[0] == "M"
print("Ex 6.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U06_P",
        title="Multiple Alignment — Exercises",
        unit_num=6,
        unit_title="Multiple Sequence Alignment",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L16–L17, Practical S8",
        before_this="U06_C1"
    ))
    nb_student.cells.append(make_setup_cell("U06_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U06_P",
        title="Multiple Alignment — Solutions",
        unit_num=6,
        unit_title="Multiple Sequence Alignment",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L16–L17, Practical S8",
        before_this="U06_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U06_P"))
    
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
1. Why does the 'once a gap, always a gap' rule in progressive alignment sometimes produce suboptimal multiple alignments, and how do iterative algorithms (like MUSCLE) attempt to fix it?
2. Why is calculating the exact optimal multiple sequence alignment with dynamic programming computationally infeasible for 20 sequences of length 300?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u06_q():
    salt = "U06_Q"
    questions = [
        QuizQuestion("q1", "What is the primary computational reason that exact dynamic programming is not used for large multiple sequence alignments?",
                     ["(a) Sequence alphabets are too large", "(b) Computational complexity scales exponentially as O(L^N)", "(c) Substitution matrices do not exist for MSAs", "(d) Dynamic programming cannot handle gaps"],
                     "b", "U06_C1 §3"),
        QuizQuestion("q2", "In progressive alignment algorithms (such as ClustalW), what guides the order in which sequences are aligned?",
                     ["(a) A phylogenetic guide tree based on pairwise distances", "(b) Random sequence order", "(c) Sequence length from shortest to longest", "(d) GC content"],
                     "a", "U06_C1 §4"),
        QuizQuestion("q3", "What does an asterisk (`*`) beneath an alignment column signify in Clustal format?",
                     ["(a) Fully conserved / invariant residue across all sequences", "(b) Strongly similar substitution", "(c) A gap opening", "(d) A sequencing error"],
                     "a", "U06_C1 §7"),
        QuizQuestion("q4", "What does a colon (`:`) beneath an alignment column signify in Clustal format?",
                     ["(a) Completely invariant residue", "(b) Conservation between groups of strongly similar properties", "(c) Conservation of weakly similar properties", "(d) An unaligned column"],
                     "b", "U06_C1 §7"),
        QuizQuestion("q5", "What is the meaning of the principle 'once a gap, always a gap' in progressive alignment?",
                     ["(a) Gaps cannot be opened in initial sequences", "(b) Gaps introduced early between close sequences cannot be shifted or removed in later steps", "(c) Gaps carry infinite penalty", "(d) Terminal gaps are ignored"],
                     "b", "U06_C1 §4"),
        QuizQuestion("q6", "Which module in Biopython is designed specifically to read, write, and manipulate multiple sequence alignments?",
                     ["(a) Bio.SeqIO", "(b) Bio.AlignIO", "(c) Bio.Entrez", "(d) Bio.PDB"],
                     "b", "U06_C1 §5"),
        QuizQuestion("q7", "How does structural alignment differ from pure sequence alignment?",
                     ["(a) It aligns 3D atomic coordinates in space rather than primary sequence alone", "(b) It ignores amino acid properties completely", "(c) It only applies to RNA molecules", "(d) It runs in O(1) time"],
                     "a", "U06_C1 §3"),
        QuizQuestion("q8", "If you slice a Biopython MultipleSeqAlignment object as `alignment[:, 10]`, what does the result represent?",
                     ["(a) The 10th sequence in the alignment", "(b) The 10th column across all sequences", "(c) The first 10 characters of sequence 1", "(d) The gap count"],
                     "b", "U06_C1 §5"),
        QuizQuestion("q9", "Which widely-used alignment tool uses an iterative refinement strategy to correct early progressive alignment errors?",
                     ["(a) Needleman–Wunsch", "(b) MUSCLE", "(c) BLAST", "(d) Dotter"],
                     "b", "U06_C1 §4"),
        QuizQuestion("q10", "What biological feature do invariant columns in an enzyme or globin family alignment typically signify?",
                     ["(a) Non-essential surface residues", "(b) Core catalytic or ligand-binding functional residues", "(c) Repetitive sequence artifacts", "(d) Polyadenylation signals"],
                     "b", "U06_C1 §6")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U06_Q",
        title="Multiple Alignment — Quiz",
        unit_num=6,
        unit_title="Multiple Sequence Alignment",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L16–L17, Practical S8",
        before_this="U06_C1, U06_P"
    ))
    nb_student.cells.append(make_setup_cell("U06_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U06_Q",
        title="Multiple Alignment — Quiz Key",
        unit_num=6,
        unit_title="Multiple Sequence Alignment",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L16–L17, Practical S8",
        before_this="U06_C1, U06_P"
    ))
    nb_key.cells.append(make_setup_cell("U06_Q"))
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


def generate_unit06():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 06 notebooks...")
    c1 = build_u06_c1()
    save_notebook(c1, UNIT_DIR / "U06_C1_Multiple_Alignment_and_Conservation.ipynb", clear=True)
    
    p_student, p_sol = build_u06_p()
    save_notebook(p_student, UNIT_DIR / "U06_P_Multiple_Alignment.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U06_P_Multiple_Alignment_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u06_q()
    save_notebook(q_student, UNIT_DIR / "U06_Q_Multiple_Alignment.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U06_Q_Multiple_Alignment_Key.ipynb", clear=False)
    
    print("  ✓ Unit 06 files written successfully.")
