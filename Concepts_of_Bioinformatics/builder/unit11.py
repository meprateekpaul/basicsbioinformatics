"""
unit11.py - Builder for Unit 11: Comparative Genome Analysis
Notebooks:
- U11_C1_Comparing_Two_Genomes.ipynb
- U11_P_Comparative_Genomics.ipynb
- solutions/U11_P_Comparative_Genomics_Solutions.ipynb
- U11_Q_Comparative_Genomics.ipynb
- solutions/U11_Q_Comparative_Genomics_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U11_Comparative_Genomics"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u11_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U11_C1",
        title="Comparing Two Genomes",
        unit_num=11,
        unit_title="Comparative Genome Analysis",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L29–L30 (Genome Annotation & Comparative Genomics)",
        before_this="U10_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Compare** fundamental genome statistics (length, GC content, gene count) across related genomes [LO8].
- **Calculate** coding density and recognize overlapping reading frames in compact viral genomes [LO8].
- **Identify** homologous gene sets from tabular BLAST comparisons [LO8].
- **Evaluate** gene order conservation (synteny) between divergent viral genomes [LO8].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Bacteriophages $\\phi X174$ (5386 bp) and G4 (5577 bp) are single-stranded DNA microviruses that infect enteric bacteria. They were the very first DNA genomes ever sequenced (Fred Sanger, 1977). Despite substantial nucleotide divergence, how do their gene repertoires compare? How do compact viruses squeeze 11 proteins into only 5.4 kb of DNA, and how does comparative genomics prove their functional orthology?
"""))

    nb.cells.append(make_setup_cell("U11_C1"))

    # Concept 1: Genome Summary Metrics
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Fundamental Genome Metrics
### Theory
Comparative genomics begins by contrasting summary macro-metrics:
1. **Genome Size**: Measured in base pairs (bp), kilobases (kb), or megabases (Mb).
2. **Overall GC Percentage**: Dictated by mutational bias, replication machinery, and ecological niche.
3. **Gene and CDS Count**: Number of transcribed units and protein-coding open reading frames.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading and comparing PhiX174 vs G4 Phage
from Bio import SeqIO

phix_path = DATA_DIR / "genomes" / "phix174.gb"
g4_path = DATA_DIR / "genomes" / "g4_phage.gb"

phix_rec = SeqIO.read(phix_path, "genbank")
g4_rec = SeqIO.read(g4_path, "genbank")

def summarize_genome(rec):
    length = len(rec.seq)
    gc = ((rec.seq.count("G") + rec.seq.count("C")) / length) * 100
    cds_features = [f for f in rec.features if f.type == "CDS"]
    return {
        "accession": rec.id,
        "organism": rec.annotations.get("organism", ""),
        "length_bp": length,
        "gc_percent": round(gc, 2),
        "cds_count": len(cds_features)
    }

meta_phix = summarize_genome(phix_rec)
meta_g4 = summarize_genome(g4_rec)

