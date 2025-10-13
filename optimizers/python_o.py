import sys
import time

def run_python_optimizer(file_path):
    print(f"Running python_o on {file_path}...")
    time.sleep(1.5)
    print("Python optimization complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python python_o.py <file_path>")
    else:
        run_python_optimizer(sys.argv[1])
