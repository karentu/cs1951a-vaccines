import csv, sqlite3
"""
    POVERTY ESTIMATES
    SOURCE: https://data.wa.gov/Demographics/Poverty-Estimates-for-Washington-Counties-Age-0-17/d9f5-fgsr

"""
file = "../data/Poverty_Estimates_for_Washington_Counties_Age_0-17.csv"

con = sqlite3.connect("""washington.db""")
cur = con.cursor()

#delete before adding
cur.execute("""DROP TABLE IF EXISTS "poverty_estimates";""")
table = """CREATE TABLE poverty_estimates(id INTEGER PRIMARY KEY AUTOINCREMENT, county TEXT, poverty_2012 INTEGER, percent_of_0_through_17_2012 DECIMAL, poverty_2011 INTEGER, poverty_2010 INTEGER);"""
cur.execute(table)

with open(file,'r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    [i['County'], \
    i['2012 Poverty'], \
    i['2012 % of 0-17 Population'], \
    i['2011 Poverty '], \
    i['2010 Poverty']] for i in dr]

    for row in to_db:
        str = """INSERT INTO poverty_estimates(county, poverty_2012, percent_of_0_through_17_2012, poverty_2011, poverty_2010) VALUES (?, ?, ?, ?, ?);"""
        cur.execute(str, row)

con.commit()
con.close()
