# coding=utf-8
import base64, sys
print("This file has been encrypted by the hacker team V1agRAx01")
print("In order to read this file, you must answer this enigm...")
print("""
$ENIGM$
""")


nbrs = ["ڐ","ڿ","؄","؁","﷽","ﰱ","ﳑ","ﷲ","؀","ۼ"]

def myHash(text:str):
  hash=0
  for ch in text:
    hash = ( hash*281  ^ ord(ch)*997) & 0xFFFFFFFF
  return hex(hash)[2:].upper().zfill(8)

def decrypt(content, key):
    content = base64.b64decode(content.encode()).decode()
    key = str(myHash(key.lower()))
    long_key = ""
    result = []
    enc_numbers = content.split("⁣")
    chars = []
    for enc in enc_numbers:
        nbr_txt = ""
        for c in enc:
            nbr_txt += str(nbrs.index(c))
        num = int(nbr_txt)
        chars.append(num)
    while len(long_key) < len(content):
        long_key += key
    result = ""
    for text_nbr, key_char in zip(chars, long_key):
        key_nbr = ord(key_char) #Return the key number
        char = chr(text_nbr - key_nbr)
        result += char
    if result[0] != nbrs[0] or result[-1] != nbrs[-1]:
        raise ValueError("Nope ! This is not the correct answer :) \nTry again :)\n(An advice might be in the README)")
    else:
        return result[1:-1]

content = "$CONTENT$"
result = ""
if __name__ != "__main__":
    print("You're trying to use an encrypted file !")

while True:
    key = input("Answer: ")
    try:
        result = decrypt(content, key)
        with open(__file__, "w") as u:
            u.write(result)
        break
    except ValueError as e:
        print(e)

  

print("Hourra ! You found the key ! Try to run this file again.")
sys.exit(0)
