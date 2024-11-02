import csv
import re
import pandas as pd

def generate_sql_queries(FD, Key, tables, data_types):
    sql_statements = []
    unique_table_definitions = set()  # Set to track unique table structures
    lhs_fd = set(attr.strip() for fd in FD for attr in fd.split("->")[0].split(","))

    for table_name, columns in tables.items():
        # Ensure table name is a valid identifier (not numeric)
        if str(table_name).isdigit():
            table_name = f"Table_{table_name}"

        # List to store column definitions and constraints for each table
        column_definitions = []
        primary_keys = []
        foreign_keys = []

        # Convert columns to list if necessary
        if isinstance(columns, dict):
            columns = list(columns.keys())
        elif not isinstance(columns, list):
            raise TypeError(f"Expected list or dict for table columns, got {type(columns)} for table {table_name}")

        # Create column definitions
        for attr in columns:
            data_type = data_types.get(attr, 'VARCHAR(255)')
            column_def = f"{attr} {data_type}"
            if attr not in lhs_fd:
                column_def += " NOT NULL"

            # Handle primary key and foreign key constraints
            if attr in Key and len(Key) == 1:
                primary_keys.append(attr)
            elif attr == table_name:
                primary_keys.append(attr)
            elif attr in lhs_fd:
                foreign_keys.append(f"FOREIGN KEY ({attr}) REFERENCES {attr}({attr})")

            column_definitions.append(column_def)

        # Handle composite primary keys for the "Candidate" table
        if table_name == "Candidate":
            primary_keys = Key

        # Create the SQL query
        primary_key_clause = f", PRIMARY KEY ({', '.join(primary_keys)})" if primary_keys else ""
        foreign_key_clause = ", " + ", ".join(foreign_keys) if foreign_keys else ""
        query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)}{primary_key_clause}{foreign_key_clause});"

        # Only add unique table structures
        table_signature = (frozenset(column_definitions), frozenset(primary_keys), frozenset(foreign_keys))
        if table_signature not in unique_table_definitions:
            unique_table_definitions.add(table_signature)
            sql_statements.append(query)

    return sql_statements

def check_datatypes(csv_filePath):
    def get_datatype(value):
        if re.match(r'^[0-9]+$', value):
            return "INT"
        elif re.match(r'^[.a-zA-Z0-9]*$', value):
            return "VARCHAR(100)"
        try:
            pd.to_datetime(value)
            return "DATE"
        except ValueError:
            pass
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', value):
            return "VARCHAR(50)"
        return "VARCHAR(100)"  # Default for unmatched types

    with open(csv_filePath, 'r') as file:
        csv_reader = csv.reader(file)
        header, first_row = next(csv_reader), next(csv_reader)
        return {col: get_datatype(val) for col, val in zip(header, first_row)}
