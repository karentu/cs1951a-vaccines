import csv, sqlite3

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE washington(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"school_name TEXT, school_year, k12_enrollment INTEGER, " +
"all_immunizations INTEGER, any_exempt INTEGER, medical_exempt INTEGER, personal_exempt INTEGER, religious_exempt INTEGER, religious_mem_exempt INTEGER, " +
"diphtheria_tetanus INTEGER, pertussis INTEGER, mmr INTEGER, polio INTEGER, hepatitisB INTEGER, varicella INTEGER, " +
"school_district TEXT, county TEXT, grade_levels);") # use your column names here

with open('wa_1617.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['School_Name'], \
    i['School_year'], \
    i['Reported'],\
    i['K_12_enrollment'],\
    i['Number_complete_for_all_immunizations'],\
    i['Number_with_any_exemption'],\
    i['Number_with_medical_exemption'],\
    i['Number_with_personal_exemption'],\
    i['Number_with_religious_exemption'],\
    i['Number_with_religious_membership_exemption'],\
    i['Number_exempt_for_diphtheria_tetanus'],\
    i['Number_exempt_for_pertussis'],\
    i['Number_exempt_for_measles_mumps_rubella'],\
    i['Number_exempt_for_polio'],\
    i['Number_exempt_for_HepatitisB'],\
    i['Number_exempt_for_varicella'],\
    i['School_District'],\
    i['County'],\
    i['Grade_Levels']) for i in dr]

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        if (row[2] == 'Y'):
            del row[2]
            cur.execute("INSERT INTO washington(school_name, school_year, k12_enrollment, " +
            "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
            "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
            "school_district, county, grade_levels)" +
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

# cur.executemany("INSERT INTO washington(school_name, school_year, reported, k12_enrollment, " +
# "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
# "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
# "school_district, county, grade_levels)" +
# " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()
