import itertools
import xlwt
import random 

suitability = {
    'Landscape': {
        'Conservation value': {
            'Relationship to protected areas|Connected,Disconnected': None,
            'Identified in conservation plan|Identified,Not Identified': None,
            'Biotic conditions|Suitable,Unsuitable': {
                'Habitat features|Suitable,Unsuitable': {
                    'Cold water refugia|Exists,Does not exist': None,
                    'Intact floodplain forest|Intact,Missing': None,
                    'Other|Suitable,Not Suitable': None
                },
                'Species of interest|Present,Not Present': None
            }
        },
        'Abiotic conditions': {
            'Water quality|High Quality,Low Quality': None,
            'Connectivity barriers|Connected,Disconnected': {
                'Upstream|Connected,Disconnected': None,
                'Downstream|Connected,Disconnected': None,
                'On property|Connected,Disconnected': None,
            }
        },
        'Geomorphic Controls': {
            'Channel mobility|Mobile,Not mobile': None,
            'Material availability|Available,Unavailable': None,
            'Substrate|Suitable,Unsuitable': None,
            'Infrastructure constraints|No restrictions,Unsuitable': None,
        },
        'Floodplain characteristics': {
            'Gradient|Suitable,Unsuitable': None,
            'Width|Suitable,Unsuitable': None,
            'Within X-year floodplain|Within,Outside': None,
            'Location in floodplain|Strategic,Ineffective': None,
        }
    },
    'Socio-Economic': {
        'Cost benefit|Costly,Inexpensive': {
            'Public perception|Supportive,Unfavorable': None,
            'Contamination or Hazardous waste|Clean,Contaminated': None,
            'Property value|Costly,Inexpensive': None,
        },
        'Threats to other areas or Permittability': {
            'Surrounding ownership|Ammenable,Unfriendly': None,
            'Surrounding land use|Ammenable,Unfriendly': None,
            'Water rights|Threatened,No threats': None,
            'Infrastructure|Threatened,No threats': {
                'Levies|Threatened,No threats': None,
                'Dams|Threatened,No threats': None,
                'Structures|Threatened,No threats': None,
                'Bridges|Threatened,No threats': None,
                'Road crossings|Threatened,No threats': None,
            }
        },
    },
    'Site': {
        'Practical property-level restorability': {
            'Continuing property access': None,
            'Fill material availability|Available,Unavailable': None,
            'Site accessibility|Accessible,Inaccessible': None,
        },
        'Pit restorability': {
            'Water quality threat': {
                'Contamination': None,
                'Restorable Substrate': None,
            },
            'Practical restorability': {
                'Adjacent river depth': None,
                'Pit-adjacent levees': None,
                'Slope distance to river': None,
            },
            'Pit geometry': {
                'Surface area': None,
                'Circumference': None,
                'Bank slope': None,
                'Depth': None,
            },
        },
    }
}

DEFAULT_LEVELS = ['Suitable', 'Unsuitable']

def expand(node, decision):
    """ recursively build excel file """
    if not node:
        return
    keys = node.keys()
    levels = []
    keynames = []
    decision = decision.split('|')[0]
    sheet = BOOK.add_sheet(decision[:24])
    for key in keys:
        ks = key.split("|")
        keynames.append(ks[0])
        if len(ks) == 1:
            levels.append(DEFAULT_LEVELS)
        else:
            levels.append(ks[1].split(","))

    rowx = 0
    headings = keynames + [decision]
    heading_fmt = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value, heading_fmt)

    aa = itertools.product(*levels)

    for bb in aa:
        row = [str(x) for x in bb] + ["50"]
        rowx += 1
        for colx, value in enumerate(row):
            sheet.write(rowx, colx, value)

    for i in range(len(row)):
        sheet.col(i).width =  0x0d00 + 100
        
    for key in keys:
        res = expand(node[key], key)
        if res:
            print res

BOOK = xlwt.Workbook()
expand(suitability, 'Suitability')
BOOK.save('test.xls')


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
    decision = slugify(decision.split('|')[0])

    for key in keys:
        ks = key.split("|")
        keynames.append(ks[0])
        if len(ks) == 1:
            levels.append(DEFAULT_LEVELS)
        else:
            levels.append(ks[1].split(","))

    headings = keynames + [decision]

    aa = itertools.product(*levels)
    tf = list(itertools.product(*([(True, False)] * len(keys))))  # assume first level == True

    levelsrows = ""
    for i, bb in enumerate(aa):
        com = "            # %s" % (', '.join(["%s" % x for x in bb]))
        #row = "            (%s): %s" % (', '.join(["'%s'" % x for x in tf[i]]), "50")
        row = "            (%s): %s" % (', '.join([str(x) for x in tf[i]]),  "0.5,")  # str(random.random()) + ",") 
        levelsrows += com + "\n" + row + "\n\n"

    varlist = ', '.join([slugify(x) for x in keynames])
    print template % locals()

    NODELIST.append(decision)

    for key in keys:
        if node[key]:
            res = expand_py(node[key], key)
        else:
            newkey = slugify(key.split('|')[0])
            NODELIST.append(newkey)
            TERMLIST.append(newkey)
            print terminalnode_template % {'key': newkey}


print """from bayesian.bbn import build_bbn

def main(user_data=None):
    if not user_data:
        user_data = {}
"""

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

if __name__ == "__main__":
    user_data = {
%s}

    print main(user_data)
"""
print end_template % (
    '\n        '.join(["f_" + x + "," for x in NODELIST]),
    '\n            '.join(["%s = levels," % x for x in NODELIST]),
    '\n        '.join([x + " = 0.5," for x in TERMLIST]),
    '\n        '.join(["'" + x + "': 0.5," for x in TERMLIST]),
)
