from flask import Flask, render_template,request, flash, redirect, url_for, session, jsonify
#import sqlite3
from flask_mysqldb import MySQL 
from email_validator import validate_email, EmailNotValidError
import string
import secrets
import base64
import requests
from datetime import datetime


app = Flask(__name__)

app.secret_key = "ilovejesus"

#mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rp_users'

mysql = MySQL(app)


def get_country_details(country_code):
    response = requests.get(
    f'https://api.countrystatecity.in/v1/countries/{country_code}',
    headers={'X-CSCAPI-KEY': 'a3RQYjRqUmhmT1hkZDdjVHA4enFMcWZ0QVlNaDU1NUN1QnZ2MjNWTQ=='}
    )
    
    if response.ok:
        return response.json()
    else:
        print('Country not found')
        return None





def get_state_details(country_code, state_code):
    response = requests.get(
    f'https://api.countrystatecity.in/v1/countries/{country_code}/states/{state_code}',
    headers={'X-CSCAPI-KEY': 'a3RQYjRqUmhmT1hkZDdjVHA4enFMcWZ0QVlNaDU1NUN1QnZ2MjNWTQ=='}
    )
    
    if response.ok:
        state = response.json()
        print(f"{state['name']}")
        return state
    else:
        print('State not found')
        return None






@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rp_code = request.form.get("rp_code")
        pwd = request.form.get("login_password")
        cursor= mysql.connection.cursor()
        cursor.execute("SELECT encoded_password FROM rp_users_info WHERE rp_code = %s", (rp_code,))
        user = cursor.fetchone()
        cursor.close()
        print(user)

        if not user:
            flash("'Invalid user'")
            return render_template("Login Form Animate.html", error='Invalid user')
            

        encoded_password = user[0]
        print(encoded_password)
        try:
            decoded_password = base64.b85decode(encoded_password).decode("utf-8")
            print(decoded_password)
        except Exception as e:
            print(f"Decoding error: {e}")
            return render_template("Login Form Animate.html", error='Invalid password encoding')

        if pwd == decoded_password:
            session['rp_code'] = rp_code
            return redirect(url_for("profile", rp_code=rp_code))
        else:
            return render_template("Login Form Animate.html", error='Invalid password')
    
    return render_template("Login Form Animate.html") 

    



def unique_code(country_code, state_code, gender):
    year= str(datetime.now().year)[-2:]
    cursor = mysql.connection.cursor()
    cursor.execute('select rp_code from rp_users_info') 
    existing_codes = {row[0] for row in cursor.fetchall()}
    if gender == "MALE":
        cursor.execute('SELECT COUNT(*) FROM rp_users_info WHERE gender = %s', (gender,))
        result = cursor.fetchone()
        count = result[0] + 1  # Add 1 to get the next user number

    else:
        cursor.execute('SELECT COUNT(*) FROM rp_users_info WHERE gender = %s', (gender,))
        result = cursor.fetchone()
        count = result[0] + 1  # Add 1 to get the next user number
        

    cursor.close()
    
    
    gender= (gender[:2]).upper()
    while True:
        
        
        
        code = country_code + state_code + year + "-" + gender + f"{count}"
        if code not in existing_codes:
            return code
    


    







    



@app.route('/signup', methods=[ "GET","POST" ])
def signup():
    return render_template("Signup Form.html")



@app.route("/register", methods=[ "GET","POST" ])
def register():
    
    
    if request.method == "POST":
        
        surname= request.form.get("surname")
        full_name= request.form.get("full_name")
        email= request.form.get("email")
        country_code= request.form.get("country")
        state_code= request.form.get("state")
        city= request.form.get("city")
        country= get_country_details(country_code)
        country_name= country['name']
        country = country_name    
        state_info= get_state_details(country_code, state_code)
        state = state_info['name']
        
        
        
        address= request.form.get("address")
        date_of_birth= request.form.get("date_of_birth")
        phone_number= request.form.get("phone_number")
        gender = request.form.get("gender")
        rp_code= unique_code(country_code, state_code, gender)
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password != confirm_password:
            flash("Error: Passwords do not match!")
            return redirect(url_for('signup'))
        
        else:
            encoded_password = base64.b85encode(password.encode("utf-8"))
            print(encoded_password)

        
        try:
            cursor = mysql.connection.cursor()

            # 2. Check for existing email securely
            cursor.execute("SELECT email FROM rp_users_info WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash(f'Email {email} is already registered. Please use a different email.', 'error')
                print(f'Email {email} is already registered. Please use a different email.', 'error')
                cursor.close()
                return redirect(url_for('signup'))

        except Exception as e: 
            # General database or unexpected error handling
            flash(f'An error occurred during registration: {str(e)}', 'error')
            print(f"Database Error: {e}")
            return redirect(url_for('signup'))

            
        print("Received form data:")
        print("First Name:", surname)
        print("Email:", email)
        print("rp_code:", rp_code)
        
        
        cursor = mysql.connection.cursor()
        #cursor.execute("create table if not exists users (id integer primary key autoincrement, first_name text, last_name text, email text, address text, date_of_birth integer, phone_number integer)")
        
        sql = """
        INSERT INTO rp_users_info 
        (rp_code, surname, full_name, email, country, state, city, address, date_of_birth, phone_number, gender, encoded_password) 
        VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        data = (
        rp_code, 
        surname, 
        full_name, 
        email,
        country,
        state,
        city, 
        address, 
        date_of_birth, 
        phone_number, 
        gender, 
        encoded_password
        )
        
        cursor.execute(sql, data)
        
        mysql.connection.commit()
        
        
        cursor.close()
        
        
        
        session['rp_code'] = rp_code
        #return redirect(url_for("profile"))
        return redirect(url_for("profile", rp_code=rp_code))
    return render_template("Signup Form.html")    

    
        


    


    
   

#app.run(debug=True)

@app.route("/profile")
def profile():
    if 'rp_code' in session:
        rp_code = session.get('rp_code')

    if not rp_code:
        # user not logged in, redirect to login
        flash("Please log in first.")
        return redirect(url_for('login'))

    # Fetch user details from DB
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rp_users_info WHERE rp_code = %s", (rp_code,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        flash("User not found.")
        return redirect(url_for('login'))

    # Pass user to template

    return render_template("D.board.html", user=user)
    #else:
    #return redirect(url_for('login'))
    
    #return render_template("D.board.html")


@app.route("/logout")
def logout():
    session.pop('rp_code', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
        app.run(debug=True)