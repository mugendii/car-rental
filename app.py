from flask import Flask, render_template ,flash, redirect, url_for, session, request, logging
from flask import session
from flask import request
from flask import redirect
import pymysql
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
"""from passlib.hash import sha256_crypt
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES"""
import timeit
import datetime
"""from flask_mail import Mail, Message
import os
# from wtforms.fields.html5 import EmailField
"""

app = Flask(__name__)
app.secret_key = 'mugi$#@!8)'



app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_USER'] = 'nur'
app.config['MYSQL_PASSWORD'] = 'secret'
app.config['MYSQL_DB'] = 'menshut'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about us')
def about():
    return render_template('about us.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/reservation', methods=['POST', 'GET'])
def reservation():
    if request.method == 'POST':
        names = request.form['names']
        email = request.form['email']
        phone= request.form['phone']
        nationality = request.form['nationality']
        address = request.form['address']
        appointment_date= request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        category = request.form['category']
        doctor = request.form['doctor']
        fee = request.form['fee']
        conn = pymysql.connect('localhost', 'root', '', 'pottersdb')
        sql = "INSERT INTO `appointments`(`names`, `email`, `phone`, `nationality`, `address`, `appointment_date`, `appointment_time`, `category`, `doctor`, `fee`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # execute above using a cursor
        cursor = conn.cursor()  # create cursor using conn
        #try:
        cursor.execute(sql, (names,email, phone, nationality,address, appointment_date, appointment_time,category,doctor,fee))
        conn.commit()
        return render_template('appointments.html',
                               msg='Your appointment is received')
        # except:
        #     return render_template('appointments.html',
        #                            msg='Your appointment is not received ')

    else:
        return render_template("reservation.html")



@app.route('/gallery')
def gallery():
    return render_template('gallery.html')



@app.route('/view')
def view():
    if 'username' in session:
        conn = pymysql.connect('localhost', 'root', '', 'gabrieldb')
        sql = "select* from reservation"

        cursor = conn.cursor()
        cursor.execute(sql)
        #check how many rows cursor found
        if cursor.rowcount<=0:
            return render_template('view.html',
                                   msg='no bookings')
        #below returns rows from table back to the template
        else:
            rows  = cursor.fetchall()
            return render_template('view.html',
                                   rows = rows)
    else:
        from flask import redirect
        return redirect('/login')








@app.route('/search', methods =['POST', 'GET'])
def search():
    if request.method == 'POST':
        phone = str(request.form['phone'])

        conn = pymysql.connect('localhost', 'root', '', 'gabrieldb')

        sql = "select * from reservation where phone=%s"
        cursor = conn.cursor()
        cursor.execute(sql, (phone))

        if cursor.rowcount == 0:
            return render_template('search.html',
                                   msg='No user Has reserved a vehicle!!Try Again Later')


        else:
            rows = cursor.fetchall()
            return render_template('search.html',
                                   rows=rows)
            return redirect('/')


    else:
        return render_template('search.html')


@app.route('/contact us', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':


        firstname = request.form['first name']
        lastname = request.form['last name']
        email = request.form['your email']
        conn = pymysql.connect('localhost', 'root', '', 'pottersdb')
        sql = "INSERT INTO `newsletter`(`first name`, `last name`, `your email`) VALUES (%s,%s,%s)"
        # execute above using a cursor
        cursor = conn.cursor()  # create cursor using conn
        #try:
        cursor.execute(sql, (firstname,lastname, email))
        conn.commit()
        return render_template('contact us.html',
                               msg='You have subscribed')
       #

    else:
        return render_template("contact us.html")
def message():
    if request.method == 'POST':


        firstname = request.form['first name']
        lastname = request.form['last name']
        email = request.form['email']
        location = request.form['location']
        find = request.form['know']
        message = request.form['message']
        conn = pymysql.connect('localhost', 'root', '', 'pottersdb')
        sql = "INSERT INTO `messages`(`first name`, `last name`,  `email`, `location`, `know`'message',) VALUES (%s,%s,%s,%s,%s,%s)"
        # execute above using a cursor
        cursor = conn.cursor()  # create cursor using conn
        try:
            cursor.execute(sql, ( firstname,lastname, email, location,message, find))
            conn.commit()
            return render_template('contact us.html',
                                   msg='Your message has been received')
        except:
            return render_template('contact us.html',
                                   msg='An error occured')

    else:
        return render_template('contact us.html')

if __name__ == '__main__':

    app.run(debug=True, port=5000)
