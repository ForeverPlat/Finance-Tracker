import sqlite3

con = sqlite3.connect("tracking.db")
cursor = con.cursor()

for row in cursor.execute('SELECT * FROM tracking'):
    #this take index 1 of the row and the slices it
    latestRow = row

most_recent_transaction_operator = latestRow[1][0:1]

most_recent_transaction = float(row[1][1:])
most_recent_total = float(row[0])

if most_recent_transaction != 0.0:

    if most_recent_transaction_operator == "+":
        new_total = most_recent_total +  most_recent_transaction
    elif most_recent_transaction_operator == "-":
        new_total = most_recent_total -  most_recent_transaction


    #print(most_recent_transaction)
    #print(most_recent_transaction_operator)
    print(new_total)


