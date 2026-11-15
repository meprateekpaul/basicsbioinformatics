"""
unit02.py - Builder for Unit 02: Information Retrieval from Biological Databases
Notebooks:
- U02_C1_Entrez_Search_from_Python.ipynb
- U02_P_Entrez_Search.ipynb
- solutions/U02_P_Entrez_Search_Solutions.ipynb
- U02_Q_Information_Retrieval.ipynb
- solutions/U02_Q_Information_Retrieval_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U02_Information_Retrieval"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u02_c1():
    nb = nbf.v4.new_notebook()
    
    # Header
    nb.cells.append(make_header_cell(
        notebook_id="U02_C1",
        title="Entrez Search from Python",
        unit_num=2,
        unit_title="Information Retrieval from Biological Databases",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L3–L4, Practicals S2–S3 (NCBI & PubMed Retrieval)",
        before_this="U01_C1"
    ))
    
    # Outcomes
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** the Entrez integrated retrieval system and RefSeq accession prefixes [LO1, LO2].
- **Construct** precise queries using field tags (`[GENE]`, `[ORGN]`, `[FILT]`) and Boolean operators [LO2].
- **Search** and retrieve biological records programmatically with `Bio.Entrez` (`esearch`, `esummary`, `efetch`) [LO2].
- **Implement** an offline-first fallback mechanism for robust classroom execution [LO2].
"""))

    # Biological question
    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
A clinical geneticist identifies a mutation suspected of causing beta-thalassemia. To interpret the mutation, they need the official curated reference transcript for human hemoglobin subunit beta (*HBB*). If you simply type `HBB` into the NCBI search bar, you get over 50,000 nucleotide records! How do we write a search query that returns *only* the official, curated human *HBB* RefSeq mRNA (`NM_000518.5`), and how do we fetch this record directly into Python?
"""))

    # Setup
    nb.cells.append(make_setup_cell("U02_C1"))

    # Concept 1
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The Entrez System and RefSeq Accession Prefixes
### Theory
NCBI **Entrez** is an integrated database cross-referencing system connecting literature (PubMed), genes (Gene), sequences (Nucleotide, Protein), structures (Structure), and taxonomy (Taxonomy).

To distinguish raw submitted data from curated benchmarks, NCBI maintains **RefSeq** (Reference Sequence Database). RefSeq accessions contain an underscore `_` and standard two-letter prefixes:
- `NM_`: Curated mRNA transcript (e.g. `NM_000518` for human *HBB*)
- `NP_`: Curated protein sequence (e.g. `NP_000509` for beta-globin)
- `NR_`: Curated non-coding RNA
- `NC_`: Complete genomic molecule / chromosome (e.g. viral genome or human chromosome)
- `XM_` / `XP_`: Model (computationally predicted) mRNA and protein

Primary GenBank accessions (e.g. `V00497`, `AF123456`) do *not* have underscores.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Distinguishing accession types in Python
accessions = ["NM_000518.5", "NP_000509.1", "NC_001422.1", "V00497.1", "P68871"]

def classify_accession(acc):
    if "_" in acc:
        prefix = acc.split("_")[0]
        mapping = {
            "NM": "RefSeq Curated mRNA",
            "NP": "RefSeq Curated Protein",
            "NC": "RefSeq Complete Chromosome / Genome",
            "XM": "RefSeq Predicted mRNA",
            "XP": "RefSeq Predicted Protein"
        }
        return mapping.get(prefix, f"Other RefSeq ({prefix})")
    elif len(acc) == 6 and acc[0] in "OPQ":
        return "UniProtKB Accession"
    else:
        return "Primary GenBank / INSDC Submission"

for a in accessions:
    print(f"{a:15} -> {classify_accession(a)}")
'''))

    # Concept 2
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Query Syntax with Field Tags
### Theory
Searching without field tags searches all fields (text words, titles, authors, organisms). **Field tags** restrict search terms to specific indexed fields:
- `[GENE]` or `[Gene Name]`: Official gene symbol (e.g., `HBB[GENE]`)
- `[ORGN]` or `[Organism]`: Scientific or common name (e.g., `Homo sapiens[ORGN]`)
- `[PROP]` or `[FILT]`: Property or filter flag (e.g., `biomol_mrna[PROP]`, `RefSeq[FILT]`)
- `[TITL]`: Article or sequence definition title words

Boolean operators must be **UPPERCASE** (`AND`, `OR`, `NOT`).
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Precise Entrez Query String
query_broad = "HBB"
query_precise = "HBB[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]"

print("Broad search query:  ", query_broad)
print("Precise search query:", query_precise)
'''))

    # Concept 3
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Programmatic Search with Bio.Entrez (esearch)
### Theory
Biopython provides the `Bio.Entrez` module to access NCBI E-utilities:
1. `Entrez.email`: Must be set to identify yourself to NCBI (usage policy).
2. `Entrez.esearch(db, term, ...)`: Performs the search and returns XML/JSON listing matching Primary IDs (UIDs or GIs).
3. `Entrez.read(handle)`: Parses NCBI XML responses into native Python dictionaries.

**Offline-First Fallback:** Whenever calling NCBI servers in teaching code, wrap the network call in a `try...except` block so that network interruptions fallback to pre-saved records in `data/expected/`.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Searching Nucleotide via Bio.Entrez with offline fallback
import json
from Bio import Entrez

Entrez.email = "student@example.edu"  # Use your own educational email in practice

query = "HBB[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]"
offline_file = DATA_DIR / "expected" / "entrez_hbb_search.json"

try:
    # Attempt real Entrez search
    handle = Entrez.esearch(db="nucleotide", term=query, retmax=5)
    record = Entrez.read(handle)
    handle.close()
    count = int(record["Count"])
    id_list = record["IdList"]
    print("NCBI ESearch succeeded online!")
except Exception as e:
    # Offline fallback
    print(f"Network call skipped or unavailable ({e}). Loading offline fallback...")
    with open(offline_file) as f:
        data = json.load(f)
    count = int(data["count"])
    id_list = data["idlist"]

print(f"Query: {query}")
print(f"Matching records found: {count}")
print(f"Retrieved primary UIDs: {id_list}")
'''))

    nb.cells.append(nbf.v4.new_code_cell('''# Try it: Change the query term to search for human insulin (INS)
ins_query = "INS[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]"
print("Constructed query:", ins_query)
'''))

    nb.cells.append(nbf.v4.new_markdown_cell("""**Common mistakes:**
