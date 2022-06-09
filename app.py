#!/usr/bin/env python2.7
import arrow
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, session
from db import Database
import helper as helper


tmpl_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = '\x17af*\xaee3\xd00\xca\xdf\xeeE\xd5\x89w\xdb\xe0_/\xed\xd8\x02h'

db = Database()

@app.before_request
def before_request():
    g.connection = db.create_connection()

@app.teardown_request
def teardown_request(exception):
    db.close_connection()


@app.route('/')
def index():
    return redirect('/login')

@app.route('/landing', methods=['GET'])
def landing():
    return render_template("landing.html")

@app.route('/login', methods=['GET'])
def login():
    if check_login():
        return redirect('/listshirts')
    return render_template("login.html")

@app.route('/validate', methods=['POST'])
def validate_user():
    email = str(request.form.get("email")).lower()
    pw = request.form.get("pw")
    res = db.login(email, pw)
    if res:
        user = db.get_user(email)
        session['email'] = email
        session["user_id"] = user["user_id"]
        return redirect('/listshirts')
    session["exists"] = True
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if check_login():
        return redirect('/listshirts')
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("pw")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        id = db.create_user(email, pw, first_name, last_name)
        session['email'] = email
        session['user_id'] = id
        return redirect('/listshirts')
    session["exists"] = True
    return redirect('/signup')

@app.route('/addshirt', methods=['GET', 'POST'])
def addshirt():
    if not check_login():
        return redirect('/login')
    if request.method == "GET":
        return render_template("addshirt.html")
    elif request.method == "POST":
        name = request.form.get("name")
        text = request.form.get("text")
        url = request.form.get("url")
        img_id = ''
        # check if the post request has the file part
        if 'file' in request.files:
            img_id = helper.handleImageUpload(request)
        id = db.create_shirt(session["user_id"], name, text, url, "created", img_id)
        return redirect('/listshirts')
    return redirect('/addshirt')


@app.route('/signout', methods = ['GET','POST'])
def sign_out():
    session.pop("email")
    session.pop("user_id")

    return redirect("/login")

@app.route('/editshirt/<shirt_id>', methods=['GET','POST'])
def editshirt(shirt_id):
    if check_login():
        #lets fetch the shirt
        shirt = db.get_shirt(shirt_id)
        if(shirt["user_id"] != session["user_id"]):
             return redirect("/listshirts")
        if request.method == "POST":
            name = request.form.get("name")
            text = request.form.get("text")
            url = request.form.get("url")
            img_id = ''
            # check if the post request has the file part
            if 'file' in request.files:
                img_id = helper.handleImageUpload(request)
            db.update_shirt(shirt_id, name, text, url, img_id)
            shirt = db.get_shirt(shirt_id)
        qr_url, options = helper.getImageUrl(shirt["qr_id"])
        img_url = None
        if(shirt["image_id"] != None and shirt["image_id"] != "None"):
            img_url, options = helper.getImageUrl(shirt["image_id"])
        return render_template("editshirt.html", name=shirt["name"], text=shirt["text_content"], url=shirt["redirect_url"], id=shirt["shirt_id"], qr_url=qr_url, img_url=img_url)
    return redirect('/login')

@app.route('/deleteshirt/<shirt_id>', methods=['GET'])
def deleteshirt(shirt_id):
    if check_login():
        #lets fetch the shirt
        shirt = db.get_shirt(shirt_id)
        if(shirt["user_id"] != session["user_id"]):
             return redirect("/listshirts")
        shirt = db.delete_shirt(shirt_id)
        return redirect('/listshirts')
    return redirect('/login')

@app.route('/listshirts', methods=['GET'])
def listshirts():
    if check_login():
        shirts = db.get_user_shirts(session["user_id"])
        user = db.get_user(session["email"])
        for shirt in shirts:
            qr_url, options = helper.getImageUrl(shirt["qr_id"])
            shirt['qr_url'] = qr_url
        if request.method == "GET":
            return render_template("listshirts.html", shirts=shirts, user=user)
    return redirect('/login')

@app.route('/shirt/<shirt_id>', methods=['GET'])
def shirt(shirt_id):
    shirt = db.get_shirt(shirt_id)
    if(shirt["redirect_url"]):
        return redirect(shirt["redirect_url"])
    else:
        img_url = None
        if(shirt["image_id"] != None and shirt["image_id"] != "None"):
            img_url, options = helper.getImageUrl(shirt["image_id"])
        return render_template("shirt.html", name=shirt["name"], text=shirt["text_content"], url=shirt["redirect_url"], id=shirt["shirt_id"], img_url=img_url)


def check_login():
    if "email" and "user_id" in session:
        return True
    return False

if __name__ == "__main__":
    app.secret_key = '\x17af*\xaee3\xd00\xca\xdf\xeeE\xd5\x89w\xdb\xe0_/\xed\xd8\x02h'
    import click
    @click.command()
    @click.option('--debug', is_flag = True)
    @click.option('--threaded', is_flag = True)
    @click.argument('HOST', default = '0.0.0.0')
    @click.argument('PORT', default = 8111, type = int)

    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:
            python server.py
        Show the help text using:
            python server.py --help
        """

        HOST, PORT=host, port
        print("running on %s : %d" % (HOST, PORT))
        app.secret_key = '\x17af*\xaee3\xd00\xca\xdf\xeeE\xd5\x89w\xdb\xe0_/\xed\xd8\x02h'
        app.run(host = HOST, port = PORT, debug = debug, threaded = threaded)

    app.secret_key = '\x17af*\xaee3\xd00\xca\xdf\xeeE\xd5\x89w\xdb\xe0_/\xed\xd8\x02h'
    run()
