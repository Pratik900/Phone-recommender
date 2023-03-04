from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  
        password = request.form['password']
        confirm_psk = request.form['confirm-password']
        if password == confirm_psk:
            conn = sqlite3.connect(".\database\signup.db")
            cursor = conn.cursor()
            insert_query =  ''' INSERT INTO signup (username,email,password,confirm_psk) VALUES(?,?,?,?)'''
            cursor.execute(insert_query,(username,email,password,confirm_psk))
            conn.commit()
            conn.close()
            conn = sqlite3.connect(".\database\login.db")
            cursor = conn.cursor()
            login_insert_query = ''' INSERT INTO login (username,password) values(?,?)'''
            cursor.execute(login_insert_query,(username,password))
            conn.commit()
            conn.close()
            return render_template('login.html')
        else:
            return redirect('register')
    return render_template('register.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(".\database\login.db")
        cursor = conn.cursor()
        select_query = '''SELECT * FROM login WHERE username=? AND password=?'''
        cursor.execute(select_query,(username,password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[0]
            session['password'] = user[1]
            return render_template('index.html')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def p():
    selected_image = ''
    if request.method == 'POST':
        selected_image = request.form['selected-image']
    return render_template('index.html', selected_image=selected_image)


@app.route('/index/about')
def about():
    return render_template('about.html')

@app.route('/about/index/')
def back():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
