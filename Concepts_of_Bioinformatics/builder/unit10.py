"""
unit10.py - Builder for Unit 10: Structure Databases
Notebooks:
- U10_C1_Reading_a_PDB_File.ipynb
- U10_P_PDB_Structures.ipynb
- solutions/U10_P_PDB_Structures_Solutions.ipynb
- U10_Q_Structure_Databases.ipynb
- solutions/U10_Q_Structure_Databases_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U10_Structure_Databases"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u10_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U10_C1",
        title="Reading a PDB File",
        unit_num=10,
        unit_title="Structure Databases",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L26–L27, Practicals S12–S13 (PDB & VMD)",
        before_this="U09_C2"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Navigate** the Structure-Model-Chain-Residue-Atom (SMCRA) object hierarchy in Biopython's `Bio.PDB` [LO7].
- **Differentiate** standard polymer amino acid records (`ATOM`) from non-polymer heteroatoms/ligands (`HETATM`) [LO7].
- **Extract** 3D Cartesian coordinates $(x, y, z)$ and compute Euclidean distances between functional atoms [LO7].
- **Locate** the haem-binding pocket and measure the coordination distance between proximal His92 and the iron atom [LO7].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Human adult hemoglobin is a heterotetramer ($\\alpha_2\\beta_2$) containing four heme groups. Each heme group binds one molecule of oxygen ($O_2$) reversibly at an iron (Fe) atom coordinated by a conserved proximal histidine residue. By inspecting the 2.0 Å X-ray crystal structure of deoxyhemoglobin (PDB `1A3N`), how do we navigate chains A, B, C, D, extract 3D coordinates, and verify the physical distance between His92 and the iron atom?
"""))

    nb.cells.append(make_setup_cell("U10_C1"))

    # Concept 1: SMCRA Hierarchy
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: The SMCRA Data Hierarchy
### Theory
Biopython structures macromolecular crystallographic models using the **SMCRA** object architecture:
- **`Structure`**: The entire entry (e.g. PDB ID `1A3N`).
- **`Model`**: An individual conformational state (X-ray structures typically contain 1 model, index 0; NMR entries contain an ensemble of 10–30 models).
- **`Chain`**: An individual polypeptide or nucleic acid macromolecule (e.g. Chain A, B, C, D in hemoglobin).
- **`Residue`**: An individual amino acid or hetero group. Identified by a tuple `(' ', res_number, insertion_code)`.
- **`Atom`**: An individual atomic center storing 3D coordinates $(x, y, z)$, B-factor (temperature factor), and occupancy.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Parsing 1A3N with Bio.PDB
from Bio.PDB import PDBParser
import numpy as np

parser = PDBParser(QUIET=True)
pdb_path = DATA_DIR / "structures" / "1a3n.pdb"
structure = parser.get_structure("1A3N", pdb_path)

model = structure[0]
chains = list(model.get_chains())
chain_ids = [c.id for c in chains]

