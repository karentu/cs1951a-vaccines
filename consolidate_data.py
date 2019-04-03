import csv, sqlite3

# BEFORE RUNNING THIS run python3 on education_read, poverty_read, data_read,
#unemployment_read,  median_household_income_data_read, political_election_read,
#racial_demographics_read 


# Run your query, the result is stored as `data`
with sqlite3.connect('washington.db') as conn:
    cur = conn.cursor()
    sql = """SELECT e.id, e.county, rural_urban, urban_influence, less_than_high_school, 
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
hispanicLatino, whiteAlone,
census_2009, estimate_2010, estimate_2011, estimate_2012, estimate_2013,
estimate_2014, estimate_2015, prelim_estimate_2016, projection_2017,
s.id, school_name, 
school_year, k12_enrollment, 
all_immunizations, any_exempt, medical_exempt, personal_exempt, religious_exempt, religious_mem_exempt,
diphtheria_tetanus, pertussis, mmr, polio, hepatitisB, varicella,
school_district, start_grade, end_grade
FROM education as e INNER JOIN politicalElection as pe
ON e.county = pe.county
INNER JOIN poverty as pv
ON e.county = pv.county
INNER JOIN unemployment as u
ON e.county = u.county
INNER JOIN raceEthnicity as r
on e.county = r.county
INNER JOIN median_household_income_estimates as m
on e.county = m.county
INNER JOIN vaccination as v
on e.county = v.county
INNER JOIN schools as s
on v.id = s.id"""
    cur.execute(sql)
    data = cur.fetchall()


# food and population stuff

# INNER JOIN food as f
# on e.county = f.county
# INNER JOIN population as po
# on e.county = po.county
# census_2009, estimate_2010, estimate_2011, estimate_2012, estimate_2013,
# estimate_2014, estimate_2015, prelim_estimate_2016, projection_2017,
# census_tract, total_housing_units, low_access, low_access_low_income,
# kids_low_access_percent, snap_number, no_vehicle_number,
# pop_chg_2015, pop_chg_2016, pop_chg_2017,
# birth_2015, birth_2016, birth_2017, int_mig_2015,
# int_mig_2016, int_mig_2017, dom_mig_2015,
# dom_mig_2016, dom_mig_2017,



# Create the csv file
with open('complete.csv', 'w') as f_handle:
    writer = csv.writer(f_handle)
    # Add the header/column names
    names = list(map(lambda x: x[0], cur.description))
    writer.writerow(names)
    # Iterate over `data`  and  write to the csv file
    for row in data:
        writer.writerow(row)


