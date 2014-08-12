import itertools
from os.path import abspath, join, dirname
import os
import json

DATA_DIR = abspath(join(dirname(__file__), '..', 'dst', 'dst', 'data'))
FIXTURE_DIR = abspath(join(dirname(__file__), '..', 'dst', 'survey', 'fixtures'))

# OUTPUT FILES
QUESTIONS_JSON = join(FIXTURE_DIR, "questions.json")
OUT_BIF = join(DATA_DIR, "bbn.bif") 

# INPUTS
DEFINITION = join(DATA_DIR, 'definition.json')

DEFAULT_LEVELS = ['suitable', 'unsuitable']

from pprint import pprint


def slugify(word):
    return word.lower().replace(' ', "_").replace("-","_")

def expand_bif(node, decision):
    """ recursively build bif file """
    decision_slug = slugify(decision.split("~")[0])

    if not node:
        # it's a terminal node, assign a prior probability
        prob_str = """probability ( %s ) {
  table 0.5, 0.5;
}""" % (decision_slug,)
        PROB_LIST.append(prob_str)

        return

    keys = node.keys()
    levels = []
    keynames = []
    for key in keys:
        ks = key.split("~")
        current_key = slugify(ks[0])
        keynames.append(current_key)

        if len(ks) == 1:
            level_iter = DEFAULT_LEVELS
        else:
            level_iter = [slugify(x) for x in ks[1].split(",")]

        variable = """variable %s {
  type discrete [ %d ] { %s };
}""" % (current_key, len(level_iter), ', '.join(level_iter))

        VARIABLE_LIST.append(variable)

        levels.append(level_iter)

    headings = keynames + [decision_slug]
    actual_levels = list(itertools.product(*levels))
    tf_levels = list(itertools.product(*([(True, False)] * len(keys))))  # assume first level == True
    levels = zip(actual_levels, tf_levels)  

    prob_str = "probability ( %s | %s ) {\n" % (
        decision_slug,
        ", ".join(keynames)
    )

    for bb, tf in levels:
        val = sum(tf)/float(len(tf))
        prob_str += "  (%s) %s;\n" % (
            ', '.join(bb),
            ', '.join(["%0.2f" % x for x in [val, 1.0 - val]])  # WARNING assumes 2 levels !!!!
        )

    prob_str += "}"
    PROB_LIST.append(prob_str)

    for key in keys:
        res = expand_bif(node[key], key)
        # if res:
        #     print(key)
    #print(dict(zip(keynames, levels)))

def expand_questions(node):
    """ recursively build json file of questions """

    global QUESTION_PK
    terminalnode_template = """
{
  "pk": %d,
  "fields": {
    "order": %d,
    "choices": "[{\\\"value\\\":1.0,\\\"choice\\\":\\\"%s\\\"}, {\\\"value\\\":0.5,\\\"choice\\\":\\\"Not Sure\\\"}, {\\\"value\\\":0.0,\\\"choice\\\":\\\"%s\\\"} ]",
    "supplement": "",
    "detail": "Detail about %s",
    "title": "%s",
    "image": "",
    "name": "%s",
    "question": "%s?",
    "layers": []
  },
  "model": "bbn.question"
}"""

    if not node:
        return
    keys = node.keys()

    for key in keys:
        if node[key]:
            res = expand_questions(node[key])
        else:
            try:
                name, levels = key.split("~")
                levels = levels.split(",")
            except:
                name = key
                levels = ['Suitable', 'Unsuitable']

            QUESTION_PK += 1
            QUESTIONS_LIST.append(terminalnode_template % (
                QUESTION_PK,
                QUESTION_PK * 100.0,
                levels[0],
                levels[-1],
                name,
                name,
                name,
                name
            ))


if __name__ == "__main__":


    with open(DEFINITION, 'r') as fh:
        suitability = json.loads(fh.read())

    QUESTION_PK = 0
    QUESTIONS_LIST = []
    expand_questions(suitability)
    with open(QUESTIONS_JSON, 'w') as fh:
        fh.write("[\n")
        fh.write(",\n".join(QUESTIONS_LIST))
        fh.write("\n]")
        
    VARIABLE_LIST = ["""variable suitability {
  type discrete [ 2 ] { suitable, unsuitable };
}"""]
    PROB_LIST = []
    expand_bif(suitability, 'suitability')
    netstr = """network unknown {
}
"""
    assert len(VARIABLE_LIST) == len(PROB_LIST)
    with open(OUT_BIF, 'w') as fh:
        fh.write(netstr)
        fh.write("\n".join(VARIABLE_LIST))
        fh.write("\n")
        fh.write("\n".join(PROB_LIST))

