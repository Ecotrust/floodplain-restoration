import xlrd

def read_cpt(xls):
    workbook = xlrd.open_workbook(xls)
    sheet_res = {}
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
                    key.append(rowdict[state])
                key = tuple(key)
                rows[key] = value

            except IndexError:
                rowsleft = False
            rownum += 1

        sheet_res[sheetname] = rows
        
    return sheet_res



if __name__ == "__main__":
    import pprint 
    pprint.pprint(read_cpt('TNC_CPT_master.xls'))