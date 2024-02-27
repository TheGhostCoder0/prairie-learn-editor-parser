import re



# allows for reusability
pattern = re.compile("^[A-Z]+$")

# search for pattern existence in the string
print(pattern.search("Hello World")) # None
print(pattern.search("HELLO WORLD")) # None
print(pattern.search("HELLOWORLD")) # Match found

# 3 lowercase
# 3-5 digits
# one symbol
# up to two uppercase

# hzu6682#K
pattern = re.compile("^[a-z]{3}[0-9]{3, 5}$[^a-zA-Z0-9]{1}[A-Z]{0, 2}$")


#r indicates raw string
def use_regex(input_text):
    pattern = re.compile(r"#edit", re.IGNORECASE)
    return pattern.match(input_text)

# pl stuff
open = "#edit"
close = "#!edit"

# def nested(matches):
#     stack = []
#     for i in matches:
#         if i == open:
#             stack.append(i)
#         else:
#             stack.pop(i)
file_string = 'def main(): \
  #edit print("hello world!") #edit, #!edit #!edit \
  return '

pl_pattern = re.compile(f"{open}|{close}", re.MULTILINE)

result = pl_pattern.findall(file_string)
print(result)

