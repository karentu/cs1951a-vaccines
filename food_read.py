import csv, sqlite3

# Food Access Data
# Data from https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data/

con = sqlite3.connect('washington.db')
cur = con.cursor()
cur.execute("CREATE TABLE food(id INTEGER PRIMARY KEY AUTOINCREMENT," +
"census_tract INTEGER, county TEXT, total_housing_units INTEGER," +
" low_access BOOLEAN, low_access_low_income BOOLEAN, kids_low_access_percent REAL, " +
"snap_number INTEGER, no_vehicle_number INTEGER);") # use your column names here

with open('Food.csv','r', encoding ='latin-1') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [\
    (i['CensusTract'], \
    i['State'], \
    i['County'], \
    i['OHU2010'], \
    i['LA1and10'], \
    i['LILATracts_1And10'], \
    i['lakids10share'], \
    i['TractSNAP'], \
    i['TractHUNV']) for i in dr]

    # OHU2010 - Total number of housing units
    # LA1and10 - Flag for low access tract at 1 mile for urban areas or 10 miles for rural areas
    # LILATracts_1And10 - Flag for low income low access tract at same qualifications
    # lakids10share - Share of tract population that are kids beyond 10 miles from supermarket
    # TractSNAP - Housing units receiving SNAP benefits
    # TractHUNV - Housing units without a vehicle

    to_db_lst = list(to_db)
    for row in to_db_lst:
        row = list(row)
        if row[1] == 'Washington':
            del row[1]
            print(row)
            cur.execute("INSERT INTO food(" +
"census_tract, county, total_housing_units, low_access, low_access_low_income," +
" kids_low_access_percent, snap_number, no_vehicle_number)" +
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?);", row)

    to_db = tuple(to_db_lst)

con.commit()
con.close()
