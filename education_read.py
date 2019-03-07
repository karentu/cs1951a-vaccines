import csv, sqlite3

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE education(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"county TEXT, rural_urban INTEGER, " +
"urban_influence INTEGER, less_than_high_school INTEGER, high_school INTEGER, some_college INTEGER,"
"bachelors INTEGER);") # use your column names here

with open('Education.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['State'], \
    i['Area name'], \
    i['2013 Rural-urban Continuum Code'],\
    i['2013 Urban Influence Code'],\
    i['Less than a high school diploma, 2013-17'],\
    i['High school diploma only, 2013-17'],\
    i['Some college or associate\'s degree, 2013-17'],\
    i['Bachelor\'s degree or higher, 2013-17']) for i in dr]

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        if row[0] == "WA" and row[1] != 'Washington':
            del row[0]
            cur.execute("INSERT INTO education(" +
"county, rural_urban, " +
"urban_influence, less_than_high_school, high_school, some_college,"
"bachelors)" +
            " VALUES (?, ?, ?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

# cur.executemany("INSERT INTO washington(school_name, school_year, reported, k12_enrollment, " +
# "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
# "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
# "school_district, county, grade_levels)" +
# " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
