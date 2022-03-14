'''
This python file will be used to answer all the question 1 to made for the SQL Challenge,
the task will be presente as a comment and bellow will be the answer and the respective code.
'''

from csv import list_dialects
from os import confstr_names
import sqlite3
from threading import local

conn = sqlite3.connect('cocktails_database.sqlite')
c = conn.cursor()

# Task 9: Create a MY_COCKTAILS table that has the same structure as COCKTAIL. 
# Insert the contents of table COCKTAIL into MY_COCKTAILS at the same time. 
# You execute all subsequent changes exclusively on MY_COCKTAILS.

c.execute('''
CREATE TABLE IF NOT EXISTS My_Cocktails AS
    SELECT cid, cname, alkoholisch, gid
    FROM cocktail
''')
#conn.commit()
print("\nTask 9:\nTable was created and added to the database.")

# Task 10: insert a new cocktail "Purple cow" in the table MY_COCKTAILS. 
# The cocktail is alcoholic, served in a snifter and has the ID 18.

c.execute('''DELETE FROM My_Cocktails WHERE My_Cocktails.cid = 18''')# so it doenst doubles again if the code is executed again.

c.execute('''
INSERT INTO My_Cocktails (cid, cname, alkoholisch, gid)
VALUES (18,'Purple cow', 'y', (
    SELECT glas.gid
    FROM glas
    WHERE glas.gname= 'Schwenker'))
''')
#conn.commit()     # this line is commented out since if executed again it would add this row again,
# since python is being used the IGNORE command does not work.
print("\nTask 10:\nNew row with new cocktail created in My_Cocktails.")

# Task 11: The cocktail "Purple Cow" is actually called "Blue Cow". Correct this mistake. 

c.execute('''
UPDATE My_Cocktails
SET cname = 'Blue Cow'
WHERE cname = 'Purple cow'
''')
print("\nTask 11:\nPurple Cow cocktail renamed to Blue Cow.")

#Task 12:  first create a table MY_INGREDIENT that has the same structure as INGREDIENT. 
# Let's assume that the alcohol content of all ingredients of the cocktail Knieweich is actually 
# twice as high as the entered value. Then correct this error in the MY_INGREDIENTS table.

c.execute('''
DROP TABLE My_Ingredient;
''') # so it doenst doubles again if the code is executed again.

c.execute('''
CREATE TABLE IF NOT EXISTS My_Ingredient AS
    SELECT zid, zname, alkoholgehalt
    FROM ingredient
''')

c.execute('''
UPDATE My_Ingredient
SET alkoholgehalt = alkoholgehalt * 2
WHERE zid IN (
    SELECT Ingredient_Cocktail.zid
    FROM Ingredient_Cocktail
    WHERE Ingredient_Cocktail.cid = (
        SELECT cocktail.cid
        FROM cocktail
        WHERE cocktail.cname='Knieweich'))
''')
print("\nTask 12:\nMy_Ingredient table created and Knieweich's ingredients alcohol content was corrected.")

# Task 13: Delete all cocktails from the MY_COCKTAILS table that contain "Campari" as an ingredient.

c.execute('''
DELETE FROM My_cocktails WHERE My_cocktails.cid IN (
    SELECT Ingredient_Cocktail.cid
    FROM Ingredient_Cocktail
    WHERE Ingredient_Cocktail.zid = (
        SELECT ingredient.zid
        FROM ingredient
        WHERE ingredient.zname='Campari'
    )
)
''')
print("\nTask 13:\nCocktails that contained the ingredient 'Campari' were deleted.")

# Task 14: which restaurants offer cocktails with ID 8 or ID 11?

c.execute('''
SELECT local.lname
FROM local
WHERE local.lid IN (
    SELECT cocktail_local.lid
    FROM cocktail_local
    WHERE cocktail_local.cid=8 OR cocktail_local.cid=11
    )
''')
rest_cock_8or11= c.fetchall()
rest_cock_8or11 = [x[0] for x in rest_cock_8or11]
print("\nTask 14:\nThis are the restaurants that offer the cocktails with the ID 8 or 11: "+(', '.join(rest_cock_8or11)))

