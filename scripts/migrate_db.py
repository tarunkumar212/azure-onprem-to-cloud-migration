import pyodbc
import os
import re

server   = os.environ.get('SQL_SERVER')
database = os.environ.get('SQL_DATABASE')
username = os.environ.get('SQL_USERNAME')
password = os.environ.get('SQL_PASSWORD')

conn_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=" + server + ";"
    "Database=" + database + ";"
    "Uid=" + username + ";"
    "Pwd=" + password + ";"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

conn = pyodbc.connect(conn_string)
cursor = conn.cursor()
print("Connected to Azure SQL")

# Read export file and extract real statements
with open('/home/azureuser/database-export.sql', 'r') as f:
    lines = f.readlines()

real_statements = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    match = re.search(r"INSERT INTO \"table\" VALUES\('(.+)'\);$", line)
    if match:
        inner = match.group(1)
        inner = inner.replace("''", "'")
        real_statements.append(inner)

print("Statements extracted:", len(real_statements))

# The problem: SQLite exports without column list
# INSERT INTO products VALUES(1,'Laptop',...)
# Azure SQL needs column list when IDENTITY_INSERT is ON
# INSERT INTO products (id,name,description,price,stock,created_at) VALUES(1,'Laptop',...)

# Fix: add column list to each statement
def add_column_list(stmt):
    # Fix products statements
    stmt = re.sub(
        r"INSERT INTO products VALUES\(",
        "INSERT INTO products (id,name,description,price,stock,created_at) VALUES(",
        stmt
    )
    # Fix migration_log statements
    stmt = re.sub(
        r"INSERT INTO migration_log VALUES\(",
        "INSERT INTO migration_log (id,event,details,logged_at) VALUES(",
        stmt
    )
    return stmt

# Apply fix to all statements
fixed_statements = [add_column_list(s) for s in real_statements]

print("")
print("Fixed statements:")
for s in fixed_statements:
    print(" ", s[:90])

print("")

# Insert products with IDENTITY_INSERT ON
print("Inserting products...")
cursor.execute("SET IDENTITY_INSERT products ON")

product_count = 0
for stmt in fixed_statements:
    if 'INTO products' in stmt:
        try:
            cursor.execute(stmt)
            product_count += 1
        except Exception as e:
            print("  Error:", str(e))

cursor.execute("SET IDENTITY_INSERT products OFF")
conn.commit()
print("Products inserted:", product_count)

# Insert migration_log with IDENTITY_INSERT ON
print("Inserting migration log...")
cursor.execute("SET IDENTITY_INSERT migration_log ON")

log_count = 0
for stmt in fixed_statements:
    if 'INTO migration_log' in stmt:
        try:
            cursor.execute(stmt)
            log_count += 1
        except Exception as e:
            print("  Error:", str(e))

cursor.execute("SET IDENTITY_INSERT migration_log OFF")
conn.commit()
print("Log entries inserted:", log_count)

# Validate
print("")
print("=== Validation ===")
cursor.execute("SELECT COUNT(*) FROM products")
print("Products in Azure SQL:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM migration_log")
print("Migration log entries:", cursor.fetchone()[0])

print("")
print("Products:")
cursor.execute("SELECT id, name, price, stock FROM products ORDER BY id")
for row in cursor.fetchall():
    print("  ID:" + str(row[0]) + " | " + str(row[1]) + " | Rs." + str(row[2]) + " | Stock:" + str(row[3]))

conn.close()
print("")
print("Import complete")