print("=== PDB Structure: 1A3N (Human Deoxyhemoglobin) ===")
print("Header Title:", structure.header.get("name", "Deoxyhemoglobin"))
print("Resolution:  ", structure.header.get("resolution", 2.0), "Å")
print(f"Number of Chains in Model 0: {len(chains)} ({chain_ids})")
'''))

    # Concept 2: ATOM vs HETATM
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: ATOM vs. HETATM Records
### Theory
The PDB flat file distinguishes standard biological residues from non-standard components:
- **`ATOM`**: Standard amino acid or nucleotide residues that form the covalently bonded polymer chain. In Biopython residue ID: `id[0] == ' '`.
- **`HETATM`**: Hetero-atoms, including prosthetic groups (haem `HEM`), cofactors, crystallographic waters (`HOH`), and small-molecule drugs. In Biopython: `id[0].startswith('H_')` or `'W'`.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Inspecting Chain B and finding the Haem Ligand
chain_b = model["B"]

amino_acids = [r for r in chain_b if r.id[0] == " "]
hetero_groups = [r for r in chain_b if r.id[0] != " "]

print(f"Chain B (Beta globin):")
print(f"  Standard amino acid residues: {len(amino_acids)}")
print(f"  Hetero residues (HETATM):     {len(hetero_groups)}")

# Locate the haem prosthetic group
haem_res = next(r for r in hetero_groups if r.resname == "HEM")
print("\\nHaem Prosthetic Group Details:")
print("  Residue Name: ", haem_res.resname)
print("  Residue ID:   ", haem_res.id)
print("  Number of Atoms in Haem:", len(haem_res))

fe_atom = haem_res["FE"]
print(f"  Iron Atom Coordinates: x={fe_atom.coord[0]:.3f}, y={fe_atom.coord[1]:.3f}, z={fe_atom.coord[2]:.3f}")
'''))

    # Concept 3: 3D Distance Calculation
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: Measuring Physical 3D Distances
### Theory
In structural biophysics, the distance between two atoms $A$ and $B$ with coordinates $(x_1, y_1, z_1)$ and $(x_2, y_2, z_2)$ is the 3D Euclidean distance:
$$d(A, B) = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$$
In Biopython, subtracting two `Atom` objects (`atomA - atomB`) automatically computes this Euclidean distance in Angstroms (Å)!
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Measuring proximal His92 coordination distance
# Residue 92 in chain B is the proximal histidine
his92 = chain_b[92]
print("Residue 92 Name:", his92.resname)

# NE2 is the epsilon-nitrogen that coordinates the Fe atom
ne2_atom = his92["NE2"]
coord_distance = ne2_atom - fe_atom

