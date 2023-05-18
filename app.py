from flask import *
import psycopg2
import psycopg2.extras
import urllib.request
import os
from werkzeug.utils import secure_filename
# from sqlalchemy.orm import Session
# from sqlalchemy.sql import select
# from xmodels import Account,db
# from sqlalchemy import select




app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:imali54321@localhost:5432/dbms'
# db = db(app)
# db.init_app(app)
  





@app.route('/', methods=['GET', "POST"])
def index():
    return render_template('index.html')
                   
conn=psycopg2.connect(
host='localhost',
database='dbms',
user='postgres',
password='imali54321',
port=5432
)     


print('Connecting to the PostgreSQL database...')

@app.route('/reg', methods=['GET', "POST"])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email=request.form['email']
        password = request.form['password']
        print(name,email,password)
        query="'" + name + "'" + "," + "'" + password + "'" + "," + "'" + email + "'"  
        cur=conn.cursor()
        cur.execute("select *from account where username='{name}' ")
        res=cur.fetchall()
        print(res)
        if len(res)==0:
            cur=conn.cursor()
            cur.execute("insert into account (username,pass,email) values(" + query + ")")
            conn.commit()
            msg="Account Created Successfully"
            return render_template('user2.html',msg=msg)
        else:
            msg="Username already exsists"
            return render_template('user2.html',msg=msg)
        # cnonnection open with db
        # create cursor
        # ecue the query INSERT

    return render_template('user2.html')



