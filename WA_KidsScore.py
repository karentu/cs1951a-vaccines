import csv, sqlite3

# Unexcused Absences Data
# Data from http://reportcard.ospi.k12.wa.us/DataDownload.aspx

def clean_school_name(name):
    school = list(map(lambda x: x.lower(), name.split()))
    if (school[-1] == 'school' or school[-1] == 'sch' or school[-1] == 'schl'):
        del school[-1]
    return " ".join(school)

def main():
    con = sqlite3.connect('washington.db')
    cur = con.cursor()
    #Notes - district name does not contain SCHOOL district
    cur.execute('DROP TABLE IF EXISTS "wakids";')
    cur.execute("CREATE TABLE wakids(id INTEGER PRIMARY KEY AUTOINCREMENT," +
    "district_code INTEGER, district TEXT, " +
    "school_code INTEGER, school TEXT, total_percent_absences REAL," +
    " low_income_absence_percent REAL);") # use your column names here

    # District Code/District/School Code/School/Grade 1-8 Students/Low Income
    # 14005/Aberdeen/2834/A J West Elementary/0.99%/1.23%

    with open('unexcusedabsences16-17.csv','r', encoding ='latin-1') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [\
        (i['District Code'], \
        i['District'], \
        i['School Code'], \
        i['School'], \
        i['Grade 1-8 Students'], \
        i['Low Income']) for i in dr]

        to_db_lst = list(to_db)
        for row in to_db_lst:
            row = list(row)
            if (not (row[4] == 'n/a' or row[0] == '')):
                row[1] = row[1].lower()
                row[3] = row[3].lower()
                row[3] = clean_school_name(row[3])
                cur.execute("INSERT INTO absences(district_code, district, school_code, " +
                "school, total_percent_absences, low_income_absence_percent)" +
                " VALUES (?, ?, ?, ?, ?, ?);", row)

        to_db = tuple(to_db_lst)

    con.commit()
    con.close()

if __name__== "__main__":
  main()
