from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database=None )

cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS results;")
cursor.execute("USE results")
cursor.execute("CREATE TABLE IF NOT EXISTS result (ID INT AUTO_INCREMENT PRIMARY KEY, Datum DATETIME, Tocke INT)")

@app.route('/')
def index():
    return render_template('vprasanja.html')

@app.route('/dnevnik', methods=["GET", "POST"])  
def dnevnik():
    cursor.execute("SELECT Datum, Tocke FROM result")
    entries = cursor.fetchall()
    return render_template('dnevnik.html', entries=entries)

@app.route('/drop_table', methods=["POST"])
def drop():
    if request.method == "POST":
        cursor.execute("DROP TABLE IF EXISTS result")
        cursor.execute("CREATE TABLE IF NOT EXISTS result (ID INT AUTO_INCREMENT PRIMARY KEY, Datum DATETIME, Tocke INT)")
        return redirect(url_for('index'))

@app.route('/submit', methods=['POST'])
def submit():
    scoreR = 0
    scoreC = 0
    scoreT = 0

    for i in range(1, 4):
        if 'q1_' + str(i) in request.form:
            answer = request.form['q1_' + str(i)]
            if answer == 'correct':
                scoreR += 1

    for i in range(1, 13):
        answers = request.form.getlist('q2_' + str(i))
        if 'correct' in answers:
            scoreC += 1
        elif 'incorrect' in answers and scoreC > 0:
            scoreC -= 1

    user_input = request.form['q3']
    if user_input.lower() == 'mount everest':
        scoreT += 1
    
    score = scoreR + scoreC + scoreT

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO result (Datum, Tocke) VALUES (%s, %s)", (current_time, score))
    mydb.commit()

    return render_template('rezultat.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
