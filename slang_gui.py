import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from slang_parser import SlangParser
from slang_interpreter import SlangInterpreter

class SlangGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SICEM-Lang Interface")
        self.root.geometry("800x600")
        
        # Initialize components
        self.parser = SlangParser()
        self.interpreter = None
        self.current_file = None
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create widgets
        self._create_widgets()
        
    def _create_widgets(self):
        # File selection
        ttk.Label(self.main_frame, text=".slang File:").grid(row=0, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, sticky=tk.W)
        ttk.Button(self.main_frame, text="Browse", command=self._browse_file).grid(row=0, column=2)
        
        # CI Level slider
        ttk.Label(self.main_frame, text="Intelligence Level:").grid(row=1, column=0, sticky=tk.W)
        self.ci_level = tk.DoubleVar(value=0.5)
        ttk.Scale(self.main_frame, from_=0.0, to=1.0, variable=self.ci_level, 
                 orient=tk.HORIZONTAL, length=200).grid(row=1, column=1, sticky=tk.W)
        
        # Function selection
        ttk.Label(self.main_frame, text="Function:").grid(row=2, column=0, sticky=tk.W)
        self.function_var = tk.StringVar()
        self.function_combo = ttk.Combobox(self.main_frame, textvariable=self.function_var, state="readonly")
        self.function_combo.grid(row=2, column=1, sticky=tk.W)
        
        # Input area
        ttk.Label(self.main_frame, text="Input:").grid(row=3, column=0, sticky=tk.W)
        self.input_text = scrolledtext.ScrolledText(self.main_frame, width=50, height=5)
        self.input_text.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        # Output area
        ttk.Label(self.main_frame, text="Output:").grid(row=4, column=0, sticky=tk.W)
        self.output_text = scrolledtext.ScrolledText(self.main_frame, width=50, height=10)
        self.output_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E))
        
        # Execute button
        ttk.Button(self.main_frame, text="Execute", command=self._execute).grid(row=5, column=1, pady=10)
        
        # Help button
        ttk.Button(self.main_frame, text="Help", command=self._show_help).grid(row=5, column=2, pady=10)
        
    def _browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Slang files", "*.slang"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            self._load_file(file_path)
            
    def _load_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            parsed_content = self.parser.parse(content)
            
            # Update function combo box
            functions = list(parsed_content['functions'].keys())
            self.function_combo['values'] = functions
            if functions:
                self.function_combo.set(functions[0])
                
            # Initialize interpreter
            self.interpreter = SlangInterpreter(ci_level=self.ci_level.get())
            
            self.current_file = file_path
            self.output_text.insert(tk.END, f"Loaded file: {file_path}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            
    def _execute(self):
        if not self.current_file or not self.interpreter:
            messagebox.showwarning("Warning", "Please load a .slang file first")
            return
            
        try:
            # Get input and function
            input_text = self.input_text.get("1.0", tk.END).strip()
            function_name = self.function_var.get()
            
            if not function_name:
                messagebox.showwarning("Warning", "Please select a function")
                return
                
            # Execute function
            with open(self.current_file, 'r') as f:
                content = f.read()
            parsed_content = self.parser.parse(content)
            
            result = self.interpreter.execute_function(
                parsed_content['functions'][function_name],
                input_text
            )
            
            # Display result
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Result:\n{result}\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def _show_help(self):
        help_text = """
        How to use this program:
        
        1. Click 'Browse' to select a .slang file
        2. Use the slider to set the intelligence level
        3. Select a function from the dropdown
        4. Type your input in the input box
        5. Click 'Execute' to run the function
        
        Intelligence Levels:
        - 0.0-0.3: Very simple responses
        - 0.3-0.6: Basic understanding
        - 0.6-0.8: Detailed analysis
        - 0.8-1.0: Advanced processing
        """
        messagebox.showinfo("Help", help_text)

def main():
    root = tk.Tk()
    app = SlangGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 