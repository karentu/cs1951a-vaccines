import csv, sqlite3
"""
    MEDIAN HOUSEHOLD INCOME
    SOURCE: https://www.ofm.wa.gov/washington-data-research/economy-and-labor-force/median-household-income-estimates

"""

file = "median_household_income_estimates.csv"
#create db
con = sqlite3.connect("""washington.db""")
cur = con.cursor()


# NOTE: THE CSV FILE HAD AN EMPTY STRING AS THE HEADER FOR THE COUNTY SO
#       I ADDED THE WORD 'County' TO LINE 5 OF THE CSV
def clean(s):
    return str(s).strip().replace(',','')

#delete before adding
cur.execute("""DROP TABLE IF EXISTS "median_household_income_estimates";""")
table = """CREATE TABLE median_household_income_estimates(id INTEGER PRIMARY KEY AUTOINCREMENT, county TEXT, census_2009 INTEGER, estimate_2010 INTEGER, estimate_2011 INTEGER, estimate_2012 INTEGER, estimate_2013 INTEGER, estimate_2014 INTEGER, estimate_2015 INTEGER, prelim_estimate_2016 INTEGER, projection_2017 INTEGER);"""
cur.execute(table)

with open(file,'r') as fin: # `with` statement available in 2.5+
    # # skipping the first few lines
    # next(fin)
    # next(fin)
    # next(fin)
    # next(fin)

    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    [i['County'], \
    i['2009'], \
    i['2010'], \
    i['2011'], \
    i['2012'], \
    i['2013'], \
    i['2014'], \
    i['2015'], \
    i['2016'], \
    i['2017']] for i in dr]

    for row in to_db:
        if (len(row[0]) > 0):
            # clean = list(map(lambda s: s.strip().replace(',',''), row))
            row = list(row)
            row[0] = row[0] + " County"
            sql_string = """INSERT INTO median_household_income_estimates(county, census_2009, estimate_2010, estimate_2011, estimate_2012, estimate_2013, estimate_2014, estimate_2015, prelim_estimate_2016, projection_2017) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
            cur.execute(sql_string, row)

con.commit()
con.close()
