import pyodbc
import sqlite3

class db(object):

    def __init__(self):
        self.server = ''
        self.database = ''
        self.username = ''
        self.password = ''   
        self.driver= ''
        #connects with database
        with pyodbc.connect('DRIVER='+self.driver+';SERVER=tcp:'+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password) as self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
                row = cursor.fetchone()
                while row:
                    print (str(row[0]) + " " + str(row[1]))
                    row = cursor.fetchone()
        #cursor creates endpoint
        self.cursor = self.conn.cursor()
        #insert into database
        #cursor.execute('''
        #                INSERT INTO testinginfo (user_id, user_Name, user_hb)
        #                VALUES
        #                (0,'John',120),
        #                (1,'Fionn',300)
        #               ''')
        #conn.commit()

    #date in format yyyy-mm-dd
    def data_entry(self,email, hb, date):
        user_Name = email
        user_hb = hb
        self.cursor.execute("INSERT INTO clienthb ( user_Name, user_hb, hb_date) VALUES( ?, ?, ?)", ( user_Name, user_hb, date))
        self.conn.commit()


    def query_table(self,email):
        hbs = self.cursor.execute('SELECT user_hb, hb_date, id FROM clienthb WHERE user_Name = ?',(email))
        rows = self.cursor.fetchall()
        print("The database is returning->")
        print(rows)
        print("for the email"+email)
        return rows 

#datbas=db()
#print fom table
#email = "test@gmail.com"
#datbas.data_entry(email, 102, "2021-03-05")
#data = datbas.query_table(email)
#print(data)