print(f"His92 NE2 Coordinates: {ne2_atom.coord}")
print(f"Haem Fe Coordinates:   {fe_atom.coord}")
print(f"Physical Coordination Distance (NE2 - Fe): {coord_distance:.2f} Å")
print("Physiological covalent coordination bond distance is typically ~2.1 - 2.3 Å!")
'''))

    # Concept 4: Haem Binding Pocket
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Concept 4: Mapping the Haem Pocket
### Theory
Any residue with an atom within $4.5$ Å of the haem group constitutes part of the haem-binding pocket that stabilizes the porphyrin ring through hydrophobic packing.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Identifying residues in the haem pocket within 4.5 Å
pocket_residues = set()

for res in amino_acids:
    for atom_res in res:
        for atom_haem in haem_res:
            if (atom_res - atom_haem) < 4.5:
                pocket_residues.add((res.id[1], res.resname))
                break

print(f"Found {len(pocket_residues)} amino acids in Chain B within 4.5 Å of the haem group:")
for res_num, res_name in sorted(pocket_residues):
    print(f"  Residue {res_num:3}: {res_name}")
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Summary
- `Bio.PDB.PDBParser` constructs a hierarchical SMCRA tree (Structure, Model, Chain, Residue, Atom).
- `ATOM` records define standard protein residues; `HETATM` records define ligands, cofactors, and waters.
- Subtracting two atoms (`atomA - atomB`) returns Euclidean distance in Angstroms.
- Proximal His92 directly coordinates the haem iron atom at $\\approx 2.26$ Å in 1A3N.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 8. Next Steps
- Analyze sickle-cell hemoglobin (2HBS) in `U10_P_PDB_Structures.ipynb`.
- Self-test structure database concepts in `U10_Q_Structure_Databases.ipynb`.
"""))

    return nb


def build_u10_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 10.1",
            stars="★☆☆",
            title="Load 1A3N and report chain identifiers",
            biology="Hemoglobin A is a heterotetramer composed of two alpha and two beta chains.",
            task="Load `data/structures/1a3n.pdb` using `PDBParser(QUIET=True)`. Extract the chain IDs from model 0 into a list `chains_1a3n`.",
            expected="`chains_1a3n` as list `['A', 'B', 'C', 'D']`.",
            student_code="""# TODO: replace the ... with your code
from Bio.PDB import PDBParser

parser = PDBParser(QUIET=True)
struct = parser.get_structure("1A3N", DATA_DIR / "structures" / "1a3n.pdb")
model = struct[0]

chains_1a3n = ...
""",
            solution_code="""from Bio.PDB import PDBParser

parser = PDBParser(QUIET=True)
struct = parser.get_structure("1A3N", DATA_DIR / "structures" / "1a3n.pdb")
model = struct[0]

chains_1a3n = [c.id for c in model.get_chains()]
""",
            check_code="""# Check — do not edit
assert len(chains_1a3n) == 4, f"Expected 4 chains, got {len(chains_1a3n)}"
assert set(chains_1a3n) == {"A", "B", "C", "D"}
print("Ex 10.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.2",
            stars="★☆☆",
            title="Inspect residue 6 in normal adult hemoglobin (1A3N)",
            biology="In wild-type hemoglobin beta (HbA), residue 6 is a negatively charged glutamic acid (GLU).",
            task="Extract residue 6 from Chain B of 1A3N. Store its 3-letter residue name in `res6_1a3n_name`.",
            expected="`res6_1a3n_name` == 'GLU'.",
            student_code="""# TODO: replace the ... with your code
chain_b = model["B"]
res6 = chain_b[6]
res6_1a3n_name = ...
""",
            solution_code="""chain_b = model["B"]
res6 = chain_b[6]
res6_1a3n_name = res6.resname
""",
            check_code="""# Check — do not edit
assert res6_1a3n_name == "GLU", f"Expected GLU, got {res6_1a3n_name}"
print("Ex 10.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.3",
            stars="★☆☆",
            title="Inspect residue 6 in sickle-cell hemoglobin (2HBS)",
            biology="In sickle-cell hemoglobin (HbS), residue 6 is mutated to a hydrophobic valine (VAL).",
            task="Load `data/structures/2hbs.pdb`. Extract residue 6 from Chain B of model 0. Store its 3-letter residue name in `res6_2hbs_name`.",
            expected="`res6_2hbs_name` == 'VAL'.",
            student_code="""# TODO: replace the ... with your code
struct_2hbs = parser.get_structure("2HBS", DATA_DIR / "structures" / "2hbs.pdb")
res6_hbs = struct_2hbs[0]["B"][6]
res6_2hbs_name = ...
""",
            solution_code="""struct_2hbs = parser.get_structure("2HBS", DATA_DIR / "structures" / "2hbs.pdb")
res6_hbs = struct_2hbs[0]["B"][6]
res6_2hbs_name = res6_hbs.resname
""",
            check_code="""# Check — do not edit
assert res6_2hbs_name == "VAL", f"Expected VAL in sickle-cell structure, got {res6_2hbs_name}"
print("Ex 10.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.4",
            stars="★★☆",
            title="Extract alpha-carbon (CA) coordinates of residue 6",
            biology="The alpha-carbon defines the backbone trace of the protein.",
            task="Extract the 3D coordinate vector of the `'CA'` atom from `res6_hbs` (Val6 in 2HBS) into variable `ca_coords`. Verify it is a NumPy array of length 3.",
            expected="`ca_coords` as a 1D NumPy array with 3 coordinates.",
            student_code="""# TODO: replace the ... with your code
ca_atom = res6_hbs["CA"]
ca_coords = ...
""",
            solution_code="""ca_atom = res6_hbs["CA"]
ca_coords = ca_atom.coord
""",
            check_code="""# Check — do not edit
import numpy as np
assert isinstance(ca_coords, np.ndarray), "Coordinates must be a NumPy array"
assert ca_coords.shape == (3,), f"Expected shape (3,), got {ca_coords.shape}"
print("Ex 10.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.5",
            stars="★★☆",
            title="Calculate Euclidean distance between proximal His and haem iron in 1A3N",
            biology="The iron atom must be held close to the proximal histidine to allow reversible oxygen coordination.",
            task="In 1A3N Chain B, locate proximal `his92 = chain_b[92]` and the haem residue `haem_res`. Calculate the distance in Angstroms between `his92['NE2']` and `haem_res['FE']` into float variable `fe_his_dist`.",
            expected="`fe_his_dist` as float between 2.1 and 2.4 Å.",
            student_code="""# TODO: replace the ... with your code
haem_res = next(r for r in chain_b if r.resname == "HEM")
fe_atom = haem_res["FE"]
his92 = chain_b[92]
ne2_atom = his92["NE2"]

fe_his_dist = ...
""",
            solution_code="""haem_res = next(r for r in chain_b if r.resname == "HEM")
fe_atom = haem_res["FE"]
his92 = chain_b[92]
ne2_atom = his92["NE2"]

fe_his_dist = round(float(ne2_atom - fe_atom), 2)
""",
            check_code="""# Check — do not edit
assert 2.1 <= fe_his_dist <= 2.4, f"Expected coordination distance ~2.26 Å, got {fe_his_dist}"
print("Ex 10.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.6",
            stars="★★☆",
            title="Calculate mean B-factor for Chain B in 1A3N",
            biology="Crystallographic B-factors (temperature factors) reflect local atomic flexibility and thermal motion.",
            task="Iterate over all atoms in standard amino acid residues of Chain B in 1A3N. Compute the average B-factor across all atoms and store in `mean_bfactor` as a float rounded to 2 decimal places.",
            expected="`mean_bfactor` between 15.0 and 45.0.",
            student_code="""# TODO: replace the ... with your code
b_factors = []
for res in chain_b:
    if res.id[0] == " ":
        for atom in res:
            ...

mean_bfactor = ...
""",
            solution_code="""b_factors = []
for res in chain_b:
    if res.id[0] == " ":
        for atom in res:
            b_factors.append(atom.get_bfactor())

mean_bfactor = round(sum(b_factors) / len(b_factors), 2)
""",
            check_code="""# Check — do not edit
assert isinstance(mean_bfactor, float)
assert 15.0 <= mean_bfactor <= 45.0, f"Expected mean B-factor in range 15-45, got {mean_bfactor}"
print("Ex 10.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 10.7",
            stars="★★★",
            title="Find all alpha-carbons within 10 Å of Val6 in 2HBS",
            biology="Measuring spatial neighbor density around the sickle-cell contact mutation site.",
            task="In 2HBS model 0, find all CA atoms from other residues in Chain B located within 10.0 Å of `res6_hbs['CA']`. Store the count of such neighboring residues in `num_neighbors`.",
            expected="`num_neighbors` as integer between 2 and 20.",
            student_code="""# TODO: replace the ... with your code
chain_b_hbs = struct_2hbs[0]["B"]
val6_ca = res6_hbs["CA"]
num_neighbors = 0

for res in chain_b_hbs:
    if res.id[0] == " " and res.id[1] != 6:
        if "CA" in res:
            ...
""",
            solution_code="""chain_b_hbs = struct_2hbs[0]["B"]
val6_ca = res6_hbs["CA"]
num_neighbors = 0

for res in chain_b_hbs:
    if res.id[0] == " " and res.id[1] != 6:
        if "CA" in res:
            d = res["CA"] - val6_ca
            if d < 10.0:
                num_neighbors += 1
""",
            check_code="""# Check — do not edit
assert 2 <= num_neighbors <= 20, f"Expected 2-20 neighbors within 10 Å, got {num_neighbors}"
print("Ex 10.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U10_P",
        title="PDB Structures — Exercises",
        unit_num=10,
        unit_title="Structure Databases",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L26–L28, Practicals S12–S13",
        before_this="U10_C1"
    ))
    nb_student.cells.append(make_setup_cell("U10_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U10_P",
        title="PDB Structures — Solutions",
        unit_num=10,
        unit_title="Structure Databases",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L26–L28, Practicals S12–S13",
        before_this="U10_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U10_P"))
    
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
1. How does the SMCRA hierarchy in Biopython reflect the experimental reality of macromolecular X-ray crystallography?
2. What does a high B-factor (temperature factor) indicate about a region of a protein crystal structure compared to a low B-factor?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u10_q():
    salt = "U10_Q"
    questions = [
        QuizQuestion("q1", "What does the SMCRA acronym stand for in Biopython's macromolecular structural data model?",
                     ["(a) Sequence, Molecule, Codon, Residue, Atom", "(b) Structure, Model, Chain, Residue, Atom", "(c) Subunit, Macromolecule, Coordinate, Ribosome, Assembly", "(d) System, Method, Calculation, Resolution, Area"],
                     "b", "U10_C1 §3"),
        QuizQuestion("q2", "In a standard PDB format file, which record type holds non-polymer ligand, water, or cofactor atoms?",
                     ["(a) ATOM", "(b) HETATM", "(c) SEQRES", "(d) CONECT"],
                     "b", "U10_C1 §4"),
        QuizQuestion("q3", "In protein crystallography, which numerical value represents a higher quality, more detailed structure?",
                     ["(a) 3.5 Å resolution", "(b) 1.5 Å resolution", "(c) High R-free factor", "(d) High B-factor"],
                     "b", "U10_C1 §3"),
        QuizQuestion("q4", "What does the crystallographic B-factor (temperature factor) measure for an atom?",
                     ["(a) Covalent bond strength", "(b) Thermal vibration and static positional disorder", "(c) Partial electrical charge", "(d) Hydrophobic volume"],
                     "b", "U10_P §Ex 10.6"),
        QuizQuestion("q5", "In human hemoglobin (PDB 1A3N), which specific atom in the haem group coordinates the proximal histidine residue?",
                     ["(a) Oxygen (O2)", "(b) Iron (FE)", "(c) Magnesium (MG)", "(d) Carbon (CA)"],
                     "b", "U10_C1 §5"),
        QuizQuestion("q6", "In Biopython, what does subtracting two Atom objects (`atom1 - atom2`) calculate?",
                     ["(a) A new vector difference", "(b) The 3D Euclidean distance in Angstroms", "(c) The bond angle", "(d) The difference in B-factor"],
                     "b", "U10_C1 §5"),
        QuizQuestion("q7", "Which amino acid substitution is present at residue 6 in the beta chain of sickle-cell hemoglobin (PDB 2HBS)?",
                     ["(a) Glu -> Lys", "(b) Glu -> Val", "(c) Val -> Ala", "(d) His -> Tyr"],
                     "b", "U10_P §Ex 10.3"),
        QuizQuestion("q8", "What standard metric measures the structural similarity between two superimposed protein structures based on atomic coordinates?",
                     ["(a) E-value", "(b) RMSD (Root Mean Square Deviation)", "(c) Bit score", "(d) Q3"],
                     "b", "U10_C1 §1"),
        QuizQuestion("q9", "Why is protein 3D structure generally more conserved during evolution than primary amino acid sequence?",
                     ["(a) Structure is not subject to natural selection", "(b) Secondary and tertiary folds can tolerate many neutral sequence mutations that maintain the same overall shape and function", "(c) DNA codons do not affect structure", "(d) AlphaFold enforces structure conservation"],
                     "b", "U10_C1 §1"),
        QuizQuestion("q10", "What organization oversees the deposition and standardization of macromolecular structure data globally?",
                     ["(a) INSDC", "(b) wwPDB (Worldwide Protein Data Bank)", "(c) Expasy", "(d) Ensembl"],
                     "b", "U10_C1 §3")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U10_Q",
        title="Structure Databases — Quiz",
        unit_num=10,
        unit_title="Structure Databases",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L26–L28, Practicals S12–S13",
        before_this="U10_C1, U10_P"
    ))
    nb_student.cells.append(make_setup_cell("U10_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U10_Q",
        title="Structure Databases — Quiz Key",
        unit_num=10,
        unit_title="Structure Databases",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L26–L28, Practicals S12–S13",
        before_this="U10_C1, U10_P"
    ))
    nb_key.cells.append(make_setup_cell("U10_Q"))
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


def generate_unit10():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 10 notebooks...")
    c1 = build_u10_c1()
    save_notebook(c1, UNIT_DIR / "U10_C1_Reading_a_PDB_File.ipynb", clear=True)
    
    p_student, p_sol = build_u10_p()
    save_notebook(p_student, UNIT_DIR / "U10_P_PDB_Structures.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U10_P_PDB_Structures_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u10_q()
    save_notebook(q_student, UNIT_DIR / "U10_Q_Structure_Databases.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U10_Q_Structure_Databases_Key.ipynb", clear=False)
    
    print("  ✓ Unit 10 files written successfully.")
