import xlrd

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
 
def xls2cptdict(xls):
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
                    # TODO tilde delimited ? 
                    #key.append("{}~{}".format(state, rowdict[state]))
                    key.append("{}".format(rowdict[state]))
                key = tuple(key)
                rows[key] = value

            except IndexError:
                rowsleft = False
            rownum += 1

        cptdict[sheetname] = rows
        
    return cptdict

def cptdict2xls(cptdict, xls):
    for sheetname, sheetdata in cptdict.items():
        # TODO create new sheet

        # columns should all be the same
        cols = [x.split("~")[0] for x in list(sheetdata.keys())[0]]
        print(sheetname)
        print(cols)
        print()
        print(sheetdata)
        print()
        print()
        print()
        # TODO write sheetdata to rows
        #  renamed headers accd to cols

        #print("{}\n\t{}".format(sheetname, sheetdata))
        


if __name__ == "__main__":
    cptd = xls2cptdict('cpt.xls')
    cptdict2xls(cptd, 'cpt_out.xls')
    