@app.route('/log', methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        print(name,password)
         
    
        curr=conn.cursor()
        sql=f"select username,pass from account where username='{name}' and pass='{password}'"
        curr.execute(sql)
        res=curr.fetchall()
        print(res)
        conn.commit()
        if res:
            print("Logged in successfully")
            msg="Logged in Successfully"
            curr = conn.cursor()
            sql = f"CALL update_current_user('{name}')"
            curr.execute(sql)
            conn.commit()
            return render_template('products2.html',msg=msg)


        else:
            print("Invalid credentials")    
            msg="Invalid Credintials"
            return render_template('user2.html',msg=msg)

    return render_template('user2.html')

#         # cnonnection open with db
#         # create cursor
#         # ecue the query INSERT

#     return render_template('user2.html')

 ##-----------------------ORM-----------------------------
   
# @app.route("/log", methods=['GET', 'POST'])
# def login1():
#     if request.method == 'POST':
#          name = request.form['username']
#          password = request.form['password']
#          print(name,password)
         
#          account=Account.query.filter_by(username=name, password=password).one()
#          if account:
#             print("logged in successfully")
#             msg = "logged in successfully"
#             return render_template("student-portal.html", msg=msg, name=name)

#          else:
#             print("Incorrect email or password")
#             msg = "Incorrect email or password"

#     return render_template("/student-login.html")


@app.route('/forgot', methods=['GET', "POST"])
def forgot():
    if request.method == 'POST':
        username=request.form['name']
        email=request.form['email']
        password=request.form['password']
        #print(username,email,password)
        curr=conn.cursor()
        sql=f"select *from account where username='{username}' and email='{email}'"
        curr.execute(sql)
        res=curr.fetchall()
        print(res)
        if len(res)==0:
            msg="Username and Email donot match"
            return render_template('forgot.html',msg=msg)
        else:
            res2=res[0]
            print(res2[0])
            curr=conn.cursor()
            sql2=f"select newpassword('{res2[0]}','{password}')"
            curr.execute(sql2)
            conn.commit()
            msg="Password updated"
        
        return render_template('forgot.html',msg=msg)
    return render_template('forgot.html')    



 
UPLOAD_FOLDER = 'static'
  
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




images=[]



@app.route('/addprod', methods=['GET', "POST"])
def addprod():
    if request.method == 'POST':
        prodname = request.form['prodname']
        quantity = request.form['quantity']
        description=request.form['description']
        username=request.form['username']
        print(prodname,quantity,description,username)
        sql=f"select id from account where username='{username}'"
        sql2=f"call vendors('{username}','{prodname}')"
        curr=conn.cursor()
        curr.execute(sql)
        res=curr.fetchone()
        curr=conn.cursor()
        curr.execute(sql2)
        conn.commit()

        prodid=''
        prodid=prodid.join(map(str,res))
       
        #print(res)
       

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
        
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            images.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #print('upload_image filename: ' + filename)
    
            query="'" + prodname + "'" + "," + "'" + quantity + "'" + "," + "'" + description  + "'" + "," + "'" + prodid + "'" + "," + "'" + filename  + "'"
            curr=conn.cursor()
            curr.execute("insert into product (prodname,price,description,id,image) values(" + query + ")")
            conn.commit()
            print(images)
    
            flash('Image successfully uploaded and displayed below')
            return render_template('addprod.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
            

    

    return render_template('addprod.html')
         
    
    #-------------------------TESTING FOR GITHUB-----------------------------------


  
  
# @app.route('/addprod', methods=['GET', "POST"  ])
# def upload_image():
   
#    if request.method=='POST':
#        if request.files:
#            image=request.files['image']
#            print(image)
#            return redirect(request.url)
       
#    return render_template('addprod.html')        



 
# UPLOAD_FOLDER = 'templates\image'
  
# app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
      
  
  
# @app.route('/addprod', methods=['POST','GET'])
# def upload_image():
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    
#     file = request.files['image']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #print('upload_image filename: ' + filename)
 
#         cursor.execute("INSERT INTO product (image) VALUES (%s)", (filename,))
#         conn.commit()
 
#         flash('Image successfully uploaded and displayed below')
#         return render_template('addprod.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect(request.url)
          



@app.route('/products', methods = ['GET', 'POST'])
def display():
    cur = conn.cursor()
    cur.execute("SELECT image FROM product")
    rows = cur.fetchall()
    cur.close()
    
    # Create a list of image paths
    #\dbms\templates\dynamic
    prices=[]
    curr = conn.cursor()
    image_paths = ['/static/' + row[0] for row in rows]
    image=[row[0] for row in rows]
    for i,j in zip(image_paths, image):
        curr.execute(f"select price from product where image='{j}'")
        price=curr.fetchone()
        prices.append([price[0], i])
    if request.method == 'POST':
        price = request.form['price']
        #print(price)
        image = request.form['img']
        image = image[8:]
        curr = conn.cursor()
        sql = 'select username from currentuser where uid = 1'
        curr.execute(sql)
        username = curr.fetchall()
        un = username[0]
        curr = conn.cursor()
        sql = f"select id from account where username = '{un[0]}'"
        curr.execute(sql)
        uid = curr.fetchall()
        sql = f"insert into cart values('{uid[0][0]}', '{price}', '{image}'); "
        #print(type(price))
        #print(sql)
        curr.execute(sql)
        conn.commit()
    # Render the HTML template with the image paths
    return render_template('products2.html',prices=prices)



# @app.route('/log', methods=['GET', "POST"])
# def login():
#     if request.method == 'POST':
#         name = request.form['username']
#         password = request.form['password']
#         print(name,password)


username2=None
@app.route('/checkout', methods = ['POST','GET'])
def checkout():
    if request.method == 'POST': 
        curr=conn.cursor()
        curr.execute("select username from currentuser where uid=1")
        res=curr.fetchall()
        name=res[0]
        #print(name[0])
        #print(123)
        username=request.form['name']
        username2=username
        address=request.form['address']
        city=request.form['city']
        phone=request.form['phone']
        if(name[0]==username):
           # print(username,address,city,phone)
            query="'" + username + "'" + "," + "'" + address + "'" + "," + "'" + city  + "'" + "," + "'" + phone + "'" 
          
            curr=conn.cursor()
            curr.execute("insert into details (username,address,city,phone) values(" + query + ")")
            conn.commit()
            curr=conn.cursor()
            sql=f"select image, price from account inner join cart on account.id=cart.id where username='{username}'" 
            curr.execute(sql)
            res=curr.fetchall()
            print(res)
            curr=conn.cursor()
            curr.execute("select image,sum(price),count(image) from cart group by id,image having id =(select id from account inner join currentuser on account.username=currentuser.username)")
            msg=curr.fetchall()
            conn.commit()
            msg2="ORDER CONFIRMED"

            sql1=f"select id from cart where id =(select id from account inner join currentuser on account.username=currentuser.username)"
            curr=conn.cursor()
            curr.execute(sql1)
            res1=curr.fetchone()
            val=res1[0]
            


            curr=conn.cursor()
            sql2=f"select string_agg(image,',') from cart where id =(select id from account inner join currentuser on account.username=currentuser.username)"
            curr.execute(sql2)
            res2=curr.fetchall()
            
            sql3=f"select sum(price) from cart where id =(select id from account inner join currentuser on account.username=currentuser.username)"
            curr=conn.cursor()
            curr.execute(sql3)
            res3=curr.fetchone()
            val2=res3[0]
            #print(res1,res2,res3)
            curr=conn.cursor()
            sql4=f"insert into orders(id,price) values ('{val}','{val2}')"
            curr.execute(sql4)
            # msg=curr.fetchall()
            conn.commit()
            return render_template("order.html",msg=msg,msg2=msg2)
        else:
            msg="Invalid username"
            return render_template('checkout.html',msg=msg)
        
    return render_template('checkout.html')


@app.route('/delete', methods = ['POST','GET'])
def delete():
     curr=conn.cursor()
     curr.execute("select cart.image,cart.price From cart inner join account on account.id=cart.id where account.username=(select username from currentuser)group by cart.image,cart.price")
     res=curr.fetchall() 
     if request.method == 'POST':
        prod=request.form['product'] 
        id=request.form['name']
        print(prod,id)
        curr=conn.cursor()
        curr.execute("select cart.image,cart.price From cart inner join account on account.id=cart.id where account.username=(select username from currentuser)group by cart.image,cart.price")
        res=curr.fetchall() 
        cur=conn.cursor()
        sql="delete from cart where i"
        cur.execute(sql)
        return render_template("delete.html",res=res)
     return render_template("delete.html",res=res)
    


# @app.route('/confirm', methods = ['POST','GET'])
# def confirm():
#     #if request.method == 'POST': 
#     curr=conn.cursor() 
#     curr.execute("select image, price from account inner join cart on account.id=cart.id")
#     res=curr.fetchall()
#     print(res)

#     return render_template('confirmorder.html')



@app.route('/admin',methods=['GET','POST'])
def display2():
     if request.method == 'POST':
        print("admin")
        value=request.form['value']
        #print(value)
        curr=conn.cursor()
        if(value=='products'):
            curr.execute("select prodid,prodname from product")
            res=curr.fetchall()
            print(res)
            msg=res
            return render_template("admin.html",msg=msg)
        
        elif(value=='vendors'):
            curr=conn.cursor()
            curr.execute("select username,prodname from vendor")
            res=curr.fetchall()
            print(res)
            msg=res
            return render_template("admin.html",msg=msg)
        
        elif(value=='accounts'):
            curr=conn.cursor()
            curr.execute("select id,username from account")
            res=curr.fetchall()
            print(res)
            msg=res
            return render_template("admin.html",msg=msg)
       
     
        return render_template('admin.html')
     
     
     return render_template('admin.html')



@app.route('/admin2',methods=['GET','POST'])
def display3():
     if request.method == 'POST':
        print("admin")
        value=request.form['valuee']
        id=request.form['id']
        if(value=='account'):
            curr=conn.cursor()
            sql=f"delete from account where id='{id}'"
            curr.execute(sql)
            conn.commit()
            msg="Account deleted successfully"
            render_template('admin.html',msg=msg)
        print(value,id)
     return render_template('admin.html')

    # curr=conn.cursor()
    # curr.execute("Select totalaccounts()")
    # res=curr.fetchall()
    # print(res)
    # msg="Total Number of accounts are "+str(res)
    #     dropdown_value = request.form['dropdown']
    #     if dropdown_value=='Accounts':
    #         curr=conn.cursor()
    #         curr.execute("select *from account")
    #         msg=curr.fetchall()
    #         # Handle 'Accounts' query
    #         return render_template('admin.html',msg=msg)
    #     elif dropdown_value=='Products':
    #         # Handle 'Products' query
    #         curr=conn.cursor()
    #         curr.execute("select *from product")
    #         msg=curr.fetchall()
    #         return render_template('admin.html',msg=msg)
    #     elif dropdown_value=='Vendors':
    #         # Handle 'Vendors' query
    #         curr=conn.cursor()
    #         curr.execute("select *from account inner join product on account.id=product.id")
    #         msg=curr.fetchall()
    #         return render_template('admin.html',msg=msg)
    # else:
    #     # Handle GET request
    #     return "Something is wrong"

    # # Default response
    # return "Something went wrong"

if __name__ == '__main__':
    app.run(debug=True)  

