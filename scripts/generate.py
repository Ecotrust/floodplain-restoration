import itertools
import xlwt
from os.path import abspath, join, dirname
import os
import json

# OUTPUT FILES
DATA_DIR = abspath(join(dirname(__file__), '..', 'data'))
CPT_XLS = join(DATA_DIR, "cpt.xls")
CPT_PY = join(DATA_DIR, "cpt.py")
QUESTIONS_JSON = join(DATA_DIR, "questions.json")

# INPUTS
DEFINITION = join(DATA_DIR, 'definition.json')

DEFAULT_LEVELS = ['Suitable', 'Unsuitable']
MAX_SHEETNAME_WIDTH = 25


def expand(node, decision):
    """ recursively build excel file """
    if not node:
        return
    keys = node.keys()
    levels = []
    keynames = []
    decision = decision.split('~')[0][:MAX_SHEETNAME_WIDTH]
    sheet = BOOK.add_sheet(decision)
    for key in keys:
        ks = key.split("~")
        # keynames.append(ks[0])
        keynames.append(key)  # don't split!!!
        if len(ks) == 1:
            level_iter = zip([ks[0]] * len(DEFAULT_LEVELS), DEFAULT_LEVELS)
        else:
            tls = ks[1].split(",")
            level_iter = zip([ks[0]] * len(tls), tls)

        levels.append(["~".join(x) for x in level_iter])

    rowx = 0
    headings = keynames + [decision]
    heading_fmt = xlwt.easyxf('font: bold on; align: wrap off, vert centre, horiz center')
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value, heading_fmt)

    actual_levels = itertools.product(*levels)
    tf_levels = list(itertools.product(*([(True, False)] * len(keys))))  # assume first level == True
    levels = zip(actual_levels, tf_levels)

    for bb, tf in levels:
        row = [str(x) for x in bb] + [int(100 * (sum(tf)/float(len(tf))))]
        rowx += 1
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value)

    for i in range(len(row)):
        sheet.col(i).width =  0x0d00 + 100
        
    for key in keys:
        res = expand(node[key], key)
        if res:
            print(res)


def slugify(word):
    return word.lower().replace(' ', "_").replace("-","_")


def expand_py(node, decision, fh):
    """ recursively build python file """

    terminalnode_template = """
    def f_%(key)s(%(key)s):
        if %(key)s:
            return prob['%(key)s']
        else:
            return 1.0 - prob['%(key)s']
    """
            
    template = """
    def f_%(decision)s(%(varlist)s, %(decision)s):
        cpt = {
 %(levelsrows)s
        }
        p = cpt[(%(varlist)s)]
        if %(decision)s:
            return p
        else:
            return 1.0 - p
    """
    if not node:
        return
    keys = node.keys()
    levels = []
    keynames = []
    decision_xls = decision.split('~')[0][:MAX_SHEETNAME_WIDTH]
    decision = slugify(decision.split('~')[0])

    for key in keys:
        ks = key.split("~")
        keynames.append(ks[0])

        if len(ks) == 1:
            level_iter = zip([ks[0]] * len(DEFAULT_LEVELS), DEFAULT_LEVELS)
        else:
            tls = ks[1].split(",")
            level_iter = zip([ks[0]] * len(tls), tls)

        levels.append(["~".join(x) for x in level_iter])

    headings = keynames + [decision]

    actual_levels = list(itertools.product(*levels))
    tf_levels = list(itertools.product(*([(True, False)] * len(keys))))  # assume first level == True
    level_dict = dict(zip(actual_levels, tf_levels))

    levelsrows = ""
    for actual, tf in level_dict.items():
        com = "            # %s" % (', '.join(["%s" % x for x in actual]))
      # row = "            (%s): %s" % (', '.join([str(x) for x in tf[i]]),  "0.5,")
        row = "            (%s): CPT['%s'][(%s)]," % (', '.join([str(x) for x in tf]), 
                                                    decision_xls,
                                                    ', '.join(["'%s'" % x for x in actual]))
        levelsrows += com + "\n" + row + "\n\n"

    varlist = ', '.join([slugify(x) for x in keynames])
    fh.write(template % locals())

    NODELIST.append(decision)

    for key in keys:
        if node[key]:
            res = expand_py(node[key], key, fh)
        else:
            newkey = slugify(key.split('~')[0])
            NODELIST.append(newkey)
            TERMLIST.append(newkey)
            fh.write(terminalnode_template % {'key': newkey})


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
        
    BOOK = xlwt.Workbook()
    expand(suitability, 'suitability')
    BOOK.save(CPT_XLS)


    with open(CPT_PY, 'w') as fh:
        fh.write("""from bayesian.bbn import build_bbn
########################## REMOVE ME ????
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dst')))
#########################################
from bbn.cpt.xls import xls2cptdict

def query_cpt(CPT, user_data=None, output_nodes=('suitability',)):
""")

        end_template = """
    levels = [True, False]
    net = build_bbn(
        %s

        # assume simple binary
        domains=dict(
            %s
        )
    )

    prob = dict(
    %s)

    if not user_data:
        user_data = {}

    for k,v in user_data.items():
        if k in prob:
            prob[k] = v

    nq = net.query()
    res = []
    for onode in output_nodes:
        res.append(nq[(onode, True)])

    return res


if __name__ == "__main__":
    inputnodes = {
        'water_rights': 0.7,
        'surrounding_ownership': 1.0,
        'identified_in_conservation_plan': 1.0,
        'relationship_to_protected_areas': 1.0,
        'intact_floodplain_forest': 1.0,
        'habitat_features': 1.0,
        'species_of_interest': 1.0,}

    CPT = xls2cptdict('%s')

    import random
    for i in range(10):
        k = random.choice(list(inputnodes.keys()))
        inputnodes[k] = random.random()

        val = query_cpt(CPT, inputnodes, output_nodes=(
            'suitability',
            'socio_economic',
            'site',
            'landscape')
        )
        print(val)

        """

        NODELIST = []
        TERMLIST = []
        expand_py(suitability, 'suitability', fh)

        fh.write(end_template % (
            '\n        '.join(["f_" + x + "," for x in NODELIST]),
            '\n            '.join(["%s = levels," % x for x in NODELIST]),
            '\n        '.join([x + " = 1.0," for x in TERMLIST]),
            CPT_XLS
            #'\n     '.join(["'" + x + "': 1.0," for x in TERMLIST]),
        ))