# Task 15: Which cocktail is alcoholic and is served in the 'cocktailglas'?

c.execute('''
SELECT cocktail.cname
FROM cocktail
WHERE cocktail.alkoholisch='y' AND cocktail.gid IN (
    SELECT glas.gid
    FROM glas
    WHERE glas.gname='Cocktailglas'
    )
''')
cockglas_alco= c.fetchall()
cockglas_alco = [x[0] for x in cockglas_alco]
print("\nTask 15:\nThis are the cocktails that are alcoholic and are served in the Cocktail Glass: "+(', '.join(cockglas_alco)))

# Task 16: Which glasses are never used?

c.execute('''
SELECT glas.gname 
FROM glas 
WHERE glas.gid NOT IN (
    SELECT cocktail.gid 
    FROM cocktail)
''')
g_not_used= c.fetchall()
g_not_used = [x[0] for x in g_not_used]
print("\nTask 16:\nThis are the glasses that are never used in any cocktail: "+(', '.join(g_not_used)))

# Task 17: which cocktails do you talk about (table COCKTAIL _PERSON)? Output the names of the cocktails!

c.execute('''
SELECT cocktail.cname 
FROM cocktail 
WHERE cocktail.cid IN (
    SELECT Cocktail_person.cid 
    FROM Cocktail_person)
''')
talk_cocktails= c.fetchall()
talk_cocktails = [x[0] for x in talk_cocktails]
print("\nTask 17:\nThis are the cocktails that are talked about: "+(', '.join(talk_cocktails)))

# Task 18: Which ingredients have an alcohol content between 0 and 50?

c.execute('''
SELECT ingredient.zname 
FROM ingredient 
WHERE ingredient.alkoholgehalt BETWEEN 0 AND 50
''')
ing_alcohol= c.fetchall()
ing_alcohol = [x[0] for x in ing_alcohol]
print("\nTask 18:\nThis are the ingredients that have an alcohol content between 0 and 50 according to the table Ingredients (not My_Ingredientes): "+(', '.join(ing_alcohol)))

# Task 19: What personal names begin with S?

c.execute('''
SELECT person.name 
FROM person 
WHERE person.name LIKE 'S%'
''')
name_s= c.fetchall()
name_s = [x[0] for x in name_s]
print("\nTask 19:\nThis are the personal names begin with S: "+(', '.join(name_s)))

# Task 20: Is there a place that doesn't serve cocktails?

c.execute('''
SELECT IFNULL (max('All places serve cocktails.'), 'Some places do not serve any cocktails.')
FROM  Cocktail_local
WHERE Cocktail_local.lid IN (
    SELECT local.lid
    FROM local
)
''')
if_local_serves_cocktails= c.fetchall()
if_local_serves_cocktails = [x[0] for x in if_local_serves_cocktails]
print("\nTask 20:\n"+(', '.join(if_local_serves_cocktails)))

# Task 21: How many ingredients are there?

c.execute('''
SELECT COUNT(DISTINCT ingredient.zid) FROM ingredient
''') #counting all rows except null or duplicates
count_ing= c.fetchall()
count_ing = [x[0] for x in count_ing]
print("\nTask 21:\nThere are "+(str(count_ing)[1:-1])+" ingredients in total.")

# Task 22: What is the average alcohol content of the ingredients?

c.execute('''
Select avg(ingredient.alkoholgehalt) from ingredient
''')
avg_alcohol= c.fetchall()
avg_alcohol = avg_alcohol[0][0]
avg_alcohol_rounded = round(float(avg_alcohol))
print(f"\nTask 21:\nThere average of alcohol content of the ingredients is {avg_alcohol}, or {avg_alcohol_rounded} if rounded up, according to the table Ingredients (not My_Ingredientes)")


# task 23: 


conn.commit()
