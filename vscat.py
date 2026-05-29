import sys
import json

STYLES = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "black": "\033[30m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "reverse": "\033[7m",
    "hidden": "\033[8m",
    "strike": "\033[9m"
}

STYLES = STYLES | {s + "-bold":c + "\033[1m" for s, c in STYLES.items()}


def read_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()
    
def process_line(line: str, words: dict, i):
    if numeration:
        sys.stdout.write(str(i) + '\t')
    buf = ""
    string = ""
    for char in line:
        if strings_view:
            if char in ["'", '"'] and string:
                string += char
                sys.stdout.write(f"{STYLES['green']}{string}{STYLES['reset']}")
                string = ""
                continue

            elif char in ["'", '"'] and not string:
                if buf:
                    sys.stdout.write(buf)
                    buf = ""
                string += char
                continue 

            elif char not in ["'", '"'] and string:
                string += char
                continue
            
        if char in [" ", "\n"]:
            if buf in words:
                sys.stdout.write(f"{STYLES[words[buf]]}{buf}{STYLES['reset']}")
            else:
                sys.stdout.write(buf)
            buf = ""
            sys.stdout.write(char)
        
        elif char in words:
            if buf:
                if buf in words:
                    sys.stdout.write(f"{STYLES[words[buf]]}{buf}{STYLES['reset']}")
                else:
                    sys.stdout.write(buf)
            sys.stdout.write(f"{STYLES[words[char]]}{char}{STYLES['reset']}")   
            buf = ""
        else:
            buf += char
            if buf in words:
                sys.stdout.write(f"{STYLES[words[buf]]}{buf}{STYLES['reset']}")
                buf = ""
        
def unpack_words(style, words):
    for i, w in enumerate(words):
        if w in aliases:
            words = words[:i] + aliases[w] + words[i+1:]
    unpacked = {}   
    for w in words:
        unpacked[w] = style
    return unpacked



filename = sys.argv[1]
filetype = filename.split('.')[-1]
config_path = sys.argv[2]

config = read_config(config_path)
lines = read_file(filename)


if not filetype in config:
    exit(f'Config for {filetype} unfound')


aliases = {
    "0-9": list("0123456789")
} 

style_config: dict = config[filetype]

strings_view = style_config.get("strings_view")
if strings_view:
    del style_config['strings_view']

numeration = style_config.get("numeration")

if numeration:
    del style_config['numeration']

full_dict = dict()

for style, words in style_config.items():
    full_dict = full_dict | unpack_words(style, words)

for i, line in enumerate(lines):
    process_line(line, full_dict, i + 1)

