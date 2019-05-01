import csv, sqlite3, re
"""
    DEMOGRAPHIC DATA BY SCHOOL
    SOURCE: http://reportcard.ospi.k12.wa.us/DataDownload.aspx

"""
def getfile(k,n):
    return "school_data/1" + str(k) + "_1" + str(n) + "_Demographic_Data_By_School.csv"

file_school_diretory = "school_data/Washington_School_Directory.csv"

# school name -> list( elems, elems, ... )
#           where each elems is list( school code, city, zip code, district code )
school_dir = {}

# Lowercases school name and gets rid of school in name because school names
# can sometimes either be Roosevelt Elementary School or Roosevelt Elementary
def clean_school_name(name):
    school = list(map(lambda x: x.lower(), name.split()))
    if (school[-1] == 'school' or school[-1] == 'sch' or school[-1] == 'schl'):
        del school[-1]
    return " ".join(school)

def clean_str(inp):
    return inp.strip().lower()

def clean_code(num):
    return re.sub('[^0-9]','', num)

# zip codes come in 2 different versions: 98331-0000 or 98331
# this only returns the first
def clean_zip(zipcode):
    nums = list(map(lambda x: x.strip().lower(), zipcode.split('-')))
    if len(nums) > 2:
        print("UNEXPECTED BEHAVIOR SEE THIS ZIP: ", nums)
    return nums[0]

def main():
    with open (file_school_diretory, 'r') as fin:
        dr = csv.DictReader(fin)
        pre_school_directory = [\
        [i['SchoolCode'], \
        i['SchoolName'], \
        i['City'], \
        i['ZipCode'], \
        i['LEACode']] for i in dr]

        for row in pre_school_directory:
            clean = clean_school_name(row[1])
            if clean not in school_dir:
                school_dir[clean] = []
            school_dir[clean].append([clean_code(row[0]), clean_str(row[2]), clean_zip(row[3]), clean_code(row[4])])

    #########################################################################
    ########## Actual stuff for db
    #########################################################################




    con = sqlite3.connect("""washington.db""")
    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS "school_dem";')


    table = """CREATE TABLE school_dem(id INTEGER PRIMARY KEY AUTOINCREMENT, \
        county TEXT, school TEXT, total_enrollment INTEGER, school_american_indian_alaskan_native INTEGER, \
        school_asian INTEGER, school_asian_pacific_islander INTEGER, school_pacific_islander INTEGER, \
        school_black INTEGER, school_hispanic INTEGER, school_white INTEGER, school_two_or_more_race INTEGER, \
        male INTEGER, female INTEGER, num_free_reduced_meals INTEGER, \
        district_number TEXT, city TEXT, zip TEXT, school_code TEXT, year INTEGER);"""

    cur.execute(table)
    with open('clean_school_data.csv', 'w') as s_file:
        headers = ['county', 'school', 'total_enrollment', 'american_indian_alaskan_native', \
        'asian', 'asian_pacific_islander', 'pacific_islander', 'black', 'hispanic', \
        'white', 'two_or_more_race', 'male', 'female', 'num_free_reduced_meals', \
        'district_number', 'city', 'zip', 'school_code', 'year']

        swrite = csv.writer(s_file, delimiter=',')
        swrite.writerow(headers)

        for index in range(4):
            k = 4+index
            n = 5+index
            with open(getfile(k,n),'r') as fin: # `with` statement available in 2.5+
                # csv.DictReader uses first line in file for column headings by default
                dr = csv.DictReader(fin) # comma is default delimiter

                to_db = [\
                [i['County'], \
                i['School'], \
                i['TotalEnrollment'], \
                i['NumberAmericanIndianorAlaskanNative'], \
                i['NumberAsian'], \
                i['NumberPacificIslander'], \
                i['NumberAsianPacificIslander'], \
                i['NumberBlack'], \
                i['NumberHispanic'], \
                i['NumberWhite'], \
                i['NumberTwoOrMoreRaces'], \
                i['NumberMales'], \
                i['NumberFemales'], \
                i['NumberFreeorReducedPricedMeals'], \
                i['CountyDistrictNumber']] for i in dr]

                for row in to_db:
                    clean_school = clean_school_name(row[1])
                    row[1] = clean_school
                    clean_county = clean_str(row[0])
                    row[0] = clean_county
                    zip = ""
                    code = ""
                    city = ""

                    #school does not have a school code
                    if (clean_school not in school_dir):
                        #print(clean_school, " DOES NOT EXIST IN STATE DIRECTORY")
                        continue


                    if (len(school_dir[clean_school]) < 2):
                        lea_code = school_dir[clean_school][0][3]
                        if (row[-1] == ""):
                            row[-1] = lea_code
                        zip = school_dir[clean_school][0][2]
                        city = school_dir[clean_school][0][1]
                        code = school_dir[clean_school][0][0]

                    else:
                        issue = 1
                        for ls in school_dir[clean_school]:
                            if (row[-1] == ls[3]):
                                issue -= 1
                                zip = ls[2]
                                code = ls[0]
                                city = ls[1]
                                if (row[-1] == ""):
                                    row[-1] = school_dir[clean_school][0][3]

                        #if (issue < 0):
                            #print("ALERT: ", clean_school," MORE THAN ONE SCHOOL WITH SAME NAME AND DISTRICT CODE")
                            #never hits this case
                        # if the school is not (the district codes don't match)
                        # usually due to incorrectly or not fully writing name
                        if (issue > 0):
                            #print("ALERT: ", clean_school," NEVER FOUND")
                            continue

                    insert_this = row.copy()
                    insert_this.append(city)
                    insert_this.append(zip)
                    insert_this.append(code)
                    ## TODO SEE THIS LINE
                    insert_this.append(2015+index)

                    if ("" in insert_this):
                        continue

                    if (insert_this[2] == "0"):
                        continue

                    swrite.writerow(insert_this)

                    insrt_str = """INSERT INTO school_dem(county, school, total_enrollment, \
                        school_american_indian_alaskan_native, school_asian, school_asian_pacific_islander, school_pacific_islander, \
                        school_black, school_hispanic, school_white, school_two_or_more_race, male, female, num_free_reduced_meals, \
                        district_number, city, zip, school_code, year) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                    cur.execute(insrt_str, insert_this)

    con.commit()
    con.close()

if __name__== "__main__":
  main()
