import csv, sqlite3

con = sqlite3.connect('washington.db')
cur = con.cursor()
files = {'wa_1617.csv', 'wa_1516.csv', 'wa_1415.csv'}

def delete_tables():
    cur.execute('DROP TABLE IF EXISTS "schools";')
    cur.execute('DROP TABLE IF EXISTS "vaccination";')

def create_school_table():
    cur.execute("CREATE TABLE schools(id INTEGER PRIMARY KEY AUTOINCREMENT, school_name TEXT NOT NULL);")

def create_vaccination_table():
    cur.execute("CREATE TABLE vaccination(id INTEGER, " +
    "school_year INTEGER NOT NULL, k12_enrollment INTEGER NOT NULL, all_immunizations INTEGER NOT NULL, " +
    "any_exempt INTEGER NOT NULL, medical_exempt INTEGER NOT NULL, personal_exempt INTEGER NOT NULL, religious_exempt INTEGER NOT NULL, religious_mem_exempt INTEGER NOT NULL, " +
    "diphtheria_tetanus INTEGER NOT NULL, pertussis INTEGER NOT NULL, mmr INTEGER NOT NULL, polio INTEGER NOT NULL, hepatitisB INTEGER NOT NULL, varicella INTEGER NOT NULL, " +
    "school_district TEXT NOT NULL, county TEXT NOT NULL, start_grade INTEGER NOT NULL, end_grade INTEGER NOT NULL, FOREIGN KEY(id) REFERENCES schools(id));")

def get_school_id(school_name):
    cur.execute("SELECT id FROM schools WHERE school_name=?", (school_name,))
    id = cur.fetchone()
    if (id):
        return id[0]
    else:
        insert_into_schools_db(school_name)
        return get_school_id(school_name)

def main():
    delete_tables()
    create_school_table()
    create_vaccination_table()
    for file in files:
        with open(file,'r') as fin: # `with` statement available in 2.5+
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
                row[-2] = row[-2].lower().capitalize()
                if (row[2] == 'Y'): # check to see if it was reported
                    del row[2]
                    school_year, _ = row[1].split('-')
                    row[1] = school_year
                    grade_levels = row[-1]
                    del row[-1]
                    row = clean_grades(grade_levels, row)
                    if (row):
                        row[0] = get_school_id(row[0])
                        insert_into_vacc_db(row)

    con.commit()
    con.close()

def clean_grades(grade_levels, row):
    if ('-' in grade_levels):
        start, end = grade_levels.split('-')
    elif ('/' in grade_levels):
        start, end = grade_levels.split('/')
    else:
        return
    start_year, end_year = process_grades(start, end)
    row.append(start_year)
    row.append(end_year)
    return row

def process_grades(start, end):
    start_grade = start.strip()
    end_grade = end.strip()
    if (start_grade == 'K'):
        start_grade = 0
    elif (start_grade == 'PK' or start_grade == 'P'):
        start_grade = -1
    else:
        if (not start_grade.isdigit()):
            print("start grade: " + str(start_grade))

    if (end_grade == 'K'):
        end_grade = 0
    elif (end_grade == 'PK' or end_grade == 'P'):
        end_grade = -1
    else:
        if (not end_grade.isdigit()):
            print("end grade: " + str(end_grade))
    return start_grade, end_grade

def insert_into_schools_db(school_name):
    cur.execute("INSERT INTO schools(school_name) VALUES (?);", (school_name, ))

def insert_into_vacc_db(row):
    cur.execute("INSERT INTO vaccination(id, school_year, k12_enrollment, " +
    "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
    "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
    "school_district, county, start_grade, end_grade)" +
    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

if __name__== "__main__":
  main()
