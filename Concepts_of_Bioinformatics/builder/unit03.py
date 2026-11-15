"""
unit03.py - Builder for Unit 03: The NCBI Data Model
Notebooks:
- U03_C1_Inside_a_Sequence_Record.ipynb
- U03_P_NCBI_Data_Model.ipynb
- solutions/U03_P_NCBI_Data_Model_Solutions.ipynb
- U03_Q_NCBI_Data_Model.ipynb
- solutions/U03_Q_NCBI_Data_Model_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U03_NCBI_Data_Model"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u03_c1():
    nb = nbf.v4.new_notebook()
    
    # Header
    nb.cells.append(make_header_cell(
        notebook_id="U03_C1",
        title="Inside a Sequence Record — The NCBI Data Model",
        unit_num=3,
        unit_title="The NCBI Data Model",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L5–L6 (NCBI Data Model, ASN.1, Seq-id, Bioseq)",
        before_this="U02_C1"
    ))
    
    # Outcomes
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Map** Biopython's `SeqRecord` attributes to the NCBI Abstract Syntax Notation One (ASN.1) data model components (`Seq-id`, `Bioseq`, `Seq-descr`, `Seq-annot`, `Seq-feat`) [LO1, LO2].
- **Navigate** the `record.annotations` dictionary to extract taxonomic and publication metadata (`Seq-descr`) [LO2].
- **Iterate** over `record.features` to inspect sequence annotations (`Seq-feat`), coordinates, and qualifiers [LO2].
- **Understand** how structured data models allow complex queries and relational database linkages [LO1].
"""))

    # Biological question
    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
