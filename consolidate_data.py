import csv, sqlite3

# con = sqlite3.connect('washington.db')
# c = con.cursor()


# #to export as csv file
# with open("wub.csv", "wb") as write_file:
#     cursor = connection.cursor()
#     for row in cursor.execute("SELECT * FROM table"):
#         writeRow = " ".join([str(i) for i in row])
#         write_file.write(writeRow.encode())

# c.close()
# con.close()


# Run your query, the result is stored as `data`
with sqlite3.connect('washington.db') as conn:
    cur = conn.cursor()
    sql = """SELECT e.id, e.county, rural_urban, urban_influence, less_than_high_school 
high_school, bachelors, 
clinton, trump, otherVotes, totalVotes,
num_pov_all, percent_pov_all, num_pov_child, percent_pov_child,
labor_total_2014, employed_2014, unemployed_2014,
labor_total_2015, employed_2015, unemployed_2015,
labor_total_2016, employed_2016, unemployed_2016,
labor_total_2017, employed_2017, unemployed_2017, 
med_household_income_2017, medHHIncome_percent_state_2017,
totalPop, white, black, native,
asian, pacificIslander, otherRace, multiracial,
hispanicLatino, whiteAlone
FROM education as e INNER JOIN politicalElection as pe
ON e.county = pe.county
INNER JOIN poverty as p
ON e.county = p.county
INNER JOIN unemployment as u
ON e.county = u.county
INNER JOIN raceEthnicity as r
on e.county = r.county;"""
    cur.execute(sql)
    data = cur.fetchall()




# Create the csv file
with open('county.csv', 'w') as f_handle:
    writer = csv.writer(f_handle)
    # Add the header/column names
    names = list(map(lambda x: x[0], cur.description))
    writer.writerow(names)
    # Iterate over `data`  and  write to the csv file
    for row in data:
        writer.writerow(row)


