import subprocess


def format_file(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()

    to_space = ["\n", "\t", "\r", "\v", "\f", "\\", "/", "(", ")"]

    txt = txt.upper()
    new_text = ""
    for c in txt:
        if c in to_space:
            new_text += " "
        elif c in "ZXCVBNMASDFGHJQWERTYU":
            new_text += c
    txt = new_text
    while "  " in txt:
        txt = txt.replace("  ", " ")
    txt = txt.strip().split(" ")
    for i, line in enumerate(txt):
        txt[i] = ''.join(sorted(list(line)))
    txt = "\n".join(txt) + "\n"

    with open(path, "w+") as f:
        f.write(txt)

def compare(in_path, out_path):
    args = ['diff', in_path, out_path]
    print("$>", *args)
    subprocess.call(['wsl'] + args)

def edit_using_notepad(path):
    with open(path, "w+"):
        pass
    notepad_process = subprocess.Popen(f"notepad.exe {path}")
    notepad_process.wait()

def main():
    input_path = r"data/existing_score.txt"
    output_path = r"data/output_score.txt"

    print("Processing complete")
    input("press enter to compare with existing score")
    edit_using_notepad(input_path)
    format_file(input_path)
    format_file(output_path)
    compare(input_path, output_path)

if __name__ == '__main__':
    main()