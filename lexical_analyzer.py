import re
from tkinter import *
from tkinter import filedialog, messagebox



keywords = {
    "int","float","double","char","if","else","while","for",
    "return","class","public","static","void","new","switch","case","break"
}

operators = {
    "++","--","!","=","+","-","*","/","%","<","<=",">",">=","==","!=","&&","||"
}

symbols = {"(",")","{","}","[","]",".",",",";",":","'","\""}



def remove_comments(code):
    code = re.sub(r'//.*', '', code)  # single-line
    code = re.sub(r'/\.?\*/', '', code, flags=re.DOTALL)  # multi-line
    return code



def tokenize(code):
    pattern = r'\".?\"|\'.?\'|\+\+|--|==|!=|<=|>=|&&|\|\||[a-zA-Z_]\w*|\d+\.\d+|\d+|[^\s]'
    return re.findall(pattern, code)




def classify(token):
    if token in keywords:
        return "KEYWORD"

    elif token in operators:
        return "OPERATOR"

    elif token in symbols:
        return "SYMBOL"

    elif re.fullmatch(r'[+-]?\d+', token):
        return "INTEGER"

    elif re.fullmatch(r'[+-]?\d+\.\d+', token):
        return "REAL NUMBER"

    elif re.fullmatch(r"'(.)'", token):
        return "CHARACTER LITERAL"

    elif re.fullmatch(r'"(.*?)"', token):
        return "STRING LITERAL"

    elif re.fullmatch(r'[a-zA-Z_]\w*', token):
        return "IDENTIFIER"

    else:
        return "INVALID"




def process_code(code):
    output_box.delete(1.0, END)

    code = remove_comments(code)
    tokens = tokenize(code)

    for token in tokens:
        token_type = classify(token)
        output_box.insert(END, f"{token}  →  {token_type}\n")




def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[("Java Files", ".java"), ("Text Files", ".txt")])
    
    if file:
        code = file.read()
        input_box.delete(1.0, END)
        input_box.insert(END, code)
        process_code(code)


def scan_text():
    code = input_box.get(1.0, END)
    if code.strip() == "":
        messagebox.showwarning("Warning", "Please enter or load code first!")
    else:
        process_code(code)



root = Tk()
root.title("Java Scanner (Lexical Analyzer)")
root.geometry("800x600")

# Title
Label(root, text="Scanner / Lexical Analyzer", font=("Arial", 16, "bold")).pack(pady=10)

# Input box
Label(root, text="Input Code:").pack()
input_box = Text(root, height=10, width=90)
input_box.pack(pady=5)

# Buttons
frame = Frame(root)
frame.pack(pady=5)

Button(frame, text="Open File", command=open_file, bg="lightblue").grid(row=0, column=0, padx=10)
Button(frame, text="Scan Code", command=scan_text, bg="lightgreen").grid(row=0, column=1, padx=10)

# Output box
Label(root, text="Output Tokens:").pack()
output_box = Text(root, height=15, width=90)
output_box.pack(pady=5)

root.mainloop()