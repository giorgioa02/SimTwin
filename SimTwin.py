# =============================
# Imports
# =============================
import ast                              # Parses Python code into Abstract Syntax Trees (ASTs)
import sys                              # Handles command-line file inputs
from z3 import Solver, Int, sat         # SMT solver for symbolic variable reasoning

# =============================
# Summarize Logic
# =============================
def summarize_logic(ast_tree):
    """Summarizes logic in terms of key constructs used."""
    summary = {
        'binop': 0,
        'assign': 0,
        'return': 0,
        'loop': 0,
        'if': 0,
        'call': 0,
        'listcomp': 0
    }

    for node in ast.walk(ast_tree):
        if isinstance(node, ast.BinOp):
            summary['binop'] += 1
        elif isinstance(node, ast.Assign):
            summary['assign'] += 1
        elif isinstance(node, ast.Return):
            summary['return'] += 1
        elif isinstance(node, (ast.For, ast.While)):
            summary['loop'] += 1
        elif isinstance(node, ast.If):
            summary['if'] += 1
        elif isinstance(node, ast.Call):
            summary['call'] += 1
        elif isinstance(node, ast.ListComp):
            summary['listcomp'] += 1

    return summary

# =============================
# Similarity Score
# =============================
def logic_similarity_score(summary1, summary2):
    """Computes a similarity score between two summaries."""
    keys = summary1.keys()
    diffs = [abs(summary1[k] - summary2[k]) for k in keys]
    return sum(diffs)

# =============================
# AST Parsing
# =============================
def parse_ast(code):
    """Parses a Python function into an AST."""
    return ast.parse(code).body[0]

# =============================
# Structural Equivalence Checker
# =============================
def ast_structure_match(ast1, ast2):
    """Checks if two ASTs have the same structure, ignoring names."""
    if type(ast1) != type(ast2):
        return False

    if isinstance(ast1, ast.FunctionDef) and isinstance(ast2, ast.FunctionDef):
        return ast_structure_match(ast1.args, ast2.args) and ast_structure_match(ast1.body, ast2.body)

    if isinstance(ast1, ast.arguments) and isinstance(ast2, ast.arguments):
        return ast_structure_match(ast1.args, ast2.args)

    if isinstance(ast1, ast.arg) and isinstance(ast2, ast.arg):
        return True

    if isinstance(ast1, ast.Name) and isinstance(ast2, ast.Name):
        return True

    if isinstance(ast1, ast.BinOp) and isinstance(ast2, ast.BinOp):
        return (
            ast_structure_match(ast1.left, ast2.left) and
            ast_structure_match(ast1.right, ast2.right) and
            type(ast1.op) == type(ast2.op)
        )

    if isinstance(ast1, list) and isinstance(ast2, list):
        return all(ast_structure_match(n1, n2) for n1, n2 in zip(ast1, ast2))

    if hasattr(ast1, '_fields') and hasattr(ast2, '_fields'):
        return all(ast_structure_match(getattr(ast1, f), getattr(ast2, f)) for f in ast1._fields)

    return False

# =============================
# Variable Mapping Consistency Checker
# =============================
def check_variable_consistency(code1, code2):
    """Uses Z3 to check if variables in two code snippets maintain consistency."""
    tree1, tree2 = parse_ast(code1), parse_ast(code2)
    var_map = {}
    solver = Solver()

    for node1, node2 in zip(ast.walk(tree1), ast.walk(tree2)):
        if isinstance(node1, ast.Name) and isinstance(node2, ast.Name):
            if node1.id not in var_map:
                var_map[node1.id] = Int(node2.id)
            solver.add(var_map[node1.id] == Int(node2.id))

    return solver.check() == sat

# =============================
# Control Flow Shape Comparison
# =============================
def extract_control_flow_sequence(ast_tree):
    """Returns a list of control flow node types in order."""
    control_flow_nodes = (ast.If, ast.For, ast.While, ast.Try, ast.Return)
    return [type(node).__name__ for node in ast.walk(ast_tree) if isinstance(node, control_flow_nodes)]

# =============================
# Input/Output Classification
# =============================
def extract_io_pattern(ast_tree):
    inputs = set()
    outputs = set()
    
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.arg):
            inputs.add(node.arg)
        elif isinstance(node, ast.Return):
            if isinstance(node.value, ast.Name):
                outputs.add(node.value.id)
            elif isinstance(node, ast.Return):
                outputs.add('implicit_return')
    
    return inputs, outputs

def analyze_runtime_behavior(func1, func2):
    def compile_and_exec(code):
        tree = ast.parse(code)
        func_name = tree.body[0].name
        compiled = compile(code, "<string>", "exec")
        namespace = {}
        exec(compiled, namespace)
        return namespace[func_name]

    func1 = compile_and_exec(code1)
    func2 = compile_and_exec(code2)

    test_inputs = [0, 1, 5, 10]
    results1 = [func1(i) for i in test_inputs]
    results2 = [func2(i) for i in test_inputs]
    return results1 == results2

