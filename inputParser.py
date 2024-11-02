# Importing necessary packages
import csv
import re
import pandas as pd
from itertools import combinations  
from Normalizations import (
    check_normal_form,
    convert_to_1NF,
    convert_to_2NF,
    convert_to_3NF,
    convert_to_BCNF,
    convert_to_4NF,
    convert_to_5NF,
    check_1NF

)
from Sqlgeneration import generate_sql_queries, check_datatypes 

# Input commands
print("Enter the CSV file path:")
csv_filePath = input()  # Storing CSV file path

# Functional Dependencies Input
FD = []
print("Enter Functional Dependencies (e.g., A->B, A,B->C):")
print("Enter 'Done' when finished.")
while True:
    dependency = input()
    if dependency.lower() == "done":
        break
    FD.append(dependency)

# Multi-Valued Dependencies Input
MVD = []
print("Enter Multi-Valued Dependencies (e.g., A->>B):")
print("Enter 'Done' when finished.")
while True:
    dependency = input()
    if dependency.lower() == "done":
        break
    MVD.append(dependency)

# Key Input
print("Enter Key (comma-separated if multiple):")
Key = input().split(",")

# Option to Find Highest Normal Form
print("Find the highest normal form of the input table? (1: Yes, 2: No):")
input_choice = int(input())
input_normal_form = "The given input table is "
if input_choice == 1:
    input_normal_form += check_normal_form(csv_filePath, FD, Key, MVD)

# User Choice for Highest Normal Form to Reach
print("Choose the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF):")
choice = input().upper()
user_choice = {'1': 1, '2': 2, '3': 3, 'B': 3.5, '4': 4, '5': 5}.get(choice, 0)

# Convert to 1NF if chosen
result_1NF = []
if user_choice >= 1 and not check_1NF(csv_filePath):
    result_1NF = convert_to_1NF(csv_filePath)
    print("Enter output CSV file path to store the result after converting to 1NF:")
    with open('converted1NF.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result_1NF)

# Conversion up to the Selected Normal Form
res_tables = {}
if user_choice >= 2:
    res_tables = convert_to_2NF(FD, Key)
if user_choice >= 3:
    res_tables = convert_to_3NF(FD, Key, res_tables)
if user_choice >= 3.5:
    res_tables = convert_to_BCNF(FD, Key, res_tables)
if user_choice >= 4:
    res_tables = convert_to_4NF(FD, Key, MVD, res_tables)
if user_choice == 5:
    res_tables = convert_to_5NF(FD, Key, MVD, res_tables)

# Determine data types for SQL query generation
data_types = check_datatypes(csv_filePath)

# Generate SQL Queries for Decomposed Relations
SQL_queries = generate_sql_queries(FD, Key, res_tables, data_types)
print(SQL_queries)

# Writing Output to a Text File
with open('Output.txt', mode='w') as file:
    # Write 1NF result if converted
    if result_1NF:
        for row in result_1NF:
            file.write(''.join(map(str, row)) + '\n')
        file.write('\n')

    # Write SQL queries to the file
    for query in SQL_queries:
        file.write(query + '\n')
    
    # Write the highest normal form if checked
    if input_choice == 1:
        file.write(f"\n{input_normal_form}\n")

print("Loading complete")
