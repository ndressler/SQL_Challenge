'''
This python file will be used to answer the questions 
24 to 27
made for the SQL Challenge,
the task will be presente as a comment and bellow its respective code,
the answer will be generated by running the code.
'''

from csv import list_dialects
from os import confstr_names
import sqlite3
from threading import local

conn = sqlite3.connect('cocktails_database.sqlite')
c = conn.cursor()


# Task 24: A cocktail consists of several ingredients. 
# The number of units of each Ingredients per cocktail are listed in the table INGREDIENT_COCKTAIL.

#(a) The number of ingredients per cocktail.

c.execute('''

''')
x = c.fetchall()








#(b) The number of ingredients per cocktail is required, but only for cocktails with more than 2 ingredients.

c.execute('''
''')
x = c.fetchall()

#(c) The sum of the units of measure of the respective ingredients per cocktail is sought.

c.execute('''
''')
x = c.fetchall()

#(d) The sum of the units of measure of the respective alcoholic ingredients per cocktail is sought.

c.execute('''
''')
x = c.fetchall()