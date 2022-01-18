import email
import flask
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime

# from session_flask import Session

import MySQLdb.cursors

app = Flask(__name__)
app.secret_key="azeemasad"
# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ajutt92441312'
app.config['MYSQL_DB'] = 'HR'
mysql = MySQL(app)

#index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Sign Up', methods=['GET', 'POST'])
def signUp():
    msg=''
    if request.method == 'POST':
 # Fetch form data
        userDetails = request.form
        firstName = userDetails['fname']
        lastlName = userDetails['lname']
        age=userDetails['age']
        username=userDetails['uname']
        email=userDetails['email']
        password = userDetails['pwd']
        confirmPassword=userDetails['psw']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM regTable WHERE username = %s or email=%s' , (username, email))
        accountOne = cursor.fetchone()
        print(accountOne)
        if accountOne:
            msg="This username or email already exists"
        else:
            cursor = mysql.connection.cursor()
            if password==confirmPassword:      
                cursor.execute("INSERT INTO regTable (firstName ,lastName,age,username ,email, password) VALUES(%s,%s,%s,%s,%s,%s)",(firstName,lastlName ,age,username ,email , password))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('signIn'))

    return render_template('signup.html',msg=msg)

#sign in page
@app.route("/Sign In",methods=['POST','GET'])

def signIn():
    msg=''
    if request.method == 'POST':
        username = request.form['uname']
        passwordd = request.form['pwd']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM regTable WHERE username = %s and password = %s', (username, passwordd))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account[4]
            session['password'] =account[6]
            name=session['username']
            session['email']=account[5]
            email=session['email']
            print(email)
            if account[4]=="admin":
                # return render_template('dashboard.html', name=name)
                return redirect(url_for('dashboard',name=name))


            else:
                return redirect(url_for('usr_dashboard',namees=name))
                # return render_template('usrDashboard.html',name=name)
        else:
            msg='invalid username or password'


    return render_template('signin.html', msg=msg)

@app.route('/Dashboard')

def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM employeesTable')
    totalemp = cursor.fetchone()  
    mysql.connection.commit()
    cursor.close()  
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM applicantsTable')
    total_candidates = cursor.fetchone()  
    mysql.connection.commit()
    cursor.close() 
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM jobsTable')
    totaljobs = cursor.fetchone()  
    mysql.connection.commit()
    cursor.close() 
    return render_template('dashboard.html',emp=totalemp,candidates=total_candidates, tjobs=totaljobs)


@app.route('/Log Out')
def logOut():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('signIn'))


@app.route('/Add Employee', methods=['GET', 'POST'])
def addEmployees():
    msg=''
    name="admin"
    if request.method == 'POST':
     # Fetch form data
        emp_Details = request.form
        emp_name = request.form.get("name", False)
        emp_uname=request.form.get("uname", False)

        emp_email = request.form.get("email", False)
        emp_cnic=request.form.get("cnic", False)
        emp_dept=request.form.get("dept", False)
        emp_type=request.form.get("type", False)



        if not emp_name or not emp_uname or not emp_email or not emp_cnic or not emp_dept :
            msg="*Please complete all the details"
        else:
             
            cursor=mysql.connection.cursor()
            cursor.execute('SELECT * FROM employeesTable WHERE email = %s and dept=%s' , (emp_email, emp_dept))
            accountOne = cursor.fetchone()
            if accountOne :
                msg="This Employee exists in the same Department  "
            else:
                mycursor=mysql.connection.cursor()
                mycursor.execute("INSERT INTO employeesTable(name,username,email ,cnic, dept, typee) VALUES (%s,%s,%s,%s,%s,%s)",(emp_name,emp_uname,emp_email ,emp_cnic,emp_dept, emp_type))
                mysql.connection.commit()
                mycursor.close()
                msg="Employee added!"
            
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT empID, name,email,cnic, dept from employeesTable")
    
    job_Details=mycursor.fetchall()
    mysql.connection.commit()
    mycursor.close()
    header=("ID","Name", "Email","CNIC ","Dept")

    return render_template('addEmployees.html',msg=msg,header=header, data=job_Details, name=name)         
        

# Admin Recruitment jobs
@app.route('/Recruitment')

def recruitment():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * from jobsTable")
    job_Details=mycursor.fetchall()
    mysql.connection.commit()
    mycursor.close()
    header=("Job ID", "Job Title","Catagory","Type","Country")

    return render_template('recruitmentJobs.html', header=header, data=job_Details)

#a form to create new jobs

