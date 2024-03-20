import sqlite3

# Function to search for missing BOS documents
def find_missing_bos(connection, file_numbers_to_search):
    cursor = connection.cursor()

    # Get distinct file numbers with BOS (case-insensitive)
    cursor.execute("SELECT DISTINCT FILENO FROM YourTableName WHERE LOWER(CMT) = 'bos'")
    file_numbers_with_bos = {row[0] for row in cursor.fetchall()}

    # Get distinct file numbers without BOS (case-insensitive)
    cursor.execute("SELECT DISTINCT FILENO FROM YourTableName WHERE LOWER(CMT) != 'bos'")
    file_numbers_without_bos = {row[0] for row in cursor.fetchall()}

    # Calculate missing BOS file numbers from the specified list
    missing_bos_file_numbers = set(file_numbers_to_search) - file_numbers_with_bos

    return file_numbers_with_bos, missing_bos_file_numbers

# Read file numbers from a .txt file
def read_file_numbers_from_txt(filename):
    with open(filename, 'r') as file:
        file_numbers = [int(line.strip()) for line in file.readlines()]
    return file_numbers

# Connect to the SQLite database
try:
    connection = sqlite3.connect("your_database.db")  # Replace with your actual database name

    # Specify the path to the .txt file with file numbers to search
    file_numbers_to_search = read_file_numbers_from_txt("file_numbers.txt")

    # Call the function with file numbers to search
    file_numbers_with_bos, missing_bos_file_numbers = find_missing_bos(connection, file_numbers_to_search)

    # Print results
    print("File Numbers with BOS:", file_numbers_with_bos)
    print("File Numbers without BOS:", missing_bos_file_numbers)

except sqlite3.Error as e:
    print("Error connecting to the database:", e)

finally:
    if connection:
        connection.close()