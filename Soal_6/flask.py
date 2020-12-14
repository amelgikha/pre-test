from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask.wrappers import Response 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
import cv2
import xlsxwriter
import io
import os
  
app = Flask(__name__) 
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your password'
app.config['MYSQL_DB'] = 'astra'
  
mysql = MySQL(app) 
  
@app.route('/') 
@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, )) 
        account = cursor.fetchone() 
        if account: 
            session['loggedin'] = True
            session['id'] = account['id'] 
            session['username'] = account['username'] 
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg) 
        else: 
            msg = 'Incorrect username / password !'
    return render_template('user_login.html', msg = msg) 
  
@app.route('/download')
def download():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    result = cursor.fetchall()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook()
    sheet = workbook.add_worksheet('Report')
    sheet.write(0,0,'nama')
    sheet.write(0,1,'email')
    sheet.write(0,2,'video')

    idx = 0
    for row in result:
        sheet.write(idx+1, 0, str(row['nama']))
        sheet.write(idx+1, 1, str(row['email']))
        sheet.write(idx+1, 2, str(row['video']))
        idx += 1
    
    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/ms-excel", headers="Content-Disposition:atactchment;filename=filterimage.xlsx")
  
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 
        username = request.form['username'] 
        password = request.form['password'] 
        email = request.form['email'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, )) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('user_register.html', msg = msg) 

@app.route('/filterimage', methods=['GET','POST'])
def filterimage():
    filename = 'video.avi'
    fps = 24.0
    my_res = '720p'

    def change_res(cap,width,height):
        cap.set(3,width)
        cap.set(4,height)

    STD_DIMENSION = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920,1080),
        "4k": (3840, 2160)
    }
    
    def get_dims(cap,res='1080p'):
        width, height = STD_DIMENSION['480']
        if res in STD_DIMENSION:
            width, height = STD_DIMENSION[res]
        change_res(cap, width, height)
        return width, height

    VIDEO_TYPE = {
        '.avi': cv2.VideoWriter_fourcc(*'XVID'),
        '.mp4': cv2.VideoWriter_fourcc(*'H264')
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    cap = cv2.VideoCapture(0)
    dims = get_dims(cap,res=my_res)
    video_type_cv2 = get_video_type(filename)

    out = cv2.VideoWriter(filename, video_type_cv2, fps, dims)

    while(True):
        ret,frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    out.releas()
    cv2.destroyAllWindows()