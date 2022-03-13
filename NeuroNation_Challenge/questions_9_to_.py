'''
This python file will be used to answer all the question 1 to made for the SQL Challenge,
the task will be presente as a comment and bellow will be the answer and the respective code.
'''

from os import confstr_names
import sqlite3

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




conn.commit()