A biological sequence without metadata is just a string of letters. In clinical and computational genetics, knowing *what* the sequence is, *where* it came from (organism, chromosome, tissue), *which* parts code for protein, and *who* published the evidence is essential. NCBI designed a formal data specification called the **NCBI Data Model** (implemented in ASN.1 and XML). How does Biopython's `SeqRecord` represent this model, and how do we programmatically navigate its layers on human *HBB*?
"""))

    # Setup
    nb.cells.append(make_setup_cell("U03_C1"))

    # Concept 1
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The NCBI Data Model Architecture
### Theory
To store diverse biological data without format inconsistencies, NCBI developed an object-oriented specification structured into five core concepts:
1. **`Bioseq`**: The fundamental biological sequence unit (a sequence object with length, alphabet, and topology).
2. **`Seq-id`**: The unambiguous identifier of the sequence (e.g. `NM_000518.5`, GI, or accession).
3. **`Seq-descr`** (Descriptors): Metadata applying to the entire sequence (organism, taxonomy, title, references, comments).
4. **`Seq-annot`** & **`Seq-feat`** (Features): Annotations placed at specific sequence intervals (e.g. `gene`, `CDS`, `exon`, `variation`).
5. **`Bioseq-set`**: Collections of related Bioseqs (e.g. mRNA + protein translated pair, or population phylogenetic set).

In Biopython, loading a GenBank record creates a `SeqRecord` that maps directly onto this hierarchy:
- `record.id` $\\leftrightarrow$ `Seq-id`
- `record.seq` $\\leftrightarrow$ `Bioseq` raw sequence
- `record.description` & `record.annotations` $\\leftrightarrow$ `Seq-descr`
- `record.features` $\\leftrightarrow$ `Seq-annot` (list of `SeqFeature` objects)
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Loading HBB and mapping top-level NCBI Data Model elements
from Bio import SeqIO

gb_path = DATA_DIR / "genbank" / "hbb_human.gb"
record = SeqIO.read(gb_path, "genbank")

print("=== NCBI Data Model: Top-level Mapping ===")
print("Seq-id (record.id):         ", record.id)
print("Seq-id (record.name):       ", record.name)
print("Bioseq Length (len):        ", len(record.seq), "bp")
print("Bioseq Alphabet / Molecule: ", record.annotations.get("molecule_type", "mRNA"))
print("Seq-descr (record.description):")
print("  ", record.description)
'''))

    # Concept 2
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Exploring Descriptors (Seq-descr)
### Theory
Descriptors (`Seq-descr`) provide contextual biological provenance. In Biopython, these are stored in `record.annotations` as a Python dictionary. Key descriptors include:
- `taxonomy`: Hierarchical lineage list (e.g. `['Eukaryota', 'Metazoa', 'Chordata', ...]`)
- `organism`: Scientific species name (e.g. `'Homo sapiens'`)
- `references`: List of literature citations (`Reference` objects with authors, title, journal, pubmed_id)
- `comment`: Curatorial comments from NCBI staff
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Extracting Seq-descr elements from record.annotations
annotations = record.annotations

print("Organism:", annotations.get("organism"))
print("Taxonomic Lineage:")
lineage = annotations.get("taxonomy", [])
print(" -> ".join(lineage[:5]) + " -> ... -> " + lineage[-1])

print(f"Number of literature citations (Seq-descr References): {len(annotations.get('references', []))}")
first_ref = annotations["references"][0]
print("Primary Reference:")
print("  Title:  ", first_ref.title)
print("  Authors:", first_ref.authors)
print("  Journal:", first_ref.journal)
print("  PubMed: ", first_ref.pubmed_id)
'''))

    # Concept 3
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Features and Annotations (Seq-annot & Seq-feat)
### Theory
A `Seq-feat` (Sequence Feature) attaches biological meaning to a specific sequence interval. In Biopython, `record.features` is a list of `SeqFeature` objects. Each feature has:
- `.type`: The biological classification (e.g. `'source'`, `'gene'`, `'CDS'`, `'exon'`, `'misc_feature'`)
- `.location`: Sequence coordinates specifying `start`, `end`, and `strand`
- `.qualifiers`: A dictionary of key-value pairs (e.g. `{'gene': ['HBB']}`, `{'protein_id': ['NP_000509.1']}`)
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Inspecting Seq-feat items on HBB
print(f"Total Seq-feat annotations: {len(record.features)}")

# Tabulate feature types present
feature_types = {}
for feat in record.features:
    feature_types[feat.type] = feature_types.get(feat.type, 0) + 1

print("\\nFeature types breakdown:")
for ftype, count in feature_types.items():
    print(f"  {ftype:15} : {count}")

# Inspect the CDS (Coding Sequence) feature
cds_feat = next(f for f in record.features if f.type == "CDS")
print("\\n=== CDS Seq-feat Details ===")
print("Location:   ", cds_feat.location)
print("Coordinates:", f"start={cds_feat.location.start}, end={cds_feat.location.end}, strand={cds_feat.location.strand}")
print("Gene symbol:", cds_feat.qualifiers.get("gene", ["None"])[0])
print("Protein ID: ", cds_feat.qualifiers.get("protein_id", ["None"])[0])
print("Translation (first 30 aa):", cds_feat.qualifiers.get("translation", [""])[0][:30])
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Locate the 'exon' features and print their coordinates
exons = [f for f in record.features if f.type == "exon"]
print(f"HBB mRNA contains {len(exons)} exon annotations:")
for i, ex in enumerate(exons, 1):
    print(f"  Exon {i}: {ex.location}")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Compare with NCBI Web Interface
When viewing `NM_000518.5` on the NCBI website:
- At the top right, clicking **Display Settings** allows toggling between **GenBank** flat file and **ASN.1 (text)**.
- In the ASN.1 view, you can see the literal `Bioseq ::= { id { other { accession "NM_000518" , version 5 } } ... }` syntax!
Biopython parses this exact underlying object graph into `record.id`, `record.annotations`, and `record.features`.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Summary
- The NCBI Data Model formalizes sequence records into objects rather than raw text flat files.
- `Seq-id` identifies the molecule; `Bioseq` holds sequence data; `Seq-descr` provides contextual metadata; `Seq-feat` annotates specific sequence intervals.
- In Biopython:
  - `record.id` = `Seq-id`
  - `record.annotations` = `Seq-descr`
  - `record.features` = `Seq-feat`

| NCBI Model Concept | Biopython Attribute | Description |
|---|---|---|
| `Seq-id` | `record.id` | Accession and version |
| `Bioseq` | `record.seq`, `len(record)` | Molecule data, length, sequence |
| `Seq-descr` | `record.description`, `record.annotations` | Organism, lineage, citations, comments |
| `Seq-feat` | `record.features` | Genes, CDS, exons, variations with locations |
| `Qualifiers` | `feature.qualifiers` | Dictionary of feature tags (`gene`, `product`, `protein_id`) |
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Next Steps
- Apply your understanding in `U03_P_NCBI_Data_Model.ipynb`.
- Self-test data model vocabulary in `U03_Q_NCBI_Data_Model.ipynb`.
"""))

    return nb