print("=== Comparative Summary Table ===")
print(f"{'Feature':20} | {'PhiX174':15} | {'G4 Phage':15}")
print("-" * 56)
print(f"{'Accession':20} | {meta_phix['accession']:15} | {meta_g4['accession']:15}")
print(f"{'Genome Length':20} | {meta_phix['length_bp']:<15} | {meta_g4['length_bp']:<15}")
print(f"{'GC Content (%)':20} | {meta_phix['gc_percent']:<15} | {meta_g4['gc_percent']:<15}")
print(f"{'Protein CDS Count':20} | {meta_phix['cds_count']:<15} | {meta_g4['cds_count']:<15}")
'''))

    # Concept 2: Coding Density
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Coding Density and Overlapping Reading Frames
### Theory
**Coding density** measures the proportion of genomic DNA dedicated to protein coding:
$$\\text{Coding Density} = \\frac{\\sum \\text{Length of all CDS (bp)}}{\\text{Genome Length (bp)}} \\times 100$$
- In humans, protein-coding exons comprise $< 2\\%$ of the genome.
- In bacteria, coding density is $\\approx 85-90\\%$.
- In microviruses (like $\\phi X174$), coding density can exceed $100\\%$ because genes overlap and are translated in different reading frames (e.g. gene B is encoded completely within gene A; gene E is within gene D).
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Calculating coding density
def calc_coding_density(rec):
    total_cds_nt = 0
    for f in rec.features:
        if f.type == "CDS":
            total_cds_nt += len(f.extract(rec.seq))
    density = (total_cds_nt / len(rec.seq)) * 100
    return total_cds_nt, round(density, 1)

nt_phix, dens_phix = calc_coding_density(phix_rec)
nt_g4, dens_g4 = calc_coding_density(g4_rec)

print(f"PhiX174: {nt_phix} coding nt in {len(phix_rec.seq)} bp genome -> Coding Density = {dens_phix}%")
print(f"G4 Phage: {nt_g4} coding nt in {len(g4_rec.seq)} bp genome -> Coding Density = {dens_g4}%")
'''))

    # Concept 3: Homologous Gene Sets
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Shared Homologous Genes via Tabular BLAST
### Theory
Comparing gene content involves running all-against-all protein BLAST (BLASTP) between the proteomes of two genomes. The resulting High-Scoring Segment Pairs identify homologous pairs, their percent identity, and evolutionary divergence.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Inspecting shared orthologues from BLAST table
import pandas as pd

blast_path = DATA_DIR / "expected" / "blast_phix174_vs_g4.tsv"
df_shared = pd.read_csv(blast_path, sep="\\t")

print("=== Homologous Proteins Shared Between PhiX174 and G4 Phage ===")
print(df_shared[["query_id", "subject_id", "identity", "evalue", "subject_title"]])

