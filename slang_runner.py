import re
import sys

class SlangRunner:
    def __init__(self, filename):
        self.filename = filename
        self.blocks = []

    def load_slang_file(self):
        with open(self.filename, 'r') as file:
            content = file.read()

        pattern = r'function: (.*?)\nagent: (.*?)\nintent: (.*?)\n(?:context:.*?\n)?input:(.*?)\noutput:(.*?)\n'
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            block = {
                "function": match[0].strip(),
                "agent": match[1].strip(),
                "intent": match[2].strip(),
                "input": match[3].strip(),
                "output": match[4].strip()
            }
            self.blocks.append(block)

    def run(self):
        print(f"Running {len(self.blocks)} function blocks from: {self.filename}\n")
        for i, block in enumerate(self.blocks, 1):
            print(f"--- Function {i}: {block['function']} ---")
            print(f"Agent: {block['agent']}")
            print(f"Intent: {block['intent']}")
            print(f"Input:\n{block['input']}")
            print(f"Output:\n{block['output']}")
            print("-" * 40)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python slang_runner.py your_file.slang")
        sys.exit(1)

    filename = sys.argv[1]
    runner = SlangRunner(filename)
    runner.load_slang_file()
    runner.run()