def identify_computational_pattern(ast_tree):
    patterns = []
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.For):
            patterns.append('iteration')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == node.func.id:
            patterns.append('recursion')
    return patterns

def io_similarity(io1, io2):
    """Computes similarity between two I/O patterns."""
    inputs1, outputs1 = io1
    inputs2, outputs2 = io2
    
    input_sim = 1 if len(inputs1) == len(inputs2) else 0
    output_sim = 1 if ('implicit_return' in outputs1 or 'implicit_return' in outputs2) or outputs1 == outputs2 else 0
    
    return (input_sim + output_sim) / 2


# =============================
# Determine Clone Type
# =============================
def identifiers_exact_match(code1, code2):
    """Returns True if variable/function names are identical in both snippets."""
    tree1_ids = sorted({node.id for node in ast.walk(parse_ast(code1)) if isinstance(node, ast.Name)})
    tree2_ids = sorted({node.id for node in ast.walk(parse_ast(code2)) if isinstance(node, ast.Name)})
    return tree1_ids == tree2_ids

def detect_clone_type(structure_match, var_match, code1, code2):
    if structure_match and var_match:
        return "Type 1" if identifiers_exact_match(code1, code2) else "Type 2"

    if var_match:
        # Allow for loose structural similarity
        tree1 = parse_ast(code1)
        tree2 = parse_ast(code2)

        # Collect all operators
        ops1 = {type(node.op) for node in ast.walk(tree1) if isinstance(node, ast.BinOp)}
        ops2 = {type(node.op) for node in ast.walk(tree2) if isinstance(node, ast.BinOp)}

        # Collect total node count difference
        node_diff = abs(sum(1 for _ in ast.walk(tree1)) - sum(1 for _ in ast.walk(tree2)))
        
        summary1 = summarize_logic(tree1)
        summary2 = summarize_logic(tree2)
        
        score = logic_similarity_score(summary1, summary2)
        
        cf_seq1 = extract_control_flow_sequence(tree1)
        cf_seq2 = extract_control_flow_sequence(tree2)
        
        print(cf_seq1)
        print(cf_seq2)

        # If they share operators and the ASTs aren't wildly different (node_diff <= 5)
        if score <= 4:
            return "Type 3"
    

    # Check for Type 4 clones
    tree1 = parse_ast(code1)
    tree2 = parse_ast(code2)
    io1 = extract_io_pattern(tree1)
    io2 = extract_io_pattern(tree2)
    io_sim = io_similarity(io1, io2)
    
    runtime_match = analyze_runtime_behavior(code1, code2)

    pattern1 = identify_computational_pattern(tree1)
    pattern2 = identify_computational_pattern(tree2)
    
    if io_sim > 0.7 and runtime_match and pattern1 != pattern2:  # You can adjust this threshold
        return "Type 4"

    return "No Clone"

# =============================
# Main Execution
# =============================
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clone_verifier.py <file1.py> <file2.py>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    try:
        with open(file1_path, 'r') as f1:
            code1 = f1.read()
        with open(file2_path, 'r') as f2:
            code2 = f2.read()

        ast1 = parse_ast(code1)
        ast2 = parse_ast(code2)

        print("\n===== Clone Verification =====")
        print(f"Comparing: {file1_path} <==> {file2_path}")
        print("\n--- Raw Code Snippets ---")
        print(f"Code 1:\n{code1.strip()}\n")
        print(f"Code 2:\n{code2.strip()}\n")

        # Run checks
        structure_match = ast_structure_match(ast1, ast2)
        variable_match = check_variable_consistency(code1, code2)
        clone_type = detect_clone_type(structure_match, variable_match, code1, code2)
        final_result = clone_type != "No Clone"

        print("--- AST Comparison ---")
        print("Structurally Similar:", structure_match)
        print("Variable Mapping Consistent:", variable_match)
        print("Logic Similarity Score:", logic_similarity_score(summarize_logic(ast1), summarize_logic(ast2)))
        print("\n")
        print("Semantic Summary 1:", summarize_logic(ast1))
        print("Semantic Summary 2:", summarize_logic(ast2))
        
        # Add I/O pattern comparison
        io1 = extract_io_pattern(ast1)
        io2 = extract_io_pattern(ast2)
        io_sim = io_similarity(io1, io2)
        print("\n--- I/O Pattern Comparison ---")
        print("I/O Pattern 1:", io1)
        print("I/O Pattern 2:", io2)
        print("I/O Similarity Score:", io_sim)

        if final_result:
            print("\nVerified Clone Match:", True)
        else:
            print("\nNot a Verified Clone")

        print("Clone Type Identified:", clone_type)
        print("================================\n")

    except Exception as e:
        print(f"Error: Could not process one or both files.\n{e}")
