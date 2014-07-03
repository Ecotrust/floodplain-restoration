import csv
from slugify import slugify

lookup = dict()
header = None

# load lookup
with open('testsites_lookup.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if header == None:
            header = row
            continue
        # off-by-one
        k = int(row[0]) - 1

        try:
            v = (row[1], float(row[2]))
        except ValueError:
            continue
        lookup[k] = v

print lookup

# loop through xls sheets
import xlrd
workbook = xlrd.open_workbook('TestSites_mp.xls')
print workbook.sheet_names()

# tuples of socio_economic, site, landscape
scoring = {
    u'Coast Fork Site': (1.00, .85, .75),
    u'Pudding Ponds Site': (1.00, .95, .85),
    u'Lower Middle Fork Site': (.80, .40, .75),
    u'Turtle Flats Site': (.70, .85, .75),
    u'Delta Ponds Site': (.35, .60, .70),
    u'Green Island': (.100, .80, .85),
    u'Russian River Site': (.50, .40, .30),
    u"Bower's Rock Site": (.60, .50, .75)
}

for sheetname, scores in scoring.items():
    print sheetname
    worksheet = workbook.sheet_by_name(sheetname)
    nrows = worksheet.nrows
    with open(slugify(sheetname) + ".txt", 'w') as fh:
        for rownum in xrange(nrows):
            val = worksheet.cell_value(rownum, 1)
            try:
                val = val.lower()
            except:
                continue

            if val == 'x':
                res = lookup[rownum]
                print "\t", res
                fh.write("%s,%s\n" % res)

        for x in zip("socio_economic site landscape".split(), scores):
            print "\t", x
            fh.write("%s,%s\n" % x)

