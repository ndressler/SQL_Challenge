'''
This python file will be used to answer all the question 1 to made for the SQL Challenge,
the task will be presente as a comment and bellow will be the answer and the respective code.
'''

from os import confstr_names
import sqlite3

conn = sqlite3.connect('cocktails_database.sqlite')
c = conn.cursor()

# Task 1: Provide the names of all cocktails that exist in the database.

c.execute('''
SELECT cname FROM cocktail
''')
name_of_all_cocktails = c.fetchall()
print('Task 1:\nThis are the names of all cocktails that exist in the database: '+', '.join([x[0] for x in name_of_all_cocktails])+'\n')


# Task 2: Find all the information about places that have the postal code 39108.

c.execute('''
SELECT *
FROM local
WHERE local.plz = 39108
''')
zipinfo_39108 = c.fetchall()

lid_zip39108 = [] #local's id
lname_zip39108 = [] #local's name
stadt_zip39108 = [] #local's city

for tuple in zipinfo_39108:
    lid_zip39108.append(tuple[0])
    lname_zip39108.append(tuple[1])
    stadt_zip39108.append(tuple[3])

stadt_zip39108 = list(dict.fromkeys(stadt_zip39108)) # to exclude repetitive cities

print('Task 2:')
print("This are all the identity numbers of the locals that belong to the postal code 39108: "+(str(lid_zip39108)[1:-1]))
print("This are all the names of the locals that belong to the postal code 39108: "+(', '.join(lname_zip39108)))
print("Lastly, the postal code 39108 belongs to only one city: "+(', '.join(stadt_zip39108))+"\n")

# Task 3: Provide all postal codes (without duplicates).

c.execute('''
SELECT local.plz
FROM local
ORDER BY
    plz ASC
''')
all_zips = c.fetchall()
all_zips = list(dict.fromkeys(all_zips)) # remove duplicates
all_zips_clean = [x[0] for x in all_zips] # remove of tuple
print("Task 3:\nThis are all postal codes: "+(str(all_zips_clean)[1:-1]))

# Task 4: Which ingredient has an alcohol content greater than 30?

c.execute('''
SELECT ingredient.zname
FROM ingredient
WHERE ingredient.ALKOHOLGEHALT >= 30
''')
alcohol_30 = c.fetchall()
alcohol_30 = [x[0] for x in alcohol_30]
print("\nTask 4:\nThe ingredients that have an alcohol content greater than 30 are: "+(', '.join(alcohol_30)))

# Task 5: In a drinking game, everyone should play with everyone. Display the corresponding list of game pairs (Name, Name).

c.execute('''
SELECT person.name
FROM person
''')
all_people= c.fetchall()
all_people = [x[0] for x in all_people]

matches = []

for x in range(len(all_people)):
    for z in range(x + 1, len(all_people)):
        if x != z:
            matches.append((all_people[x],(all_people[z])))
print("\nTask 5:\nHere's the list of all round paired playes for the drinking game:\n"+ '\n'.join(map(str, matches)))

# Task 6: Display the names of all glasses and cocktails in a single-column table. Use a suitable quantity operation.

c.execute('''
SELECT cocktail.cname,
glas.gname
FROM Glas
LEFT JOIN Cocktail ON cocktail.gid = glas.gid
''')
gs_and_cs= c.fetchall()
all_gscs = [z for x in gs_and_cs for z in x if z != None]
all_gscs = list(dict.fromkeys(all_gscs)) 
print("\nTask 6:\nHere's the list of  names of all glasses and cocktails: "+(', '.join(all_gscs)))

# Task 7: for which cocktails there is still no recipe in the database (which cocktails are not mentioned in INGREDIENT_COCKTAIL)?
 
c.execute('''
SELECT cocktail.cname 
FROM cocktail 
WHERE cocktail.cname NOT IN (
    SELECT cocktail.cname 
    from ingredient_cocktail
    LEFT JOIN cocktail ON cocktail.cid = ingredient_cocktail.cid)
''')
c_ing_missing= c.fetchall()
c_ing_missing = [x[0] for x in c_ing_missing]
print("\nTask 7:\nThis are the cocktails which recipe are still not in the database: "+(', '.join(c_ing_missing)))

# Task 8:  In which restaurants is no Knieweich served?

c.execute('''
SELECT local.lname
FROM local
WHERE local.lid NOT IN (
    SELECT cocktail_local.lid
    FROM cocktail_local
    WHERE cocktail_local.cid = (
        SELECT cocktail.cid
        FROM cocktail
        WHERE cocktail.cname='Knieweich'
    )
)
''')
rest_not_knieweich= c.fetchall()
rest_not_knieweich = [x[0] for x in rest_not_knieweich]
print("\nTask 8:\nThis are the restaurants where Knieweich is not serverd: "+(', '.join(rest_not_knieweich)))