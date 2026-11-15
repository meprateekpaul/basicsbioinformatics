# Concepts of Bioinformatics (CBBI-501)

> **Undergraduate Curriculum · B.Tech. Bioinformatics · Semester II**  
> *Inspired by the B.Tech. Bioinformatics Programme of [Sam Higginbottom University of Agriculture, Technology and Sciences (SHUATS)](https://shuats.edu.in/), Prayagraj, India*  
> *Department of Computational Biology & Bioinformatics, Jacob Institute of Biotechnology & Bioengineering (JSBB)*  
> **Credits:** 3 (L-T-P: 2-0-1) | 30 Theory Lectures · 15 Practical Sessions · 11 Python Notebook Units

Welcome to the course repository for **Concepts of Bioinformatics**. This course introduces first-year B.Tech. undergraduates to the core computational, structural, and evolutionary concepts underpinning contemporary bioinformatics.

---

## Pedagogical Architecture & Design

1. **Central Molecular Thread:** Human beta-globin (*HBB*, RefSeq `NM_000518`, protein `P68871`, PDB `1A3N`/`4HHB`), insulin (*INS*), *TP53*, and the vertebrate globin gene family serve as continuous case studies across databases, alignments, phylogenetic trees, biochemical prediction, and 3D structural analysis. The sickle-cell mutation (HbS, Glu6Val) provides a direct link between sequence variation and phenotypic disease.
2. **Dual-Track Learning:**
   - **Theory & Syllabus Practicals:** Canonical university curriculum using production web tools and servers (NCBI Entrez, BLAST, EBI FASTA, Clustal Omega, Jalview, NPS@ GOR IV, RCSB PDB, VMD/Mol*).
   - **Interactive Python Notebooks:** Run-and-modify Jupyter notebooks (`C` Course, `P` Practice with self-checks, and `Q` Quiz with instant hashed feedback) powered by Biopython, strictly following [`../NOTEBOOK_GUIDE.md`](../NOTEBOOK_GUIDE.md).
3. **Resilience & Offline First:** All datasets, accession records, expected outputs, and structure coordinates are bundled in `data/` so classes and practicals never stall due to external server outages or network lag.

---

## Course Navigation

```
Concepts_of_Bioinformatics/
├── COURSE_PLAN.md            Detailed university syllabus mapping and weekly schedule
├── FOUR_MONTH_ROADMAP.md     15-week (4-month) structured study guide & time budget
├── SYLLABUS.md               Official syllabus text and learning outcomes (LO1–LO8)
├── data/                     Standardized biological sequences, structures, and offline fallbacks
├── lectures/                 Lecture slides and comprehensive study notes for Units 1–11 (L01–L30)
├── practicals/               Lab sheets, student worksheets, and instructor keys (S01–S15)
├── notebooks/                Jupyter notebooks (C, P, Q) and solutions across Units U01–U11
├── assessments/              Question bank, quizzes, assignments, mini-project, and examination papers
└── references/               Recommended textbooks, web portals, and printable cheat sheets
```

---

## Unit Breakdown at a Glance

| Unit | Title | Lectures | Syllabus Practical | Notebooks |
|---|---|---|---|---|
| **U01** | Bioinformatics and Internet | L01–L02 | S01: Linux Commands | `U01_C1`, `U01_P`, `U01_Q` |
| **U02** | Information Retrieval from Biological Databases | L03–L04 | S02: NCBI Tour · S03: Entrez Literature | `U02_C1`, `U02_P`, `U02_Q` |
| **U03** | The NCBI Data Model | L05–L06 | *(integrated with U02/U04)* | `U03_C1`, `U03_P`, `U03_Q` |
| **U04** | GenBank Sequence Database | L07–L09 | S04: DNA Retrieval · S05: Protein Retrieval | `U04_C1`, `U04_C2`, `U04_P`, `U04_Q` |
| **U05** | Sequence Alignment & Database Searching | L10–L15 | S06: BLAST · S07: FASTA | `U05_C1`, `U05_C2`, `U05_C3`, `U05_P`, `U05_Q` |
| **U06** | Multiple Sequence Alignment (MSA) | L16–L17 | S08: ClustalW & Clustal Omega | `U06_C1`, `U06_P`, `U06_Q` |
| **U07** | Phylogenetic Analysis | L18–L20 | *(tree building from S08 MSA)* | `U07_C1`, `U07_P`, `U07_Q` |
| **U08** | Predictive Methods: Nucleotide Sequence | L21–L22 | S09: DNA Sequence Analysis | `U08_C1`, `U08_P`, `U08_Q` |
| **U09** | Predictive Methods: Protein Sequence | L23–L25 | S10: Protein Analysis · S11: GOR Algorithm | `U09_C1`, `U09_C2`, `U09_P`, `U09_Q` |
| **U10** | Structure Databases & Visualisation | L26–L28 | S12: PDB Database · S13: VMD Visualisation | `U10_C1`, `U10_P`, `U10_Q` |
| **U11** | Comparative Genome Analysis | L29–L30 | S14: Mini-Project · S15: Practical Exam | `U11_C1`, `U11_P`, `U11_Q` |

---

## Environment & Prerequisites

Python dependencies are managed via [`btech/requirements.txt`](../requirements.txt):
```bash
pip install -r ../requirements.txt
```

Launch JupyterLab to interact with course notebooks:
```bash
jupyter lab
```

---

## License

This educational curriculum is open-source and distributed under the **MIT License**.
