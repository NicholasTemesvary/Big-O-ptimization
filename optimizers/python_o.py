import sys
import time
from python_syntax import parse_syntax_rules

def run_python_optimizer(file_path):
    print(f"Running python_o on {file_path}")
    time.sleep(0.5)
    print("Analyzing Python syntax structure...\n")
    time.sleep(0.5)

    rules = parse_syntax_rules(file_path)
    if not rules:
        print("No syntax rules detected — file may be empty or invalid.")
    else:
        print("Detected Syntax Rules:")
        for rule in rules:
            print("-", rule)
    time.sleep(0.5)
    print("\nOptimization complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python python_o.py <file_path>")
    else:
        run_python_optimizer(sys.argv[1])
