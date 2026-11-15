"""
unit08.py - Builder for Unit 08: Predictive Methods using Nucleotide Sequence
Notebooks:
- U08_C1_ORFs_GC_and_Codon_Usage.ipynb
- U08_P_Nucleotide_Analysis.ipynb
- solutions/U08_P_Nucleotide_Analysis_Solutions.ipynb
- U08_Q_Predictive_Nucleotide.ipynb
- solutions/U08_Q_Predictive_Nucleotide_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U08_Predictive_Nucleotide"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u08_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U08_C1",
        title="ORFs, GC Content, and Codon Usage",
        unit_num=8,
        unit_title="Predictive Methods using Nucleotide Sequence",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L21–L22, Practical S9 (ORFfinder & EMBOSS cusp)",
        before_this="U07_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** the six reading frames of double-stranded DNA [LO6].
- **Identify** Open Reading Frames (ORFs) using start (ATG) and stop (TAA, TAG, TGA) codons with a length threshold [LO6].
- **Calculate** sliding-window GC content to identify CpG islands and compositional shifts [LO6].
- **Quantify** codon usage bias in protein-coding genes [LO6].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
When a new genome or cDNA sequence is determined, how do computational pipelines locate the protein-coding genes without prior laboratory evidence? Because stop codons occur by chance once every 21 codons in random DNA ($3 / 64 \\approx 1/21$), an unusually long stretch without a stop codon starting with ATG strongly suggests a functional protein-coding gene. How do we scan all six reading frames of human *HBB* mRNA to pinpoint its true coding sequence?
"""))

    nb.cells.append(make_setup_cell("U08_C1"))

    # Concept 1: Six Reading Frames
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The Six Reading Frames
### Theory
Because the genetic code is read in non-overlapping triplets of nucleotides (codons), any DNA sequence has three reading frames on the forward strand depending on whether translation begins at index 0 (+1), index 1 (+2), or index 2 (+3).

Because DNA is double-stranded and transcription can occur on the opposite complementary strand, there are also three reading frames on the reverse complement strand (-1, -2, -3). Thus, any genomic DNA locus has **six possible reading frames**.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Translating in all six reading frames
from Bio import SeqIO

hbb_path = DATA_DIR / "sequences" / "hbb_human_mrna.fasta"
record = SeqIO.read(hbb_path, "fasta")
dna = record.seq

frames = {}
for i in range(3):
    frames[f"+{i+1}"] = dna[i:].translate()

rc = dna.reverse_complement()
for i in range(3):
    frames[f"-{i+1}"] = rc[i:].translate()

print("=== 6-Frame Translation of HBB mRNA ===")
for frame_name, peptide in frames.items():
    stop_count = peptide.count("*")
    print(f"Frame {frame_name}: Length = {len(peptide)} aa | Stop Codons (*) = {stop_count:2} | Start: {peptide[:20]}...")
'''))

    # Concept 2: ORF Finding
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Identifying Open Reading Frames (ORFs)
### Theory
An **Open Reading Frame (ORF)** is a continuous stretch of codons beginning with a start codon (canonical `ATG`), containing sense codons, and terminating at an in-frame stop codon (`TAA`, `TAG`, `TGA`).
- Random non-coding DNA has an expected stop codon every $64 / 3 \\approx 21.3$ codons.
- True eukaryotic and bacterial proteins typically contain $>100$ amino acids (300 bp).
- Applying a minimum length threshold (e.g. $\\ge 100$ aa) filters out false-positive random stop-free intervals.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Scanning for genuine ORFs in HBB mRNA
def find_forward_orfs(seq_str, min_aa=50):
    seq_str = seq_str.upper()
    orfs = []
    for frame in range(3):
        for i in range(frame, len(seq_str) - 2, 3):
            if seq_str[i:i+3] == "ATG":
                for j in range(i + 3, len(seq_str) - 2, 3):
                    if seq_str[j:j+3] in ["TAA", "TAG", "TGA"]:
                        aa_len = (j + 3 - i - 3) // 3
                        if aa_len >= min_aa:
                            orfs.append({
                                "frame": frame + 1,
                                "start_1based": i + 1,
                                "end_1based": j + 3,
                                "length_nt": j + 3 - i,
                                "length_aa": aa_len,
                                "subseq": seq_str[i:j+3]
                            })
                        break
    return orfs

found_orfs = find_forward_orfs(str(dna), min_aa=50)
print(f"Found {len(found_orfs)} candidate ORFs >= 50 aa:")
for idx, orf in enumerate(found_orfs, 1):
    print(f"  ORF {idx}: Frame +{orf['frame']} | 1-based Coordinates: {orf['start_1based']}..{orf['end_1based']} "
          f"| Length: {orf['length_nt']} nt ({orf['length_aa']} aa)")
'''))

    # Concept 3: Sliding-Window GC Content
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Sliding-Window GC Content
### Theory
GC content varies locally across chromosomes. Promoters often contain unmethylated **CpG islands** ($>50\\%$ GC and observed-to-expected CpG ratio $>0.6$). Exons frequently exhibit elevated GC content compared to surrounding introns. A **sliding window** moves across the sequence with step size $S$ and window size $W$, calculating local GC percentage.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Sliding window GC profile
import matplotlib.pyplot as plt

