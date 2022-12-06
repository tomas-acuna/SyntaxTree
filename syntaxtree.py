# "part" refers to a string representing the nodes in a syntax tree such as "NP", "A", or "spoon"
# "rule" refers to a list holding the old part at index 0 and the new parts afterwards
# for example, "VP->V NP" is represented as ["VP", "V", "NP"]
# "sling" refers to any list consisting of parts and smaller slings
# "rewrite" refers to a sling after it has a rule applied to it
# for example, the sling ["NP", "V", "NP", "PP"] can have the rule ["VP", "V", "NP"] applied to it and be rewritten to the new sling ["NP", ["VP", "V", "NP"], "PP"]

def get_old_part(rule):
    return rule[0]

def get_new_parts(rule):
    return rule[1:]

def get_length(rule):
    return len(new_part(rule))

def get_subsling(sling, start, end):
    subsling = []
    for i in range(start, end):
        subsling.append(sling[i][0])
    return subsling

def get_apply_rule(sling, rule, start):
    end = start + len(get_new_parts(rule))
    if end > len(sling):
        return False
    if get_subsling(sling, start, end) == get_new_parts(rule):
        return sling[:start] + [[get_old_part(rule)] + sling[start:end]] + sling[end:]
    return True

def get_rewrites(sling, rules):
    rewrites = []
    for rule in rules:
        start = 0
        current = True
        while current := get_apply_rule(sling, rule, start):
            if current != True:
                rewrites.append(current)
            start += 1
    return rewrites

# the next 3 functions just exist for optimization

def get_the_rule(part, rules):
    the_rules = []
    for rule in rules:
        if part in get_new_parts(rule):
            if len(get_new_parts(rule)) > 1:
                return False
            the_rules.append(rule)
    if len(the_rules) == 1:
        return the_rules[0]
    return False

def simplify_once_with_rules(sling, rules):
    simplified = []
    for thing in sling:
        the_rule = get_the_rule(thing[0], rules)
        if the_rule:
            simplified.append([get_old_part(the_rule), thing])
        else:
            simplified.append(thing)
    return simplified

def simplify_with_rules(sling, rules):
    simplified = sling
    while simplified != (simplified := simplify_once_with_rules(simplified, rules)):
        pass
    return simplified

def add_if_original(listo, element):
    if element not in listo:
        listo.append(element)

def get_end_rewrites(sling, rules):
    def simplify(some_sling):
        return simplify_with_rules(some_sling, rules)
    end_rewrites = []
    current_rewrites = [sling]
    while current_rewrites:
        # the next line exists just for optimization
        current_rewrites = mapa(simplify, current_rewrites)
        currenter_rewrites = []
        for current_rewrite in current_rewrites:
            if len(current_rewrite) == 1:
                add_if_original(end_rewrites, current_rewrite[0])
            new_rewrites = get_rewrites(current_rewrite, rules)
            if new_rewrites:
                for new_rewrite in new_rewrites:
                    add_if_original(currenter_rewrites, new_rewrite)
        current_rewrites = currenter_rewrites
    return end_rewrites

def sling_to_string(sling):
    string = "["
    for thing in sling:
        if type(thing) == list:
            string += sling_to_string(thing)
        else:
            string += thing
        string += " "
    return string[:len(string) - 1] + "]"

def string_to_rule(string):
    return string.replace("->", " ").split()

def mapa(function, listo):
    return list(map(function, listo))

def enlist(thing):
    return [thing]

def string_to_sling(string):
    return mapa(enlist, string.split())

def is_not_empty(string):
    return string != "" and string[:1] != "#"

def string_to_rules_and_sling(string):
    lines = list(filter(is_not_empty, string.split("\n")))
    rules = []
    for rule in mapa(string_to_rule, lines[:len(lines) - 1]):
        add_if_original(rules, rule)
    sling = string_to_sling(lines[len(lines) - 1])
    return [rules, sling]

with open("syntaxtree.txt") as file:
    input = file.read()

rules_and_sling = string_to_rules_and_sling(input)

print("you can paste the following into overleaf:\n\n")

print("\\documentclass{memoir}\n\\usepackage{forest}\n\\usepackage[a4paper, total={6in, 10in}]{geometry}\n\\pagestyle{empty}\n\\begin{document}\n")

for thing in get_end_rewrites(rules_and_sling[1], rules_and_sling[0]):
    print("\\begin{forest}\n" + sling_to_string(thing) + "\n\\end{forest}\n")

print("\\end{document}\n\n")
