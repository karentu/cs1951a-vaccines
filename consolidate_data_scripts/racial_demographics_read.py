import csv, sqlite3

def main():
    con = sqlite3.connect('washington.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS "raceEthnicity";')
    cur.execute("CREATE TABLE raceEthnicity(id INTEGER PRIMARY KEY AUTOINCREMENT," +
    "county TEXT, totalPop INTEGER, white INTEGER, black INTEGER, native INTEGER," +
    "asian INTEGER, pacificIslander INTEGER, otherRace INTEGER, multiracial INTEGER," +
    "hispanicLatino INTEGER, whiteAlone INTEGER);") # use your column names here

    with open('race.csv','r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [\
        (i['County'], \
        i['Total population'], \
        i['Percent of total population - Race - One Race - White'], \
        i['Percent of total population - Race - One Race - Black or African American'],\
        i['Percent of total population - Race - One Race - American Indian and Alaska Native'],\
        i['Percent of total population - Race - One Race - Asian'], \
        i['Percent of total population - Race - One Race - Native Hawaiian and Other Pacific Islander'],\
        i['Percent of total population - Race - One Race - Some Other Race'],\
        i['Percent of total population - Race - Two or More Races'], \
        i['Percent of total population - Hispanic or Latino (of any race)'],\
        i['Percent of total population - White Alone, not Hispanic or Latino']) for i in dr]

        to_db_lst = list(to_db)
        for row in to_db_lst:
            row = list(row)
            if row[0] != "Washington":
                row[0] = row[0].replace(" County", "").lower()
                cur.execute("INSERT INTO raceEthnicity(" +
        "county, totalPop, white, black, native," +
        "asian, pacificIslander, otherRace, multiracial," +
        "hispanicLatino, whiteAlone)" + 
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

        to_db = tuple(to_db_lst)

    # cur.executemany("INSERT INTO washington(school_name, school_year, reported, k12_enrollment, " +
    # "all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt, " +
    # "diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella, " +
    # "school_district, county, grade_levels)" +
    # " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

if __name__ == "__main__":
    main()
