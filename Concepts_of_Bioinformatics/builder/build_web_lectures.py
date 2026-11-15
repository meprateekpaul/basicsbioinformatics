#!/usr/bin/env python3
"""
build_web_lectures.py - Generate structured lecture, slide, and notes data
for in-browser presentation and reading in Concepts of Bioinformatics web portal.
"""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LECTURES_DIR = REPO_ROOT / "lectures"
JS_DIR = REPO_ROOT / "js"
JS_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = JS_DIR / "lectures_data.js"
EXTERNAL_OUT_FILE = REPO_ROOT.parents[0] / "meprateekpaul.github.io" / "js" / "cbbi_lectures_data.js"

NOTEBOOK_MAPPING = {
    1: "notebooks/U01_Bioinformatics_and_Internet/U01_C1_Sequences_as_Text.ipynb",
    2: "notebooks/U01_Bioinformatics_and_Internet/U01_C1_Sequences_as_Text.ipynb",
    3: "notebooks/U02_Information_Retrieval/U02_C1_Entrez_Search_from_Python.ipynb",
    4: "notebooks/U02_Information_Retrieval/U02_C1_Entrez_Search_from_Python.ipynb",
    5: "notebooks/U03_NCBI_Data_Model/U03_C1_Inside_a_Sequence_Record.ipynb",
    6: "notebooks/U03_NCBI_Data_Model/U03_C1_Inside_a_Sequence_Record.ipynb",
    7: "notebooks/U04_GenBank_Database/U04_C1_GenBank_Flat_File.ipynb",
    8: "notebooks/U04_GenBank_Database/U04_C1_GenBank_Flat_File.ipynb",
    9: "notebooks/U04_GenBank_Database/U04_C2_Formats_and_Conversion.ipynb",
    10: "notebooks/U05_Sequence_Alignment/U05_C1_Dot_Plots_and_Global_Alignment.ipynb",
    11: "notebooks/U05_Sequence_Alignment/U05_C1_Dot_Plots_and_Global_Alignment.ipynb",
    12: "notebooks/U05_Sequence_Alignment/U05_C2_Local_Alignment_and_Scoring.ipynb",
    13: "notebooks/U05_Sequence_Alignment/U05_C2_Local_Alignment_and_Scoring.ipynb",
    14: "notebooks/U05_Sequence_Alignment/U05_C3_Reading_BLAST_Results.ipynb",
    15: "notebooks/U05_Sequence_Alignment/U05_C3_Reading_BLAST_Results.ipynb",
    16: "notebooks/U06_Multiple_Sequence_Alignment/U06_C1_Multiple_Alignment_and_Conservation.ipynb",
    17: "notebooks/U06_Multiple_Sequence_Alignment/U06_C1_Multiple_Alignment_and_Conservation.ipynb",
    18: "notebooks/U07_Phylogenetic_Analysis/U07_C1_Distances_and_Trees.ipynb",
    19: "notebooks/U07_Phylogenetic_Analysis/U07_C1_Distances_and_Trees.ipynb",
    20: "notebooks/U07_Phylogenetic_Analysis/U07_C1_Distances_and_Trees.ipynb",
    21: "notebooks/U08_Predictive_Nucleotide/U08_C1_ORFs_GC_and_Codon_Usage.ipynb",
    22: "notebooks/U08_Predictive_Nucleotide/U08_C1_ORFs_GC_and_Codon_Usage.ipynb",
    23: "notebooks/U09_Predictive_Protein/U09_C1_Protein_Properties_and_Motifs.ipynb",
    24: "notebooks/U09_Predictive_Protein/U09_C1_Protein_Properties_and_Motifs.ipynb",
    25: "notebooks/U09_Predictive_Protein/U09_C2_Secondary_Structure_Prediction_Scoring.ipynb",
    26: "notebooks/U10_Structure_Databases/U10_C1_Reading_a_PDB_File.ipynb",
    27: "notebooks/U10_Structure_Databases/U10_C1_Reading_a_PDB_File.ipynb",
    28: "notebooks/U10_Structure_Databases/U10_C1_Reading_a_PDB_File.ipynb",
    29: "notebooks/U11_Comparative_Genomics/U11_C1_Comparing_Two_Genomes.ipynb",
    30: "notebooks/U11_Comparative_Genomics/U11_C1_Comparing_Two_Genomes.ipynb",
}


