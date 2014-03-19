"""
latex-to-unicode.py

test of how well the dictionary is working
"""
import re

f = open("latex-unicode-dictionary.dat")

# what you want to do is read the file, then have the LaTeX side turned into an exact regular expression
## IMPORTANT: recall that you're an idiot and have written things like \'{e} in your LaTeX source, so don't forget to account for the curly braces

latex_unicode = []

for line in f:
    if line[0] != "#":
        latex_unicode.append([s.strip() for s in line.split(",")])

f.close()

"""
for element in latex_unicode:
    unicode_char = int(element[1],16)
    print element[0], unichr(unicode_char)
"""

latex_general_re = re.compile(r"(?P<escape>\\.)((\s)?|\[\s\])?(?P<letter>[A-Za-z])?")

def test_latex_general_re():
    assert latex_general_re.match(r"\!") is not None

for element in latex_unicode:
    match = latex_general_re.match(element[0])
    print match.group("escape")