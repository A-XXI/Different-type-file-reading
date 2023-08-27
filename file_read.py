import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

def upload_file_to_mysql(file_path):
    try:
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.csv':
            df = pd.read_csv(file_path, sep=',', skiprows=0, header=0)
        elif file_extension == '.xml':
            df = pd.read_xml(file_path)
        elif file_extension in ['.xlsx']:
            df = pd.read_excel(file_path, engine='openpyxl')
        elif file_extension in ['.xls']:
            df = pd.read_excel(file_path, engine='xlrd', skiprows=5)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        else:
            print("Unsupported file format.")
            return

        # Connect to server
        connection = mysql.connector.connect(
            host='your_host',
            database='your_database',
            user='your_user',
            password='your_password'
        )

        if connection.is_connected():
            # Upload data
            df.to_sql('your_table_name', connection, if_exists='append', index=False)

            print("File content uploaded successfully.")
        
    except Error as e:
        print("Error:", e)

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")

# Call the function with the file path
upload_file_to_mysql('data.json')