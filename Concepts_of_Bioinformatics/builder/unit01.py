"""
unit01.py - Builder for Unit 01: Bioinformatics and Internet
Notebooks:
- U01_C1_Sequences_as_Text.ipynb
- U01_P_Sequences_as_Text.ipynb
- solutions/U01_P_Sequences_as_Text_Solutions.ipynb
- U01_Q_Bioinformatics_and_Internet.ipynb
- solutions/U01_Q_Bioinformatics_and_Internet_Key.ipynb
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
    clear_outputs,
    PracticeExercise,
    QuizQuestion
)

UNIT_DIR = NOTEBOOKS_DIR / "U01_Bioinformatics_and_Internet"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u01_c1():
    nb = nbf.v4.new_notebook()
    
    # 0. Header
    nb.cells.append(make_header_cell(
        notebook_id="U01_C1",
        title="Sequences as Text",
        unit_num=1,
        unit_title="Bioinformatics and Internet",
        nb_type="Course",
        time_min=35,
        difficulty="★☆☆",
        goes_with="Lectures L1–L2, Practical S1 (Linux and Sequence Basics)",
        before_this="None"
    ))
    
    # 1. Outcomes
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Treat** biological sequences as standard Python strings with 0-based indexing and slicing [LO1].
- **Calculate** fundamental nucleotide statistics including length, base counts, and GC content [LO1].
- **Read** FASTA formatted files directly from disk using Biopython's `SeqIO` module [LO1].
- **Generate** reverse complements and understand biological strand orientation [LO1].
"""))

    # 2. Biological question
    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Human hemoglobin subunit beta (*HBB*, RefSeq accession `NM_000518.5`) encodes the 147-amino acid beta-globin chain. Mutations in this gene cause sickle-cell anemia and beta-thalassemia. When bioinformaticians receive a new sequence from a sequencing facility or database, the very first step is quality checking: How long is the transcript? What is its base composition? Where does the coding sequence begin, and what is its reverse complement? In this notebook, we explore how Python represents biological sequences as text strings.
"""))

    # 3. Setup
    nb.cells.append(make_setup_cell("U01_C1"))

    # 4. Concepts
    # Concept 1
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Sequences as Strings — Indexing and Slicing
### Theory
In Python, a sequence of DNA or protein is naturally represented as a string of characters (`str`). Python uses **0-based indexing**: the first nucleotide is at index `0`, the second at `1`, and so on. Negative indices count backward from the end (`-1` is the last character). Slicing syntax `seq[start:stop]` extracts characters from `start` up to but *excluding* `stop`. Slicing with a step `seq[start:stop:step]` allows stepping through bases, and `seq[::-1]` reverses a string.
"""))
    
    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Slicing the 5' leader of HBB mRNA
# The first 50 nucleotides of HBB mRNA contain the 5' untranslated region (5' UTR)
hbb_5utr = "ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACC"

