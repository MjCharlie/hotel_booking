import re
from flask import Flask, config ,render_template,request,redirect
import os
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.utils import secure_filename
from flask_mail import Mail
from random import randint
app = Flask(__name__)
with open("config.json","r") as c:
    params=json.load(c)["params"]
mail=Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER']=params["UPLOAD_LOCATION"]
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_passw']

)
mail = Mail(app)
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avtar=  db.Column(db.String(120), unique=True, nullable=False)
    pasw=  db.Column(db.String(120), nullable=False)
class Hotel(db.Model):
    hotel_id = db.Column(db.Integer, primary_key=True)
    # no_booked = db.Column(db.Integer, nullable=False)
    total_room = db.Column(db.Integer ,nullable=False)
    price = db.Column(db.Integer ,nullable=False)
    hotel_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
class order(db.Model):
    order_id = db.Column(db.Integer,primary_key=True)
    hotel_id = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.String(11), nullable=False)
    check_out = db.Column(db.String(11), nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
# pb=order.query.first()
# print(len(pb))
@app.route("/check",methods=['GET','POST'])
def check():
    if request.method=='POST':
        name=request.form.get("check")
        print(str(name))
    return render_template("hht.html")
@app.route("/search",methods=['GET','POST'])
def search():
    if request.method=='POST':
        name=request.form.get("LOCATION")
        EMP= Hotel.query.filter_by(location=name)
        return render_template("search.html",EMP)


@app.route("/see/<string:x>",methods=['GET','POST'])
def see(x):
    return render_template("det.html")
@app.route("/log",methods=['GET','POST'])
def log():
    return render_template("log.html")
@app.route("/sing",methods=['GET','POST'])
def sing():
    return render_template("sign.html")
@app.route("/sign",methods=['GET','POST'])
def sign():
    
    if request.method=='POST':
        name=request.form.get('user')
        passw=request.form.get('passw')
        email=request.form.get('email')
        x=randint(100,1000000000)
        # f=request.files['file']
        # f.filename=name+'.jpg'
        # x=f.filename
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        enter=User(username=name,email=email,avtar=str(x),pasw=passw)
        db.session.add(enter)
        db.session.commit()
    return render_template("index.html")
@app.route("/order/<string:x>/<string:y>",methods=['GET','POST'])
def ord(x,y):
       if request.method == 'POST':
           c_in = request.form.get("cin")
           c_out = request.form.get("cout")
           c_id = int(y)
           if order.query.filter_by(check_in=c_in,check_out=c_out).first():
               pb=order.query.filter_by(check_in=c_in,check_out=c_out)
               l=pb[-1].room
               entry=order(check_in=c_in,check_out=c_out,hotel_id=int(x),client_id=c_id,room=l+1)
               db.session.add(entry)
               db.session.commit()
               print("possible")
               lt=order.query.all()
               mail.send_message(
        "no reply ",
        sender=params["gmail_user"],
        recipients=["vidyarthivishal31@gmail.com"],
        body="THANKS FOR CHOOSING US YOUR HOTEL IS BOOKED SUCCESSFULLY \nYOUR ROOM NO. IS #"+str(1)+"\nYOUR ORDER ID "+str(lt[-1].room)
            )
           else :
               entry=order(check_in=c_in,check_out=c_out,hotel_id=int(x),client_id=c_id,room=1)
               db.session.add(entry)
               db.session.commit()
               print("working")
               lt=order.query.all()
               mail.send_message(
        "no reply ",
        sender=params["gmail_user"],
        recipients=["vidyarthivishal31@gmail.com"],
        body="THANKS FOR CHOOSING US YOUR HOTEL IS BOOKED SUCCESSFULLY \nYOUR ROOM NO. IS "+str(1)+"\nYOUR ORDER ID #"+str(lt[-1].room)+"MUSK"
            )
       return render_template("det.html" , h_id=x , cid=1)

# @app.route("/delete/<string:x>",methods=['GET','POST'])
# def ord(x):
#     pb=Hotel.query.filter_by(username=x).first()
#     db.session.delete(pb)
#     db.session.commit()
    # return "deleted"
@app.route("/hotel",methods=['GET','POST'])
def htl():
    if request.method == 'POST':
        # passw=request.form.get('passw')
        email=request.form.get('email')
        loc=request.form.get('loc')
        f=request.files['file']
        f.filename=email+'.jpg'
        x=f.filename
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        # x=randint(100,1000000000)
        enter=Hotel(price=0,total_room=100,hotel_name=email,image=str(x),location=loc)
        db.session.add(enter)
        db.session.commit()
    return render_template("hotel.html")
@app.route("/")
def hello_world():
    tr=Hotel.query.all()
    return render_template("index.html",tk=tr)
if __name__=="__main__":
    app.run(debug=True)