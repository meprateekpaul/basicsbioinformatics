"""
unit07.py - Builder for Unit 07: Phylogenetic Analysis
Notebooks:
- U07_C1_Distances_and_Trees.ipynb
- U07_P_Phylogenetic_Trees.ipynb
- solutions/U07_P_Phylogenetic_Trees_Solutions.ipynb
- U07_Q_Phylogenetic_Analysis.ipynb
- solutions/U07_Q_Phylogenetic_Analysis_Key.ipynb
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

UNIT_DIR = NOTEBOOKS_DIR / "U07_Phylogenetic_Analysis"
SOLUTIONS_DIR = UNIT_DIR / "solutions"


def build_u07_c1():
    nb = nbf.v4.new_notebook()
    
    nb.cells.append(make_header_cell(
        notebook_id="U07_C1",
        title="Distances and Trees",
        unit_num=7,
        unit_title="Phylogenetic Analysis",
        nb_type="Course",
        time_min=40,
        difficulty="★★☆",
        goes_with="Lectures L18–L20, Practical S8 (Tree extension)",
        before_this="U06_C1"
    ))
    
    nb.cells.append(nbf.v4.new_markdown_cell("""## 1. What you will learn
- **Explain** core phylogenetic terminology: nodes, branches, clades, roots, and outgroups [LO5].
- **Calculate** pairwise evolutionary distance matrices from multiple sequence alignments [LO5].
- **Perform** UPGMA clustering step-by-step by hand and with Biopython's `Bio.Phylo` [LO5].
- **Differentiate** orthologues (speciation events) from paralogues (gene duplication events) on a gene tree [LO5].
"""))

    nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Biological question
Are myoglobin (*MB*) and hemoglobin beta (*HBB*) orthologues or paralogues? When we construct a phylogenetic tree from human globin sequences, we observe that hemoglobin beta (*HBB*) and delta (*HBD*) cluster together with nearly identical sequences, while myoglobin branches much earlier. How do we reconstruct the evolutionary branching history of these genes from sequence distances?
"""))

    nb.cells.append(make_setup_cell("U07_C1"))

    # Concept 1: Tree Terminology
    nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Concept 1: Phylogenetic Tree Anatomy and Orthology
### Theory
A phylogenetic tree is a mathematical graph modeling evolutionary relationships:
- **Terminal Nodes (Leaves / Taxa)**: Extant observed sequences.
- **Internal Nodes**: Hypothetical common ancestors.
- **Branches**: Evolutionary lineages; branch length represents inferred evolutionary change (divergence time or substitutions per site).
- **Clade (Monophyletic Group)**: An ancestor and *all* of its descendants.
- **Rooted vs. Unrooted**: A rooted tree specifies the direction of evolutionary time from an ultimate common ancestor (often defined using an **outgroup**).