print("Length of 5' UTR:", len(hbb_5utr), "nucleotides")
print("First nucleotide (index 0):", hbb_5utr[0])
print("Last nucleotide (index -1):", hbb_5utr[-1])
print("First 10 nucleotides (slice 0:10):", hbb_5utr[0:10])
print("Next 10 nucleotides (slice 10:20):", hbb_5utr[10:20])
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Change the slice indices below to inspect nucleotides 20 to 35
sample_slice = hbb_5utr[20:35]
print("Slice [20:35]:", sample_slice)
print("Length of this slice:", len(sample_slice))
'''))

    nb.cells.append(nbf.v4.new_markdown_cell("""**Common mistakes:**
- *Off-by-one errors:* In Python, `seq[0:3]` returns 3 characters (indices 0, 1, 2), NOT indices 0, 1, 2, 3.
- *1-based confusion:* Biology papers and GenBank flat files use 1-based coordinates. Base 1 in GenBank is index 0 in Python!
"""))

    # Concept 2
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Counting Nucleotides and GC Content
### Theory
The GC content (fraction of guanine and cytosine bases) is a primary biophysical feature of genomes and genes. GC pairs form three hydrogen bonds, whereas AT pairs form two. GC-rich regions have higher melting temperatures ($T_m$) and distinct codon usage patterns. In mammals, exons typically have higher GC content than introns. GC percentage is defined as:

$$\\text{GC}\\% = \\frac{\\text{Count}(G) + \\text{Count}(C)}{\\text{Total Length}} \\times 100$$
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Calculating base counts and GC content
seq = "ACATTTGCTTCTGACACAACTGTGTTCACTAGCAACCTCAAACAGACACCATGGTGCACCTG"

count_a = seq.count("A")
count_c = seq.count("C")
count_g = seq.count("G")
count_t = seq.count("T")
total = len(seq)

gc_percent = ((count_g + count_c) / total) * 100

print(f"Base counts: A={count_a}, C={count_c}, G={count_g}, T={count_t} (Total={total})")
print(f"GC content: {gc_percent:.2f}%")
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Calculate AT percentage using the counts above
at_percent = ((count_a + count_t) / total) * 100
print(f"AT content: {at_percent:.2f}%")
print(f"Check sum: {gc_percent + at_percent:.1f}%")
'''))

    nb.cells.append(nbf.v4.new_markdown_cell("""**Common mistakes:**
- *Case sensitivity:* `.count("g")` will return 0 if the string is uppercase `"G"`. Always ensure case consistency with `.upper()`.
- *Ambiguous bases:* Some sequencing reads contain `N` or IUPAC degeneracy codes. Dividing by `count_a + count_c + count_g + count_t` avoids dividing by ambiguous bases.
"""))

    # Concept 3
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Reading FASTA Files with Biopython SeqIO
### Theory
FASTA is the standard text-based format for nucleotide and peptide sequences. A FASTA record starts with a single-line header beginning with `>`, followed by sequence lines. Biopython's `Bio.SeqIO` module provides unified parsers:
- `SeqIO.read(filename, "fasta")`: reads a single record from a file (raises an exception if the file contains more or fewer than one record).
- `SeqIO.parse(filename, "fasta")`: returns an iterator yielding `SeqRecord` objects for multi-FASTA files.
Each `SeqRecord` object contains `.id`, `.description`, and `.seq`.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading human HBB mRNA from data/
from Bio import SeqIO

fasta_file = DATA_DIR / "sequences" / "hbb_human_mrna.fasta"
record = SeqIO.read(fasta_file, "fasta")

print("Record ID:", record.id)
print("Record Description:", record.description)
print("Sequence Length:", len(record.seq), "bp")
print("First 60 bp of mRNA:\\n", record.seq[:60])
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Load the coding sequence (CDS) of HBB and compare lengths
cds_file = DATA_DIR / "sequences" / "hbb_human_cds.fasta"
cds_record = SeqIO.read(cds_file, "fasta")

print("CDS ID:", cds_record.id)
print("CDS Length:", len(cds_record.seq), "bp")
print("Difference (UTR length):", len(record.seq) - len(cds_record.seq), "bp")
'''))

    nb.cells.append(nbf.v4.new_markdown_cell("""**Common mistakes:**
- Calling `SeqIO.read()` on a multi-sequence FASTA file. `SeqIO.read()` requires exactly one sequence. For multiple sequences, use `for record in SeqIO.parse(handle, "fasta"):`.
- Treating `record.seq` as an ordinary string for operations where Biopython methods are needed (or forgetting `str(record.seq)` when passing to standard regex).
"""))

    # Concept 4
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Complement and Reverse Complement
### Theory
DNA is double-stranded and antiparallel. One strand runs 5' $\\to$ 3' and the complementary strand runs 3' $\\to$ 5'. When writing DNA sequences, molecular biologists always write sequences in the 5' to 3' direction. Therefore, finding the complementary strand sequence requires both complementing the bases ($A \\leftrightarrow T, G \\leftrightarrow C$) and reversing the order. Biopython provides `.reverse_complement()` directly on `Seq` objects.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Reverse complement of the first 21 bp of HBB CDS
from Bio.Seq import Seq

coding_start = cds_record.seq[:21]
rev_comp = coding_start.reverse_complement()

print("Original 5' -> 3':", coding_start)
print("Complement:        ", coding_start.complement())
print("Rev Complement:    ", rev_comp)
'''))

    # 5. Compare with the tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Compare with the Web Tool
In Practical S1, we inspected sequence records on NCBI and used command-line tools like EMBOSS `geecee`.
Let's compute the overall GC percentage of the complete 626 bp HBB mRNA and compare it with the NCBI GenBank metadata:
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Calculate full HBB mRNA GC%
full_seq = record.seq
gc_hbb = ((full_seq.count("G") + full_seq.count("C")) / len(full_seq)) * 100
at_hbb = ((full_seq.count("A") + full_seq.count("T")) / len(full_seq)) * 100

