from flask import Flask, session, render_template, jsonify, redirect, url_for, request, flash

app = Flask(__name__)


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


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    if path.startswith('notes'):
        if 'user' not in session:
            flash('請先登入')
            return redirect(url_for('index'))

        return render_template('notes.html', notes=[])

    return path


if __name__ == '__main__':
    app.run()
