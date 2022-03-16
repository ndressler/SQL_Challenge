'''
This python file will be used to answer the questions 
24 to 27
made for the SQL Challenge,
the task will be presente as a comment and bellow its respective code,
the answer will be generated by running the code.
'''

from csv import list_dialects
from importlib.machinery import FrozenImporter
from os import confstr_names
import sqlite3
from threading import local

conn = sqlite3.connect('cocktails_database.sqlite')
c = conn.cursor()


# Task 24: A cocktail consists of several ingredients. 
# The number of units of each Ingredients per cocktail are listed in the table INGREDIENT_COCKTAIL.

#(a) The number of ingredients per cocktail.

c.execute('''
SELECT Cocktail.cname,
    COUNT(Ingredient_Cocktail.zid)
FROM Ingredient_Cocktail, Cocktail
WHERE Ingredient_Cocktail.cid = Cocktail.cid
GROUP BY Cocktail.cid
''')
ing_per_cocktail = c.fetchall()
print("Task 24(a):\nThis are the number of ingredients per cocktail:")
for i in ing_per_cocktail:
    if i[1] == 1:
        print(f"The cocktail {i[0]} has {i[1]} ingredient.")
    else: print(f"The cocktail {i[0]} has {i[1]} ingredients.")

#(b) The number of ingredients per cocktail is required, but only for cocktails with more than 2 ingredients.

c.execute('''
SELECT Cocktail.cname,
    COUNT(Ingredient_Cocktail.zid)
FROM Ingredient_Cocktail, Cocktail
WHERE Ingredient_Cocktail.cid = Cocktail.cid
GROUP BY Cocktail.cid
HAVING COUNT(*) > 2
''')
more_than_2_ing = c.fetchall()
print("\nTask 24(b):\nThis are the number of ingredients for the cocktails that require more than 2:")
for i in more_than_2_ing:
    print(f"The cocktail {i[0]} has {i[1]} ingredients.")

#(c) The sum of the units of measure of the respective ingredients per cocktail is sought.

c.execute('''
SELECT Cocktail.cname,
    SUM(Ingredient_Cocktail.menge)
FROM Ingredient_Cocktail, Cocktail
WHERE Ingredient_Cocktail.cid = Cocktail.cid
GROUP BY Ingredient_Cocktail.cid
''')
ing_units = c.fetchall()
print("\nTask 24(c):\nThis are the units of measure of the respective ingredients per cocktail:")
for i in ing_units:
    print(f"The cocktail {i[0]} has {i[1]} units.")

#(d) The sum of the units of measure of the respective alcoholic ingredients per cocktail is sought.

c.execute('''
SELECT Cocktail.cname,
    SUM(Ingredient_Cocktail.menge)
FROM Ingredient_Cocktail, Cocktail, Ingredient
WHERE Ingredient_Cocktail.cid = Cocktail.cid AND
    Ingredient_Cocktail.zid = Ingredient.zid AND
    Ingredient.alkoholgehalt != 0
GROUP BY Cocktail.cname
''')
ing_units_alcoholic = c.fetchall()
print("\nTask 24(d):\nThis are the units of measure of the respective alcoholic ingredients per cocktail:")
for i in ing_units_alcoholic:
    print(f"The cocktail {i[0]} has {i[1]} units.")

# Task 25: Determine the real alcohol content of all cocktails. 
# The real alcohol content is calculated from the sum of all 
# (alcohol content of the ingredient multiplied by the quantity units of the ingredient) 
# divided by the sum of all quantity units. Rename the attributes of the solution relation appropriately.

c.execute('''
SELECT cocktail.cname, a.alcool/b.quantidade
FROM (
	SELECT SUM(ingredient.alkoholgehalt*ingredient_cocktail.menge) alcool, cocktail.cid
	FROM ingredient_cocktail, ingredient, cocktail
	WHERE ingredient.zid = ingredient_cocktail.zid AND
		ingredient_cocktail.cid = cocktail.cid
	GROUP BY cocktail.cid
) a,
(	
	SELECT SUM(ingredient_cocktail.menge) quantidade, cocktail.cid
	FROM ingredient_cocktail, cocktail
	WHERE cocktail.cid = ingredient_cocktail.cid
	GROUP BY ingredient_cocktail.cid
) b, cocktail
WHERE a.cid = b.cid AND cocktail.cid = a.cid
''')
real_alco_content = c.fetchall()
print("\nTask 25:\nThis the real alcohol content per cocktail:")
for i in real_alco_content:
    print(f"The {i[0]} cocktail real alcohol content is {i[1]}.")

# Task 26: suppose the output of task 26 is in a View called "Cocktail_alcohol_Content".
# Determine the minimum and maximum of the alcohol content for the cocktails served in a restaurant.

c.execute('''
SELECT local.lname, max(a.alcool/b.quantidade), min(a.alcool/b.quantidade)
FROM (
	SELECT SUM(ingredient.alkoholgehalt*ingredient_cocktail.menge) alcool, cocktail.cid
	FROM ingredient_cocktail, ingredient, cocktail
	WHERE ingredient.zid = ingredient_cocktail.zid AND
		ingredient_cocktail.cid = cocktail.cid
	GROUP BY cocktail.cid
) a,
(	
	SELECT SUM(ingredient_cocktail.menge) quantidade, cocktail.cid
	FROM ingredient_cocktail, cocktail
	WHERE cocktail.cid = ingredient_cocktail.cid
	GROUP BY ingredient_cocktail.cid
) b, cocktail, local, cocktail_local
WHERE a.cid = b.cid AND cocktail.cid = a.cid AND cocktail.cid = cocktail_local.cid AND cocktail_local.lid = local.lid
group by local.lname
''')
max_min_bylocal = c.fetchall()
print("\nTask 26:\nThis are the served cocktails that posses the maximun and minimum alcohol content per restaurant:")
for i in max_min_bylocal:
    print(f"Restaurant {i[0]}: the drink with the maximum alcohol content is the {i[1]} and drink with the minimum alcohol content is the {i[2]}.")


# Task 27: output the names of the glasses used for more than 2 cocktails.

c.execute('''
SELECT glas.gname
FROM glas, cocktail
WHERE glas.gid = cocktail.gid
GROUP BY glas.gid
HAVING COUNT(cocktail.gid) > 2
''')
glasses_more_than_2 = c.fetchall()
glasses_more_than_2 = [x[0] for x in glasses_more_than_2]
print(f"\nTask 27:\nThis are the glasses that are used for more than 2 cocktails: {(', '.join(glasses_more_than_2))}")