print(f"HBB mRNA (NM_000518.5) Length: {len(full_seq)} bp")
print(f"Python calculated GC%: {gc_hbb:.2f}%")
print(f"Python calculated AT%: {at_hbb:.2f}%")
print("EMBOSS geecee reported GC%: 51.76%")
'''))

    # 6. Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Summary
- Biological sequences in Python are strings of characters, indexed from 0 to $N-1$.
- `len(seq)` gives the sequence length; `seq.count('G')` counts individual base occurrences.
- `Bio.SeqIO.read()` parses a single FASTA record into a `SeqRecord` object containing `.id` and `.seq`.
- `.reverse_complement()` generates the reverse-complement strand in standard 5' $\\to$ 3' orientation.

| Function / Method | Module / Type | What it does | Example |
|---|---|---|---|
| `len()` | Built-in | Returns number of elements | `len(record.seq)` |
| `str.count()` | `str` / `Seq` | Counts occurrences of substring | `seq.count("G")` |
| `SeqIO.read()` | `Bio.SeqIO` | Reads exactly one record | `SeqIO.read(path, "fasta")` |
| `SeqIO.parse()` | `Bio.SeqIO` | Iterates over multiple records | `SeqIO.parse(path, "fasta")` |
| `.reverse_complement()` | `Bio.Seq.Seq` | Inverts orientation & complements | `seq.reverse_complement()` |
"""))

    # 7. Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 9. Next Steps
- Open `U01_P_Sequences_as_Text.ipynb` to complete hands-on practice exercises.
- Self-test your understanding with `U01_Q_Bioinformatics_and_Internet.ipynb`.
"""))

    return nb


def build_u01_p():
    """Build U01_P practice notebook (student and solution versions)."""
    exercises = [
        # Warm-up 1
        PracticeExercise(
            ex_id="Ex 1.1",
            stars="★☆☆",
            title="Calculate length and base counts of human insulin mRNA",
            biology="Insulin (INS) is a peptide hormone critical for glucose homeostasis. Its mRNA sequence is stored in data/sequences/ins_human_mrna.fasta.",
            task="Load `ins_human_mrna.fasta` using `SeqIO.read`, store its sequence length in `ins_len`, and count how many 'A' nucleotides it contains in `ins_a_count`.",
            expected="`ins_len` as an integer (around 465 bp), `ins_a_count` as an integer.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

ins_path = DATA_DIR / "sequences" / "ins_human_mrna.fasta"
ins_record = ...
ins_len = ...
ins_a_count = ...
""",
            solution_code="""from Bio import SeqIO

ins_path = DATA_DIR / "sequences" / "ins_human_mrna.fasta"
ins_record = SeqIO.read(ins_path, "fasta")
ins_len = len(ins_record.seq)
ins_a_count = ins_record.seq.count("A")
""",
            check_code="""# Check — do not edit
assert isinstance(ins_len, int), "ins_len must be an integer"
assert isinstance(ins_a_count, int), "ins_a_count must be an integer"
assert ins_len > 400 and ins_len < 500, f"Expected length ~465 bp, got {ins_len}"
assert ins_a_count > 50, f"ins_a_count too low: {ins_a_count}"
print("Ex 1.1 passed")
"""
        ),
        # Warm-up 2
        PracticeExercise(
            ex_id="Ex 1.2",
            stars="★☆☆",
            title="Calculate GC percentage of human insulin mRNA",
            biology="GC content influences mRNA stability and secondary structure folding energy.",
            task="Compute the GC percentage of human insulin mRNA and assign it to `ins_gc_percent` as a float rounded to 2 decimal places.",
            expected="`ins_gc_percent` as a float between 50.0 and 70.0.",
            student_code="""# TODO: replace the ... with your code
ins_seq = ins_record.seq
g_count = ...
c_count = ...
ins_gc_percent = ...
""",
            solution_code="""ins_seq = ins_record.seq
g_count = ins_seq.count("G")
c_count = ins_seq.count("C")
ins_gc_percent = round(((g_count + c_count) / len(ins_seq)) * 100, 2)
""",
            check_code="""# Check — do not edit
assert isinstance(ins_gc_percent, float), "ins_gc_percent should be a float"
assert 55.0 <= ins_gc_percent <= 65.0, f"Expected GC% between 55% and 65%, got {ins_gc_percent}"
print("Ex 1.2 passed")
"""
        ),
        # Warm-up 3
        PracticeExercise(
            ex_id="Ex 1.3",
            stars="★☆☆",
            title="Extract the 5' leader of HBB mRNA",
            biology="The 5' untranslated region precedes the start codon (AUG) and regulates translation initiation.",
            task="Load `hbb_human_mrna.fasta`. The first 50 bases represent the 5' UTR. Extract them into variable `hbb_leader`.",
            expected="A string or Seq of length 50 starting with 'ACATTTG'.",
            student_code="""# TODO: replace the ... with your code
hbb_record = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_mrna.fasta", "fasta")
hbb_leader = ...
""",
            solution_code="""hbb_record = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_mrna.fasta", "fasta")
hbb_leader = str(hbb_record.seq[:50])
""",
            check_code="""# Check — do not edit
assert len(hbb_leader) == 50, f"Expected length 50, got {len(hbb_leader)}"
assert hbb_leader.startswith("ACATTTG"), "hbb_leader should start with ACATTTG"
print("Ex 1.3 passed")
"""
        ),
        # Core 1
        PracticeExercise(
            ex_id="Ex 1.4",
            stars="★★☆",
            title="Compare base composition between HBB coding sequence and mRNA",
            biology="Untranslated regions (UTRs) frequently exhibit different nucleotide compositions compared to protein-coding exons.",
            task="Calculate the GC% of `hbb_human_cds.fasta` (`cds_gc`) and compare it to the full mRNA GC% (`mrna_gc`). Store the difference (`cds_gc - mrna_gc`) in `gc_diff`.",
            expected="`gc_diff` as a float rounded to 2 decimal places.",
            student_code="""# TODO: replace the ... with your code
cds_record = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_cds.fasta", "fasta")
cds_gc = ...
mrna_gc = round(((hbb_record.seq.count("G") + hbb_record.seq.count("C")) / len(hbb_record.seq)) * 100, 2)
gc_diff = ...
""",
            solution_code="""cds_record = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_cds.fasta", "fasta")
cds_gc = round(((cds_record.seq.count("G") + cds_record.seq.count("C")) / len(cds_record.seq)) * 100, 2)
mrna_gc = round(((hbb_record.seq.count("G") + hbb_record.seq.count("C")) / len(hbb_record.seq)) * 100, 2)
gc_diff = round(cds_gc - mrna_gc, 2)
""",
            check_code="""# Check — do not edit
assert isinstance(gc_diff, float), "gc_diff must be a float"
assert abs(gc_diff) < 10.0, "Difference between CDS and mRNA GC% should be modest"
print("Ex 1.4 passed")
"""
        ),
        # Core 2
        PracticeExercise(
            ex_id="Ex 1.5",
            stars="★★☆",
            title="Parse a multi-FASTA file and identify sequence lengths",
            biology="Multiple sequences in a file represent gene families, orthologues, or synthetic benchmarks.",
            task="Using `SeqIO.parse`, read `data/sequences/toy_sequences.fasta`. Store the number of records in `num_records`, and store a dictionary mapping record IDs to lengths in `length_dict`.",
            expected="`num_records` integer >= 2, `length_dict` mapping str -> int.",
            student_code="""# TODO: replace the ... with your code
toy_path = DATA_DIR / "sequences" / "toy_sequences.fasta"
length_dict = {}
for rec in SeqIO.parse(toy_path, "fasta"):
    ...

num_records = ...
""",
            solution_code="""toy_path = DATA_DIR / "sequences" / "toy_sequences.fasta"
length_dict = {}
for rec in SeqIO.parse(toy_path, "fasta"):
    length_dict[rec.id] = len(rec.seq)
num_records = len(length_dict)
""",
            check_code="""# Check — do not edit
assert isinstance(num_records, int) and num_records >= 2, "Expected at least 2 toy sequences"
assert all(isinstance(v, int) for v in length_dict.values()), "All lengths must be integers"
print("Ex 1.5 passed")
"""
        ),
        # Core 3
        PracticeExercise(
            ex_id="Ex 1.6",
            stars="★★☆",
            title="Confirm start codon complement on the minus strand",
            biology="If a gene is transcribed on the minus strand, the template DNA contains 3'-TAC-5', whose reverse complement in 5'->3' orientation is ATG.",
            task="Take the first 3 nucleotides of `cds_record.seq` (the canonical start codon). Compute its reverse complement in `rc_start`. Verify it equals 'CAT'.",
            expected="`rc_start` as a string equal to 'CAT'.",
            student_code="""# TODO: replace the ... with your code
start_codon = cds_record.seq[:3]
rc_start = ...
""",
            solution_code="""start_codon = cds_record.seq[:3]
rc_start = str(start_codon.reverse_complement())
""",
            check_code="""# Check — do not edit
assert rc_start == "CAT", f"Reverse complement of ATG should be CAT, got {rc_start}"
print("Ex 1.6 passed")
"""
        ),
        # Challenge 1
        PracticeExercise(
            ex_id="Ex 1.7",
            stars="★★★",
            title="Sliding window GC calculation across HBB mRNA",
            biology="Local GC fluctuations indicate structural features, CpG islands, or codon usage shifts.",
            task="Calculate the GC percentage in non-overlapping 100 bp windows along `hbb_record.seq`. Store the window GC percentages as a list of floats in `window_gcs`.",
            expected="A list of floats with length equal to `len(hbb_record.seq) // 100`.",
            student_code="""# TODO: replace the ... with your code
window_size = 100
full_dna = str(hbb_record.seq)
window_gcs = []

# Loop over the sequence in chunks of 100 bp
for i in range(0, len(full_dna) - window_size + 1, window_size):
    chunk = full_dna[i:i + window_size]
    ...
""",
            solution_code="""window_size = 100
full_dna = str(hbb_record.seq)
window_gcs = []

for i in range(0, len(full_dna) - window_size + 1, window_size):
    chunk = full_dna[i:i + window_size]
    gc_val = round(((chunk.count("G") + chunk.count("C")) / window_size) * 100, 2)
    window_gcs.append(gc_val)
""",
            check_code="""# Check — do not edit
assert isinstance(window_gcs, list) and len(window_gcs) == 6, f"Expected 6 windows of 100 bp, got {len(window_gcs)}"
assert all(30.0 <= x <= 75.0 for x in window_gcs), "Window GC percentages should fall in 30-75% range"
print("Ex 1.7 passed")
"""
        )
    ]
    
    # Build student notebook
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U01_P",
        title="Sequences as Text — Exercises",
        unit_num=1,
        unit_title="Bioinformatics and Internet",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L1–L2, Practical S1",
        before_this="U01_C1"
    ))
    nb_student.cells.append(make_setup_cell("U01_P"))
    
    # Build solution notebook
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U01_P",
        title="Sequences as Text — Solutions",
        unit_num=1,
        unit_title="Bioinformatics and Internet",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L1–L2, Practical S1",
        before_this="U01_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U01_P"))
    
    # Append exercises
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
        
    # Reflection section
    reflection_md = """## 5. Reflection Questions
1. Why does Python's 0-based indexing require biological coordinates to be converted when comparing against GenBank flat files?
2. Why is the reverse complement necessary when analyzing genes encoded on the opposite DNA strand, rather than just the simple string reverse (`seq[::-1]`)?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u01_q():
    """Build U01_Q quiz notebook (student and key versions)."""
    salt = "U01_Q"
    questions = [
        QuizQuestion("q1", "What three major biological databases constitute the International Nucleotide Sequence Database Collaboration (INSDC)?",
                     ["(a) NCBI, EMBL-EBI, DDBJ", "(b) PDB, UniProt, Pfam", "(c) RefSeq, Ensembl, GenBank", "(d) PubMed, PMC, OMIM"],
                     "a", "U01_C1 §1"),
        QuizQuestion("q2", "In Python 0-based indexing, how many characters does the slice `seq[0:4]` extract?",
                     ["(a) 3", "(b) 4", "(c) 5", "(d) None"],
                     "b", "U01_C1 §3"),
        QuizQuestion("q3", "What is the reverse complement of the DNA sequence 5'-ATGC-3'?",
                     ["(a) 5'-CGTA-3'", "(b) 5'-GCAT-3'", "(c) 5'-TACG-3'", "(d) 5'-ATGC-3'"],
                     "b", "U01_C1 §6"),
        QuizQuestion("q4", "Which Biopython `Bio.SeqIO` method should you use when reading a multi-FASTA file containing 100 sequences?",
                     ["(a) SeqIO.read()", "(b) SeqIO.parse()", "(c) SeqIO.load()", "(d) SeqIO.get_all()"],
                     "b", "U01_C1 §5"),
        QuizQuestion("q5", "Which character marks the beginning of a header line in a FASTA format file?",
                     ["(a) @", "(b) #", "(c) >", "(d) %"],
                     "c", "U01_C1 §5"),
        QuizQuestion("q6", "Given the 1-based GenBank CDS coordinates `51..494`, what is the length in nucleotides of the coding region?",
                     ["(a) 443", "(b) 444", "(c) 445", "(d) 494"],
                     "b", "U01_C1 §3"),
        QuizQuestion("q7", "Calculate the GC percentage of the sequence 'GCATCG'. Round your answer to 1 decimal place (e.g. 66.7).",
                     [],
                     66.7, "U01_C1 §4"),
        QuizQuestion("q8", "What network protocol is primarily used for programmatic web retrieval of REST APIs and web pages?",
                     ["(a) FTP", "(b) SMTP", "(c) HTTP", "(d) Telnet"],
                     "c", "U01_C1 §1"),
        QuizQuestion("q9", "If a double-stranded DNA sequence has 30% Adenine, what is its expected Cytosine percentage?",
                     ["(a) 20%", "(b) 30%", "(c) 40%", "(d) 70%"],
                     "a", "U01_C1 §4"),
        QuizQuestion("q10", "Which Python method converts all lowercase characters in string `s` to uppercase?",
                     ["(a) s.to_upper()", "(b) s.upper()", "(c) s.capitalize()", "(d) s.case_up()"],
                     "b", "U01_C1 §4")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    # Student notebook
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U01_Q",
        title="Bioinformatics and Internet — Quiz",
        unit_num=1,
        unit_title="Bioinformatics and Internet",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L1–L2, Practical S1",
        before_this="U01_C1, U01_P"
    ))
    nb_student.cells.append(make_setup_cell("U01_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    # Key notebook
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U01_Q",
        title="Bioinformatics and Internet — Quiz Key",
        unit_num=1,
        unit_title="Bioinformatics and Internet",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L1–L2, Practical S1",
        before_this="U01_C1, U01_P"
    ))
    nb_key.cells.append(make_setup_cell("U01_Q"))
    nb_key.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    # Section A: MCQs
    nb_student.cells.append(nbf.v4.new_markdown_cell("## Section A — Concept MCQs\nSelect the single best option for each question."))
    nb_key.cells.append(nbf.v4.new_markdown_cell("## Section A — Concept MCQs\nSelect the single best option for each question."))
    
    for q in questions:
        q_md = f"**{q.qid}.** {q.prompt}\n"
        if q.options:
            q_md += "  ".join(q.options)
        
        nb_student.cells.append(nbf.v4.new_markdown_cell(q_md.strip()))
        nb_student.cells.append(nbf.v4.new_code_cell(f'check("{q.qid}", "")'))
        
        nb_key.cells.append(nbf.v4.new_markdown_cell(q_md.strip()))
        if isinstance(q.answer, (int, float)):
            nb_key.cells.append(nbf.v4.new_code_cell(f'check("{q.qid}", {q.answer})'))
        else:
            nb_key.cells.append(nbf.v4.new_code_cell(f'check("{q.qid}", "{q.answer}")'))
            
    # Score cell
    nb_student.cells.append(nbf.v4.new_code_cell("show_score()"))
    nb_key.cells.append(nbf.v4.new_code_cell("show_score()"))
    
    # Key debug cell at end of Key notebook
    answers_repr = {q.qid: q.answer for q in questions}
    nb_key.cells.append(nbf.v4.new_code_cell(f'''# Verification of answers dictionary and generated keys
answers = {answers_repr!r}
print("Keys:", {{q: _digest(a) for q, a in answers.items()}})
'''))

    return nb_student, nb_key


def generate_unit01():
    """Generate all notebooks for Unit 1."""
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 01 notebooks...")
    c1 = build_u01_c1()
    save_notebook(c1, UNIT_DIR / "U01_C1_Sequences_as_Text.ipynb", clear=True)
    
    p_student, p_sol = build_u01_p()
    save_notebook(p_student, UNIT_DIR / "U01_P_Sequences_as_Text.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U01_P_Sequences_as_Text_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u01_q()
    save_notebook(q_student, UNIT_DIR / "U01_Q_Bioinformatics_and_Internet.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U01_Q_Bioinformatics_and_Internet_Key.ipynb", clear=False)
    
    print("  ✓ Unit 01 files written successfully.")
