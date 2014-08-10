import xlrd
import xlwt

def expand(node, decision):
    """ recursively build excel file """
    DEFAULT_LEVELS = ['Suitable', 'Unsuitable']
    MAX_SHEETNAME_WIDTH = 25
    if not node:
        return
    keys = node.keys()
    levels = []
    keynames = []
    decision = decision.split('|')[0][:MAX_SHEETNAME_WIDTH]
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

def defn2xls(defn):
    BOOK = xlwt.Workbook()
    expand(suitability, 'suitability')
    BOOK.save(CPT_XLS)
 
def xls2cptdict(xls, add_tilde=False):
    workbook = xlrd.open_workbook(xls)
    cptdict = {}
    for sheetname in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheetname)
        header = [x.value for x in sheet.row(0)]
        states = []
        for item in header:
            if item == sheetname:
                break
            states.append(item)

        rowsleft = True
        rows = {}
        rownum = 1
        while rowsleft:
            try:
                rowlist = [x.value for x in sheet.row(rownum)]
                rowdict = dict(zip(header, rowlist))
                value = float(rowdict[sheetname]) / 100.0
                key = []
                for state in states:
                    if add_tilde:
                        key.append("{}~{}".format(state, rowdict[state]))
                    else:
                        key.append("{}".format(rowdict[state]))
                key = tuple(key)
                rows[key] = value

            except IndexError:
                rowsleft = False
            rownum += 1

        cptdict[sheetname] = rows
        
    return cptdict

def cptdict2xls(cptdict, xls):
    book = xlwt.Workbook()

    for sheetname, sheetdata in cptdict.items():
        # TODO create new sheet

        # columns should all be the same
        cols = [x.split("~")[0] for x in list(sheetdata.keys())[0]]
        cols.append(sheetname)

        sheet = book.add_sheet(sheetname)

        rowx = 0
        heading_fmt = xlwt.easyxf('font: bold on; align: wrap off, vert centre, horiz center')
        for colx, value in enumerate(cols):
            sheet.write(rowx, colx, value, heading_fmt)

        for k, v in sheetdata.items():
            row = []
            for oldkey in k:
                row.append(oldkey.split("~")[1])
            row.append(v)
            rowx += 1
            for colx, value in enumerate(row):
                sheet.write(rowx, colx, value)

    book.save(xls)
    return xls
        


if __name__ == "__main__":
    cptd = xls2cptdict('../../../data/cpt_orig.xls', add_tilde=True)
    cptdict2xls(cptd, '/tmp/cpt_out.xls')
    
