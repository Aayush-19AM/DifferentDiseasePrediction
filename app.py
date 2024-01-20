from flask import Flask, flash, request, redirect, url_for, render_template

from flask_material import Material
from flask import Flask
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mankaraayush18@gmail.com'
app.config['MAIL_PASSWORD'] = 'yajt eoui mofh qhxn'
app.config['MAIL_MAX_EMAILS'] = None
mail = Mail(app)

Material(app)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login.html')
def login():

    return render_template("login.html")

""" @app.route('/')
def root():
   return render_template('login.html') """


@app.route('/registration.html')
def registration():
    return render_template("registration.html")


@app.route('/new.html', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        a = request.form['name']
        b = request.form['a']
        c = request.form['email']
        d = request.form['pass']
        e = request.form['mob']
        f = request.form['add']
        with sqlite3.connect("test3.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO PATIENT2 (NAME,ADHAR,EMAIL,PASS,MOB,ADDRESS) VALUES (?,?,?,?,?,?)",
                        (a, b, c, d, e, f))
            con.commit()
            # if(cur.execute()==True):
        with mail.connect() as conn:
            msg = Message('Credentials for Health care login', sender='mankaraayush18@gmail.com', recipients=[c])
            msg3 = "Thank you for registering with our application      "
            msg1 = "  Your user_id %s" % c
            msg2 = "   Your password %s" % d
            msg.body = msg3 + msg1 + msg2
            # msg.body=msg1
            # msg.body=msg2bb
            conn.send(msg)
            # return "Sent"
            return render_template('login.html')

    return render_template('registration.html')


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        u = str(request.form['username'])
        p = str(request.form['password'])
        with sqlite3.connect("test3.db") as con:
            cur = con.cursor()
        find_user = ("SELECT * FROM PATIENT2 WHERE PASS=?  AND EMAIL= ? ")
        cur.execute(find_user, [(u), (p)])
        # con.commit()
        result = cur.fetchall()
        if result:
            return render_template('homepage.html', u=u)
        else:
            msg = "Error message:Please Enter a valid user name or password"
            return render_template('login.html', msg=msg)
@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
