import csv
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('.\database\database.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table to store phone data
cursor.execute('''CREATE TABLE IF NOT EXISTS phone
                  (Phone_name TEXT, Phone_Image TEXT, Price TEXT, Score TEXT, Network TEXT, Technical TEXT, Storage TEXT, Battery TEXT, Display TEXT, Camera TEXT, OS TEXT, Extra TEXT)''')

# Open the CSV file with UTF-8 encoding
with open('out.csv', 'r', encoding='utf-8') as f:
    # Read the CSV data using a DictReader object
    reader = csv.DictReader(f)
    # Insert data into the table
    for row in reader:
        values = (row['\ufeffPhone_name'], row['Phone_Image'], row['Price'], row['Score'], row['Network'], row['Technical'], row['Storage'], 
                  row['Battery'], row['Display'], row['Camera'], row['OS'], row['Extra'],row['Rear_ISO'],row['Rear_Shutter_Speed'],row['Front_ISO'],row['Front_Shutter_Speed'])
        cursor.execute('INSERT INTO phone VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)

print("Done..")
# Commit the changes
conn.commit()

# Close the connection
conn.close()


# import csv

# # Open the CSV file
# with open('out.csv', 'r',encoding='utf-8') as f:
#     # Create a DictReader object
#     reader = csv.DictReader(f)
#     # Print the column names
#     print(reader.fieldnames)