**Orthologues vs. Paralogues:**
- **Orthologues**: Genes separated by a **speciation** event (e.g. human HBB vs chimp HBB). They typically perform identical biological functions in different species.
- **Paralogues**: Genes separated by an internal **gene duplication** event (e.g. human HBB and human HBD, or HBB and Myoglobin). Paralogues often evolve new or specialized functions (neofunctionalization / subfunctionalization).
"""))

    # Concept 2: Distance Matrices
    nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Concept 2: Calculating Distance Matrices
### Theory
Distance methods convert a multiple alignment into an $N \\times N$ pairwise distance matrix:
- **Fractional Dissimilarity ($p$-distance)**:
  $$p = \\frac{\\text{Number of mismatching columns}}{\\text{Total columns compared (excluding gaps)}}$$
- **Substitution Models**: Jukes-Cantor, Poisson, or BLOSUM62 matrices convert raw $p$-distances into estimates of the true number of substitutions per site, correcting for multiple hits at the same site.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Computing pairwise distance matrix with Biopython
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

aln_path = DATA_DIR / "alignments" / "globin_family.aln"
alignment = AlignIO.read(aln_path, "clustal")

calculator = DistanceCalculator("identity")
dm = calculator.get_distance(alignment)

print("=== Globin Pairwise Distance Matrix (Fractional Dissimilarity) ===")
print(dm)
'''))

    # Concept 3: UPGMA Step by Step
    nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Concept 3: UPGMA Tree Reconstruction
### Theory
**UPGMA** (Unweighted Pair Group Method with Arithmetic Mean) is a hierarchical clustering algorithm:
1. Find the two closest taxa $A$ and $B$ with minimum distance $d(A, B)$.
2. Join $A$ and $B$ to form a new node $U$. The node height is $d(A, B) / 2$.
3. Compute the distance from node $U$ to every other taxon $C$ as the unweighted arithmetic mean:
   $$d(U, C) = \\frac{d(A, C) + d(B, C)}{2}$$
4. Repeat until all taxa are merged into a single rooted tree.

**Assumption:** UPGMA assumes a constant rate of evolution across all lineages (**molecular clock**), producing an **ultrametric tree** where all leaf tips are equidistant from the root.
"""))

    nb.cells.append(nbf.v4.new_code_cell('''# Worked Example: Constructing UPGMA and NJ Trees
from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import matplotlib.pyplot as plt

constructor = DistanceTreeConstructor()
upgma_tree = constructor.upgma(dm)
nj_tree = constructor.nj(dm)

# Display ASCII text representation of UPGMA tree
print("=== UPGMA Tree (Assumes Molecular Clock) ===")
Phylo.draw_ascii(upgma_tree)

print("\\n=== Neighbor Joining Tree (Allows Variable Rates) ===")
Phylo.draw_ascii(nj_tree)

# Render publication tree plot
fig, ax = plt.subplots(figsize=(8, 5))
Phylo.draw(nj_tree, axes=ax, do_show=False)
ax.set_title("Neighbor Joining Phylogeny of Human Globin Family")
plt.tight_layout()
plt.savefig(OUT_DIR / "globin_nj_tree.png", dpi=100)
plt.show()
'''))

    # Summary
    nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Summary
- Phylogenetic trees model evolutionary divergence from sequence data.
- Orthologues originate from speciation; paralogues originate from gene duplication.
- Distance methods compress alignments into distance matrices.
- UPGMA assumes an equal molecular clock (ultrametric); Neighbor Joining allows lineage-specific rate variation.
"""))

    # Next
    nb.cells.append(nbf.v4.new_markdown_cell("""## 7. Next Steps
- Reconstruct trees for vertebrate orthologues and insulins in `U07_P_Phylogenetic_Trees.ipynb`.
- Test your tree interpretation skills in `U07_Q_Phylogenetic_Analysis.ipynb`.
"""))

    return nb


def build_u07_p():
    exercises = [
        PracticeExercise(
            ex_id="Ex 7.1",
            stars="★☆☆",
            title="Calculate pairwise distance matrix for globin family",
            biology="Pairwise sequence divergence quantifies evolutionary time since common ancestry.",
            task="Compute the identity distance matrix for `globin_family.aln` using `DistanceCalculator('identity')`. Store in variable `dist_mat`.",
            expected="`dist_mat` as a Bio.Phylo `DistanceMatrix` object with 7 taxa.",
            student_code="""# TODO: replace the ... with your code
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

aln = AlignIO.read(DATA_DIR / "alignments" / "globin_family.aln", "clustal")
calc = DistanceCalculator("identity")
dist_mat = ...
""",
            solution_code="""from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

aln = AlignIO.read(DATA_DIR / "alignments" / "globin_family.aln", "clustal")
calc = DistanceCalculator("identity")
dist_mat = calc.get_distance(aln)
""",
            check_code="""# Check — do not edit
