"""
unit04.py - Builder for Unit 04: GenBank Sequence Database
Notebooks:
- U04_C1_GenBank_Flat_File.ipynb
- U04_C2_Formats_and_Conversion.ipynb
- U04_P_GenBank_and_Formats.ipynb
- solutions/U04_P_GenBank_and_Formats_Solutions.ipynb
- U04_Q_GenBank_Database.ipynb
- solutions/U04_Q_GenBank_Database_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U04_GenBank_Database"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u04_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U04_C1",
        title="The GenBank Flat File",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L7–L8, Practicals S4–S5 (GenBank & GenPept)",
        before_this="U03_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Dissect** each mandatory section of a GenBank flat file (LOCUS, DEFINITION, ACCESSION, VERSION, SOURCE, REFERENCE, FEATURES, ORIGIN) [LO2].
- **Interpret** GenBank location syntax including intervals, `join()`, and `complement()` [LO2].
- **Walk** the feature table to extract CDS coordinates and translate coding regions with Biopython [LO2].
- **Calculate** exact translated protein lengths directly from genomic and mRNA coordinates [LO2].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
When looking at the human beta-globin flat file (`NM_000518.5`), the mRNA is 626 bp long, but the mature beta-globin chain is only 146 or 147 amino acids. How does a bioinformatician read the flat file to locate the exact codon boundaries of the protein, understand where the untranslated regions end, and extract the translated peptide?
"""))

    nb.cells.append(make_setup_cell("U04_C1"))

    # Concept 1: Flat file anatomy
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Anatomy of a GenBank Flat File
### Theory
The GenBank flat file is structured into three main blocks:
1. **Header**:
   - `LOCUS`: Locus name, sequence length, molecule type (`mRNA`, `DNA`), topology (`linear`, `circular`), GenBank division (`PRI` = Primate, `ROD` = Rodent, `BCT` = Bacteria, `VRL` = Viral), and modification date.
   - `DEFINITION`: Free-text summary of organism, gene, and function.
   - `ACCESSION` & `VERSION`: Stable identifier and versioned accession (`NM_000518.5`).
   - `SOURCE` & `ORGANISM`: Formal taxonomic classification.
   - `REFERENCE`: Citations of primary literature supporting the sequence.
2. **Feature Table (`FEATURES`)**: Key-value annotations describing biological intervals.
3. **Sequence (`ORIGIN`)**: The raw sequence displayed in blocks of 10 nucleotides with 1-based line position numbers.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Inspecting Header metadata of HBB
from Bio import SeqIO

gb_path = DATA_DIR / "genbank" / "hbb_human.gb"
record = SeqIO.read(gb_path, "genbank")