- Forgetting `Entrez.email`: NCBI will throttle or temporarily block IP addresses that fail to supply an email header.
- Lowercase boolean operators: `"hbb and human"` treats `and` as a literal word search rather than a boolean operator. Always write `AND`, `OR`, `NOT`.
"""))

    # Concept 4
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Fetching Complete Records with Bio.Entrez (efetch)
### Theory
`Entrez.efetch` downloads complete records in standard file formats:
- `db`: target database (`nucleotide`, `protein`, `pubmed`)
- `id`: accessions or UIDs
- `rettype`: return format (`gb` or `gbwithparts` for GenBank, `fasta` for FASTA, `medline` for PubMed)
- `retmode`: text or xml

The resulting handle can be parsed directly by `Bio.SeqIO.read()`!
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: efetch parsed directly into SeqRecord
from Bio import SeqIO

accession = "NM_000518.5"
local_gb = DATA_DIR / "genbank" / "hbb_human.gb"

try:
    handle = Entrez.efetch(db="nucleotide", id=accession, rettype="gbwithparts", retmode="text")
    seq_rec = SeqIO.read(handle, "genbank")
    handle.close()
    print(f"Retrieved {accession} online via efetch!")
except Exception as e:
    print(f"Using local cached copy ({e})...")
    seq_rec = SeqIO.read(local_gb, "genbank")

print("Record ID:         ", seq_rec.id)
print("Record Description:", seq_rec.description)
print("Molecule Type:     ", seq_rec.annotations.get("molecule_type", "mRNA"))
print("Sequence Length:   ", len(seq_rec.seq), "bp")
'''))

    # Compare with tool
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Compare with the Web Tool
In Practical S2, we ran the same search in the NCBI web search bar:
`HBB[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]`
The web interface returns the official RefSeq record `NM_000518.5` (Homo sapiens hemoglobin subunit beta mRNA, 626 bp). Our Python `Bio.Entrez` script retrieves exactly the same entry and parses its features.
"""))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Summary
- RefSeq accessions contain underscores (`NM_` for mRNA, `NP_` for protein, `NC_` for complete genomes).
- Entrez field tags (`[GENE]`, `[ORGN]`, `[FILT]`) narrow search space from tens of thousands of hits to exact curated records.
- `Bio.Entrez.esearch` searches for IDs; `Bio.Entrez.efetch` downloads complete formatted records.
- Always implement an offline fallback using `try...except` and local files.

