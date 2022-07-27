import json

from flask import Flask, session, render_template, jsonify, redirect, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = '208f3f25-bec7-4607-b452-516803969967'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if len(request.json['email']) == int(request.json['password']):
        session['user'] = request.json['email']
    return jsonify({
        "status": True
    })


@app.route('/save', methods=['POST'])
def save():
    data = json.load(open('data/user.json', 'r'))
    email = session['user']
    print(email)
    if email in data and data[email]:
        data[email] = data[email].update(request.form)
    else:
        data[email] = request.form
    json.dump(data, open('data/user.json', 'w'))
    return redirect('/profile')


@app.route('/logout')
def logout():
    del session['user']
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if path.startswith('profile'):
        if 'user' not in session:
            flash('請先登入')
            return redirect(url_for('index'))
        data = json.load(open('data/user.json', 'r'))
        return render_template('profile.html', user=data.get(session['user']))

    return path


if __name__ == '__main__':
    app.run()
