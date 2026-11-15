# Data Provenance and Descriptions

This directory contains biological sequences, flat files, alignments, structures, genomes, and saved server outputs for the **Concepts of Bioinformatics (CBBI-501)** curriculum.

---

## Directory Inventory

### 1. `sequences/`
- `hbb_human_mrna.fasta`: Human hemoglobin subunit beta (*HBB*) mRNA (`NM_000518.5`, 626 bp).
- `hbb_human_cds.fasta`: *HBB* coding sequence (`NM_000518.5:51-494`, 444 bp).
- `hbb_human_protein.fasta`: *HBB* mature beta-globin chain (`NP_000509.1` / UniProt `P68871`, 147 aa).
- `hbs_human_protein.fasta`: Sickle-cell variant Glu6Val (E6V, HbS).
- `ins_human_mrna.fasta`: Human insulin (*INS*) mRNA (`NM_000207.3`, 469 bp).
- `ins_human_protein.fasta`: Human insulin preproprotein (`NP_000198.1` / UniProt `P01308`, 110 aa).
- `tp53_human_mrna.fasta`: Human tumor protein p53 (*TP53*) mRNA (`NM_000546.6`).
- `tp53_human_protein.fasta`: Human p53 isoform a (`NP_000537.3` / UniProt `P04637`, 393 aa).
- `globin_family_proteins.fasta`: Human globin family members (HBA1, HBB, HBD, HBG1, MB, NGB, CYGB).
- `hbb_vertebrate_orthologues.fasta`: HBB protein orthologues from 9 vertebrate species (Human, Chimpanzee, Gorilla, Rhesus macaque, Mouse, Rat, Cattle, Chicken, Zebrafish).
- `toy_sequences.fasta`: Short benchmark sequences for hand calculation of Needleman-Wunsch and Smith-Waterman matrices.

### 2. `genbank/`
- `hbb_human.gb`: Complete GenBank flat file record for `NM_000518.5`, containing LOCUS, DEFINITION, ACCESSION, VERSION, SOURCE, REFERENCE, FEATURES (source, gene, exon, CDS, misc_feature), and ORIGIN.

### 3. `structures/`
- `1a3n.pdb`: Crystal structure of human adult deoxyhemoglobin (2.0 Å resolution, T-state quaternary conformation).
- `4hhb.pdb`: High-resolution human deoxyhemoglobin (1.74 Å resolution).
- `2hbs.pdb`: Sickle-cell hemoglobin (HbS) fiber polymer structure showing Val6 hydrophobic contact.

### 4. `alignments/`
- `globin_family.aln`: Multiple sequence alignment of 7 human globin family members in standard Clustal format.

### 5. `genomes/`
- `phix174.fasta`: Bacteriophage phiX174 circular single-stranded DNA genome (`NC_001422.1`, 5386 bp).

### 6. `expected/`
Offline reference outputs for web practicals and notebooks when servers are slow or disconnected:
- `blast_hbb_vs_refseq.tsv`: Tabular BLASTP search results for human HBB against NCBI RefSeq protein database.
- `gor4_hbb_secondary_structure.txt`: GOR IV secondary structure prediction string for HBB.
- `psipred_hbb_secondary_structure.txt`: PSIPRED secondary structure prediction string for HBB.
- `dssp_hbb_1a3n.txt`: Crystallographic DSSP secondary structure assignment from 1A3N chain B.
