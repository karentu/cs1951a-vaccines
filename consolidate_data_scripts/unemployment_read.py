import csv, sqlite3


def main():
    con = sqlite3.connect('washington.db')
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS "unemployment";')
    cur.execute("CREATE TABLE unemployment(id INTEGER PRIMARY KEY AUTOINCREMENT," +
    "county TEXT, labor_total_2014 INTEGER, employed_2014 INTEGER, unemployed_2014 INTEGER," + 
    "labor_total_2015 INTEGER, employed_2015 INTEGER, unemployed_2015 INTEGER," + 
    "labor_total_2016 INTEGER, employed_2016 INTEGER, unemployed_2016 INTEGER," +
    "labor_total_2017 INTEGER, employed_2017 INTEGER, unemployed_2017 INTEGER," +  
    "med_household_income_2017 INTEGER, medHHIncome_percent_state_2017 INTEGER);") # use your column names here

    with open('Unemployment.csv','r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [\
        (i['State'], \
        i['Area_name'], \
        i[' Civilian_labor_force_2014 '], \
        i[' Employed_2014 '], \
        i[' Unemployed_2014 '], \
        i[' Civilian_labor_force_2015 '], \
        i[' Employed_2015 '], \
        i[' Unemployed_2015 '], \
        i[' Civilian_labor_force_2016 '], \
        i[' Employed_2016 '], \
        i[' Unemployed_2016 '], \
        i['Civilian_labor_force_2017'], \
        i['Employed_2017'], \
        i['Unemployed_2017'], \
        i['Median_Household_Income_2017'], \
        i['Med_HH_Income_Percent_of_State_Total_2017']) for i in dr]

        to_db_lst = list(to_db)
        for row in to_db_lst:
            row = list(row)
            if row[0] == "WA" and row[1] != 'Washington':
                del row[0]
                row[0] = row[0].replace(" County, WA", "").lower()
                cur.execute("INSERT INTO unemployment(" +
    "county, labor_total_2014, employed_2014, unemployed_2014," + 
    "labor_total_2015, employed_2015, unemployed_2015," + 
    "labor_total_2016, employed_2016, unemployed_2016," +
    "labor_total_2017, employed_2017, unemployed_2017," +  
    "med_household_income_2017, medHHIncome_percent_state_2017)" +
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

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
