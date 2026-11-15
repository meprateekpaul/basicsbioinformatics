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
├── index.html                Interactive Course Web Portal (Slides, Notes, Notebook Hub)
├── data/                     Standardized biological sequences, structures, and offline fallbacks
├── lectures/                 Lecture study notes for Units 1–11 (L01–L30)
├── slides/                   30 Marp/Markdown presentation slide decks (L01–L30)
├── practicals/               Lab sheets, student worksheets, and instructor keys (S01–S15)
├── notebooks/                59 Jupyter notebooks (C, P, Q) and solutions across Units U01–U11
├── assessments/              Question bank, quizzes, assignments, mini-project, and exams
└── references/               Recommended textbooks, web portals, and printable cheat sheets
```

---

## Unit Breakdown at a Glance

| Unit | Title | Lectures (Notes & Slides) | Syllabus Practical | Notebooks (C, P, Q) |
|:---:|:---|:---|:---|:---|
| **U01** | Bioinformatics and Internet | [Notes (L01–02)](lectures/U01_Bioinformatics_and_Internet/) · [Slides](slides/U01_Bioinformatics_and_Internet/) | [S01: Linux Commands](practicals/S01_Linux_Commands/) | [`U01_C1`](notebooks/U01_Bioinformatics_and_Internet/U01_C1_Sequences_as_Text.ipynb), [`P`](notebooks/U01_Bioinformatics_and_Internet/U01_P_Sequences_as_Text.ipynb), [`Q`](notebooks/U01_Bioinformatics_and_Internet/U01_Q_Bioinformatics_and_Internet.ipynb) |
| **U02** | Information Retrieval | [Notes (L03–04)](lectures/U02_Information_Retrieval/) · [Slides](slides/U02_Information_Retrieval/) | [S02: NCBI Tour](practicals/S02_NCBI_Introduction/) · [S03: Entrez](practicals/S03_Entrez_Literature/) | [`U02_C1`](notebooks/U02_Information_Retrieval/U02_C1_Entrez_Search_from_Python.ipynb), [`P`](notebooks/U02_Information_Retrieval/U02_P_Entrez_Search.ipynb), [`Q`](notebooks/U02_Information_Retrieval/U02_Q_Information_Retrieval.ipynb) |
| **U03** | NCBI Data Model & ASN.1 | [Notes (L05–06)](lectures/U03_NCBI_Data_Model/) · [Slides](slides/U03_NCBI_Data_Model/) | *(integrated with U02/U04)* | [`U03_C1`](notebooks/U03_NCBI_Data_Model/U03_C1_Inside_a_Sequence_Record.ipynb), [`P`](notebooks/U03_NCBI_Data_Model/U03_P_Inside_a_Sequence_Record.ipynb), [`Q`](notebooks/U03_NCBI_Data_Model/U03_Q_NCBI_Data_Model.ipynb) |
| **U04** | GenBank Sequence Database | [Notes (L07–09)](lectures/U04_GenBank_Database/) · [Slides](slides/U04_GenBank_Database/) | [S04: DNA](practicals/S04_GenBank_DNA_Retrieval/) · [S05: Protein](practicals/S05_Protein_Retrieval_Expasy/) | [`U04_C1`](notebooks/U04_GenBank_Database/U04_C1_GenBank_Flat_File.ipynb), [`C2`](notebooks/U04_GenBank_Database/U04_C2_Formats_and_Conversion.ipynb), [`P`](notebooks/U04_GenBank_Database/U04_P_GenBank_Database.ipynb), [`Q`](notebooks/U04_GenBank_Database/U04_Q_GenBank_Database.ipynb) |
| **U05** | Alignment & BLAST/FASTA | [Notes (L10–15)](lectures/U05_Sequence_Alignment/) · [Slides](slides/U05_Sequence_Alignment/) | [S06: BLAST](practicals/S06_BLAST_Alignment/) · [S07: FASTA](practicals/S07_FASTA_Alignment/) | [`U05_C1`](notebooks/U05_Sequence_Alignment/U05_C1_Dot_Plots_and_Global_Alignment.ipynb), [`C2`](notebooks/U05_Sequence_Alignment/U05_C2_Local_Alignment_and_Scoring.ipynb), [`C3`](notebooks/U05_Sequence_Alignment/U05_C3_Reading_BLAST_Results.ipynb), [`P`](notebooks/U05_Sequence_Alignment/U05_P_Sequence_Alignment.ipynb), [`Q`](notebooks/U05_Sequence_Alignment/U05_Q_Sequence_Alignment.ipynb) |
| **U06** | Multiple Alignment (MSA) | [Notes (L16–17)](lectures/U06_Multiple_Sequence_Alignment/) · [Slides](slides/U06_Multiple_Sequence_Alignment/) | [S08: ClustalW & Jalview](practicals/S08_ClustalW_MSA/) | [`U06_C1`](notebooks/U06_Multiple_Sequence_Alignment/U06_C1_Multiple_Alignment_and_Conservation.ipynb), [`P`](notebooks/U06_Multiple_Sequence_Alignment/U06_P_Multiple_Sequence_Alignment.ipynb), [`Q`](notebooks/U06_Multiple_Sequence_Alignment/U06_Q_Multiple_Sequence_Alignment.ipynb) |
| **U07** | Phylogenetic Analysis | [Notes (L18–20)](lectures/U07_Phylogenetic_Analysis/) · [Slides](slides/U07_Phylogenetic_Analysis/) | *(tree building from S08 MSA)* | [`U07_C1`](notebooks/U07_Phylogenetic_Analysis/U07_C1_Distances_and_Trees.ipynb), [`P`](notebooks/U07_Phylogenetic_Analysis/U07_P_Phylogenetic_Trees.ipynb), [`Q`](notebooks/U07_Phylogenetic_Analysis/U07_Q_Phylogenetic_Analysis.ipynb) |
| **U08** | Predictive Nucleotide | [Notes (L21–22)](lectures/U08_Predictive_Nucleotide/) · [Slides](slides/U08_Predictive_Nucleotide/) | [S09: DNA Analysis](practicals/S09_DNA_Sequence_Analysis/) | [`U08_C1`](notebooks/U08_Predictive_Nucleotide/U08_C1_ORFs_GC_and_Codon_Usage.ipynb), [`P`](notebooks/U08_Predictive_Nucleotide/U08_P_Predictive_Nucleotide.ipynb), [`Q`](notebooks/U08_Predictive_Nucleotide/U08_Q_Predictive_Nucleotide.ipynb) |
| **U09** | Predictive Protein | [Notes (L23–25)](lectures/U09_Predictive_Protein/) · [Slides](slides/U09_Predictive_Protein/) | [S10: Protein](practicals/S10_Protein_Sequence_Analysis/) · [S11: GOR IV](practicals/S11_GOR_Secondary_Structure/) | [`U09_C1`](notebooks/U09_Predictive_Protein/U09_C1_Protein_Properties_and_Motifs.ipynb), [`C2`](notebooks/U09_Predictive_Protein/U09_C2_Secondary_Structure_Prediction_Scoring.ipynb), [`P`](notebooks/U09_Predictive_Protein/U09_P_Predictive_Protein.ipynb), [`Q`](notebooks/U09_Predictive_Protein/U09_Q_Predictive_Protein.ipynb) |
| **U10** | Structure Databases (PDB) | [Notes (L26–28)](lectures/U10_Structure_Databases/) · [Slides](slides/U10_Structure_Databases/) | [S12: PDB](practicals/S12_PDB_Structure_Database/) · [S13: VMD](practicals/S13_VMD_Visualisation/) | [`U10_C1`](notebooks/U10_Structure_Databases/U10_C1_Reading_a_PDB_File.ipynb), [`P`](notebooks/U10_Structure_Databases/U10_P_Structure_Databases.ipynb), [`Q`](notebooks/U10_Structure_Databases/U10_Q_Structure_Databases.ipynb) |
| **U11** | Comparative Genomics | [Notes (L29–30)](lectures/U11_Comparative_Genomics/) · [Slides](slides/U11_Comparative_Genomics/) | [S14: Mini-Project](practicals/S14_Mini_Project_Session/) · [S15: Exam](practicals/S15_Practical_Exam_Viva/) | [`U11_C1`](notebooks/U11_Comparative_Genomics/U11_C1_Comparing_Two_Genomes.ipynb), [`P`](notebooks/U11_Comparative_Genomics/U11_P_Comparative_Genomics.ipynb), [`Q`](notebooks/U11_Comparative_Genomics/U11_Q_Comparative_Genomics.ipynb) |

---

## Environment & Prerequisites

Python dependencies are managed via [`requirements.txt`](../requirements.txt):
```bash
pip install -r requirements.txt
```

Launch JupyterLab to interact with course notebooks:
```bash
jupyter lab
```

---

## License

This educational curriculum is open-source and distributed under the **MIT License**.
