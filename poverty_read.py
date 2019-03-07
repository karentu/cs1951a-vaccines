import csv, sqlite3

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE poverty(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"county TEXT, num_pov_all INTEGER, percent_pov_all INTEGER, num_pov_child INTEGER," +
"percent_pov_child INTEGER);") # use your column names here

with open('PovertyEstimates.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['State'], \
    i['Area_Name'], \
    i['POVALL_2017'], \
    i['PCTPOVALL_2017'], \
    i['POV017_2017'], \
    i['PCTPOV017_2017']) for i in dr]

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        if row[0] == "WA" and row[1] != 'Washington':
            del row[0]
            cur.execute("INSERT INTO poverty(" +
"county, num_pov_all, percent_pov_all, num_pov_child, percent_pov_child)" +
            " VALUES (?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

# cur.executemany("INSERT INTO washington(school_name, school_year, reported, k12_enrollment, " +
# "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
# "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
# "school_district, county, grade_levels)" +
# " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
