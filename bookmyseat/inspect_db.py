import sqlite3

# Path to your SQLite database
db_path = "db.sqlite3"  # Ensure this matches the name of your database file

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute a query to list columns in the 'movies_theater' table
cursor.execute("PRAGMA table_info(movies_theater);")
columns = cursor.fetchall()

# Print column details
print("Columns in movies_theater table:")
for column in columns:
    print(column)

# Close the connection
conn.close()
