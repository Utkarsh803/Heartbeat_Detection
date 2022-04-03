import pyodbc
import sqlite3

server = 'hbdetect.database.windows.net'
database = 'ClientHeartbeats'
username = 'Group14'
password = 'HeartbeatDetect14'   
driver= '{ODBC Driver 17 for SQL Server}'
#connects with database
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
#cursor creates endpoint
cursor = conn.cursor()
#insert into database
#cursor.execute('''
#                INSERT INTO testinginfo (user_id, user_Name, user_hb)
#                VALUES
#                (0,'John',120),
#                (1,'Fionn',300)
#               ''')
#conn.commit()


def data_entry(email, hb, date):
    user_Name = email
    user_hb = hb
    cursor.execute("INSERT INTO testing ( user_Name, user_hb, hb_date) VALUES( ?, ?, ?)", ( user_Name, user_hb, date))
    conn.commit()


def query_table(email):
    hbs = cursor.execute('SELECT user_hb, hb_date, id FROM testing WHERE user_Name = ?',(email))
    rows = cursor.fetchall()
    return rows 

#print fom table
email = "sdjnsdkjv"
data_entry(email, 102, '20001001')
data = query_table(email)
for dat in data:
 print(dat)
print(data[0])