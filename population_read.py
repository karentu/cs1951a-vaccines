import csv, sqlite3

# Population Data
# Data from https://www.ers.usda.gov/data-products/county-level-data-sets/download-data.aspx

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE population(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"county TEXT, pop_chg_2015 INTEGER, pop_chg_2016 INTEGER, pop_chg_2017 INTEGER," +
"birth_2015 INTEGER, birth_2016 INTEGER, birth_2017 INTEGER, int_mig_2015 INTEGER," +
"int_mig_2016 INTEGER, int_mig_2017 INTEGER, dom_mig_2015 INTEGER," +
" dom_mig_2016 INTEGER, dom_mig_2017 INTEGER);") # use your column names here

with open('PopulationEstimates.csv','r', encoding ='latin-1') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['State'], \
    i['Area_Name'], \
    i['N_POP_CHG_2015'], \
    i['N_POP_CHG_2016'], \
    i['N_POP_CHG_2017'], \
    i['Births_2015'], \
    i['Births_2016'], \
    i['Births_2017'], \
    i['INTERNATIONAL_MIG_2015'], \
    i['INTERNATIONAL_MIG_2016'], \
    i['INTERNATIONAL_MIG_2017'], \
    i['DOMESTIC_MIG_2015'], \
    i['DOMESTIC_MIG_2016'], \
    i['DOMESTIC_MIG_2017']) for i in dr]

    # [2] - Numeric Change in resident total population 7/1/2014 to 7/1/2015
    # [3] - Numeric Change in resident total population 7/1/2015 to 7/1/2016
    # [4] - Numeric Change in resident total population 7/1/2015 to 7/1/2017
    # [5] -Births in period 7/1/2014 to 6/30/2015
    # [6] -Births in period 7/1/2015 to 6/30/2016
    # [7] -Births in period 7/1/2016 to 6/30/2017
    # [8] - Net international migration in period 7/1/2014 to 6/30/2015
    # [9] - Net international migration in period 7/1/2015 to 6/30/2016
    # [10] - Net domestic migration in period 7/1/2014 to 6/30/2015
    # [11] - Net domestic migration in period 7/1/2015 to 6/30/2016
    # [12] - Net domestic migration in period 7/1/2016 to 6/30/2017

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        if row[0] == 'WA':
            if row[1].endswith('County'):
                del row[0]
                row[0] = row[0][:-7]
                print(row[0])
                cur.execute("INSERT INTO population(" +
                "county, pop_chg_2015, pop_chg_2016, pop_chg_2017," +
                "birth_2015, birth_2016, birth_2017, int_mig_2015," +
                "int_mig_2016, int_mig_2017, dom_mig_2015," +
                " dom_mig_2016, dom_mig_2017)" +
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

con.commit()
con.close()