print("LOCUS Name:    ", record.name)
print("Sequence Length:", len(record.seq), "bp")
print("Division:      ", record.annotations.get("data_file_division", "PRI"))
print("Topology:      ", record.annotations.get("topology", "linear"))
print("Accession:     ", record.id)
print("Definition:    ", record.description)
'''))

    # Concept 2: Location syntax and CDS walking
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Location Syntax and the Features Table
### Theory
In the `FEATURES` block:
- Standard interval: `51..494` (nucleotides 51 through 494 inclusive, 1-based)
- Spliced exons: `join(51..142, 273..494)` indicates exons spliced together in mRNA
- Opposite strand: `complement(51..494)` indicates coding on the reverse strand
- Fuzzy boundaries: `<1..500` indicates incomplete 5' end; `100..>600` indicates incomplete 3' end

In Biopython, coordinates are automatically converted into 0-based half-open Python slices (`[start:end]`).
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Walking the features table and isolating the CDS
cds_features = [f for f in record.features if f.type == "CDS"]
assert len(cds_features) == 1, "Expected single CDS in HBB mRNA"
cds_feat = cds_features[0]

print("CDS Location string in GenBank: 51..494 (1-based)")
print(f"Biopython 0-based slice:        {cds_feat.location.start}:{cds_feat.location.end}")
print(f"CDS nucleotide length:          {cds_feat.location.end - cds_feat.location.start} bp")

# Expected protein length: (CDS length - 3 stop nucleotides) / 3
cds_nt_len = cds_feat.location.end - cds_feat.location.start
expected_aa_len = (cds_nt_len - 3) // 3
print(f"Calculated protein length:      {expected_aa_len} amino acids")
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Extract and translate the CDS sequence using Biopython
cds_seq = cds_feat.extract(record.seq)
translated = cds_seq.translate(to_stop=True)

print("CDS start codon:", cds_seq[:3])
print("CDS stop codon: ", cds_seq[-3:])
print("Translated protein length:", len(translated), "aa")
print("Official /translation in flat file:", cds_feat.qualifiers["translation"][0])
print("Matches official annotation?", str(translated) == cds_feat.qualifiers["translation"][0])
'''))

    nb.cells.append(nbf.v4.new_markdown_cell("""**Common mistakes:**
- Forgetting that CDS end coordinates include the 3-nucleotide stop codon (TAA, TAG, TGA).
- Confusing 1-based GenBank coordinates (`51..494` -> length = $494 - 51 + 1 = 444$) with Python 0-based slices (`[50:494]` -> length = $494 - 50 = 444$).
"""))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Compare with the Web Tool
In Practical S4, we scrolled down the flat file on NCBI Nucleotide:
- CDS: `51..494`
- `/gene="HBB"`
- `/codon_start=1`
- `/protein_id="NP_000509.1"`
- `/translation="MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPK..."`
Our programmatic extraction produces the identical 147 amino acid sequence and verified coordinate calculation.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- The GenBank flat file contains LOCUS, DEFINITION, ACCESSION, FEATURES, and ORIGIN blocks.
- Location syntax indicates coordinates (`51..494`), spliced joints (`join()`), and opposite strand (`complement()`).
- `feature.extract(record.seq)` splices exons and extracts the exact sub-sequence.
- Coding sequence length in nucleotides (including stop codon) divided by 3 gives $(N_{\\text{aa}} + 1)$.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Learn about format conversions in `U04_C2_Formats_and_Conversion.ipynb`.
- Solve feature extraction exercises in `U04_P_GenBank_and_Formats.ipynb`.
"""))

    return nb


def build_u04_c2():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U04_C2",
        title="Formats and Conversion",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Course",
        time_min=35,
        difficulty="★★☆",
        goes_with="Lectures L7–L9, Practical S4 (EMBOSS seqret & Format Conversion)",
        before_this="U04_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Differentiate** format (syntax) from biological content (semantics) [LO2].
- **Convert** sequence records between GenBank, FASTA, and EMBL formats using `Bio.SeqIO` [LO2].
- **Recognize** information loss when converting richly annotated records into simple formats [LO2].
- **Distinguish** primary sequence archives (GenBank/ENA/DDBJ) from curated secondary databases (RefSeq, UniProt) [LO1, LO2].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Bioinformaticians constantly shuttle sequences between different tools. BLAST requires FASTA format; phylogenetic software often requires Clustal or PHYLIP; genome browsers consume GFF3 or GenBank. If you convert a GenBank record into FASTA to run BLAST, what metadata did you discard? Can you recover the lost information by converting it back?
"""))

    nb.cells.append(make_setup_cell("U04_C2"))

    # Concept 1: Format vs Content
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Format vs. Content
### Theory
Biological sequences can be serialized into many distinct syntax formats:
- **FASTA**: Minimalist format. Header line (`>id description`) followed by raw sequence. Stores *no* annotations, no features, and no coordinates.
- **GenBank**: NCBI flat file. Stores full provenance, taxonomy, citations, and coordinate-mapped feature tables.
- **EMBL**: European Molecular Biology Laboratory flat file. Uses two-letter line codes (`ID`, `AC`, `DE`, `KW`, `OS`, `FT`, `SQ`).
- **GFF3 / GTF**: Tabular format specialized for genome annotations.