def build_lectures():
    files = sorted([f for f in LECTURES_DIR.glob("**/*.md") if not f.name.startswith(".")])
    print(f"Processing {len(files)} lecture files...")

    lectures = []
    for f in files:
        txt = f.read_text(encoding="utf-8")

        # Lecture Title & ID
        m_title = re.search(r"^#\s+Lecture\s+(\d+)\s+[—\-:]\s+(.+)$", txt, re.M)
        lec_num = int(m_title.group(1)) if m_title else int(re.search(r"L(\d+)", f.name).group(1))
        lec_title = m_title.group(2).strip() if m_title else f.stem
        lec_id = f"L{str(lec_num).zfill(2)}"

        # Unit
        m_unit = re.search(r"\*\*Unit\s+(\d+):\*\*\s*(.+)", txt)
        unit_num = int(m_unit.group(1)) if m_unit else 1
        unit_name = m_unit.group(2).strip() if m_unit else ""

        # LO
        m_lo = re.search(r"\*\*Primary Learning Outcome:\*\*\s*(.+)", txt)
        lo = m_lo.group(1).strip() if m_lo else ""

        # Syllabus Topic
        m_topic = re.search(r"\*\*Syllabus Topic:\*\*\s*(.+)", txt)
        syllabus_topic = m_topic.group(1).strip() if m_topic else ""

        # Slides parsing
        slides = []
        slide_matches = list(re.finditer(r"SLIDE\s+(\d+):\s*([^\n]+)\n=+\n(.*?)(?=(?:SLIDE\s+\d+:|```|$))", txt, re.S))
        for sm in slide_matches:
            s_num = int(sm.group(1))
            s_title = sm.group(2).strip()
            s_body = sm.group(3).strip()

            # Separate speaker notes if present
            parts = re.split(r"Speaker Bullets:|Speaker Notes:", s_body, flags=re.I)
            slide_main = parts[0].strip()
            speaker_notes = parts[1].strip() if len(parts) > 1 else ""

            slides.append({
                "num": s_num,
                "title": s_title,
                "content": slide_main,
                "speaker_notes": speaker_notes
            })

        # Notes markdown (from ## Detailed Comprehensive Technical Notes onward)
        notes_split = re.split(r"##\s+Detailed\s+Comprehensive\s+Technical\s+Notes", txt, maxsplit=1)
        if len(notes_split) > 1:
            notes_md = "## Detailed Comprehensive Technical Notes" + notes_split[1]
        else:
            notes_md = txt

        rel_path = f.relative_to(REPO_ROOT).as_posix()
        companion_nb = NOTEBOOK_MAPPING.get(lec_num, "")

        lectures.append({
            "id": lec_id,
            "num": lec_num,
            "title": lec_title,
            "unit": unit_num,
            "unit_name": unit_name,
            "lo": lo,
            "syllabus_topic": syllabus_topic,
            "slide_count": len(slides),
            "slides": slides,
            "notes_md": notes_md,
            "rel_path": rel_path,
            "notebook_path": companion_nb
        })

    # Sort strictly by lecture number
    lectures.sort(key=lambda x: x["num"])

    # Write JS bundle
    js_content = f"// Concepts of Bioinformatics (CBBI-501) - Lecture Slides & Notes Registry\n"
    js_content += f"// Generated automatically from authentic Markdown files in lectures/\n"
    js_content += f"window.CBBI_LECTURES = {json.dumps(lectures, indent=2)};\n"

    OUT_FILE.write_text(js_content, encoding="utf-8")
    print(f"✓ Written {len(lectures)} lectures to {OUT_FILE} ({len(js_content):,} bytes)")

    if EXTERNAL_OUT_FILE.parent.exists():
        EXTERNAL_OUT_FILE.write_text(js_content, encoding="utf-8")
        print(f"✓ Written copy to {EXTERNAL_OUT_FILE}")

    return len(lectures)


if __name__ == "__main__":
    build_lectures()
