import os
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext

def detect_language(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    extension_map = {
        '.py': 'Python', '.js': 'JavaScript', '.java': 'Java', '.cpp': 'C++',
        '.c': 'C', '.cs': 'C#', '.html': 'HTML', '.php': 'PHP', '.rb': 'Ruby',
        '.go': 'Go', '.rs': 'Rust', '.sh': 'Shell Script'
    }
    if ext in extension_map:
        return extension_map[ext]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
    if 'def ' in code and 'import ' in code:
        return 'Python'
    elif '#include' in code:
        return 'C or C++'
    elif 'public static void main' in code:
        return 'Java'
    elif 'function ' in code and 'console.log' in code:
        return 'JavaScript'
    elif '<?php' in code:
        return 'PHP'
    elif '<html>' in code:
        return 'HTML'
    elif 'fn main()' in code:
        return 'Rust'
    elif 'echo ' in code and 'done' in code:
        return 'Shell Script'
    else:
        return 'Unknown / Unrecognized'

def browse_file():
    file_path = filedialog.askopenfilename(title="Select a code file")
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    handle_language_detection()

def handle_language_detection(*args):
    file_path = entry.get().strip()
    if not os.path.isfile(file_path):
        result_label.config(text="")
        output_box.delete(1.0, tk.END)
        return
    language = detect_language(file_path)
    result_label.config(text=f"Detected Language: {language}")
    script_map = {
        'Python': 'python_o.py', 'C++': 'cpp_o.py', 'C': 'c_o.py',
        'Java': 'java_o.py', 'JavaScript': 'js_o.py', 'Rust': 'rust_o.py',
        'Shell Script': 'sh_o.py'
    }
    script_to_run = script_map.get(language)
    if not script_to_run:
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"No optimization script defined for {language}.\n")
        return

    optimizers_dir = os.path.join(os.path.dirname(__file__), "optimizers")
    os.makedirs(optimizers_dir, exist_ok=True)
    script_path = os.path.join(optimizers_dir, script_to_run)

    if not os.path.exists(script_path):
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"Missing script: {script_path}\n")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Detected {language}\n")
    output_box.insert(tk.END, f"Running {script_to_run}...\n\n")
    root.update()

    try:
        result = subprocess.run(
            ["python", script_path, file_path],
            capture_output=True,
            text=True,
            check=True
        )
        output_box.insert(tk.END, result.stdout)
        if result.stderr:
            output_box.insert(tk.END, "\nErrors:\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        output_box.insert(tk.END, f"Error running {script_to_run}:\n{e.stderr}\n")
    except Exception as e:
        output_box.insert(tk.END, f"Unexpected error: {e}\n")

root = tk.Tk()
root.title("Detect Language & Run Optimizer")
root.geometry("500x400")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill='both')

label = tk.Label(frame, text="Enter or Browse to your code file:", font=('Arial', 11))
label.pack(pady=5)

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)
entry.bind("<KeyRelease>", handle_language_detection)

browse_button = tk.Button(frame, text="Browse", command=browse_file)
browse_button.pack(pady=5)

result_label = tk.Label(frame, text="", font=('Arial', 12, 'bold'), fg='blue', justify="center")
result_label.pack(pady=5)

output_box = scrolledtext.ScrolledText(frame, width=55, height=12, font=('Courier', 10))
output_box.pack(pady=10)

root.mainloop()
