"""
cocktail-reader.py

Reads cocktail information from completed-cocktails.tex source file and puts them into some file format for loading into a database.
"""

import re

# these are the states of reading the file
IGNORE = "ignore"
COCKTAIL = "cocktail"
BODY = "body"

state = IGNORE

STARRED = "*"

### re testing
"""
test_str = "\hi{there}"
test_re = re.compile(r"\\(?P<func>[a-z]+){(?P<arg>[a-z]+)}")
test_match = test_re.match(test_str)
print test_match
print test_match.group("func")
print test_match.group("arg")
"""
### end re testing

#begin_cocktail_re = re.compile(r"^\begin{(?P<type>[A-Z]+)?Cocktail(\*)?}{(?P<name>)[A-Z].*}{\s}?{#.*}$") # error somewhere? -- not catching everything

begin_cocktail_re = re.compile(r"\\begin\{(?P<source>[A-Za-z0-9]+)?Cocktail(?P<starred>\*)?\}\{(?P<name>.+)\}(\s)?(?P<comments>\#.*)?") ## this one is looking pretty good

end_cocktail_re = re.compile(r"\\end\{([A-Za-z0-9]+)?Cocktail\}(\s)?(?P<comments>\#.*)?")

begin_ingredient_re = re.compile(r"\\begin\{Ingredients\}(\s)?(?P<comments>\#.*)?")

end_ingredients_re = re.compile(r"\\end\{Ingredients\}(\s)?(?P<comments>\#.*)?")

ingredient_re = re.compile("")

f = open("completed-cocktails-medium.tex")

cocktail_names = []

cocktails = {}

starred = False

def append_cocktail(cocktails, source, name):
    if source in cocktails.keys():
        cocktails[source].append(name)
    else:
        cocktails[source] = [name]

#all_comments = []


## there's something buggy with the simple finite state machine right now
for line in f:
    #print line
    cocktail_match = begin_cocktail_re.match(line)
    end_cocktail_match = end_cocktail_re.match(line)
    #print repr(line)
    #print cocktail_match
    if cocktail_match:
        try:
            source = cocktail_match.group("source")
            try:
                if cocktail_match.group("starred") == STARRED:
                    starred = True
            except AttributeError:
                pass
            name = cocktail_match.group("name")
            
            """
            comments = cocktail_match.group("comments")
            if comments:
                all_comments.append(comments)
            """
            
            
            #print name
            cocktail_names.append(name)
            
            #print source, starred, name
            
            if not starred:
                if source == None:
                    source = "Classic"
                append_cocktail(cocktails, source, name)
            else:
                if source == None:
                    starred_source = "HBAR"
                else:
                    starred_source = source + "*"
                append_cocktail(cocktails, starred_source, name)
    
        except AttributeError:
            print "failed on: " + line
            #pass
        
        starred = False
        
        state = COCKTAIL
    
    elif end_cocktail_match:
        if state == COCKTAIL:
            print "exited recipe"
            state = IGNORE
    
    if state == COCKTAIL:
        print "entered recipe"
    

f.close()


for key in sorted(cocktails.keys()):
    print str(key).upper() + ":"
    for entry in sorted(cocktails[key]):
        print entry
    print ""



cocktail_names.sort()
raw_names = open("cocktail_names_latex.dat","w")
for entry in cocktail_names:
    raw_names.write(entry+"\n")
raw_names.close()

"""
for entry in all_comments:
    print entry
"""