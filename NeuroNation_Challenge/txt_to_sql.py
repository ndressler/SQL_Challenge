from webbrowser import get
import pandas as pd
import os
from pathlib import Path
import sqlite3

directory = '../raw_data'
Path('cocktails_database.db').touch()

def txt_to_csv():

    '''after TXT files were created, from the word file sent by the challenge,
    the files created dataframes that were later stored as CSV files'''

    for file in os.listdir(directory):
        if file.endswith(".txt"):
            filename = file.strip('.txt')
            df = pd.read_csv(f'{directory}/{file}')  #creates dataframe\
            df.to_csv('{}/{}.csv'.format(directory,filename),index=None)  #stores df in a csv file

txt_to_csv()


def csv_to_sql():

    '''CSV files are loaded into a SQL file, creating a database'''

    conn = sqlite3.connect('cocktails_database.db')
    c = conn.cursor()
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            filename = file.strip('.csv')
            df = pd.read_csv(f'{directory}/{file}')
            columns = [col for col in df.columns]
            c.execute(
                '''CREATE TABLE {} ({})'''.format(filename, columns)
            )
            df.to_sql(f'data/{filename}', conn, if_exists='append',
                      index=False)  # write the data to sqlite table

csv_to_sql()
