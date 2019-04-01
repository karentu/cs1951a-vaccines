import csv, sqlite3

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE politicalElection(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"county TEXT, clinton INTEGER, " +
"trump INTEGER, otherVotes INTEGER, totalVotes INTEGER);") # use your column names here

with open('2016election.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['County'], \
    i['Clinton#'], \
    i['Trump#'],\
    i['Others (excluding write-ins)#'],\
    i['Total']) for i in dr]

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        row[0] = row[0].replace(" County", "")

        cur.execute("INSERT INTO politicalElection(" +
"county, clinton, " +
"trump, otherVotes, totalVotes)" +
            " VALUES (?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

# cur.executemany("INSERT INTO washington(school_name, school_year, reported, k12_enrollment, " +
# "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
# "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
# "school_district, county, grade_levels)" +
# " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