assert len(dist_mat.names) == 7, f"Expected 7 taxa, got {len(dist_mat.names)}"
print("Ex 7.1 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.2",
            stars="★☆☆",
            title="Identify the minimum evolutionary distance pair",
            biology="The two most similar paralogues in the globin family represent the most recent gene duplication.",
            task="Find the pair of distinct taxa with the smallest distance in `dist_mat`. Store their names in a tuple `closest_pair` and their distance in `min_dist`.",
            expected="`closest_pair` containing 'HBB_HUMAN' and 'HBD_HUMAN', `min_dist` < 0.10.",
            student_code="""# TODO: replace the ... with your code
names = dist_mat.names
min_dist = 999.0
closest_pair = ()

for i in range(len(names)):
    for j in range(i + 1, len(names)):
        ...
""",
            solution_code="""names = dist_mat.names
min_dist = 999.0
closest_pair = ()

for i in range(len(names)):
    for j in range(i + 1, len(names)):
        d = dist_mat[i, j]
        if d < min_dist:
            min_dist = d
            closest_pair = (names[i], names[j])
""",
            check_code="""# Check — do not edit
assert "HBB_HUMAN" in closest_pair and "HBD_HUMAN" in closest_pair
assert min_dist < 0.10, f"Expected min_dist < 0.10, got {min_dist}"
print("Ex 7.2 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.3",
            stars="★☆☆",
            title="Construct a Neighbor Joining tree",
            biology="Neighbor Joining is a computationally efficient distance method that does not assume a constant molecular clock.",
            task="Construct a Neighbor Joining tree from `dist_mat` using `DistanceTreeConstructor().nj()`. Store in `nj_tree`. Verify it has 7 terminal taxa.",
            expected="`nj_tree` with 7 terminal clades.",
            student_code="""# TODO: replace the ... with your code
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor

constructor = DistanceTreeConstructor()
nj_tree = ...
num_taxa = len(nj_tree.get_terminals())
""",
            solution_code="""from Bio.Phylo.TreeConstruction import DistanceTreeConstructor

constructor = DistanceTreeConstructor()
nj_tree = constructor.nj(dist_mat)
num_taxa = len(nj_tree.get_terminals())
""",
            check_code="""# Check — do not edit
assert num_taxa == 7, f"Expected 7 terminal taxa, got {num_taxa}"
print("Ex 7.3 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.4",
            stars="★★☆",
            title="Construct UPGMA tree for vertebrate insulin family",
            biology="Insulin is an essential metabolic hormone conserved across all vertebrates.",
            task="Load `data/alignments/insulin_family.aln`. Compute the distance matrix with `DistanceCalculator('identity')`, and construct a UPGMA tree in `ins_upgma_tree`.",
            expected="`ins_upgma_tree` with terminal taxa matching insulin alignment.",
            student_code="""# TODO: replace the ... with your code
ins_aln = AlignIO.read(DATA_DIR / "alignments" / "insulin_family.aln", "clustal")
ins_dm = ...
ins_upgma_tree = ...
""",
            solution_code="""ins_aln = AlignIO.read(DATA_DIR / "alignments" / "insulin_family.aln", "clustal")
ins_dm = calc.get_distance(ins_aln)
ins_upgma_tree = constructor.upgma(ins_dm)
""",
            check_code="""# Check — do not edit
assert len(ins_upgma_tree.get_terminals()) == len(ins_aln)
print("Ex 7.4 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.5",
            stars="★★☆",
            title="Identify closest primate sister pair in the insulin tree",
            biology="Human and chimpanzee insulins share nearly 100% sequence identity.",
            task="Extract the pairwise distance between `'INS_HUMAN'` and `'INS_CHIMP'` from `ins_dm` into `human_chimp_dist`.",
            expected="`human_chimp_dist` as float == 0.0.",
            student_code="""# TODO: replace the ... with your code
human_chimp_dist = ...
""",
            solution_code="""human_chimp_dist = ins_dm["INS_HUMAN", "INS_CHIMP"]
""",
            check_code="""# Check — do not edit
assert human_chimp_dist == 0.0, f"Expected 0.0 distance between human and chimp insulin, got {human_chimp_dist}"
print("Ex 7.5 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.6",
            stars="★★☆",
            title="Classify gene relationships as Orthologues or Paralogues",
            biology="Speciation vs duplication determines functional homology.",
            task="Given two gene comparisons: (1) Human HBB vs Chimpanzee HBB (`comp1`), and (2) Human HBB vs Human HBD (`comp2`), assign `'Orthologues'` or `'Paralogues'` to `rel1` and `rel2`.",
            expected="`rel1` = 'Orthologues', `rel2` = 'Paralogues'.",
            student_code="""# TODO: replace the ... with your code
rel1 = ...  # Human HBB vs Chimp HBB
rel2 = ...  # Human HBB vs Human HBD
""",
            solution_code="""rel1 = "Orthologues"
rel2 = "Paralogues"
""",
            check_code="""# Check — do not edit
assert rel1 == "Orthologues", "Genes separated by speciation are orthologues"
assert rel2 == "Paralogues", "Genes separated by gene duplication within the same genome are paralogues"
print("Ex 7.6 passed")
"""
        ),
        PracticeExercise(
            ex_id="Ex 7.7",
            stars="★★★",
            title="Compare total branch length between UPGMA and NJ trees",
            biology="Neighbor Joining allows varying evolutionary branch lengths across fast- and slow-evolving lineages.",
            task="Calculate the total tree branch length (sum of all branch lengths) for `nj_tree` using `nj_tree.total_branch_length()` into `nj_length`, and `upgma_tree.total_branch_length()` into `upgma_length`.",
            expected="Both `nj_length` and `upgma_length` are positive floats.",
            student_code="""# TODO: replace the ... with your code
upgma_length = ...
nj_length = ...
""",
            solution_code="""upgma_tree = constructor.upgma(dist_mat)
upgma_length = upgma_tree.total_branch_length()
nj_length = nj_tree.total_branch_length()
""",
            check_code="""# Check — do not edit
assert isinstance(upgma_length, float) and upgma_length > 0
assert isinstance(nj_length, float) and nj_length > 0
print("Ex 7.7 passed")
"""
        )
    ]
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U07_P",
        title="Phylogenetic Trees — Exercises",
        unit_num=7,
        unit_title="Phylogenetic Analysis",
        nb_type="Practice",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L18–L20, Practical S8",
        before_this="U07_C1"
    ))
    nb_student.cells.append(make_setup_cell("U07_P"))
    
    nb_sol = nbf.v4.new_notebook()
    nb_sol.cells.append(make_header_cell(
        notebook_id="U07_P",
        title="Phylogenetic Trees — Solutions",
        unit_num=7,
        unit_title="Phylogenetic Analysis",
        nb_type="Practice Solutions",
        time_min=50,
        difficulty="★★☆",
        goes_with="Lectures L18–L20, Practical S8",
        before_this="U07_C1"
    ))
    nb_sol.cells.append(make_setup_cell("U07_P"))
    
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
1. Why does the UPGMA clustering algorithm produce an ultrametric tree, and why does this fail when different organismal lineages evolve at different rates?
2. What is the biological consequence of assuming two genes are orthologues when they are actually ancient paralogues?
"""
    nb_student.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    nb_sol.cells.append(nbf.v4.new_markdown_cell(reflection_md.strip()))
    
    return nb_student, nb_sol


def build_u07_q():
    salt = "U07_Q"
    questions = [
        QuizQuestion("q1", "What term describes homologous genes that diverged as a result of a speciation event?",
                     ["(a) Paralogues", "(b) Orthologues", "(c) Xenologues", "(d) Analogues"],
                     "b", "U07_C1 §3"),
        QuizQuestion("q2", "What event creates paralogous genes within a lineage?",
                     ["(a) Speciation", "(b) Gene duplication", "(c) Horizontal gene transfer", "(d) Point mutation alone"],
                     "b", "U07_C1 §3"),
        QuizQuestion("q3", "What key biological assumption is made by the UPGMA distance method?",
                     ["(a) Variable lineage mutation rates", "(b) Constant rate of evolution across all lineages (molecular clock)", "(c) Maximum parsimony", "(d) Maximum likelihood"],
                     "b", "U07_C1 §5"),
        QuizQuestion("q4", "What type of tree has all terminal leaves at equal distance from the root?",
                     ["(a) Additive tree", "(b) Ultrametric tree", "(c) Star tree", "(d) Unrooted network"],
                     "b", "U07_C1 §5"),
        QuizQuestion("q5", "Why is an outgroup taxon added when rooting an unrooted phylogenetic tree?",
                     ["(a) To speed up calculation", "(b) To place the root at the point where the outgroup joins the ingroup", "(c) To balance GC content", "(d) To eliminate homoplasy"],
                     "b", "U07_C1 §3"),
        QuizQuestion("q6", "In a phylogenetic tree, what does an internal node represent?",
                     ["(a) An extant living species", "(b) The most recent common ancestor of its descendants", "(c) A sequencing sequencing artifact", "(d) A deletion event"],
                     "b", "U07_C1 §3"),
        QuizQuestion("q7", "What does a bootstrap support value of 95% on a tree branch indicate?",
                     ["(a) 95% of sites in the alignment are identical", "(b) The clade appeared in 95% of trees reconstructed from pseudoreplicate alignments resampled with replacement", "(c) The tree is 95% certain to be true", "(d) 95% of species share the phenotype"],
                     "b", "U07_C1 §3"),
        QuizQuestion("q8", "Which distance-based tree building algorithm allows different lineages to evolve at different rates?",
                     ["(a) UPGMA", "(b) Neighbor Joining (NJ)", "(c) Strict consensus", "(d) Needleman-Wunsch"],
                     "b", "U07_C1 §5"),
        QuizQuestion("q9", "What is a monophyletic clade?",
                     ["(a) A common ancestor and all of its evolutionary descendants", "(b) A group sharing similar traits but different ancestors", "(c) An unrooted cluster of three leaves", "(d) A group excluding the ancestor"],
                     "a", "U07_C1 §3"),
        QuizQuestion("q10", "Which module in Biopython handles phylogenetic tree parsing, manipulation, and visualization?",
                     ["(a) Bio.SeqIO", "(b) Bio.Phylo", "(c) Bio.TreeIO", "(d) Bio.Cluster"],
                     "b", "U07_C1 §5")
    ]
    
    key_dict = {q.qid: digest_answer(salt, q.answer) for q in questions}
    revisit_dict = {q.qid: q.revisit for q in questions}
    
    nb_student = nbf.v4.new_notebook()
    nb_student.cells.append(make_header_cell(
        notebook_id="U07_Q",
        title="Phylogenetic Analysis — Quiz",
        unit_num=7,
        unit_title="Phylogenetic Analysis",
        nb_type="Quiz",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L18–L20, Practical S8",
        before_this="U07_C1, U07_P"
    ))
    nb_student.cells.append(make_setup_cell("U07_Q"))
    nb_student.cells.append(make_quiz_checker_cell(salt, key_dict, revisit_dict))
    
    nb_key = nbf.v4.new_notebook()
    nb_key.cells.append(make_header_cell(
        notebook_id="U07_Q",
        title="Phylogenetic Analysis — Quiz Key",
        unit_num=7,
        unit_title="Phylogenetic Analysis",
        nb_type="Quiz Key",
        time_min=20,
        difficulty="★☆☆",
        goes_with="Lectures L18–L20, Practical S8",
        before_this="U07_C1, U07_P"
    ))
    nb_key.cells.append(make_setup_cell("U07_Q"))
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


def generate_unit07():
    UNIT_DIR.mkdir(parents=True, exist_ok=True)
    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print("Generating Unit 07 notebooks...")
    c1 = build_u07_c1()
    save_notebook(c1, UNIT_DIR / "U07_C1_Distances_and_Trees.ipynb", clear=True)
    
    p_student, p_sol = build_u07_p()
    save_notebook(p_student, UNIT_DIR / "U07_P_Phylogenetic_Trees.ipynb", clear=True)
    save_notebook(p_sol, SOLUTIONS_DIR / "U07_P_Phylogenetic_Trees_Solutions.ipynb", clear=False)
    
    q_student, q_key = build_u07_q()
    save_notebook(q_student, UNIT_DIR / "U07_Q_Phylogenetic_Analysis.ipynb", clear=True)
    save_notebook(q_key, SOLUTIONS_DIR / "U07_Q_Phylogenetic_Analysis_Key.ipynb", clear=False)
    
    print("  ✓ Unit 07 files written successfully.")