def build_u03_p():
    """Build U03_P practice notebook."""
    exercises = [
        PracticeExercise(
            ex_id="Ex 3.1",
            stars="★☆☆",
            title="Extract Seq-id and Molecule Type from HBB",
            biology="Identifying the record accession and molecule type confirms whether data represents genomic DNA, mRNA, or peptide.",
            task="Load `hbb_human.gb` using `SeqIO.read`. Store its `id` in `hbb_id` and the `molecule_type` from `annotations` in `hbb_mol`.",
            expected="`hbb_id` as string 'NM_000518.5', `hbb_mol` as string 'DNA' or 'mRNA'.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

gb_path = DATA_DIR / "genbank" / "hbb_human.gb"
record = SeqIO.read(gb_path, "genbank")

hbb_id = ...
hbb_mol = ...
""",
            solution_code="""from Bio import SeqIO

gb_path = DATA_DIR / "genbank" / "hbb_human.gb"
record = SeqIO.read(gb_path, "genbank")

hbb_id = record.id
hbb_mol = record.annotations.get("molecule_type", "DNA")
""",
            check_code="""# Check — do not edit
assert hbb_id == "NM_000518.5", f"Expected NM_000518.5, got {hbb_id}"
assert hbb_mol in ["DNA", "mRNA"], f"Expected DNA or mRNA, got {hbb_mol}"
print("Ex 3.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.2",
            stars="★☆☆",
            title="Inspect taxonomic lineage (Seq-descr)",
            biology="Taxonomy in NCBI specifies the evolutionary tree position of the source organism.",
            task="Extract the taxonomic lineage list from `record.annotations['taxonomy']` into variable `lineage`. Store the taxonomic domain (the first element in the list) in `domain`.",
            expected="`lineage` as list of strings, `domain` as string 'Eukaryota'.",
            student_code="""# TODO: replace the ... with your code
lineage = ...
domain = ...
""",
            solution_code="""lineage = record.annotations["taxonomy"]
domain = lineage[0]
""",
            check_code="""# Check — do not edit
assert isinstance(lineage, list) and len(lineage) > 5, "Lineage should be a list of taxa"
assert domain == "Eukaryota", f"Expected Eukaryota, got {domain}"
print("Ex 3.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.3",
            stars="★☆☆",
            title="Count total Seq-feat annotations",
            biology="GenBank records contain annotations for source, gene, CDS, exon, and variation features.",
            task="Count the total number of features in `record.features` and assign to integer variable `num_features`.",
            expected="`num_features` as an integer greater than 3.",
            student_code="""# TODO: replace the ... with your code
num_features = ...
""",
            solution_code="""num_features = len(record.features)
""",
            check_code="""# Check — do not edit
assert isinstance(num_features, int) and num_features >= 3, f"Expected >= 3 features, got {num_features}"
print("Ex 3.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.4",
            stars="★★☆",
            title="Filter features for gene symbol qualifier",
            biology="Gene features annotate the transcriptional unit and cross-reference GeneID and HGNC.",
            task="Iterate over `record.features`. Find the feature where `feat.type == 'gene'`, and extract the first gene symbol from `feat.qualifiers['gene']` into variable `gene_name`.",
            expected="`gene_name` as string 'HBB'.",
            student_code="""# TODO: replace the ... with your code
gene_name = ""
for feat in record.features:
    if feat.type == "gene":
        ...
""",
            solution_code="""gene_name = ""
for feat in record.features:
    if feat.type == "gene":
        gene_name = feat.qualifiers["gene"][0]
        break
""",
            check_code="""# Check — do not edit
assert gene_name == "HBB", f"Expected HBB, got {gene_name}"
print("Ex 3.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.5",
            stars="★★☆",
            title="Extract metadata from two distinct GenBank records (HBB and INS)",
            biology="Different genes share the same standardized NCBI data model representation.",
            task="Load `data/genbank/ins_human.gb`. Create a dictionary `records_meta` with keys `'HBB'` and `'INS'`, where each value is a dict containing `'organism'` and `'length'`.",
            expected="`records_meta` containing metadata for both genes.",
            student_code="""# TODO: replace the ... with your code
ins_record = SeqIO.read(DATA_DIR / "genbank" / "ins_human.gb", "genbank")

records_meta = {
    "HBB": {
        "organism": ...,
        "length": ...
    },
    "INS": {
        "organism": ...,
        "length": ...
    }
}
""",
            solution_code="""ins_record = SeqIO.read(DATA_DIR / "genbank" / "ins_human.gb", "genbank")

records_meta = {
    "HBB": {
        "organism": record.annotations.get("organism", ""),
        "length": len(record.seq)
    },
    "INS": {
        "organism": ins_record.annotations.get("organism", ""),
        "length": len(ins_record.seq)
    }
}
""",
            check_code="""# Check — do not edit
assert records_meta["HBB"]["organism"] == "Homo sapiens"
assert records_meta["INS"]["organism"] == "Homo sapiens"
assert records_meta["HBB"]["length"] == 626
assert 400 < records_meta["INS"]["length"] < 500
print("Ex 3.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.6",
            stars="★★☆",
            title="Extract protein translation and protein ID from the CDS feature",
            biology="The CDS feature provides the conceptual translation from mRNA to protein.",
            task="Find the CDS feature in `ins_record.features`. Extract the `protein_id` into `ins_protein_id` and the length of the amino acid `translation` into `ins_protein_len`.",
            expected="`ins_protein_id` starts with 'NP_', `ins_protein_len` equals 110.",
            student_code="""# TODO: replace the ... with your code
ins_cds = next(f for f in ins_record.features if f.type == "CDS")
ins_protein_id = ...
ins_protein_len = ...
""",
            solution_code="""ins_cds = next(f for f in ins_record.features if f.type == "CDS")
ins_protein_id = ins_cds.qualifiers["protein_id"][0]
ins_protein_len = len(ins_cds.qualifiers["translation"][0])
""",
            check_code="""# Check — do not edit
assert ins_protein_id.startswith("NP_"), f"Expected RefSeq protein ID starting with NP_, got {ins_protein_id}"
assert ins_protein_len == 110, f"Expected 110 amino acids for preproinsulin, got {ins_protein_len}"
print("Ex 3.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 3.7",
            stars="★★★",
            title="Convert a SeqRecord into a simplified NCBI Data Model summary",
            biology="Programmatic pipelines transform complex nested sequence records into concise structured summaries for downstream analysis.",
            task="Write a function `summarize_ncbi_model(rec)` that returns a dictionary with keys: `'seq_id'`, `'organism'`, `'length'`, and `'num_cds'`. Compute this summary for `ins_record` and store in `ins_summary`.",
            expected="`ins_summary` dict with 4 keys and correct values.",
            student_code="""# TODO: replace the ... with your code
def summarize_ncbi_model(rec):
    ...

ins_summary = summarize_ncbi_model(ins_record)
""",
            solution_code="""def summarize_ncbi_model(rec):
    cds_count = sum(1 for f in rec.features if f.type == "CDS")
    return {
        "seq_id": rec.id,
        "organism": rec.annotations.get("organism", ""),
        "length": len(rec.seq),
        "num_cds": cds_count
    }

ins_summary = summarize_ncbi_model(ins_record)
""",
            check_code="""# Check — do not edit
assert ins_summary["seq_id"] == "NM_000207.3"
assert ins_summary["organism"] == "Homo sapiens"
assert ins_summary["num_cds"] == 1
print("Ex 3.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U03_P",
        title="NCBI Data Model — Exercises",
        unit_num=3,
        unit_title="The NCBI Data Model",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L5–L6",
        before_this="U03_C1"
    ))
    nb_student.cells.append(make_setup_cell("U03_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U03_P",
        title="NCBI Data Model — Solutions",
        unit_num=3,
        unit_title="The NCBI Data Model",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L5–L6",
        before_this="U03_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U03_P"))
    
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
1. Why did NCBI design a hierarchical specification (ASN.1 data model) rather than simply storing flat text files?
2. What is the difference between a `Seq-descr` (descriptor) and a `Seq-feat` (feature) in terms of the scope of sequence they describe?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u03_q():
    """Build U03_Q quiz notebook."""
    salt = "U03_Q"
    questions = [
        QuizQuestion("q1", "In the NCBI data model, what is the fundamental object representing an individual biological sequence?",
                     ["(a) Bioseq-set", "(b) Bioseq", "(c) Seq-annot", "(d) Seq-descr"],
                     "b", "U03_C1 §3"),
        QuizQuestion("q2", "Which NCBI data model element represents metadata that applies to the entire sequence (e.g. organism, citations)?",
                     ["(a) Seq-feat", "(b) Seq-id", "(c) Seq-descr", "(d) Seq-align"],
                     "c", "U03_C1 §3"),
        QuizQuestion("q3", "Which data structure in Biopython's `SeqRecord` corresponds directly to `Seq-feat` annotations?",
                     ["(a) record.description", "(b) record.annotations", "(c) record.features", "(d) record.id"],
                     "c", "U03_C1 §5"),
        QuizQuestion("q4", "What formal syntax standard did NCBI adopt for its underlying data model specification and exchange format?",
                     ["(a) YAML", "(b) JSON-LD", "(c) ASN.1 (Abstract Syntax Notation One)", "(d) Markdown"],
                     "c", "U03_C1 §3"),
        QuizQuestion("q5", "What concept represents a collection of related sequences, such as a genomic mRNA and its translated protein?",
                     ["(a) Bioseq-set", "(b) Multi-FASTA", "(c) Seq-graph", "(d) Seq-loc"],
                     "a", "U03_C1 §3"),
        QuizQuestion("q6", "Where in a Biopython `SeqRecord` are taxonomic lineage and publication references stored?",
                     ["(a) record.features", "(b) record.annotations", "(c) record.seq", "(d) record.letter_annotations"],
                     "b", "U03_C1 §4"),
        QuizQuestion("q7", "Which feature type (`feat.type`) in a GenBank record specifies the exact protein-coding coordinates and translation?",
                     ["(a) gene", "(b) exon", "(c) CDS", "(d) source"],
                     "c", "U03_C1 §5"),
        QuizQuestion("q8", "In a `SeqFeature` object, where are key-value tags such as `/gene=\"HBB\"` or `/protein_id=\"NP_000509.1\"` stored?",
                     ["(a) feat.location", "(b) feat.qualifiers", "(c) feat.type", "(d) feat.id"],
                     "b", "U03_C1 §5"),
        QuizQuestion("q9", "How does a `Seq-feat` define which region of a sequence it annotates?",
                     ["(a) Through a Seq-loc (Sequence Location)", "(b) Through a Seq-id only", "(c) Through a descriptor comment", "(d) It always covers the whole sequence"],
                     "a", "U03_C1 §5"),
        QuizQuestion("q10", "What is the primary identifier of a sequence in the NCBI model called?",
                     ["(a) Seq-annot", "(b) Seq-descr", "(c) Seq-id", "(d) Bioseq-code"],
                     "c", "U03_C1 §3")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U03_Q",
        title="NCBI Data Model — Quiz",
        unit_num=3,
        unit_title="The NCBI Data Model",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L5–L6",
        before_this="U03_C1, U03_P"
    ))
    nb_student.cells.append(make_setup_cell("U03_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U03_Q",
        title="NCBI Data Model — Quiz Key",
        unit_num=3,
        unit_title="The NCBI Data Model",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L5–L6",
        before_this="U03_C1, U03_P"
    ))
    nb_key.cells.append(make_setup_cell("U03_Q"))
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


def generate_unit03():
    """Generate all notebooks for Unit 3."""
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 03 notebooks...")
    c1 = build_u03_c1()
    save_notebook(c1, UNIT_DIR / "U03_C1_Inside_a_Sequence_Record.ipynb", clear=True)
    
    p_student, p_sol = build_u03_p()
    save_notebook(p_student, UNIT_DIR / "U03_P_NCBI_Data_Model.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U03_P_NCBI_Data_Model_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u03_q()
    save_notebook(q_student, UNIT_DIR / "U03_Q_NCBI_Data_Model.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U03_Q_NCBI_Data_Model_Key.ipynb", clear=False)
    
    print("  ✓ Unit 03 files written successfully.")