Converting from a rich format (GenBank) to a simple format (FASTA) is a **lossy conversion**.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Converting GenBank to FASTA and EMBL
import io
from Bio import SeqIO

gb_path = DATA_DIR / "genbank" / "hbb_human.gb"
record = SeqIO.read(gb_path, "genbank")

# Write to in-memory text buffers to inspect formatting
fasta_buffer = io.StringIO()
SeqIO.write(record, fasta_buffer, "fasta")
fasta_text = fasta_buffer.getvalue()

print("=== Converted FASTA Format (First 4 lines) ===")
print("\\n".join(fasta_text.splitlines()[:4]))
print("...")

embl_buffer = io.StringIO()
SeqIO.write(record, embl_buffer, "embl")
embl_text = embl_buffer.getvalue()

print("\\n=== Converted EMBL Format (First 6 lines) ===")
print("\\n".join(embl_text.splitlines()[:6]))
'''))

    # Concept 2: Information loss
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Demonstrating Information Loss
### Theory
When we write a `SeqRecord` loaded from GenBank to a FASTA file and re-read it:
- The sequence and ID are preserved.
- All entries in `record.features` (genes, exons, CDS, variations) are **discarded**.
- All entries in `record.annotations` (organism, taxonomy, citations) are **discarded**.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Quantifying lost information
# Save to outputs directory
out_fasta = OUT_DIR / "hbb_converted.fasta"
SeqIO.write(record, out_fasta, "fasta")

reloaded_fasta = SeqIO.read(out_fasta, "fasta")

print("Original GenBank Record:")
print("  Features count:   ", len(record.features))
print("  Annotations count:", len(record.annotations))

print("\\nReloaded FASTA Record:")
print("  Features count:   ", len(reloaded_fasta.features))
print("  Annotations count:", len(reloaded_fasta.annotations))
'''))

    # Concept 3: Primary vs Secondary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Primary vs. Secondary Databases
### Theory
- **Primary Databases (Archives)**: GenBank, ENA, DDBJ. Direct user submissions. Redundant; authors retain ownership; errors are not edited by database staff.
- **Secondary Databases (Curated)**: RefSeq, UniProtKB/Swiss-Prot. Curated by expert biocurators. Non-redundant; explicit reference standards.
- Human *HBB* primary submissions include `V00497.1` (cloned in 1978 by Lawn et al.). Its secondary RefSeq standard is `NM_000518.5`.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Checking primary source in RefSeq record
comment = record.annotations.get("comment", "")
print("RefSeq provenance comment:")
print(" ", comment[:150], "...")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Compare with EMBOSS seqret
In Practical S4, we ran `seqret -sequence hbb_human.gb -outseq hbb.fasta` from the command line.
Biopython's `SeqIO.write(record, handle, "fasta")` performs the exact same operation programmatically.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Summary
- `Bio.SeqIO.write(records, file_handle, format)` exports sequence records to standard biological formats.
- Converting GenBank to FASTA strips annotations and features irreversibly.
- Primary databases store original submitted historical data; secondary databases curate standardized benchmarks.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Next Steps
- Complete practice exercises on INS and TP53 in `U04_P_GenBank_and_Formats.ipynb`.
- Take the Unit 4 quiz in `U04_Q_GenBank_Database.ipynb`.
"""))

    return nb


def build_u04_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 4.1",
            stars="★☆☆",
            title="Extract CDS coordinates for human insulin",
            biology="Human preproinsulin (INS) is encoded by NM_000207.3.",
            task="Load `data/genbank/ins_human.gb`. Find the CDS feature and store its 1-based start coordinate in `ins_cds_start` and 1-based end coordinate in `ins_cds_end`.",
            expected="`ins_cds_start` = 60, `ins_cds_end` = 392.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

ins_gb = DATA_DIR / "genbank" / "ins_human.gb"
ins_rec = SeqIO.read(ins_gb, "genbank")

ins_cds = next(f for f in ins_rec.features if f.type == "CDS")
# Remember: Biopython location.start is 0-based; 1-based start is start + 1
ins_cds_start = ...
ins_cds_end = ...
""",
            solution_code="""from Bio import SeqIO

ins_gb = DATA_DIR / "genbank" / "ins_human.gb"
ins_rec = SeqIO.read(ins_gb, "genbank")

ins_cds = next(f for f in ins_rec.features if f.type == "CDS")
ins_cds_start = int(ins_cds.location.start) + 1
ins_cds_end = int(ins_cds.location.end)
""",
            check_code="""# Check — do not edit
assert ins_cds_start == 60, f"Expected 60, got {ins_cds_start}"
assert ins_cds_end == 392, f"Expected 392, got {ins_cds_end}"
print("Ex 4.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.2",
            stars="★☆☆",
            title="Compute protein length from nucleotide coordinates",
            biology="The mature protein length in amino acids equals $(N_{\\text{nt}} - 3) / 3$.",
            task="Using `ins_cds_start` and `ins_cds_end`, calculate the length of the coding nucleotide sequence `nt_len` and the resulting protein length `aa_len`.",
            expected="`nt_len` = 333, `aa_len` = 110.",
            student_code="""# TODO: replace the ... with your code
