from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from bs4 import BeautifulSoup
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

@app.route('/comp', methods = ['POST','GET'])
@login_required
def comp():
    return render_template('compare.html')

@app.route('/mainserach',methods = ['GET'])
def mainserach():
    query = request.args.get('term', '')
    main_results = []
    print("query")
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    c.execute("SELECT \ufeffPhone_name FROM phone WHERE \ufeffPhone_name LIKE ? ",('%' + query + '%',))
    rows = c.fetchall() 
    print(rows)
    for row in rows:
        main_results.append(row[0])
        
    return jsonify(main_results)


@app.route('/autocomplete',methods = ['GET'])
def autocomplete():
    query = request.args.get('term', '')
    selected_brands = request.args.get('t', '').split(',')
    min_price = request.args.get('min', 10000)
    max_price = request.args.get('max', 50000)
    min = "₹" + str(min_price)
    max = "₹" + str(max_price)
    results = []

    if selected_brands[0] != '':
        print("selected_brand")
        conn = sqlite3.connect('.\database\database.db')
        c = conn.cursor()
        like_clause = ' OR '.join([f"\ufeffPhone_name LIKE '%{brand}%'" for brand in selected_brands])
        query = f'''SELECT \ufeffPhone_name FROM phone WHERE ({like_clause}) AND (Price BETWEEN '{min}' AND '{max}')'''
        c.execute(query)
        rows = c.fetchall()
    else:
        print("query")
        conn = sqlite3.connect('.\database\database.db')
        c = conn.cursor()
        c.execute("SELECT \ufeffPhone_name FROM phone WHERE \ufeffPhone_name LIKE ? AND (Price BETWEEN ? AND ?)",
            ('%' + query + '%', min, max,))
        rows = c.fetchall() 
    print(rows)
    for row in rows:
        results.append(row[0])
        
    return jsonify(results)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + query + '%',))
    rows = c.fetchone()   
    results = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    return render_template('search.html', results=results)

@app.route('/se', methods=['POST', 'GET'])
@login_required
def se():
    phone1_name = request.args.get('phone1_name')
    phone2_name = request.args.get('phone2_name')
    print(phone1_name,phone2_name)
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    if phone1_name:
        c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + phone1_name + '%',))
        rows = c.fetchone()   
        result = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    else:
        c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ( "OnePlus 7 Pro ",))
        rows = c.fetchone()   
        result = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}

    if phone2_name:
        c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + phone2_name + '%',))
        rows = c.fetchone()   
        res_1 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    else:
        c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ( "OnePlus 10T ",))
        rows = c.fetchone()   
        res_1 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}

    if not phone1_name:
        c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ( "OnePlus 7 ",))
        rows = c.fetchone()   
        res_2 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    else:
        res_2 = None
        
    return render_template("se.html",result=result,res_1=res_1,res_2=res_2)

@app.route('/Auto_search')
def Auto_search():
    query = request.args.get('q', '')
    result = []
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + query + '%',))
    rows = c.fetchone()   
    phone_1 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    print(phone_1)
    return jsonify(phone_1)

@app.route('/Auto_search_1')
def Auto_search_1():
    query1 = request.args.get('w', '')
    phone_2 = []
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + query1 + '%',))
    rows = c.fetchone()   
    phone_2 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    print(phone_2)
    return jsonify(phone_2)

@app.route('/Auto_search_2')
def Auto_search_2():
    query2 = request.args.get('e', '')
    phone_3 = []
    conn = sqlite3.connect('.\database\database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM phone WHERE \ufeffPhone_name LIKE ?", ('%' + query2 + '%',))
    rows = c.fetchone()   
    phone_3 = {'column1':  rows[0], 'column2':  rows[1], 'column3':  rows[2], 'column4':  rows[3], 'column5':  rows[5],
                 'column6':  rows[6], 'column7':  rows[7], 'column8':  rows[8], 'column9':  rows[9], 'column10':  rows[10], 'column11':  rows[11]}
    print(phone_3)
    return jsonify(phone_3)

@app.route('/compare/<phone1_name>/<phone2_name>', methods=['POST'])
def compare(phone1_name, phone2_name):
    if request.method == 'POST':
        b = request.form.get('compare-btn')
        return redirect(url_for('se', phone1_name=phone1_name, phone2_name=phone2_name))

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
   