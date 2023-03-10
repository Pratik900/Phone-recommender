from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
  
    @classmethod
    def get(cls, id):
        conn = sqlite3.connect(".\database\database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM signup WHERE username=? ", (id,))
        row = cur.fetchone()
        user = cls(row[0], row[1]) if row else None
        conn.close()
        return user

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  
        password = request.form['password']
        confirm_psk = request.form['Confirm_password']
        if password == confirm_psk:
            conn = sqlite3.connect(".\database\database.db")
            cursor = conn.cursor()
            insert_query =  ''' INSERT INTO signup (username,email,password) VALUES(?,?,?)'''
            cursor.execute(insert_query,(username,email,password))
            conn.commit()
            conn.close()
            return render_template('login.html')
        else:
            return redirect('register')
    return render_template('register.html')

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('.\database\database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM signup WHERE username=? AND password=?", (user_id, password))
        row = cur.fetchone()
        conn.close()
        if row:
            user = User(row[0], row[1])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods = ['POST','GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/index', methods=['POST','GET'])
@login_required
def home():
    conn = sqlite3.connect('.\database\database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT \ufeffPhone_name FROM phone')
    dropdown_data = cursor.fetchall()
    conn.close()
    return render_template('index.html', dropdown_data=dropdown_data)


@app.route('/get_row_data_1', methods=['POST'])
def get_row_data():
        conn = sqlite3.connect('.\database\database.db')
        cursor = conn.cursor()
        selected_value = request.form.get('selected_value')
        print(selected_value)
        cursor.execute("SELECT * FROM phone WHERE  \ufeffPhone_name = ?", (selected_value,))
        row_data = cursor.fetchone()
        response = {'column1': row_data[0], 'column2': row_data[1], 'column3': row_data[2], 'column4': row_data[3], 'column5': row_data[5],
                 'column6': row_data[6], 'column7': row_data[7], 'column8': row_data[8], 'column9': row_data[9], 'column10': row_data[10], 
                 'column11': row_data[11]}
        return jsonify(response)


@app.route('/get_row_data_2', methods=['POST'])
def get_row_data_2():
        conn = sqlite3.connect('.\database\database.db')
        cursor = conn.cursor()
        selected_value_2 = request.form['selected_value_2']
        print(selected_value_2)
        cursor.execute("SELECT * FROM phone WHERE  \ufeffPhone_name = ?", (selected_value_2,))
        row_data_2 = cursor.fetchone()
        response_2 = {'column_1': row_data_2[0], 'column_2': row_data_2[1], 'column_3': row_data_2[2], 'column_4': row_data_2[3], 'column_5': row_data_2[5],
                 'column_6': row_data_2[6], 'column_7': row_data_2[7], 'column_8': row_data_2[8], 'column_9': row_data_2[9], 'column_10': row_data_2[10], 
                 'column_11': row_data_2[11]}
        return jsonify(response_2)


@app.route('/index/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
   