avg_ident = df_shared["identity"].mean()
print(f"\\nMean sequence identity across all shared viral proteins: {avg_ident:.1f}%")
'''))

    # Concept 4: Synteny
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Conserved Gene Order (Synteny)
### Theory
**Synteny** refers to the preservation of gene order on corresponding chromosomes between different species. In bacteriophages, the capsid, spike, replication, and lysis genes occur in a strictly conserved sequential order, demonstrating strong evolutionary constraint on transcriptional timing.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Verifying collinear synteny
print("Ordered gene products in G4 matching PhiX174 query order:")
for idx, title in enumerate(df_shared["subject_title"], 1):
    print(f"  Gene {idx:2}: {title}")
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Summary
- Comparative genomics reveals conserved core genes and structural genome reorganization.
- Viral genomes achieve extreme coding density ($>90-100\\%$) through overlapping reading frames.
- Synteny analysis confirms that gene order is conserved even when sequence identity has decayed to $\\sim 60\\%$.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Next Steps
- Compare polyomaviruses (SV40 vs BKV) in `U11_P_Comparative_Genomics.ipynb`.
- Self-test comparative genomics concepts in `U11_Q_Comparative_Genomics.ipynb`.
"""))

    return nb


def build_u11_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 11.1",
            stars="★☆☆",
            title="Load SV40 and BKV genomes and report sizes",
            biology="Simian virus 40 (SV40) and BK polyomavirus (BKV) are mammalian double-stranded DNA viruses.",
            task="Load `data/genomes/sv40.gb` and `data/genomes/bkv.gb` using `SeqIO.read`. Store their genome lengths in `sv40_len` and `bkv_len`.",
            expected="`sv40_len` = 5243 bp, `bkv_len` = 5153 bp.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

sv40_rec = SeqIO.read(DATA_DIR / "genomes" / "sv40.gb", "genbank")
bkv_rec = SeqIO.read(DATA_DIR / "genomes" / "bkv.gb", "genbank")

sv40_len = ...
bkv_len = ...
""",
            solution_code="""from Bio import SeqIO

sv40_rec = SeqIO.read(DATA_DIR / "genomes" / "sv40.gb", "genbank")
bkv_rec = SeqIO.read(DATA_DIR / "genomes" / "bkv.gb", "genbank")

sv40_len = len(sv40_rec.seq)
bkv_len = len(bkv_rec.seq)
""",
            check_code="""# Check — do not edit
assert sv40_len == 5243, f"Expected 5243 bp, got {sv40_len}"
assert bkv_len == 5153, f"Expected 5153 bp, got {bkv_len}"
print("Ex 11.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.2",
            stars="★☆☆",
            title="Compute GC percentage for SV40 and BKV",
            biology="Polyomaviruses infect primate kidneys and lymphocytes with conserved AT/GC composition.",
            task="Compute the GC percentage for `sv40_rec` in `sv40_gc` and `bkv_rec` in `bkv_gc` rounded to 1 decimal place.",
            expected="`sv40_gc` ~40.8%, `bkv_gc` ~39.5%.",
            student_code="""# TODO: replace the ... with your code
sv40_gc = ...
bkv_gc = ...
""",
            solution_code="""sv40_gc = round(((sv40_rec.seq.count("G") + sv40_rec.seq.count("C")) / sv40_len) * 100, 1)
bkv_gc = round(((bkv_rec.seq.count("G") + bkv_rec.seq.count("C")) / bkv_len) * 100, 1)
""",
            check_code="""# Check — do not edit
assert 40.0 <= sv40_gc <= 41.5, f"Expected ~40.8%, got {sv40_gc}"
assert 39.0 <= bkv_gc <= 40.5, f"Expected ~39.5%, got {bkv_gc}"
print("Ex 11.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.3",
            stars="★☆☆",
            title="Count protein-coding genes in each viral genome",
            biology="Polyomaviruses encode early regulatory proteins (T-antigens) and late structural capsid proteins (VPs).",
            task="Count the number of features of type `'CDS'` in `sv40_rec` into `sv40_cds_count`, and in `bkv_rec` into `bkv_cds_count`.",
            expected="`sv40_cds_count` and `bkv_cds_count` between 5 and 8.",
            student_code="""# TODO: replace the ... with your code
sv40_cds_count = ...
bkv_cds_count = ...
""",
            solution_code="""sv40_cds_count = sum(1 for f in sv40_rec.features if f.type == "CDS")
bkv_cds_count = sum(1 for f in bkv_rec.features if f.type == "CDS")
""",
            check_code="""# Check — do not edit
assert 5 <= sv40_cds_count <= 8, f"Unexpected SV40 CDS count: {sv40_cds_count}"
assert 5 <= bkv_cds_count <= 8, f"Unexpected BKV CDS count: {bkv_cds_count}"
print("Ex 11.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.4",
            stars="★★☆",
            title="Compute total coding nucleotides and coding density for SV40",
            biology="Small DNA tumor viruses maximize coding capacity within tight icosahedral capsid limits.",
            task="Sum the nucleotide length of all CDS features in `sv40_rec`. Store the total in `sv40_coding_nt` and the coding density percentage in `sv40_density` rounded to 1 decimal place.",
            expected="`sv40_density` > 80.0%.",
            student_code="""# TODO: replace the ... with your code
sv40_coding_nt = ...
sv40_density = ...
""",
            solution_code="""sv40_coding_nt = sum(len(f.extract(sv40_rec.seq)) for f in sv40_rec.features if f.type == "CDS")
sv40_density = round((sv40_coding_nt / sv40_len) * 100, 1)
""",
            check_code="""# Check — do not edit
assert sv40_coding_nt > 4000, f"Expected > 4000 coding nt, got {sv40_coding_nt}"
assert sv40_density > 80.0, f"Expected coding density > 80%, got {sv40_density}%"
print("Ex 11.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.5",
            stars="★★☆",
            title="Find the most conserved protein between SV40 and BKV",
            biology="Large T-antigen drives viral replication and host cell transformation.",
            task="Load `data/expected/blast_sv40_vs_bkv.tsv` with pandas. Find the hit with the highest `identity` percentage. Store its `subject_title` in `top_conserved_protein` and its identity in `top_identity`.",
            expected="`top_conserved_protein` contains 'large T antigen', `top_identity` > 80.0%.",
            student_code="""# TODO: replace the ... with your code
import pandas as pd

df_sv40 = pd.read_csv(DATA_DIR / "expected" / "blast_sv40_vs_bkv.tsv", sep="\\t")
max_idx = ...
top_conserved_protein = ...
top_identity = ...
""",
            solution_code="""import pandas as pd

df_sv40 = pd.read_csv(DATA_DIR / "expected" / "blast_sv40_vs_bkv.tsv", sep="\\t")
max_idx = df_sv40["identity"].idxmax()
top_conserved_protein = df_sv40.loc[max_idx, "subject_title"]
top_identity = df_sv40.loc[max_idx, "identity"]
""",
            check_code="""# Check — do not edit
assert "large t antigen" in str(top_conserved_protein).lower()
assert top_identity > 80.0, f"Expected identity > 80%, got {top_identity}%"
print("Ex 11.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.6",
            stars="★★☆",
            title="Compute mean sequence identity across all shared polyomavirus proteins",
            biology="Measuring average proteome divergence between primate polyomaviruses.",
            task="Compute the mean percentage identity across all rows in `df_sv40`. Store in `mean_polyoma_identity` as a float rounded to 2 decimal places.",
            expected="`mean_polyoma_identity` between 70.0% and 80.0%.",
            student_code="""# TODO: replace the ... with your code
mean_polyoma_identity = ...
""",
            solution_code="""mean_polyoma_identity = round(float(df_sv40["identity"].mean()), 2)
""",
            check_code="""# Check — do not edit
assert 70.0 <= mean_polyoma_identity <= 80.0, f"Expected 70-80%, got {mean_polyoma_identity}"
print("Ex 11.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 11.7",
            stars="★★★",
            title="Detect overlapping gene coordinates in SV40",
            biology="Viral genomes compress coding potential through overlapping genes (e.g. VP2 and VP3 sharing reading frames).",
            task="Find all CDS features on the forward strand (`strand == 1`). Check if any pair has overlapping coordinates (`max(start1, start2) < min(end1, end2)`). Store the boolean in `genes_overlap`.",
            expected="`genes_overlap` as boolean True.",
            student_code="""# TODO: replace the ... with your code
fwd_cds = [f for f in sv40_rec.features if f.type == "CDS" and f.location.strand == 1]
genes_overlap = ...
""",
            solution_code="""fwd_cds = [f for f in sv40_rec.features if f.type == "CDS" and f.location.strand == 1]
genes_overlap = False
for i in range(len(fwd_cds)):
    for j in range(i + 1, len(fwd_cds)):
        loc1 = fwd_cds[i].location
        loc2 = fwd_cds[j].location
        if max(loc1.start, loc2.start) < min(loc1.end, loc2.end):
            genes_overlap = True
            break
""",
            check_code="""# Check — do not edit
assert genes_overlap is True, "Expected overlapping forward strand CDS features in SV40"
print("Ex 11.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U11_P",
        title="Comparative Genomics — Exercises",
        unit_num=11,
        unit_title="Comparative Genome Analysis",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L29–L30",
        before_this="U11_C1"
    ))
    nb_student.cells.append(make_setup_cell("U11_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U11_P",
        title="Comparative Genomics — Solutions",
        unit_num=11,
        unit_title="Comparative Genome Analysis",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L29–L30",
        before_this="U11_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U11_P"))
    
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
1. Why do compact viral genomes have coding densities exceeding 80–100%, whereas the human genome has a coding density of less than 2%?
2. What is synteny, and why is the conservation of gene order between two species evidence of common evolutionary descent?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u11_q():
    salt = "U11_Q"
    questions = [
        QuizQuestion("q1", "What does the term 'synteny' describe in comparative genomics?",
                     ["(a) Synonymous mutation rates", "(b) Conservation of gene order and chromosomal organization between genomes", "(c) Simultaneous transcription of two mRNAs", "(d) Synthetic biology constructs"],
                     "b", "U11_C1 §6"),
        QuizQuestion("q2", "Approximately what percentage of the human nuclear genome encodes protein-coding exons?",
                     ["(a) Less than 2%", "(b) 25%", "(c) 50%", "(d) Over 85%"],
                     "a", "U11_C1 §4"),
        QuizQuestion("q3", "How do small viral genomes (such as PhiX174 and SV40) achieve coding densities near or above 100%?",
                     ["(a) By using quadruple-stranded DNA", "(b) Through overlapping reading frames and alternative translation starts", "(c) By eliminating stop codons", "(d) Through circular RNA only"],
                     "b", "U11_C1 §4"),
        QuizQuestion("q4", "What is structural genome annotation?",
                     ["(a) Predicting molecular function and pathways", "(b) Identifying physical genomic landmarks such as genes, exons, introns, and repeats", "(c) Solving 3D structures with X-ray crystallography", "(d) Naming authors of the paper"],
                     "b", "U11_C1 §1"),
        QuizQuestion("q5", "What is functional genome annotation?",
                     ["(a) Assigning biological roles, biochemical activities, and pathways to identified genes", "(b) Measuring GC content alone", "(c) Slicing chromosomes into contigs", "(d) Computing sequence length"],
                     "a", "U11_C1 §1"),
        QuizQuestion("q6", "In microbial comparative genomics, what is the 'core genome'?",
                     ["(a) Genes shared by ALL strains or species in a defined group", "(b) Genes found only in a single strain", "(c) Non-coding centromeric DNA", "(d) Plasmid DNA only"],
                     "a", "U11_C1 §1"),
        QuizQuestion("q7", "What is the 'pan-genome' of a bacterial species?",
                     ["(a) The essential housekeeping genes only", "(b) The complete set of all genes present across all strains of that species", "(c) Ancient viral DNA insertions", "(d) Mitochondrial genes"],
                     "b", "U11_C1 §1"),
        QuizQuestion("q8", "What mechanism transfers genetic material horizontally between unrelated prokaryotic lineages?",
                     ["(a) Meiotic recombination", "(b) Horizontal Gene Transfer (HGT / LGT)", "(c) Mitotic nondisjunction", "(d) Alternative splicing"],
                     "b", "U11_C1 §1"),
        QuizQuestion("q9", "What are Conserved Non-Coding Elements (CNEs)?",
                     ["(a) Introns with random sequence", "(b) Non-protein-coding genomic regions that show extreme evolutionary conservation, often acting as developmental enhancers", "(c) Broken pseudogenes", "(d) Sequencing errors"],
                     "b", "U11_C1 §1"),
        QuizQuestion("q10", "Which tool is commonly used to visualize comparative genome alignments and synteny blocks between bacterial genomes?",
                     ["(a) Mauve / ACT (Artemis Comparison Tool)", "(b) VMD", "(c) ProtParam", "(d) RepeatMasker"],
                     "a", "U11_C1 §6")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U11_Q",
        title="Comparative Genomics — Quiz",
        unit_num=11,
        unit_title="Comparative Genome Analysis",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L29–L30",
        before_this="U11_C1, U11_P"
    ))
    nb_student.cells.append(make_setup_cell("U11_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U11_Q",
        title="Comparative Genomics — Quiz Key",
        unit_num=11,
        unit_title="Comparative Genome Analysis",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L29–L30",
        before_this="U11_C1, U11_P"
    ))
    nb_key.cells.append(make_setup_cell("U11_Q"))
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


def generate_unit11():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 11 notebooks...")
    c1 = build_u11_c1()
    save_notebook(c1, UNIT_DIR / "U11_C1_Comparing_Two_Genomes.ipynb", clear=True)
    
    p_student, p_sol = build_u11_p()
    save_notebook(p_student, UNIT_DIR / "U11_P_Comparative_Genomics.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U11_P_Comparative_Genomics_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u11_q()
    save_notebook(q_student, UNIT_DIR / "U11_Q_Comparative_Genomics.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U11_Q_Comparative_Genomics_Key.ipynb", clear=False)
    
    print("  ✓ Unit 11 files written successfully.")
