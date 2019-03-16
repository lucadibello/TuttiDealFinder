from classes import databasemanager

DB = databasemanager.DatabaseManager()

for x in DB.query("SELECT * FROM user"):
    print(x)
