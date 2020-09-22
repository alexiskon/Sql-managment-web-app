import sqlite3

conn = sqlite3.connect('members.db')
c = conn.cursor()


c.execute('''CREATE TABLE members(
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            surname text NOT NULL,
            kilometers float NOT NULL,
            amount float NOT NULL)''')



    
c.execute('SELECT * FROM members')
print(c.fetchall())

