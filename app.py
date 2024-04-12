from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import pickle
import imutils
import sklearn
from tensorflow.keras.models import load_model
# from pushbullet import PushBullet
import joblib
import numpy as np
from tensorflow.keras.applications.vgg16 import preprocess_input
# from flask_sqlalchemy import SQLAlchemy
from flask_material import Material
from flask import Flask
from flask_mail import Mail, Message
import sqlite3

# Loading Models
# covid_model = load_model('models/covid.h5')
# braintumor_model = load_model('models/braintumor.h5')
# alzheimer_model = load_model('models/alzheimer_model.h5')
diabetes_model = pickle.load(open('models/diabetes.sav', 'rb'))
heart_model = pickle.load(open('models/heart_disease.pickle.dat', "rb"))
# pneumonia_model = load_model('models/pneumonia_model.h5')
breastcancer_model = joblib.load('models/cancer_model.pkl')

# Configuring Flask
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# , template_folder='templates'
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mankaraayush18@gmail.com'
app.config['MAIL_PASSWORD'] = 'yajt eoui mofh qhxn'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True
app.config['MAIL_MAX_EMAILS'] = None
mail = Mail(app)

Material(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")
@app.route('/login.html')
def login():
    #df = pd.read_csv("data/iris.csv")
    return render_template("login.html")

""" @app.route('/')
def root():
   return render_template('login.html') """



@app.route('/registration.html')
def registration():
    return render_template("registration.html")

@app.route('/new.html', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      a=request.form['name']
      b=request.form['a']
      c=request.form['email']
      d=request.form['pass']
      e=request.form['mob']
      f=request.form['add']
      with sqlite3.connect("test3.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO PATIENT2 (NAME,ADHAR,PASS,EMAIL,MOB,ADDRESS) VALUES (?,?,?,?,?,?)",(a,b,c,d,e,f) )   
        con.commit()
        #if(cur.execute()==True):
      with mail.connect() as conn:
        msg = Message('Credentials for Health care login', sender = 'mankaraayush18@gmail.com', recipients =[c])
        msg3="Thank you for registering with our application      "
        msg1 ="  Your user_id %s" %c
        msg2="   Your password %s" %d
        msg.body=msg3+msg1+msg2
        #msg.body=msg1
        #msg.body=msg2bb
        conn.send(msg)
        #return "Sent"
        return render_template('login.html')
        
   return render_template('registration.html')
@app.route('/validate',methods=['GET', 'POST'])
def validate():
  if request.method=='POST':
     u=str(request.form['username'])
     p=str(request.form['password'])
     with sqlite3.connect("test3.db") as con:
       cur=con.cursor()
     find_user=("SELECT * FROM PATIENT2 WHERE PASS=?  AND EMAIL= ? ")
     cur.execute(find_user,[(u),(p)]) 
       #con.commit()
     result=cur.fetchall()
     if result:
        return render_template('homepage.html',u=u)
     else:
        msg="Error message:Please Enter a valid user name or password"
        return render_template('login.html',msg=msg)
@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/index.html')
def home():
    return render_template('index.html')


############################################# BRAIN TUMOR FUNCTIONS ################################################

def preprocess_imgs(set_name, img_size):
    """
    Resize and apply VGG-15 preprocessing
    """
    set_new = []
    for img in set_name:
        img = cv2.resize(img,dsize=img_size,interpolation=cv2.INTER_CUBIC)
        set_new.append(preprocess_input(img))
    return np.array(set_new)

def crop_imgs(set_name, add_pixels_value=0):
    """
    Finds the extreme points on the image and crops the rectangular out of them
    """
    set_new = []
    for img in set_name:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # threshold the image, then perform a series of erosions +
        # dilations to remove any small regions of noise
        thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in thresholded image, then grab the largest one
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # find the extreme points
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

        ADD_PIXELS = add_pixels_value
        new_img = img[extTop[1]-ADD_PIXELS:extBot[1]+ADD_PIXELS,
                      extLeft[0]-ADD_PIXELS:extRight[0]+ADD_PIXELS].copy()
        set_new.append(new_img)

    return np.array(set_new)

########################### Routing Functions ########################################

@app.route('/home')
def home2():
    return render_template('homepage.html')

@app.route('/breastcancer')
def breast_cancer():
    return render_template('breastcancer.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/heartdisease')
def heartdisease():
    return render_template('heartdisease.html')


########################### Result Functions ########################################



@app.route('/resultd', methods=['POST'])
def resultd():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        pregnancies = request.form['pregnancies']
        glucose = request.form['glucose']
        bloodpressure = request.form['bloodpressure']
        insulin = request.form['insulin']
        bmi = request.form['bmi']
        diabetespedigree = request.form['diabetespedigree']
        age = request.form['age']
        skinthickness = request.form['skin']
        pred = diabetes_model.predict(
            [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, diabetespedigree, age]])
        # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour Diabetes test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
        return render_template('resultd.html', fn=firstname, ln=lastname, age=age, r=pred, gender=gender)


@app.route('/resultbc', methods=['POST'])
def resultbc():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        cpm = request.form['concave_points_mean']
        am = request.form['area_mean']
        rm = request.form['radius_mean']
        pm = request.form['perimeter_mean']
        cm = request.form['concavity_mean']
        pred = breastcancer_model.predict(
            np.array([cpm, am, rm, pm, cm]).reshape(1, -1))
        # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour Breast Cancer test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
        return render_template('resultbc.html', fn=firstname, ln=lastname, age=age, r=pred, gender=gender)



@app.route('/resulth', methods=['POST'])
def resulth():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        nmv = float(request.form['nmv'])
        tcp = float(request.form['tcp'])
        eia = float(request.form['eia'])
        thal = float(request.form['thal'])
        op = float(request.form['op'])
        mhra = float(request.form['mhra'])
        age = float(request.form['age'])
        print(np.array([nmv, tcp, eia, thal, op, mhra, age]).reshape(1, -1))
        pred = heart_model.predict(
            np.array([nmv, tcp, eia, thal, op, mhra, age]).reshape(1, -1))
        # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour heart test results are ready.\nRESULT: {}'.format(firstname,['NEGATIVE','POSITIVE'][pred]))
        return render_template('resulth.html', fn=firstname, ln=lastname, age=age, r=pred, gender=gender)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    app.run(debug=True)
