import itertools
import xlwt
import os
import json

CPT_XLS = "cpt.xls"
DEFINITION = 'definition.json'
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
        keynames.append(ks[0])
        if len(ks) == 1:
            levels.append(DEFAULT_LEVELS)
        else:
            levels.append(ks[1].split(","))

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

with open(DEFINITION, 'r') as fh:
    suitability = json.loads(fh.read())
    
if not os.path.exists(CPT_XLS):
    BOOK = xlwt.Workbook()
    expand(suitability, 'suitability')
    BOOK.save(CPT_XLS)


def slugify(word):
    return word.lower().replace(' ', "_").replace("-","_")


def expand_py(node, decision):
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
            levels.append(DEFAULT_LEVELS)
        else:
            levels.append(ks[1].split(","))

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
    print(template % locals())

    NODELIST.append(decision)

    for key in keys:
        if node[key]:
            res = expand_py(node[key], key)
        else:
            newkey = slugify(key.split('~')[0])
            NODELIST.append(newkey)
            TERMLIST.append(newkey)
            print(terminalnode_template % {'key': newkey})


print("""from bayesian.bbn import build_bbn
from bayes_xls import read_cpt
from flask import Flask, jsonify, redirect, request, render_template

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def main():
    items = USER_DATA.items()
    items.sort()
    length = len(items)
    n = 11
    b = range(0, length, n)
    return render_template("sliders.html", 
        user_data1=items[b[0]:b[0]+n],
        user_data2=items[b[1]:b[1]+n],
        user_data3=items[b[2]:b[2]+n],
        user_data4=items[b[3]:b[3]+n]
    )

@app.route('/query', methods = ['GET'])
def prob_json():
    print "#" * 80
    user_data = USER_DATA.copy()
    for k, v in request.args.items():
        newval = float(v) / 100.0
        if user_data[k] != newval:
            print k, v
        user_data[k] = newval

    prob = query_cpt(user_data)
    print "!!!!!!", prob
    print "#" * 80
    return jsonify({'restore': round(prob * 100, 2)})

CPT = read_cpt('%s')

def query_cpt(user_data=None):
    if not user_data:
        user_data = {}

""" % CPT_XLS)

NODELIST = []
TERMLIST = []
expand_py(suitability, 'suitability')

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

    for k,v in user_data.items():
        if prob.has_key(k):
            prob[k] = v

    return net.query()[('suitability', True)]

USER_DATA = {
    %s}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)
    #print query_cpt(USER_DATA)
"""
print(end_template % (
    '\n        '.join(["f_" + x + "," for x in NODELIST]),
    '\n            '.join(["%s = levels," % x for x in NODELIST]),
    '\n        '.join([x + " = 1.0," for x in TERMLIST]),
    '\n     '.join(["'" + x + "': 1.0," for x in TERMLIST]),
))
