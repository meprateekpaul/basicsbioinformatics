# Basics of Genomics & Proteomics — Course Plan

> **Programme:** B.Tech. Bioinformatics, Semester III (outline w.e.f. July 2017)
> **Code:** CBBI-504
> **Credits:** 3 (L-T-P 2-0-1) — two lectures and one 2-hour practical per week
> **Syllabus source:** `../BTech_Bioinformatics_CBBI_Syllabus.md`
>
> Everything under "Syllabus" is from the university documents. Lecture counts, the weekly schedule, the added practicals, the assessment split and the folder layout are proposals in this plan and can be changed.

---

## Contents

1. [Course at a glance](#1-course-at-a-glance)
2. [Learning outcomes](#2-learning-outcomes)
3. [Design decisions](#3-design-decisions)
4. [Theory plan, unit by unit](#4-theory-plan-unit-by-unit)
5. [Practical plan](#5-practical-plan)
6. [Week-by-week schedule](#6-week-by-week-schedule)
7. [Assessment plan](#7-assessment-plan)
8. [Folder structure](#8-folder-structure)
9. [Material to build](#9-material-to-build)
10. [References](#10-references)
11. [Python notebooks](#11-python-notebooks)

---

## 1. Course at a glance

| Unit | Syllabus topic | Lectures | Practicals |
|---|---|---|---|
| 1 | Organization and structure of genomes | 7 | P3 |
| 2 | The proteome and tools of proteomics | 7 | (added: A2, A3) |
| 3 | Genome annotation, gene function, comparative and structural genomics | 10 | P2, P4, P5, P6, P1 (added: A1) |
| 4 | Global expression profiling | 6 | (added: A4) |
| | **Total** | **30** | **6 syllabus + 4 added** |

Assumes a 15-teaching-week semester: 30 lecture hours and 15 practical sessions.

**Where the course sits.** Students have completed Concepts of Bioinformatics (databases, BLAST, MSA, ORFs), Molecular Biology, Biochemistry-I and Linux & Shell Programming in Semester II. Biochemistry-II and Statistical Methods run alongside. This course feeds CBBI-507 (Computational Analysis of Biomolecules), CBBI-508 (Biological Databases), CBBI-615 (Next Generation Sequencing) and CBBI-612 (Clinical Bioinformatics).

**Two imbalances in the syllabus to plan around:**

- The syllabus lists only 6 practicals for a 15-session semester, and none of them touches proteomics or expression data even though those are half the theory. Four added practicals (A1–A4) close that gap; they are marked as additions throughout so the official practical record stays intact.
- Practicals P4–P6 (BLAST, ClustalW, comparative BLAST) repeat tools from Concepts of Bioinformatics. Here they are run at genome scale and from the command line so they teach something new.

---

## 2. Learning outcomes

By the end of the course a student can:

1. Describe how viral, prokaryotic and eukaryotic genomes are organised, and explain why genome size does not track organism complexity (the C-value paradox).
2. Distinguish genome, transcriptome and proteome, and explain why the proteome cannot be read directly off the genome.
3. Explain the principle, output and limits of 2D-PAGE, liquid chromatography and the main types of mass spectrometer, and follow a peptide-mass-fingerprint identification from spectrum to protein.
4. Find genes in a raw prokaryotic sequence using ORF detection and a gene-finding program, and evaluate the predictions against a reference annotation.
5. Assign a putative function to a new gene using sequence similarity, conserved domains, Gene Ontology and pathway databases, and state how confident the assignment is.
6. Compare two genomes and interpret synteny, shared and unique genes.
7. Describe traditional and global methods of expression profiling and carry out a basic differential-expression query on a public dataset.

Each lecture and practical below is tagged with the outcome it serves (LO1–LO7).

---

## 3. Design decisions

**One organism pair all semester.** *Escherichia coli* K-12 MG1655 (NC_000913) is the main genome: small enough to handle on lab machines, the best-annotated bacterial genome, and suitable for GLIMMER, which is a prokaryotic gene finder. Its pathogenic relative *E. coli* O157:H7 Sakai (NC_002695) is the comparison genome, which gives comparative genomics a concrete question: what does the pathogen have that the lab strain does not? For eukaryotic gene structure (introns, exons, alternative splicing), use human *HBB* and *TP53*, already familiar from Semester II. Bacteriophage lambda (NC_001416) is the warm-up genome for first runs because every tool finishes on it in seconds.

**Biology and technique before software.** This is the "basics" course. Each computational step is tied to the wet-lab measurement it depends on, so students know what the data is before they analyse it.

**Syllabus items that need updating in delivery.** Teach the concept the syllabus names and add the current state in a clearly marked segment:

| Syllabus item | What to add |
|---|---|
| "Traditional routes of gene identification" | Keep as written (cDNA/EST evidence, ORF scanning, homology), then contrast with RNA-seq-supported annotation |
| GLIMMER | Use GLIMMER3 as specified; show Prodigal output on the same genome for comparison |
| "Traditional approaches to expression profiling" / "analysis of RNA expression" | Northern blot, RT-PCR, SAGE, microarrays as the syllabus implies; one lecture on RNA-seq as the current standard (depth is left to CBBI-615) |
| "Types of mass spectrometers" | Ionisation (MALDI, ESI) and analysers (TOF, quadrupole, ion trap, Orbitrap); MS vs MS/MS |
| "Tandem liquid chromatography" | Teach as multidimensional LC coupled to tandem MS (MudPIT, LC-MS/MS); "tandem" in the syllabus line most likely refers to this |
| "Protein structural genomics" | Structural genomics initiatives, then AlphaFold DB as the present-day outcome |
| ClustalW | Run Clustal Omega/MUSCLE; show ClustalW once for the practical record |

**Server and install dependence.** GLIMMER, BLAST+ and EMBOSS need local installation; test on the lab image before week 1. Keep saved expected output for every practical in `data/expected/`.

---

## 4. Theory plan, unit by unit

### Unit 1 — Organization and structure of genomes (7 lectures) · LO1

*Syllabus:* Introduction: organization and structure of genomes — genome size — sequence complexity — introns and exons — genome structure in viruses and prokaryotes, C-value paradox.

| L | Content |
|---|---|
| 1 | What genomics is; from gene-by-gene to whole-genome biology. Brief history: phage ΦX174 → *H. influenzae* → human genome. Course map and the *E. coli* thread. |
| 2 | Genome size across life: units (bp, kb, Mb, Gb), C-value, range from viruses to plants and amphibians. Gene number vs genome size. |
| 3 | The C-value paradox and its resolution: non-coding DNA, repeats, polyploidy. Gene density compared across *E. coli*, yeast, human. |
| 4 | Sequence complexity: unique, moderately repetitive and highly repetitive DNA; reassociation kinetics (Cot curves) in outline; satellites, tandem repeats, transposable elements (LINEs, SINEs). |
| 5 | Viral genomes: DNA/RNA, single/double-stranded, linear/circular/segmented, overlapping genes. Lambda and one RNA virus as cases. |
| 6 | Prokaryotic genomes: circular chromosome, plasmids, operons, high coding density, little non-coding DNA, genomic islands and horizontal transfer. |
| 7 | Eukaryotic gene structure: exons, introns, UTRs, promoters; splicing and alternative splicing; why one gene can give many proteins. Organelle genomes in brief. |

*Check:* Quiz 1 — given genome size and gene count for five organisms, compute gene density and explain the outliers.

### Unit 2 — The proteome and tools of proteomics (7 lectures) · LO2, LO3

*Syllabus:* The proteome, genomics vs proteomics, proteomics and the new biology. Tools of proteomics: two-dimensional PAGE, tandem liquid chromatography, types of mass spectrometers.

| L | Content |
|---|---|
| 8 | The proteome: definition, dynamic nature, dependence on cell type and condition. Why proteome ≠ genome: alternative splicing, post-translational modification, turnover, localisation. |
| 9 | Genomics vs proteomics: what each measures, weak mRNA–protein correlation. "Proteomics and the new biology": expression, structural, functional and interaction proteomics. |
| 10 | Separation I — 2D-PAGE: isoelectric focusing (pI), SDS-PAGE (mass), staining, spot detection, strengths and blind spots (membrane, very basic, low-abundance proteins). DIGE in brief. |
| 11 | Separation II — liquid chromatography: reverse-phase, ion-exchange, multidimensional LC; coupling to MS; gel-based vs gel-free ("shotgun") workflows. |
| 12 | Mass spectrometry I: what m/z is; ionisation by MALDI and ESI; analysers — TOF, quadrupole, ion trap, Orbitrap; reading a mass spectrum. |
| 13 | Mass spectrometry II: peptide mass fingerprinting step by step (digest → masses → database match); tandem MS, b- and y-ions, peptide sequencing in outline. |
| 14 | From spectra to proteins: database search engines (Mascot, SEQUEST idea), false discovery in one slide; proteomics repositories (PRIDE, UniProt proteomes). Applications: biomarker discovery, PTM mapping. |

*Check:* Quiz 4 — place given proteins on a blank 2D gel from their pI and mass; identify a protein from a list of tryptic peptide masses.

### Unit 3 — Genome annotation and gene function (10 lectures) · LO4, LO5, LO6

*Syllabus:* Genome annotation: traditional routes of gene identification — detecting open-reading frames — software programs for finding genes — identifying the function of a new gene — gene ontology — overview of comparative genomics — protein structural genomics — introduction — determining gene function by sequence comparison and through conserved protein structure.

| L | Content |
|---|---|
| 15 | From sequencing to annotation: how a genome is sequenced and assembled (Sanger shotgun → NGS, in outline), what an assembly is, structural vs functional annotation. |
| 16 | Traditional routes of gene identification: cDNA and EST evidence, homology to known genes, experimental mapping. |
| 17 | Detecting ORFs: six-frame translation, start/stop codons, minimum length thresholds, why ORF ≠ gene, false positives on the opposite strand. |
| 18 | Gene-finding software I — prokaryotes: signals (RBS, start codons) and content (codon usage, hexamer frequencies); interpolated Markov models as used by GLIMMER, as an idea without the mathematics; Prodigal. |
| 19 | Gene-finding software II — eukaryotes: why it is harder (introns, splice sites, low coding density); GENSCAN/AUGUSTUS in outline; evidence-based annotation. Sensitivity and specificity of predictions. |
| 20 | Identifying the function of a new gene I — sequence comparison: BLAST against annotated proteins, orthologues vs paralogues, limits of annotation transfer, "hypothetical protein". |
| 21 | Identifying function II — conserved domains and structure: Pfam, InterPro, CDD; function from conserved protein structure when sequence similarity is gone. |
| 22 | Gene Ontology: three aspects (molecular function, biological process, cellular component), the graph structure, evidence codes, annotation files; pathways in KEGG. |
| 23 | Overview of comparative genomics: synteny, core and accessory genomes, orthologue clusters (COGs), genomic islands; *E. coli* K-12 vs O157:H7 as the worked case. |
| 24 | Protein structural genomics: aims and output of structural genomics initiatives, fold space, structure-based function assignment; AlphaFold DB as today's coverage of fold space. |

*Check:* Assignment 1 — annotate a 20 kb unlabelled bacterial contig (see §7).

### Unit 4 — Global expression profiling (6 lectures) · LO7

*Syllabus:* Global expression profiling: introduction — traditional approaches to expression profiling — analysis of RNA expression — applications of genome analysis and genomics.

| L | Content |
|---|---|
| 25 | Why measure expression globally: same genome, different cell states. Traditional single-gene methods: Northern blot, RT-PCR/qPCR, in situ hybridisation. |
| 26 | From single genes to global: EST counting, SAGE, differential display. |
| 27 | DNA microarrays: spotted vs oligonucleotide arrays, one- vs two-colour designs, from image to expression matrix. |
| 28 | Analysis of RNA expression: normalisation in concept, fold change, why replicates and a statistical test are needed, clustering and heat maps. Public data: GEO, ArrayExpress. |
| 29 | RNA-seq as the current standard (added segment): principle, counts vs intensities, what it adds over arrays. Proteome-level expression profiling as the link back to Unit 2. |
| 30 | Applications of genome analysis and genomics: medicine (disease genes, pharmacogenomics, pathogen surveillance), agriculture, evolution, metagenomics. Course wrap-up and bridge to Semester IV–VI courses. |

*Check:* in-class exercise (and end-semester questions) — interpret a heat map and a volcano plot; choose a profiling method for three scenarios.

---

## 5. Practical plan

One 2-hour session each. "P" numbers are the syllabus practicals; "A" numbers are additions proposed in this plan.

| Session | No. | Practical | Tools and data | What the student submits | LO |
|---|---|---|---|---|---|
| 1 | P3 (part 1) | Analysing nucleotide sequence with computational tools: genome records and statistics | NCBI Genome/Assembly; download NC_001416 and NC_000913; EMBOSS `infoseq`, `geecee`, `compseq`; shell | Table: size, GC%, gene count, coding density for lambda, *E. coli*, yeast, human | 1 |
| 2 | P3 (part 2) | Analysing nucleotide sequence: repeats, GC skew and gene structure | EMBOSS `etandem`/`einverted`, GC-skew plot; Ensembl/NCBI Gene view of *HBB* and *TP53* exon–intron structure | GC-skew plot locating the origin; exon/intron table for two human genes | 1 |
| 3 | A1 | ORF detection (supports syllabus theory "detecting open-reading frames") | ORFfinder, EMBOSS `getorf` on lambda | ORF count at three length thresholds vs the number of annotated genes in the RefSeq record; explain the difference | 4 |
| 4 | P2 (part 1) | Gene finding using GLIMMER | GLIMMER3: `long-orfs` → `build-icm` → `glimmer3` on lambda, then *E. coli* | Prediction file; commands used | 4 |
| 5 | P2 (part 2) | Gene finding using GLIMMER: evaluating predictions | Compare GLIMMER output with RefSeq annotation (shell, spreadsheet); Prodigal for contrast | Sensitivity and specificity; five missed or wrong genes examined | 4 |
| 6 | P4 | Finding similar sequences using BLAST | BLAST+ on the command line: `makeblastdb`, `blastp` of predicted proteins vs Swiss-Prot subset | Function assignments for 10 predicted genes with E-value, identity, coverage | 5 |
| 7 | A2 | Function from domains and Gene Ontology (supports syllabus theory "identifying the function of a new gene — gene ontology") | InterProScan (web), QuickGO/AmiGO, UniProt | GO terms with evidence codes for the same 10 genes; where BLAST and domain evidence disagree | 5 |
| 8 | P1 | Exploring KEGG | KEGG PATHWAY, KEGG Mapper, organism codes `eco` and `ecs` | Glycolysis and one other pathway mapped; genes present in one strain only | 5, 6 |
| 9 | P5 | Comparative sequence analysis using multiple sequence alignment — ClustalW | Orthologues of one protein across 8 genomes; ClustalW and Clustal Omega; Jalview | MSA with conserved functional residues annotated | 5, 6 |
| 10 | P6 (part 1) | Comparative genomics and BLAST: whole-genome comparison | BLASTN of K-12 vs O157:H7; dot plot / Artemis Comparison Tool or Mauve | Synteny plot with inversions and islands marked | 6 |
| 11 | P6 (part 2) | Comparative genomics and BLAST: shared and unique genes | Reciprocal best BLAST hits between the two proteomes | Counts of shared and strain-specific genes; function of 10 O157-specific genes | 6 |
| 12 | A3 | Proteomics in silico (supports syllabus theory "tools of proteomics") | Expasy Compute pI/Mw, PeptideMass (tryptic digest), PeptideCutter; a supplied peak list searched with Mascot PMF (free web version) | Predicted 2D-gel position of 10 *E. coli* proteins; protein identified from the peak list | 2, 3 |
| 13 | A4 | Expression profiling from public data (supports syllabus theory "analysis of RNA expression") | NCBI GEO, GEO2R on one *E. coli* stress dataset | Top 20 differentially expressed genes, mapped to KEGG pathways from session 8 | 7 |
| 14 | — | Mini-project work session | | See §7 | all |
| 15 | — | Practical examination and viva | | | |

Sessions 3–8 form one pipeline on the same gene set: raw sequence → ORFs → predicted genes → evaluated → function by similarity → function by domain/GO → pathway. Students keep one running results table across those weeks.

**If only the six syllabus practicals may be recorded:** run P1–P6 as sessions 1, 2, 4, 5, 6, 8, 9, 10, 11 (nine sessions) and use the remaining slots for tutorials, the mini-project and revision. A1–A4 can then be offered as demonstrations.

**Lab sheet format:** aim → background (half a page) → procedure with exact accessions and commands → observations table → 3–5 interpretation questions → one extension task.

---

## 6. Week-by-week schedule

| Week | Lecture 1 | Lecture 2 | Practical | Assessment |
|---|---|---|---|---|
| 1 | L1 What is genomics | L2 Genome size | S1 Genome records and statistics | |
| 2 | L3 C-value paradox | L4 Sequence complexity | S2 Repeats, GC skew, gene structure | |
| 3 | L5 Viral genomes | L6 Prokaryotic genomes | S3 ORF detection (A1) | |
| 4 | L7 Eukaryotic gene structure | L15 Sequencing to annotation | S4 GLIMMER I | Quiz 1 (Unit 1) |
| 5 | L16 Traditional gene identification | L17 Detecting ORFs | S5 GLIMMER II | |
| 6 | L18 Gene finders: prokaryotes | L19 Gene finders: eukaryotes | S6 BLAST function assignment | |
| 7 | L20 Function by sequence comparison | L21 Function by domains and structure | S7 Domains and GO (A2) | Quiz 2 (gene finding) |
| 8 | L22 Gene Ontology and pathways | L23 Comparative genomics | S8 KEGG | Mid-semester test (Unit 1, Unit 3 to L21) |
| 9 | L24 Structural genomics | L8 The proteome | S9 MSA of orthologues | Assignment 1 issued |
| 10 | L9 Genomics vs proteomics | L10 2D-PAGE | S10 Whole-genome comparison | |
| 11 | L11 Liquid chromatography | L12 Mass spectrometry I | S11 Shared and unique genes | Quiz 3 (Unit 3) |
| 12 | L13 Mass spectrometry II | L14 Spectra to proteins | S12 Proteomics in silico (A3) | Assignment 1 due; mini-project issued |
| 13 | L25 Traditional expression methods | L26 SAGE and early global methods | S13 Expression from GEO (A4) | Quiz 4 (Unit 2) |
| 14 | L27 Microarrays | L28 Analysis of RNA expression | S14 Mini-project | |
| 15 | L29 RNA-seq; proteome profiling | L30 Applications, wrap-up | S15 Practical exam | Mini-project due |

**Teaching order differs from syllabus order.** The syllabus lists proteomics second; here genome annotation (Unit 3) is taught straight after genome organisation, and proteomics (Unit 2) moves to weeks 9–12. Reasons: the practicals are almost all genome annotation and need the theory early, and proteomics then leads directly into expression profiling. If the department requires syllabus order, swap the Unit 2 and Unit 3 blocks and move sessions 12 and 3–8 accordingly.

---

## 7. Assessment plan

The split below is a proposal; replace the weights with the department's scheme.

| Component | Weight | Notes |
|---|---|---|
| Quizzes (4, best 3 count) | 10% | 15 minutes each, closed book |
| Assignment 1 | 5% | "Annotate a contig": each student gets a different 20 kb unlabelled bacterial region; deliver gene coordinates, putative functions with evidence, and GO terms |
| Mid-semester test | 20% | Unit 1 and Unit 3 up to L21 |
| Practical record and continuous lab evaluation | 15% | Marked each session from the lab sheet and the running results table |
| Mini-project | 10% | Groups of 2–3: pick a pair of related bacterial genomes (list supplied), compare them, and explain one biological difference from the gene content; 4-page report |
| Practical exam and viva | 10% | One gene-finding or BLAST task and one database task drawn at random |
| End-semester exam | 30% | All units |

**Question bank target:** 20 MCQs, 8 short-answer and 3 long-answer questions per unit, each tagged with its learning outcome. Include numerical items: gene density, coding fraction, peptide masses, pI/mass placement, sensitivity/specificity of a gene finder, fold change.

---

## 8. Folder structure

```
Basics_of_Genomics_and_Proteomics/
├── COURSE_PLAN.md            this file
├── README.md                 one-page overview for students
├── SYLLABUS.md               official syllabus text for this course only
├── lectures/
│   ├── U1_Genome_Organization/              L01–L07 slides + notes
│   ├── U2_Proteome_and_Proteomics_Tools/    L08–L14
│   ├── U3_Genome_Annotation/                L15–L24
│   └── U4_Expression_Profiling/             L25–L30
├── practicals/
│   ├── S01_Genome_Records_and_Statistics/   lab_sheet.md, worksheet, answer key
│   ├── ...
│   └── S13_Expression_from_GEO/
├── notebooks/                 Python notebooks: course (C), practice (P), quiz (Q) per unit — see §11
│   ├── U1_Genome_Organization/              U1_C1_....ipynb, U1_P_....ipynb, U1_Q_....ipynb, solutions/
│   └── ...
├── outputs/                   written by notebooks; git-ignored
├── data/
│   ├── genomes/              lambda, E. coli K-12, E. coli O157:H7 (FASTA, GenBank, GFF, proteomes)
│   ├── proteomics/           peak list for PMF, protein list for 2D-gel exercise
│   ├── expression/           GEO accession notes, exported tables
│   └── expected/             saved outputs for each practical
├── scripts/                  shell commands for GLIMMER, BLAST+, EMBOSS runs
├── assessments/
│   ├── quizzes/
│   ├── assignment_1/         per-student contigs + key
│   ├── mini_project/         brief, genome-pair list, rubric
│   ├── question_bank/        one file per unit
│   └── exams/
└── references/               reading list, tool links, cheat sheets
```

Whole genomes are large for a Google Drive/Git folder: keep the lambda files in `data/genomes/` and a download script with accession numbers for the *E. coli* genomes.

---

## 9. Material to build

Checklist, in the order it is needed.

- [ ] `SYLLABUS.md` and `README.md`
- [ ] Lab image check: GLIMMER3, Prodigal, BLAST+, EMBOSS, Jalview, Artemis/ACT or Mauve installed and tested
- [ ] `data/genomes/` and download script; Swiss-Prot subset for local BLAST
- [ ] Lecture slides and notes for Unit 1 (L1–L7) and Unit 3 (L15–L24)
- [ ] Lab sheets S1–S8 with tested commands and saved expected output; template for the running results table
- [ ] Quiz 1, Quiz 2, mid-semester paper
- [ ] Assignment 1 contig set (one per student) and marking key
- [ ] Lecture slides and notes for Unit 2 (L8–L14) and Unit 4 (L25–L30)
- [ ] Lab sheets S9–S13; PMF peak list with known answer; chosen GEO dataset checked in GEO2R
- [ ] Mini-project brief, genome-pair list, rubric
- [ ] Quiz 3, Quiz 4, practical exam task pool, end-semester paper
- [ ] Question bank, one file per unit
- [ ] Python notebooks: 12 course, 5 practice, 5 quiz, with solutions and keys (list, build order and tracker in §11)
- [ ] One-page cheat sheets: genome sizes and gene counts, GLIMMER workflow, BLAST+ commands, GO evidence codes, mass spectrometer types

---

## 10. References

The syllabus PDF lists no textbooks. Suggested:

**Core texts**
- Brown T.A. *Genomes.* Garland Science / CRC Press. Covers Units 1, 3 and 4.
- Liebler D.C. *Introduction to Proteomics: Tools for the New Biology.* Humana Press. The syllabus phrases "proteomics and the new biology" and "tools of proteomics" echo this title, so it fits Unit 2 closely.
- Primrose S.B., Twyman R.M. *Principles of Genome Analysis and Genomics.* Blackwell. The phrase "applications of genome analysis and genomics" in Unit 4 matches this title.

**Supporting**
- Pevsner J. *Bioinformatics and Functional Genomics.* Wiley.
- Lesk A.M. *Introduction to Genomics.* Oxford University Press.
- Twyman R.M. *Principles of Proteomics.* Garland Science.
- Campbell A.M., Heyer L.J. *Discovering Genomics, Proteomics and Bioinformatics.* Pearson.

**Online**
- NCBI Genome, Assembly and GEO help pages
- GLIMMER3 release notes and manual (CCB, Johns Hopkins)
- Gene Ontology Resource documentation
- KEGG help and KEGG Mapper
- Expasy proteomics tools
- EMBL-EBI Training on-demand courses (genomics, proteomics)

---

## 11. Python notebooks

Each unit gets Jupyter notebooks of three types: **course** (`C`, teaches with worked examples), **practice** (`P`, exercises with self-checks) and **quiz** (`Q`, short self-test with a score). How to write them — templates, naming, the quiz checker, the checklist — is in [`../NOTEBOOK_GUIDE.md`](../NOTEBOOK_GUIDE.md). This section lists what to build for this course.

**Level.** Semester III students have not yet had a Python course (Python for Bioinformatics is in Semester V), though those who used the Concepts of Bioinformatics notebooks have run and edited simple cells. Keep course notebooks run-and-modify and practice tasks to a few lines with the pattern shown above. Tables are handled with pandas; introduce each pandas operation where it is first used.

**Running examples.** Bacteriophage lambda (NC_001416) for anything computed live in the notebook, because it runs in seconds; *E. coli* K-12 MG1655 and O157:H7 Sakai through saved result tables; human *HBB* and *TP53* for gene structure.

**How they fit the week.** The command-line and web-tool sessions in §5 produce files (GLIMMER predictions, BLAST tables, GEO exports). The notebooks pick those files up and analyse them, so most notebooks are used in the *second half* of the matching practical or as homework after it. Each notebook also ships with a saved copy of its input in `data/expected/`, so it works for a student whose tool run failed. Quiz notebooks are for self-testing and do not replace the four graded quizzes in §7.

Unit numbers below follow the syllabus (Unit 2 = proteomics), not the teaching order.

### Notebooks to build

All paths are under `notebooks/U<n>_<Unit>/`.

| Unit | Course notebook | What the student does in it | With |
|---|---|---|---|
| 1 | `U1_C1_Genome_Size_and_Gene_Density` | Table of genome size and gene count for ~15 organisms; plot size vs gene number on log axes; compute gene density; see the C-value paradox in the plot | L2–L3, S1 |
| 1 | `U1_C2_GC_Content_Skew_and_Repeats` | Sliding-window GC content and cumulative GC skew for lambda and (from a saved table) *E. coli*; locate the origin; find simple tandem repeats | L4–L6, S2 |
| 1 | `U1_C3_Exons_Introns_and_Coding_Fraction` | Read gene features from GenBank records of *HBB* and *TP53*; exon and intron lengths; coding fraction of a human gene vs a bacterial genome | L6–L7, S2 |
| 3 | `U3_C1_Finding_ORFs` | Six-frame translation of lambda; ORFs at different length thresholds; compare the count with the annotated genes | L17, S3 |
| 3 | `U3_C2_Evaluating_Gene_Predictions` | Load GLIMMER output and the RefSeq annotation as tables; match predictions to genes; sensitivity and specificity; inspect missed genes | L18–L19, S4–S5 |
| 3 | `U3_C3_Function_from_BLAST_Hits` | Load a BLAST tabular file with pandas; best hit per gene; filter by E-value, identity and coverage; flag "hypothetical" hits | L20, S6 |
| 3 | `U3_C4_Gene_Ontology_Annotations` | Read a GO annotation (GAF) extract; count terms per aspect; evidence codes; most common terms in a gene set | L21–L22, S7–S8 |
| 3 | `U3_C5_Comparing_Two_Genomes` | Reciprocal best hits from two saved BLAST tables (K-12 vs O157:H7); shared and strain-specific gene counts; dot plot of gene positions to show synteny | L23, S10–S11 |
| 2 | `U2_C1_Virtual_2D_Gel` | Compute pI and molecular weight for a set of *E. coli* proteins with `ProtParam`; plot them as a 2D gel; see which proteins fall outside a typical gel's range | L10, S12 |
| 2 | `U2_C2_Peptide_Mass_Fingerprinting` | In-silico tryptic digest; peptide masses; match a supplied peak list against a small protein database and rank candidates | L12–L14, S12 |
| 4 | `U4_C1_Fold_Change_and_Volcano_Plot` | Expression table from one GEO dataset: log2 transform, fold change, t-test per gene, volcano plot | L27–L28, S13 |
| 4 | `U4_C2_Clustering_and_Heat_Maps` | Top variable genes; hierarchical clustering; heat map; read co-expressed groups against KEGG pathways | L28–L29, S13 |

| Unit | Practice notebook | Focus | Quiz notebook | Focus |
|---|---|---|---|---|
| 1 | `U1_P_Genome_Organization` | Gene density and coding fraction for three new genomes; GC skew of a plasmid | `U1_Q_Genome_Organization` | Genome sizes, C-value paradox, repeat classes, prokaryote vs eukaryote gene structure |
| 3 | `U3_P1_Gene_Finding` | ORFs and prediction accuracy on a 20 kb contig | `U3_Q1_Gene_Finding` | ORF vs gene, gene-finder signals, sensitivity and specificity |
| 3 | `U3_P2_Function_and_Comparison` | Assign functions and GO terms to ten genes; shared/unique genes for a second genome pair | `U3_Q2_Function_and_Comparative_Genomics` | Orthologue vs paralogue, GO aspects and evidence codes, synteny |
| 2 | `U2_P_Proteomics` | Place ten proteins on the virtual gel; identify two unknowns from peak lists | `U2_Q_Proteomics` | 2D-PAGE axes, ionisation and analyser types, PMF logic, m/z arithmetic |
| 4 | `U4_P_Expression_Profiling` | Differential expression on a second dataset; interpret the top genes | `U4_Q_Expression_Profiling` | Profiling methods, fold change, reading a volcano plot and a heat map |

**Count:** 12 course, 5 practice, 5 quiz notebooks, plus 5 practice solutions and 5 quiz keys.

`U3_P1` doubles as a dry run for Assignment 1 (annotate a contig), so use a different contig from any assignment sequence.

### Extra data these notebooks need

Add to `data/` (and to the checklist in §9): a genome size and gene count table with sources; saved GC-skew table for *E. coli*; GLIMMER output and RefSeq feature tables for lambda and *E. coli*; BLAST tabular results (predicted proteins vs Swiss-Prot subset; K-12 vs O157:H7 in both directions); a GO annotation extract for *E. coli*; a FASTA of ~200 *E. coli* proteins for the virtual gel; two peak lists with known answers; one or two GEO expression tables trimmed to a few thousand genes.

### Build order

1. Unit 1 and Unit 3 notebooks before week 1, since they cover weeks 1–8 in the teaching order.
2. For each unit: course notebooks → practice solution → practice student copy → quiz key → quiz student copy.
3. Unit 2 and Unit 4 notebooks before week 9.
4. Generate every saved input file by actually running the matching practical once on the lab image; record the tool version and date in `data/README.md`.

### Progress tracker

| Unit | C | P | P solutions | Q | Q key |
|---|---|---|---|---|---|
| 1 | ☐ ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
| 3 | ☐ ☐ ☐ ☐ ☐ | ☐ ☐ | ☐ ☐ | ☐ ☐ | ☐ ☐ |
| 2 | ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
| 4 | ☐ ☐ | ☐ | ☐ | ☐ | ☐ |
