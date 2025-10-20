import ast

def parse_syntax_rules(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        code = file.read()

    tree = ast.parse(code)
    syntax_rules = set()

    def analyze(node):
        if isinstance(node, ast.FunctionDef):
            syntax_rules.add("function definition")
        elif isinstance(node, ast.ClassDef):
            syntax_rules.add("class definition")
        elif isinstance(node, ast.If):
            syntax_rules.add("if/elif/else statement")
        elif isinstance(node, ast.For):
            syntax_rules.add("for loop")
        elif isinstance(node, ast.While):
            syntax_rules.add("while loop")
        elif isinstance(node, ast.Try):
            syntax_rules.add("try/except/finally")
        elif isinstance(node, ast.With):
            syntax_rules.add("with statement")
        elif isinstance(node, ast.Import):
            syntax_rules.add("import statement")
        elif isinstance(node, ast.ImportFrom):
            syntax_rules.add("from-import statement")
        elif isinstance(node, ast.Assign):
            syntax_rules.add("variable assignment")
        elif isinstance(node, ast.AnnAssign):
            syntax_rules.add("annotated assignment")
        elif isinstance(node, ast.Return):
            syntax_rules.add("return statement")
        elif isinstance(node, ast.Lambda):
            syntax_rules.add("lambda expression")
        elif isinstance(node, ast.AsyncFunctionDef):
            syntax_rules.add("async function definition")
        elif isinstance(node, ast.Await):
            syntax_rules.add("await expression")
        elif hasattr(ast, "Match") and isinstance(node, ast.Match):
            syntax_rules.add("match/case statement")

        for child in ast.iter_child_nodes(node):
            analyze(child)

    analyze(tree)
    return sorted(syntax_rules)