| Function | Purpose | Input Arguments | Output |
|---|---|---|---|
| `Entrez.esearch` | Search database | `db`, `term`, `retmax` | XML handle containing `IdList`, `Count` |
| `Entrez.esummary` | Document summary | `db`, `id` | XML handle containing title, date, length |
| `Entrez.efetch` | Download records | `db`, `id`, `rettype`, `retmode` | Text/XML handle parsed by `SeqIO` |
| `Entrez.read` | Parse NCBI XML | handle | Python dict / list |
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 9. Next Steps
- Practice building queries and handling responses in `U02_P_Entrez_Search.ipynb`.
- Test your query logic and RefSeq prefix knowledge in `U02_Q_Information_Retrieval.ipynb`.
"""))

    return nb


def build_u02_p():
    """Build U02_P practice notebook."""
    exercises = [
        PracticeExercise(
            ex_id="Ex 2.1",
            stars="★☆☆",
            title="Classify biological database accession numbers",
            biology="Different accession formats indicate whether a sequence is raw submitted GenBank, curated RefSeq, or Swiss-Prot protein.",
            task="Given a list of accessions `test_accs`, classify each as `'RefSeq'` if it contains an underscore `'_'`, otherwise `'GenBank/UniProt'`. Store the result as a dictionary mapping accession to category in `classification_dict`.",
            expected="`classification_dict` mapping str -> str with 4 entries.",
            student_code="""# TODO: replace the ... with your code
test_accs = ["NM_000518.5", "V00497.1", "NP_000509.1", "P68871"]
classification_dict = {}

for acc in test_accs:
    ...
""",
            solution_code="""test_accs = ["NM_000518.5", "V00497.1", "NP_000509.1", "P68871"]
classification_dict = {}

for acc in test_accs:
    classification_dict[acc] = "RefSeq" if "_" in acc else "GenBank/UniProt"
""",
            check_code="""# Check — do not edit
