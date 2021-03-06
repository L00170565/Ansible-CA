#!/usr/bin/env python3

# ------------------------------------------
# File Name = csv_to_mysql.py
# Project = csv_to_mysql
#
# Author = Panagiotis Drakos, L00170565
# Date = 11/04/22
# ------------------------------------------
""" Description: This script is reads the contents of a csv file and writes them into an sql table that is created
within than script. """

# Import the CSV File.

import pandas as pd
import mysql.connector
from mysql.connector import Error
import os
from getpass import getpass
from dotenv import load_dotenv

student_data = pd.read_csv('/home/l00170565/Desktop/s3_database/mydbdetails-new.csv', index_col=False, delimiter=',')
student_data.head()

load_dotenv()  # .env file for credentials.

try:
    conn = mysql.connector.connect(user=os.getenv('db_user'), password=os.getenv('db_pass'), host='localhost',
                                   database='students_db')
except Error as e:
    print("Error while connecting to MySQL", e)

try:
    conn = mysql.connector.connect(host='localhost', database='students_db', user=os.getenv('db_user'),
                                   password=os.getenv('db_pass'))
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS USER;')
        print('Creating table....')

        # Create table User inside students_db database

        cursor.execute("CREATE TABLE USER(Lnumber varchar(20),Name varchar(20),Year_Of_Course int)")
        print("Table USER created")

        for i, row in student_data.iterrows():
            # Insert string values 
            sql = "INSERT INTO students_db.USER VALUES (%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # commit to save changes
            conn.commit()
except Error as e:
    print("Error while connecting to MySQL", e)

# Query the Table

# Execute query
sql = "SELECT * FROM students_db.USER"
cursor.execute(sql)
# Fetch all the records
result = cursor.fetchall()
for i in result:
    print(i)