@app.route('/Recruitment/Create Jobs', methods=['GET', 'POST'])
def createJobs():
    msg=''
    if request.method == 'POST':
     # Fetch form data
        jobsDetails = request.form
        p_title = request.form.get("title", False)
        p_catgory = request.form.get("catagory", False)
        p_type=request.form.get("type", False)
        p_salary=request.form.get("salary", False)
        p_expire=request.form.get("expire", False)
        p_country = request.form.get("country", False)

        if not p_title or not p_catgory or not p_type or not p_expire or not p_country:
            msg="*Please complete all the details"
        else:
            mycursor=mysql.connection.cursor()
            mycursor.execute("INSERT INTO jobsTable(title,catagory ,type,salary,expr ,country) VALUES (%s,%s,%s,%s,%s,%s)",(p_title,p_catgory ,p_type,p_salary ,p_expire , p_country))
            mysql.connection.commit()
            mycursor.close()
            msg="This Job has been posted"

    return render_template('jobs.html', msg=msg)
#candidates page 
@app.route('/Candidates')
def candidates():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT formID, name,email,phone,cnic,job from applicantsTable")
    
    job_Details=mycursor.fetchall()
    mysql.connection.commit()
    mycursor.close()
    header=("ID","Name", "Email","Phone ","CNIC","Job")

    return render_template('candidates.html',header=header, data=job_Details) 


# Admin Payroll

@app.route('/Admin Payroll',methods=['GET', 'POST'])

def admin_payroll():
    msg=''
    if request.method == 'POST':
     # Fetch form data
        jobsDetails = request.form
        ust = request.form.get("name", False)
        email = request.form.get("email", False)
        salary=request.form.get("salary", False)
        time=request.form.get("time", False)

        if not ust or not email or not salary or not time :
            msg="*Please complete all the details"
        else:
            mycursor=mysql.connection.cursor()
            mycursor.execute("INSERT INTO payroll(username,email ,salary,timee ) VALUES (%s,%s,%s,%s)",(ust,email ,salary,time))
            mysql.connection.commit()
            mycursor.close()
            msg="This has been posted"
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT username, email, salary,timee FROM payroll")
    job_Details=mycursor.fetchall()
    mysql.connection.commit()
    mycursor.close()      
    header=("Username","Email", "Salary","Date ")
    

    return render_template('payroll1.html', header=header, data=job_Details)











#pages for user dashboards
@app.route('/User Dashboard/<namees>')
def usr_dashboard(namees):
    return render_template('usrDashboard.html',name=namees)
    # return 'page of {namees}'

# User recruitment jobs
@app.route('/User Recruitment')

def usr_recruitment():
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT * from jobsTable")
    job_Details=mycursor.fetchall()
    header=("ID","Title", "Catagory","Type ")

    mysql.connection.commit()
    mycursor.close()
    name=session['username']

    

    return render_template('usrRecruitment.html',header=header, jobsList=job_Details, name=name)

 

@app.route('/User Profile')
def usrProfile():
    return render_template('usrProfile.html')

#user form for applying jobs
@app.route('/User Recruitment/applyJobs',methods=['GET', 'POST'])

def usr_apply():
    msg=''
    name=session['username']
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT email from regTable where username=%s", (name,))
    emails=mycursor.fetchone()
    mysql.connection.commit()
    mycursor.close()
    if request.method == 'POST':
     # Fetch form data
        apply_Details = request.form
        usr_name = request.form.get("name", False)
        usr_email = request.form.get("email", False)
        usr_phone=request.form.get("phone", False)
        usr_cnic=request.form.get("cnic", False)
        usr_job=request.form.get("job", False)


        if not usr_name or not usr_email or not usr_phone or not usr_cnic:
            msg="*Please complete all the details"
        else:
            mycursor=mysql.connection.cursor()
            mycursor.execute("INSERT INTO applicantsTable(name,email ,phone,cnic,job) VALUES (%s,%s,%s,%s,%s)",(usr_name,usr_email ,usr_phone,usr_cnic,usr_job))
            mysql.connection.commit()
            mycursor.close()
            msg="Your FORM has been received!"
        
    return render_template('usrApply.html',msg=msg, name=name, email=emails)

#User Payroll
@app.route('/User Payroll',methods=['GET', 'POST'])

def usr_payroll():

    
    name=session['username']
    mycursor=mysql.connection.cursor()
    mycursor.execute("SELECT payID,salary, timee from payroll where username=%s", (name,))
    job_Details=mycursor.fetchall()
    mysql.connection.commit()
    mycursor.close()
    header=("No","Salary", "Date")

    
    return render_template('payroll2.html', name=name, data=job_Details, header=header)


