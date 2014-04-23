import itertools
import xlwt

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
                'Substrate': None,
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
