from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,json
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import time
import redis
from flask_session import Session
import os


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("db_name")
app.config["MYSQL_HOST"] = "bucketlistapp-mysql-svc"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.secret_key = "bucketapp"
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://bucketlistapp-redis-svc:6379')


mysql.init_app(app)
sess = Session(app)
sess.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        
        if _name and _email and _password:
        
            cursor = mysql.connection.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                mysql.connection.commit()
                return json.dumps({'status':'true','message':'User created successfully !'})  
            else:
                return json.dumps({'status':'false','error':str(data[0])}) 
        else:
            return json.dumps({'status':'false','error':'Enter the required fields'}) 
            

    except Exception as e:
        return json.dumps({'status':'false','error':str(e)})
        

@app.route("/signin")
def showSignIn():
    return render_template("signin.html")

@app.route("/validateLogin", methods=["POST"])
def validateLogin():
    try:
        _username = request.form["inputEmail"]
        _password = request.form["inputPassword"]
        cursor = mysql.connection.cursor()
        query = cursor.callproc("sp_validateLogin",(_username,))
        

        if len(query) > 0:
            data = cursor.fetchone()
            real_password = data["user_password"]
            if check_password_hash(real_password,_password):
                session["logged_in"] = True
                session["username"] = _username
                flash("Login succes","success")
                return redirect("/dashboard")
            else:
                #return render_template("error.html",error="Wrong email adress or password")
                flash("Wrong email address or password","danger")
                return redirect(url_for("showSignIn"))
        else:
            #return render_template("error.html",error="Wrong email adress or password ")
            flash("Wrong email address or password","danger")
    except Exception as e:
        #return render_template("error.html",error="FUCK OFF")
        flash("Wrong email address or password","danger")
        return redirect(url_for("showSignIn"))
    finally: 
        cursor.close()
        

@app.route("/dashboard")
def userHome():
    if session.get('username'):
        return render_template("dashboard.html")
    else:
        return render_template('error.html',error="Unauthorized Acceess")

@app.route("/logout")
def signout():
    session.clear()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
