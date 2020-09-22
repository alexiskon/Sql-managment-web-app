from flask import Flask, render_template, url_for, request, flash, redirect
import sqlite3
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64




app = Flask(__name__, static_url_path='/Users/alexis/Desktop/webapp/static')
app.secret_key = 'Alexis___kon'

conn = sqlite3.connect('members.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    surname text NOT NULL,
    kilometers float NOT NULL,
    amount float NOT NULL)''')


@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/insert', methods = ["POST", "GET"])
def insert():
    if request.method == "POST":
        onoma = request.form['name']
        epitheto = request.form['surname']
        km = (request.form['kilometers'])
        poso = (request.form['amount'])
        if onoma == "" or epitheto == "" or km == "" or poso == "" :
            flash("Please fill all fields")
            return render_template('insert.html')
        else:    
            conn = sqlite3.connect('members.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM members WHERE name LIKE ? AND surname LIKE ? ''', (onoma, epitheto))
            rows = c.fetchall()
            if rows:
                new_km = float(rows[0][3]) + float(km)
                new_poso = float(rows[0][4]) + float(poso)
                c.execute('''UPDATE members SET kilometers = ?, amount = ? WHERE name = ? AND surname = ?''', (new_km, new_poso, onoma, epitheto) )
                conn.commit()
                print(new_poso, new_km, onoma, epitheto)
            else:
                c.execute('''INSERT INTO members (name, surname, kilometers, amount) VALUES (?, ?, ?, ?)''', (onoma, epitheto, km, poso))
                conn.commit()

            return render_template('insert.html')
    else:
        return render_template('insert.html')


@app.route('/Search', methods =["POST", "GET"])
def search():
    if request.method == "POST":
        conn = sqlite3.connect('members.db')
        c = conn.cursor()
        search_user = request.form['search_user']
        c.execute('''SELECT * from members WHERE name LIKE ? OR surname  LIKE ?''', (search_user, search_user))
        rows = []
        while True:
            entry = c.fetchone()
            if entry is None:
                break
            else:
                rows.append(entry)
        return render_template('results.html', rows = rows)
    return render_template('Search.html')

@app.route('/results')
def results():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM members''')
    rows = []
    while True:
        entry = c.fetchone()
        if entry is None:
            break
        else:
            rows.append(entry)

    return render_template('results.html', rows = rows)

@app.route('/delete/<row_id>')
def delete(row_id):
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute('''DELETE FROM members WHERE id LIKE ?''', [row_id])
    conn.commit()
    flash("Record deleted successfully")
    return redirect(url_for('results'))

@app.route('/stats')
def stats():
    img1 = io.BytesIO()
    conn = sqlite3.connect('members.db')
    query = ('''SELECT * FROM members ORDER BY kilometers DESC LIMIT 5''')
    sqldtbase = pd.read_sql_query(query, conn)
    sqldtbase.plot.barh(x = 'surname', y = 'kilometers', title = "top travellers")
    plt.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()
    return render_template('stats.html', plot_url1 = plot_url1)

if __name__ == '__main__':
    app.run(debug=True)

conn.close