assert len(classification_dict) == 4, f"Expected 4 items, got {len(classification_dict)}"
assert classification_dict["NM_000518.5"] == "RefSeq"
assert classification_dict["V00497.1"] == "GenBank/UniProt"
print("Ex 2.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.2",
            stars="★☆☆",
            title="Construct an Entrez query for human insulin mRNA",
            biology="Insulin (INS) mRNA should be retrieved without genomic fragments or other species.",
            task="Construct an Entrez query string that searches for gene symbol `'INS'`, organism `'Homo sapiens'`, and includes filters `'biomol_mrna[PROP]'` and `'RefSeq[FILT]'`. Store it in variable `ins_query`.",
            expected="`ins_query` as a string containing all 4 required tags and uppercase 'AND'.",
            student_code="""# TODO: replace the ... with your code
# Construct the query string
ins_query = ...
""",
            solution_code="""ins_query = "INS[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]"
""",
            check_code="""# Check — do not edit
assert isinstance(ins_query, str), "ins_query must be a string"
assert "INS[GENE]" in ins_query, "Must specify INS[GENE]"
assert "Homo sapiens[ORGN]" in ins_query, "Must specify Homo sapiens[ORGN]"
assert "biomol_mrna[PROP]" in ins_query and "RefSeq[FILT]" in ins_query, "Must include biomol_mrna and RefSeq filters"
assert "AND" in ins_query, "Must use uppercase AND"
print("Ex 2.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.3",
            stars="★☆☆",
            title="Parse an Entrez search result dictionary",
            biology="An Entrez search returns an XML object with total count and a list of UIDs.",
            task="Given sample search dictionary `mock_search_result`, extract the total count as an integer into `hit_count` and the first accession/ID into `top_hit`.",
            expected="`hit_count` as int (1), `top_hit` as str ('NM_000518.5').",
            student_code="""# TODO: replace the ... with your code
mock_search_result = {
    "Count": "1",
    "RetMax": "1",
    "IdList": ["NM_000518.5"],
    "TranslationSet": []
}

hit_count = ...
top_hit = ...
""",
            solution_code="""mock_search_result = {
    "Count": "1",
    "RetMax": "1",
    "IdList": ["NM_000518.5"],
    "TranslationSet": []
}

hit_count = int(mock_search_result["Count"])
top_hit = mock_search_result["IdList"][0]
""",
            check_code="""# Check — do not edit
assert hit_count == 1, f"Expected 1, got {hit_count}"
assert top_hit == "NM_000518.5", f"Expected NM_000518.5, got {top_hit}"
print("Ex 2.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.4",
            stars="★★☆",
            title="Build an Entrez query with title keywords for TP53",
            biology="Tumor suppressor p53 has many isoforms and pseudo-entries; restricting to title keywords ensures retrieving the primary isoform.",
            task="Construct an Entrez query for `TP53` in `Homo sapiens`, with `biomol_mrna[PROP]`, `RefSeq[FILT]`, and title word `transcript variant 1[TITL]`. Store in `tp53_query`.",
            expected="`tp53_query` string containing the title filter and uppercase 'AND'.",
            student_code="""# TODO: replace the ... with your code
tp53_query = ...
""",
            solution_code="""tp53_query = "TP53[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT] AND transcript variant 1[TITL]"
""",
            check_code="""# Check — do not edit
assert "TP53[GENE]" in tp53_query
assert "transcript variant 1[TITL]" in tp53_query
assert "RefSeq[FILT]" in tp53_query
print("Ex 2.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.5",
            stars="★★☆",
            title="Implement an offline-fallback loader for GenBank records",
            biology="Teaching scripts must run reliably regardless of network connectivity.",
            task="Write a function `load_record_offline_first(acc, local_path)` that attempts to open `local_path` using `SeqIO.read(..., 'genbank')`. Store the loaded record in `my_record`.",
            expected="`my_record` is a valid Biopython `SeqRecord` for HBB with length 626 bp.",
            student_code="""# TODO: replace the ... with your code
from Bio import SeqIO

def load_record_offline_first(acc, local_path):
    # Try reading from local_path
    ...

local_file = DATA_DIR / "genbank" / "hbb_human.gb"
my_record = load_record_offline_first("NM_000518.5", local_file)
""",
            solution_code="""from Bio import SeqIO

def load_record_offline_first(acc, local_path):
    if local_path.exists():
        return SeqIO.read(local_path, "genbank")
    raise FileNotFoundError(f"File {local_path} not found")

local_file = DATA_DIR / "genbank" / "hbb_human.gb"
my_record = load_record_offline_first("NM_000518.5", local_file)
""",
            check_code="""# Check — do not edit
assert my_record.id == "NM_000518.5", f"Expected NM_000518.5, got {my_record.id}"
assert len(my_record.seq) == 626, f"Expected 626 bp, got {len(my_record.seq)}"
print("Ex 2.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.6",
            stars="★★☆",
            title="Extract PubMed identifiers (PMIDs) from a GenBank record",
            biology="GenBank records cite primary literature establishing the sequence.",
            task="From `my_record.annotations['references']`, extract all PubMed IDs (`ref.pubmed_id`) that are non-empty strings. Store them in a list `pmids`.",
            expected="`pmids` list of string PMIDs containing at least one publication.",
            student_code="""# TODO: replace the ... with your code
pmids = []
for ref in my_record.annotations.get("references", []):
    ...
""",
            solution_code="""pmids = []
for ref in my_record.annotations.get("references", []):
    if ref.pubmed_id:
        pmids.append(str(ref.pubmed_id))
""",
            check_code="""# Check — do not edit
assert isinstance(pmids, list) and len(pmids) >= 1, "Expected at least 1 PubMed ID"
assert all(p.isdigit() for p in pmids), "PubMed IDs must be numeric strings"
print("Ex 2.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 2.7",
            stars="★★★",
            title="Build a multi-organism comparative query table",
            biology="Comparative genomics requires querying homologous genes across model organisms.",
            task="Given a dictionary of organisms `organisms = {'Human': 'Homo sapiens', 'Mouse': 'Mus musculus', 'Zebrafish': 'Danio rerio'}`, construct a dictionary `queries` mapping each organism name to an Entrez query for `HBB` RefSeq mRNA.",
            expected="`queries` dictionary with 3 entries, each containing `HBB[GENE]` and the respective organism tag.",
            student_code="""# TODO: replace the ... with your code
organisms = {
    "Human": "Homo sapiens",
    "Mouse": "Mus musculus",
    "Zebrafish": "Danio rerio"
}
queries = {}

for name, sci_name in organisms.items():
    ...
""",
            solution_code="""organisms = {
    "Human": "Homo sapiens",
    "Mouse": "Mus musculus",
    "Zebrafish": "Danio rerio"
}
queries = {}

for name, sci_name in organisms.items():
    queries[name] = f"HBB[GENE] AND {sci_name}[ORGN] AND biomol_mrna[PROP] AND RefSeq[FILT]"
""",
            check_code="""# Check — do not edit
assert len(queries) == 3
assert "Mus musculus[ORGN]" in queries["Mouse"]
assert "Danio rerio[ORGN]" in queries["Zebrafish"]
print("Ex 2.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U02_P",
        title="Entrez Search — Exercises",
        unit_num=2,
        unit_title="Information Retrieval from Biological Databases",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L3–L4, Practicals S2–S3",
        before_this="U02_C1"
    ))
    nb_student.cells.append(make_setup_cell("U02_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U02_P",
        title="Entrez Search — Solutions",
        unit_num=2,
        unit_title="Information Retrieval from Biological Databases",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L3–L4, Practicals S2–S3",
        before_this="U02_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U02_P"))
    
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
1. Why does searching `HBB` without field tags in NCBI Nucleotide return over 50,000 hits, whereas searching `HBB[GENE] AND Homo sapiens[ORGN] AND RefSeq[FILT]` returns fewer than 5 records?
2. What is the fundamental distinction between a primary archival record (GenBank) and a secondary curated record (RefSeq)?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u02_q():
    """Build U02_Q quiz notebook."""
    salt = "U02_Q"
    questions = [
        QuizQuestion("q1", "What does the RefSeq accession prefix 'NP_' signify?",
                     ["(a) Curated genomic DNA", "(b) Curated protein sequence", "(c) Curated mRNA", "(d) Predicted protein"],
                     "b", "U02_C1 §3"),
        QuizQuestion("q2", "Which Entrez field tag restricts a search term to the official gene symbol?",
                     ["(a) [ORGN]", "(b) [TITL]", "(c) [GENE]", "(d) [AUTH]"],
                     "c", "U02_C1 §4"),
        QuizQuestion("q3", "How does Entrez evaluate the query `HBB OR INS AND human` without parentheses?",
                     ["(a) (HBB OR INS) AND human", "(b) HBB OR (INS AND human)", "(c) All terms with equal precedence left to right", "(d) It produces a syntax error"],
                     "b", "U02_C1 §4"),
        QuizQuestion("q4", "Which Biopython Entrez function is used to download formatted records (such as FASTA or GenBank) by accession/UID?",
                     ["(a) Entrez.esearch", "(b) Entrez.esummary", "(c) Entrez.efetch", "(d) Entrez.einfo"],
                     "c", "U02_C1 §6"),
        QuizQuestion("q5", "What is the primary purpose of setting `Entrez.email` in Biopython?",
                     ["(a) To receive spam from NCBI", "(b) To comply with NCBI usage policy for contact before IP blocking", "(c) To decrypt sequence files", "(d) To authenticate a paid subscription"],
                     "b", "U02_C1 §5"),
        QuizQuestion("q6", "Which of the following is a primary INSDC accession (NOT a curated RefSeq)?",
                     ["(a) NM_000518.5", "(b) NP_000509.1", "(c) NC_001422.1", "(d) V00497.1"],
                     "d", "U02_C1 §3"),
        QuizQuestion("q7", "Which database within Entrez indexes biomedical research literature and MeSH terms?",
                     ["(a) Nucleotide", "(b) Gene", "(c) PubMed", "(d) OMIM"],
                     "c", "U02_C1 §3"),
        QuizQuestion("q8", "What format return type (`rettype`) should be specified in `efetch` to retrieve a complete GenBank flat file?",
                     ["(a) fasta", "(b) gbwithparts", "(c) xml", "(d) docsum"],
                     "b", "U02_C1 §6"),
        QuizQuestion("q9", "What does the RefSeq accession prefix 'NC_' represent?",
                     ["(a) Non-coding RNA", "(b) Complete chromosome or viral genome", "(c) Cloned cDNA", "(d) Contig"],
                     "b", "U02_C1 §3"),
        QuizQuestion("q10", "Which Entrez utility provides summary metadata (document summaries) without downloading the full sequence record?",
                     ["(a) esearch", "(b) esummary", "(c) egquery", "(d) elink"],
                     "b", "U02_C1 §5")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U02_Q",
        title="Information Retrieval — Quiz",
        unit_num=2,
        unit_title="Information Retrieval from Biological Databases",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L3–L4, Practicals S2–S3",
        before_this="U02_C1, U02_P"
    ))
    nb_student.cells.append(make_setup_cell("U02_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U02_Q",
        title="Information Retrieval — Quiz Key",
        unit_num=2,
        unit_title="Information Retrieval from Biological Databases",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L3–L4, Practicals S2–S3",
        before_this="U02_C1, U02_P"
    ))
    nb_key.cells.append(make_setup_cell("U02_Q"))
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


def generate_unit02():
    """Generate all notebooks for Unit 2."""
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 02 notebooks...")
    c1 = build_u02_c1()
    save_notebook(c1, UNIT_DIR / "U02_C1_Entrez_Search_from_Python.ipynb", clear=True)
    
    p_student, p_sol = build_u02_p()
    save_notebook(p_student, UNIT_DIR / "U02_P_Entrez_Search.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U02_P_Entrez_Search_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u02_q()
    save_notebook(q_student, UNIT_DIR / "U02_Q_Information_Retrieval.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U02_Q_Information_Retrieval_Key.ipynb", clear=False)
    
    print("  ✓ Unit 02 files written successfully.")
