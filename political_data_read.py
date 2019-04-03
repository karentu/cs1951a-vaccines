import csv, sqlite3
"""
    POLITICAL CONTRIBUTIONS
    SOURCE: https://data.wa.gov/Politics/Contributions-to-Candidates-and-Political-Committe/kv7h-kjye

"""

file = "../data/Contributions_to_Candidates_and_Political_Committees.csv"
con = sqlite3.connect("""washington.db""")
cur = con.cursor()
cur.execute("""DROP TABLE IF EXISTS "political_contributions";""")


table = """CREATE TABLE political_contributions(id INTEGER PRIMARY KEY AUTOINCREMENT, political_party TEXT, county TEXT, year INTEGER, amount TEXT, primary_general TEXT, contributor_city TEXT, contributor_state TEXT, contributor_occupation TEXT);"""
cur.execute(table)

with open(file,'r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    [i['party'], \
    i['jurisdiction_county'], \
    i['election_year'], \
    i['amount'], \
    i['primary_general'], \
    i['contributor_city'], \
    i['contributor_state'], \
    i['contributor_occupation']] for i in dr]

    for row in to_db:
        if ((len(row[0]) > 0) and (len(row[1]) > 0)):
            str = """INSERT INTO political_contributions(political_party, county, year, amount, primary_general, contributor_city, contributor_state, contributor_occupation) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            cur.execute(str, row)

con.commit()
con.close()