window_size = 50
step = 10
dna_str = str(dna)
gc_profile = []
positions = []

for i in range(0, len(dna_str) - window_size + 1, step):
    window = dna_str[i:i + window_size]
    gc_val = ((window.count("G") + window.count("C")) / window_size) * 100
    gc_profile.append(gc_val)
    positions.append(i + window_size // 2)

fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(positions, gc_profile, color="teal", lw=1.5)
ax.axhline(51.8, color="red", linestyle="--", alpha=0.7, label="Mean GC% (51.8%)")
ax.axvspan(51, 494, color="yellow", alpha=0.2, label="Coding CDS (51-494)")
ax.set_xlabel("Nucleotide Position in HBB mRNA")
ax.set_ylabel("GC Percentage")
ax.set_title("Sliding Window GC Profile (Window = 50 bp, Step = 10 bp)")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig(OUT_DIR / "hbb_gc_profile.png", dpi=100)
plt.show()
'''))

    # Concept 4: Codon Usage Bias
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Codon Usage Bias
### Theory
The genetic code has 64 codons encoding 20 amino acids and 3 stops. Most amino acids are specified by 2 to 6 synonymous codons. Organisms do *not* use synonymous codons equally:
- Highly expressed genes preferentially use codons recognized by the most abundant cellular tRNAs (**translational efficiency**).
- Heterologous expression (e.g. human insulin in *E. coli*) often requires codon optimization to match host codon preferences.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Computing codon counts for HBB coding sequence
cds_str = str(found_orfs[0]["subseq"])
codon_counts = {}

for i in range(0, len(cds_str) - 2, 3):
    codon = cds_str[i:i+3]
    codon_counts[codon] = codon_counts.get(codon, 0) + 1

# Inspect Leucine codons (encoded by 6 codons: CTT, CTC, CTA, CTG, TTA, TTG)
leu_codons = ["CTT", "CTC", "CTA", "CTG", "TTA", "TTG"]
print("Leucine Synonymous Codon Usage in Human HBB CDS:")
for lc in leu_codons:
    cnt = codon_counts.get(lc, 0)
    print(f"  {lc} : {cnt:2} occurrences")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Compare with NCBI ORFfinder
In Practical S9, we pasted the HBB mRNA sequence into NCBI ORFfinder. The primary returned ORF was:
- Frame: `+3` (or 1-based coordinates 51..494)
- Length: `444 nt` / `147 aa`
Our Python code produces the exact same start position (51), end position (494), and translated protein length.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Summary
- Double-stranded DNA has 6 reading frames (3 forward, 3 reverse complement).
- An ORF starts with ATG and ends at an in-frame stop codon (TAA, TAG, TGA).
- Length thresholds (e.g. $>300$ nt) eliminate the high background of random stop-free segments.
- Codon bias reflects evolutionary optimization for translational accuracy and efficiency.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 9. Next Steps
- Complete practice exercises in `U08_P_Nucleotide_Analysis.ipynb`.
- Self-test ORF finding and codon bias concepts in `U08_Q_Predictive_Nucleotide.ipynb`.
"""))

    return nb


def build_u08_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 8.1",
            stars="★☆☆",
            title="Count stop codons in Frame +1 of HBB mRNA",
            biology="Non-coding frames typically contain numerous stop codons.",
            task="Translate `hbb_human_mrna.fasta` in Frame +1 (starting at index 0) and count the number of stop codons (`'*'`). Store the count in `frame1_stops`.",
            expected="`frame1_stops` as an integer > 5.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

rec = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_mrna.fasta", "fasta")
dna = rec.seq
trans_f1 = ...
frame1_stops = ...
""",
            solution_code="""from Bio import SeqIO

rec = SeqIO.read(DATA_DIR / "sequences" / "hbb_human_mrna.fasta", "fasta")
dna = rec.seq
trans_f1 = dna.translate()
frame1_stops = trans_f1.count("*")
""",
            check_code="""# Check — do not edit
assert frame1_stops > 5, f"Expected > 5 stop codons in non-coding frame, got {frame1_stops}"
print("Ex 8.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 8.2",
            stars="★☆☆",
            title="Identify canonical stop codons",
            biology="Standard nuclear genetic code uses three stop codons: TAA (ochre), TAG (amber), and TGA (opal).",
            task="Create a set `stop_codons` containing the three canonical DNA stop codon strings. Verify whether `'TGA'` is in `stop_codons`.",
            expected="`stop_codons` is a set with 3 elements.",
            student_code="""# TODO: replace the ... with your code
stop_codons = ...
""",
            solution_code="""stop_codons = {"TAA", "TAG", "TGA"}
""",
            check_code="""# Check — do not edit
assert len(stop_codons) == 3
assert "TAA" in stop_codons and "TAG" in stop_codons and "TGA" in stop_codons
print("Ex 8.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 8.3",
            stars="★★☆",
            title="Find the primary coding ORF in human insulin mRNA",
            biology="Human preproinsulin (INS) is encoded by NM_000207.3.",
            task="Scan `ins_human_mrna.fasta` for the longest ORF starting with `'ATG'` and ending with a canonical stop codon. Store its amino acid length in `ins_orf_aa_len`.",
            expected="`ins_orf_aa_len` == 110.",
            student_code="""# TODO: replace the ... with your code
ins_dna = str(SeqIO.read(DATA_DIR / "sequences" / "ins_human_mrna.fasta", "fasta").seq).upper()

longest_aa = 0
for frame in range(3):
    for i in range(frame, len(ins_dna) - 2, 3):
        if ins_dna[i:i+3] == "ATG":
            for j in range(i + 3, len(ins_dna) - 2, 3):
                if ins_dna[j:j+3] in stop_codons:
                    aa_len = (j + 3 - i - 3) // 3
                    if aa_len > longest_aa:
                        longest_aa = aa_len
                    break

ins_orf_aa_len = ...
""",
            solution_code="""ins_dna = str(SeqIO.read(DATA_DIR / "sequences" / "ins_human_mrna.fasta", "fasta").seq).upper()

longest_aa = 0
for frame in range(3):
    for i in range(frame, len(ins_dna) - 2, 3):
        if ins_dna[i:i+3] == "ATG":
            for j in range(i + 3, len(ins_dna) - 2, 3):
                if ins_dna[j:j+3] in stop_codons:
                    aa_len = (j + 3 - i - 3) // 3
                    if aa_len > longest_aa:
                        longest_aa = aa_len
                    break

ins_orf_aa_len = longest_aa
""",
            check_code="""# Check — do not edit
assert ins_orf_aa_len == 110, f"Expected 110 amino acids for preproinsulin ORF, got {ins_orf_aa_len}"
print("Ex 8.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 8.4",
            stars="★★☆",
            title="Simulate beta-thalassemia codon 39 nonsense mutation",
            biology="A common Mediterranean beta-thalassemia mutation mutates codon 39 (CAG, Gln) to UAG (stop), truncating beta-globin.",
            task="Take the wild-type HBB coding sequence `hbb_cds`. Mutate codon 39 from `'CAG'` to `'TAG'`. Translate to stop and store the resulting truncated peptide length in `trunc_len`.",
            expected="`trunc_len` == 38 amino acids.",
            student_code="""# TODO: replace the ... with your code
hbb_cds = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_cds.fasta", "fasta").seq)

# Codon 39 (1-based codon 39 = 0-based nt indices 38*3 to 38*3+3 = 114 to 117)
c39_start = 38 * 3
mutated_cds = hbb_cds[:c39_start] + "TAG" + hbb_cds[c39_start + 3:]

trunc_peptide = ...
trunc_len = ...
""",
            solution_code="""hbb_cds = str(SeqIO.read(DATA_DIR / "sequences" / "hbb_human_cds.fasta", "fasta").seq)

c39_start = 38 * 3
mutated_cds = hbb_cds[:c39_start] + "TAG" + hbb_cds[c39_start + 3:]

from Bio.Seq import Seq
trunc_peptide = Seq(mutated_cds).translate(to_stop=True)
trunc_len = len(trunc_peptide)
""",
            check_code="""# Check — do not edit
assert trunc_len == 38, f"Expected 38 aa truncated peptide, got {trunc_len}"
print("Ex 8.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 8.5",
            stars="★★☆",
            title="Calculate overall codon usage in human HBB CDS",
            biology="Quantifying codon frequency across a coding sequence.",
            task="Iterate across `hbb_cds` in codons of 3. Store the total number of codons in `total_codons`, and count how many times `'CTG'` occurs in `ctg_count`.",
            expected="`total_codons` = 148 (147 amino acids + stop), `ctg_count` > 5.",
            student_code="""# TODO: replace the ... with your code
total_codons = ...
ctg_count = ...
""",
            solution_code="""codons = [hbb_cds[i:i+3] for i in range(0, len(hbb_cds) - 2, 3)]
total_codons = len(codons)
ctg_count = codons.count("CTG")
""",
            check_code="""# Check — do not edit
assert total_codons == 148, f"Expected 148 codons, got {total_codons}"
assert ctg_count >= 5, f"Expected >= 5 CTG codons, got {ctg_count}"
print("Ex 8.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 8.6",
            stars="★★★",
            title="Calculate GC skew along sliding windows",
            biology="GC skew $(G - C) / (G + C)$ changes sign at bacterial replication origins and reveals transcription strand asymmetry.",
            task="Write a function `calc_gc_skew(dna_seq)` returning $(G - C) / (G + C)$ as a float rounded to 3 decimal places (return 0.0 if $G+C=0$). Compute the skew for `hbb_cds` in `cds_skew`.",
            expected="`cds_skew` as a float between -0.5 and +0.5.",
            student_code="""# TODO: replace the ... with your code
def calc_gc_skew(dna_seq):
    ...

cds_skew = calc_gc_skew(hbb_cds)
""",
            solution_code="""def calc_gc_skew(dna_seq):
    g = dna_seq.count("G")
    c = dna_seq.count("C")
    if g + c == 0:
        return 0.0
    return round((g - c) / (g + c), 3)

cds_skew = calc_gc_skew(hbb_cds)
""",
            check_code="""# Check — do not edit
assert isinstance(cds_skew, float)
assert -0.5 <= cds_skew <= 0.5, f"Unexpected GC skew: {cds_skew}"
print("Ex 8.6 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U08_P",
        title="Nucleotide Analysis — Exercises",
        unit_num=8,
        unit_title="Predictive Methods using Nucleotide Sequence",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L21–L22, Practical S9",
        before_this="U08_C1"
    ))
    nb_student.cells.append(make_setup_cell("U08_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U08_P",
        title="Nucleotide Analysis — Solutions",
        unit_num=8,
        unit_title="Predictive Methods using Nucleotide Sequence",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L21–L22, Practical S9",
        before_this="U08_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U08_P"))
    
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
1. Why does a random sequence of DNA contain stop codons approximately every 21 codons on average, and why does this make long ORFs good candidate protein-coding genes?
2. What are the major differences between gene prediction in prokaryotes (dense, continuous ORFs) and eukaryotes (interrupted by introns, alternative splicing)?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u08_q():
    salt = "U08_Q"
    questions = [
        QuizQuestion("q1", "How many possible reading frames exist for a given double-stranded DNA molecule?",
                     ["(a) 1", "(b) 3", "(c) 6", "(d) 12"],
                     "c", "U08_C1 §3"),
        QuizQuestion("q2", "Which codon serves as the universal canonical start codon in eukaryotes?",
                     ["(a) UAA", "(b) ATG (AUG)", "(c) TGA", "(d) GUG"],
                     "b", "U08_C1 §4"),
        QuizQuestion("q3", "Which of the following is NOT a canonical stop codon in the standard genetic code?",
                     ["(a) TAA", "(b) TAG", "(c) TGA", "(d) TGG"],
                     "d", "U08_C1 §4"),
        QuizQuestion("q4", "In random DNA with equal base frequencies, what is the expected average frequency of stop codons in any given reading frame?",
                     ["(a) 1 in 4", "(b) 1 in 21.3", "(c) 1 in 64", "(d) 1 in 300"],
                     "b", "U08_C1 §4"),
        QuizQuestion("q5", "What formula defines GC skew in genome analysis?",
                     ["(a) (G + C) / Total", "(b) (G - C) / (G + C)", "(c) G / C", "(d) (A + T) / (G + C)"],
                     "b", "U08_C1 §5"),
        QuizQuestion("q6", "What biological phenomenon causes synonymous codons for the same amino acid to be used with unequal frequencies in a genome?",
                     ["(a) Genetic drift alone", "(b) Codon usage bias", "(c) Wobble elimination", "(d) Alternative splicing"],
                     "b", "U08_C1 §6"),
        QuizQuestion("q7", "What ribosomal binding consensus sequence precedes bacterial start codons to position the mRNA for translation?",
                     ["(a) Kozak consensus", "(b) Shine–Dalgarno sequence", "(c) TATA box", "(d) Polyadenylation signal"],
                     "b", "U08_C1 §4"),
        QuizQuestion("q8", "What nucleotide motif often marks mammalian promoter regions and is characterized by elevated GC content and unmethylated cytosines?",
                     ["(a) Alu repeat", "(b) CpG island", "(c) Pribnow box", "(d) CAAT box"],
                     "b", "U08_C1 §5"),
        QuizQuestion("q9", "Why is ab initio gene prediction significantly more difficult in eukaryotic genomes than in bacterial genomes?",
                     ["(a) Eukaryotic genomes lack start codons", "(b) Eukaryotic genes are interrupted by introns and often undergo alternative splicing", "(c) Eukaryotes have circular DNA", "(d) Eukaryotes do not use the standard genetic code"],
                     "b", "U08_C1 §4"),
        QuizQuestion("q10", "What program in EMBOSS calculates codon usage tables from nucleotide sequences?",
                     ["(a) geecee", "(b) cusp", "(c) transeq", "(d) needle"],
                     "b", "U08_C1 §6")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U08_Q",
        title="Predictive Nucleotide — Quiz",
        unit_num=8,
        unit_title="Predictive Methods using Nucleotide Sequence",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L21–L22, Practical S9",
        before_this="U08_C1, U08_P"
    ))
    nb_student.cells.append(make_setup_cell("U08_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U08_Q",
        title="Predictive Nucleotide — Quiz Key",
        unit_num=8,
        unit_title="Predictive Methods using Nucleotide Sequence",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L21–L22, Practical S9",
        before_this="U08_C1, U08_P"
    ))
    nb_key.cells.append(make_setup_cell("U08_Q"))
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


def generate_unit08():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 08 notebooks...")
    c1 = build_u08_c1()
    save_notebook(c1, UNIT_DIR / "U08_C1_ORFs_GC_and_Codon_Usage.ipynb", clear=True)
    
    p_student, p_sol = build_u08_p()
    save_notebook(p_student, UNIT_DIR / "U08_P_Nucleotide_Analysis.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U08_P_Nucleotide_Analysis_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u08_q()
    save_notebook(q_student, UNIT_DIR / "U08_Q_Predictive_Nucleotide.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U08_Q_Predictive_Nucleotide_Key.ipynb", clear=False)
    
    print("  ✓ Unit 08 files written successfully.")
