from flask import Flask, render_template , request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.secret_key = 'adivis'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hr_erp_db'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/admin-dashboard' , methods=['POST'])
def admin_dashboard():
    u = request.form['txtName']
    p = request.form['password']
    if (u=='admin' and p=='admin123'):
       session['username']=u
       session['name']='Admin'
       return render_template("admin_dashboard.html")
    else:
       msg="Invalid Username or Password"
       return render_template("admin.html", info=msg)
      

@app.route('/add-employee')
def add_employee():
    return render_template("addemp.html")

@app.route('/show-employee')
def show_employee():
  cursor = mysql.connection.cursor()
  cursor.execute('select empid,name,designation from registration')
  emplist=cursor.fetchall()
  return render_template("showemp.html" ,recordlist=emplist)

@app.route('/search-employee')
def search_employee():
    return render_template("searchemp.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/save-employee' , methods=['POST'])
def save_employee():
    #get form data
    i= request.form['txtempid']
    n= request.form['txtname']
    e= request.form['txtemail']
    m= request.form['txtmobile']
    d= request.form['txtdesig']
    s= request.form['txtsalary']


# database connection
    cursor = mysql.connection.cursor()
    #query to insert employee details
    cursor.execute('insert into registration(empid,name,email,mobile,designation,salary)  values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))
    mysql.connection.commit()
    cursor.close()
    return render_template("save_emp.html")

@app.route('/emp-profile')
def emp_profile():
    id=request.args.get('eid')
    # database connection
    cursor = mysql.connection.cursor()
    #query to fetch employee details
    cursor.execute('select * from registration where empid=%s',(id,))
    emplist=cursor.fetchall()
    return render_template("emp_profile.html", recordlist=emplist)

@app.route('/emp-update', methods=['POST'])
def emp_update():
    i= request.form['txtempid']
    n= request.form['txtname']
    e= request.form['txtemail']
    m= request.form['txtmobile']
    d= request.form['txtdesig']
    s= request.form['txtsalary']
# database connection
    cursor = mysql.connection.cursor()
    #query to update employee details
    cursor.execute('update registration set name=%s,email=%s,mobile=%s,designation=%s,salary=%s where empid=%s',(n,e,m,d,s,i))
    mysql.connection.commit()
    cursor.close()
    return render_template("emp_update.html")

@app.route('/emp-delete')
def emp_delete():
    i=request.args.get('id')
    # database connection
    cursor = mysql.connection.cursor()
    #query to delete employee details
    cursor.execute('delete from registration where empid=%s',(i,))
    mysql.connection.commit()
    cursor.close()
    return render_template("emp_delete.html")
    
@app.route('/emp_searchprocess', methods=['POST'])
def emp_search_process():
    n = request.form['txtName']
    # database connection
    cursor = mysql.connection.cursor()
    #query to search employee details
    cursor.execute('select * from registration where name=%s',(n,))
    emplist=cursor.fetchall()
    cursor.close()

    return render_template("emp_searchresult.html" , recordlist=emplist)
    
@app.route('/logout')
def logout():
  session['name']=''
  return render_template("admin.html")

if __name__ == '__main__':
    app.run(debug=True)