# Basics of Bioinformatics (CBBI Curricula)

[![SHUATS Inspired](https://img.shields.io/badge/Academic%20Inspiration-SHUATS%20B.Tech.%20Bioinformatics-7c3aed.svg)](https://shuats.edu.in/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Notebooks: 59](https://img.shields.io/badge/Jupyter%20Notebooks-59%20Tested-cyan.svg)](Concepts_of_Bioinformatics/notebooks/)
[![Slides: 240](https://img.shields.io/badge/Interactive%20Slides-240%20Decks-violet.svg)](https://meprateekpaul.github.io/conceptsbio.html#lectures)

Comprehensive undergraduate and graduate university curricula in computational biology, sequence analysis, structural bioinformatics, molecular dynamics, immunoinformatics, and precision genomics.

---

## Academic Framework & Institutional Provenance

This multi-course curriculum repository is inspired by and adapted from the official undergraduate **Bachelor of Technology (B.Tech.) in Bioinformatics** degree outline of the:

> **Department of Computational Biology & Bioinformatics**  
> Jacob Institute of Biotechnology & Bioengineering (JSBB)  
> **[Sam Higginbottom University of Agriculture, Technology and Sciences (SHUATS)](https://shuats.edu.in/)**  
> *(Formerly Allahabad Agricultural Institute / SHIATS)*  
> Prayagraj (Allahabad), Uttar Pradesh, India.

Official syllabus source specifications are documented in [SYLLABUS.md](SYLLABUS.md).

---

## Curricula Directory (Folderwise Course Structure)

Every course is organized into its own dedicated folder containing complete theory lecture notes, laboratory practical sheets, interactive Jupyter notebooks with automated assert checks, assessment banks, and reference datasets:

| Semester | Code | Folder / Course Title | Credits | Status | Highlights |
|:---:|:---:|:---|:---:|:---:|:---|
| **Sem II** | `CBBI-501` | [**Concepts_of_Bioinformatics/**](Concepts_of_Bioinformatics/)<br>• [30 Theory Notes](Concepts_of_Bioinformatics/lectures/)<br>• [30 Slide Decks](Concepts_of_Bioinformatics/slides/)<br>• [59 Notebooks](Concepts_of_Bioinformatics/notebooks/)<br>• [15 Practicals](Concepts_of_Bioinformatics/practicals/)<br>• [Interactive Portal](https://meprateekpaul.github.io/conceptsbio.html) | **3 (2-0-1)** | **100% COMPLETE & VERIFIED** | **30 Lectures**, **15 Practicals**, **59 Jupyter Notebooks**, **25 Assessment Suites**, **240 Interactive In-Browser Slides & Notes**, Capstone Mini-Project, and Central *HBB* Thread. |
| **Sem III** | `CBBI-504` | [**Basics_of_Genomics_and_Proteomics/**](Basics_of_Genomics_and_Proteomics/) | **3 (2-0-1)** | **Course Plan Ready** | 30 Lectures across 4 Units, 10 Practicals, 2D-PAGE, Mass Spectrometry, Gene Finding, Synteny, and Expression Profiling. |
| **Sem IV** | `CBBI-507` | [**Computational_Analysis_of_Biomolecules/**](Computational_Analysis_of_Biomolecules/) | **4 (2-0-2)** | **Planned** | Force fields, energy minimization, Monte Carlo & MD simulations, and AutoDock virtual screening. |
| **Sem IV** | `CBBI-510` | [**Immunoinformatics/**](Immunoinformatics/) | **3 (2-0-1)** | **Planned** | MHC-peptide binding prediction (NetMHCpan), B/T-cell epitope mapping, and reverse vaccinology. |
| **Sem V** | `CBBI-508` | [**Biological_Databases/**](Biological_Databases/) | **4 (2-0-2)** | **Planned** | Relational SQL database design, NoSQL/graph biological networks (Neo4j), and RESTful APIs. |
| **Sem V** | `CBBI-602` | [**Molecular_Structure_Prediction/**](Molecular_Structure_Prediction/) | **4 (2-0-2)** | **Planned** | Homology modeling, threading, ab initio modeling, and AlphaFold / ESMFold architectures. |
| **Sem V** | `CBBI-604` | [**Phyloinformatics/**](Phyloinformatics/) | **4 (2-1-1)** | **Planned** | Maximum Likelihood (IQ-TREE/RAxML), Bayesian MCMC (BEAST/MrBayes), and molecular clocks. |
| **Sem VI** | `CBBI-615` | [**Next_Generation_Sequencing/**](Next_Generation_Sequencing/) | **4 (2-0-2)** | **Planned** | FASTQ QC, BWA/Minimap2 alignment, GATK variant calling, and DESeq2 differential expression. |
| **Sem VI** | `CBBI-616` | [**Machine_Learning_in_Bioinformatics/**](Machine_Learning_in_Bioinformatics/) | **3 (3-0-0)** | **Planned** | Supervised/unsupervised sequence learning, Random Forests, SVMs, GNNs, and ESM protein language models. |
| **Sem VII** | `CBBI-611` | [**Metabolic_Network_Analysis/**](Metabolic_Network_Analysis/) | **4 (2-0-2)** | **Planned** | Genome-scale metabolic reconstructions, stoichiometric modeling, and Flux Balance Analysis (COBRApy). |
| **Sem VII** | `CBBI-612` | [**Clinical_Bioinformatics/**](Clinical_Bioinformatics/) | **4 (2-0-2)** | **Planned** | Translational genomics, ACMG/AMP clinical variant interpretation, pharmacogenomics, and oncology panels. |
| **Sem VII** | `CBBI-614` | [**Computational_Drug_Designing/**](Computational_Drug_Designing/) | **4 (2-0-2)** | **Planned** | Structure- and ligand-based CADD, pharmacophore modeling, QSAR, and ADMET profiling. |

---

## Pedagogical Philosophy & Quality Standards

1. **Biological Reality Over Toy Examples:** All algorithms and code exercises run on real macromolecular targets (human $\beta$-globin *HBB*, sickle-cell variant HbS, insulin *INS*, tumor suppressor *TP53*, bacteriophage $\Phi\text{X174}$, polyomaviruses SV40/BKV).
2. **Offline First:** All web service queries (Entrez, UniProt, RCSB PDB) have pre-saved local fallbacks in `data/expected/` so exercises execute reliably without requiring external network connectivity.
3. **Automated Verification:** All Jupyter notebooks adhere to [NOTEBOOK_GUIDE.md](NOTEBOOK_GUIDE.md) and feature unit self-check assertions (`assert`) with cryptographic SHA-256 quiz scoring.
4. **Interactive In-Browser Learning:** The course portal includes full presentation slide carousels (240 slides) with keyboard navigation and instant markdown study notes reader.

---

## Web Course Portals

- **Concepts of Bioinformatics (CBBI-501) Web Portal:**  
  [https://meprateekpaul.github.io/conceptsbio.html](https://meprateekpaul.github.io/conceptsbio.html)
- **Master Course Catalog:**  
  [https://meprateekpaul.github.io/courses.html](https://meprateekpaul.github.io/courses.html)
- **Programming for Computational Biology (PCB-101):**  
  [https://meprateekpaul.github.io/programmingcb.html](https://meprateekpaul.github.io/programmingcb.html)
- **Practical Cheminformatics & CADD (CHEM-501):**  
  [https://meprateekpaul.github.io/cheminformatics.html](https://meprateekpaul.github.io/cheminformatics.html)

---

## License

Distributed under the **MIT License**. Created and maintained by [Prateek Paul](https://meprateekpaul.github.io/).
