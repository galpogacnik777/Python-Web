from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('vprasanja.html')

@app.route('/submit', methods=['POST'])
def submit():
    score = 0

    # Check answers for radio button questions
    for i in range(1, 4):
        answer = request.form['q1_' + str(i)]
        if answer == 'correct':
            score += 1

    # Check answers for checkbox questions
    for i in range(1, 13):
        answers = request.form.getlist('q2_' + str(i))
        if 'correct' in answers and 'incorrect' not in answers:
            score += 1

    # Check answer for user input question
    user_input = request.form['q3']
    if user_input.lower() == 'mount everest':
        score += 1

    return render_template('rezultat.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)