nt_len = ...
aa_len = ...
""",
            solution_code="""nt_len = ins_cds_end - ins_cds_start + 1
aa_len = (nt_len - 3) // 3
""",
            check_code="""# Check — do not edit
assert nt_len == 333, f"Expected 333 nt, got {nt_len}"
assert aa_len == 110, f"Expected 110 aa, got {aa_len}"
print("Ex 4.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.3",
            stars="★☆☆",
            title="Extract protein length for TP53 tumor suppressor",
            biology="Tumor protein p53 (TP53) regulates the cell cycle and genomic stability.",
            task="Load `data/genbank/tp53_human.gb`. Find the CDS feature and calculate its translated protein length in `tp53_aa_len`.",
            expected="`tp53_aa_len` = 393.",
            student_code="""# TODO: replace the ... with your code
tp53_gb = DATA_DIR / "genbank" / "tp53_human.gb"
tp53_rec = SeqIO.read(tp53_gb, "genbank")

tp53_cds = next(f for f in tp53_rec.features if f.type == "CDS")
tp53_aa_len = ...
""",
            solution_code="""tp53_gb = DATA_DIR / "genbank" / "tp53_human.gb"
tp53_rec = SeqIO.read(tp53_gb, "genbank")

tp53_cds = next(f for f in tp53_rec.features if f.type == "CDS")
tp53_aa_len = len(tp53_cds.qualifiers["translation"][0])
""",
            check_code="""# Check — do not edit
assert tp53_aa_len == 393, f"Expected 393 aa for TP53, got {tp53_aa_len}"
print("Ex 4.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.4",
            stars="★★☆",
            title="Translate CDS and confirm identity with official GenBank translation",
            biology="Translating extracted coding nucleotides must exactly reproduce the curated protein annotation.",
            task="Extract the CDS nucleotide sequence of INS with `ins_cds.extract(ins_rec.seq)` into `ins_cds_dna`. Translate it with `to_stop=True` into `ins_trans`. Compare with `ins_cds.qualifiers['translation'][0]`.",
            expected="`is_identical` as boolean True.",
            student_code="""# TODO: replace the ... with your code
ins_cds_dna = ...
ins_trans = ...
is_identical = ...
""",
            solution_code="""ins_cds_dna = ins_cds.extract(ins_rec.seq)
ins_trans = str(ins_cds_dna.translate(to_stop=True))
is_identical = (ins_trans == ins_cds.qualifiers["translation"][0])
""",
            check_code="""# Check — do not edit
assert is_identical is True, "Calculated translation does not match GenBank translation"
print("Ex 4.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.5",
            stars="★★☆",
            title="Convert INS GenBank file to FASTA and verify file contents",
            biology="Converting records to FASTA facilitates similarity searching with BLAST.",
            task="Write `ins_rec` to `OUT_DIR / 'ins_converted.fasta'` in `'fasta'` format using `SeqIO.write`. Read it back and store sequence length in `fasta_len`.",
            expected="`fasta_len` equals length of `ins_rec.seq`.",
            student_code="""# TODO: replace the ... with your code
out_fasta_path = OUT_DIR / "ins_converted.fasta"
...
reloaded = SeqIO.read(out_fasta_path, "fasta")
fasta_len = len(reloaded.seq)
""",
            solution_code="""out_fasta_path = OUT_DIR / "ins_converted.fasta"
SeqIO.write(ins_rec, out_fasta_path, "fasta")
reloaded = SeqIO.read(out_fasta_path, "fasta")
fasta_len = len(reloaded.seq)
""",
            check_code="""# Check — do not edit
assert fasta_len == len(ins_rec.seq), f"Expected {len(ins_rec.seq)}, got {fasta_len}"
print("Ex 4.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.6",
            stars="★★☆",
            title="Check feature stripping during FASTA conversion",
            biology="FASTA format does not support feature tables.",
            task="Store the number of features in `ins_rec` in `orig_feat_count`, and the number of features in `reloaded` in `fasta_feat_count`.",
            expected="`orig_feat_count` > 1, `fasta_feat_count` == 0.",
            student_code="""# TODO: replace the ... with your code
orig_feat_count = ...
fasta_feat_count = ...
""",
            solution_code="""orig_feat_count = len(ins_rec.features)
fasta_feat_count = len(reloaded.features)
""",
            check_code="""# Check — do not edit
assert orig_feat_count > 1, "Original record should have features"
assert fasta_feat_count == 0, "FASTA record cannot contain features"
print("Ex 4.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 4.7",
            stars="★★★",
            title="Inspect EMBL format two-letter line codes",
            biology="EMBL/ENA records use line identifiers such as ID (Identification), AC (Accession), and FT (Feature Table).",
            task="Convert `ins_rec` into EMBL format string using `io.StringIO()`. Count how many lines begin with `'FT   '` and store in `ft_line_count`.",
            expected="`ft_line_count` as integer > 5.",
            student_code="""# TODO: replace the ... with your code
import io

buf = io.StringIO()
...
embl_text = buf.getvalue()
ft_line_count = sum(1 for line in embl_text.splitlines() if line.startswith("FT   "))
""",
            solution_code="""import io

buf = io.StringIO()
SeqIO.write(ins_rec, buf, "embl")
embl_text = buf.getvalue()
ft_line_count = sum(1 for line in embl_text.splitlines() if line.startswith("FT   "))
""",
            check_code="""# Check — do not edit
assert ft_line_count > 5, f"Expected > 5 FT lines, got {ft_line_count}"
print("Ex 4.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U04_P",
        title="GenBank and Formats — Exercises",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L7–L9, Practicals S4–S5",
        before_this="U04_C1, U04_C2"
    ))
    nb_student.cells.append(make_setup_cell("U04_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U04_P",
        title="GenBank and Formats — Solutions",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L7–L9, Practicals S4–S5",
        before_this="U04_C1, U04_C2"
    ))
    nb_sol.cells.append(make_setup_cell("U04_P"))
    
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
1. Why does converting a GenBank flat file to FASTA discard biological feature locations, and why is this conversion non-reversible?
2. What are the key governance differences between primary database submissions (GenBank/ENA/DDBJ) and secondary databases (RefSeq)?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u04_q():
    salt = "U04_Q"
    questions = [
        QuizQuestion("q1", "In a GenBank flat file, which line specifies the molecule length, type, division, and modification date?",
                     ["(a) DEFINITION", "(b) ACCESSION", "(c) LOCUS", "(d) ORIGIN"],
                     "c", "U04_C1 §3"),
        QuizQuestion("q2", "What does the location descriptor `join(100..250, 400..550)` signify in a eukaryotic genomic record?",
                     ["(a) Two alternative alleles", "(b) Spliced exons forming a single mature transcript", "(c) Overlapping genes", "(d) Repetitive sequence"],
                     "b", "U04_C1 §4"),
        QuizQuestion("q3", "What does the GenBank division abbreviation `PRI` represent?",
                     ["(a) Primary database", "(b) Primate sequences", "(c) Prokaryotic RNA", "(d) Provisional RefSeq"],
                     "b", "U04_C1 §3"),
        QuizQuestion("q4", "If a CDS nucleotide feature spans coordinates `1..303` (inclusive), how many amino acids will the translated protein contain?",
                     ["(a) 100", "(b) 101", "(c) 300", "(d) 303"],
                     "a", "U04_C1 §4"),
        QuizQuestion("q5", "Which format conversion results in permanent loss of feature coordinates and citation metadata?",
                     ["(a) GenBank to EMBL", "(b) GenBank to FASTA", "(c) GenBank to ASN.1", "(d) GenBank to XML"],
                     "b", "U04_C2 §4"),
        QuizQuestion("q6", "What European resource is the INSDC partner to NCBI GenBank?",
                     ["(a) DDBJ", "(b) ENA (European Nucleotide Archive / EMBL)", "(c) Swiss-Prot", "(d) Ensembl"],
                     "b", "U04_C2 §5"),
        QuizQuestion("q7", "Which line code in an EMBL flat file denotes Feature Table annotations?",
                     ["(a) ID", "(b) SQ", "(c) FT", "(d) DE"],
                     "c", "U04_C2 §3"),
        QuizQuestion("q8", "What qualifier under the CDS feature in a GenBank record specifies which reading frame to use for translation?",
                     ["(a) /transl_table", "(b) /codon_start", "(c) /protein_id", "(d) /gene"],
                     "b", "U04_C1 §5"),
        QuizQuestion("q9", "In GenBank location syntax, what does `complement(100..200)` mean?",
                     ["(a) The feature is an antisense RNA", "(b) The feature is encoded on the reverse strand (3' to 5' in reference)", "(c) The sequence is an exact palindrome", "(d) The feature is duplicated"],
                     "b", "U04_C1 §4"),
        QuizQuestion("q10", "What section of a GenBank flat file marks the beginning of the raw nucleotide sequence text?",
                     ["(a) FEATURES", "(b) BASE COUNT", "(c) ORIGIN", "(d) SEQUENCE"],
                     "c", "U04_C1 §3")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U04_Q",
        title="GenBank Sequence Database — Quiz",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L7–L9, Practicals S4–S5",
        before_this="U04_C1, U04_C2, U04_P"
    ))
    nb_student.cells.append(make_setup_cell("U04_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U04_Q",
        title="GenBank Sequence Database — Quiz Key",
        unit_num=4,
        unit_title="GenBank Sequence Database",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L7–L9, Practicals S4–S5",
        before_this="U04_C1, U04_C2, U04_P"
    ))
    nb_key.cells.append(make_setup_cell("U04_Q"))
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


def generate_unit04():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 04 notebooks...")
    c1 = build_u04_c1()
    save_notebook(c1, UNIT_DIR / "U04_C1_GenBank_Flat_File.ipynb", clear=True)
    
    c2 = build_u04_c2()
    save_notebook(c2, UNIT_DIR / "U04_C2_Formats_and_Conversion.ipynb", clear=True)
    
    p_student, p_sol = build_u04_p()
    save_notebook(p_student, UNIT_DIR / "U04_P_GenBank_and_Formats.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U04_P_GenBank_and_Formats_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u04_q()
    save_notebook(q_student, UNIT_DIR / "U04_Q_GenBank_Database.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U04_Q_GenBank_Database_Key.ipynb", clear=False)
    
    print("  ✓ Unit 04 files written successfully.")
