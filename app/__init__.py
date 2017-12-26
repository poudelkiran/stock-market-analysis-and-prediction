from flask import Flask, send_file ,render_template, request, url_for, redirect, session, g, jsonify
from werkzeug import secure_filename
import sqlite3 as sql
from flask.ext.uploads import UploadSet, configure_uploads
import models as dbHandler
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import json
import datetime

from analyzer import analyzeSymbol
from dbtojson import dbtojsonfunction
from insertinto import insertintotable
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'uploads/'
UPLOAD_FOLDERPIC = 'images/'
ALLOWED_EXTENSIONSFILE = set(['csv'])
ALLOWED_EXTENSIONSIMAGE = set(['png', 'jpg'])


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()   in ALLOWED_EXTENSIONSFILE

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()   in ALLOWED_EXTENSIONSIMAGE




@app.route('/login', methods=['POST', 'GET'])
def home():
    users = "None"
    
    if 'user' in session:
        #return session['user']
        return redirect(url_for('admin'))

    if request.method=='POST':
        

        session.pop('user', None)
        username = request.form['username']
        password = request.form['password']
        #dbHandler.insertUser(username, password)
        users = dbHandler.retrieveUsers(username, password, 0)

        error = "Invalid Credentials."

      
        if username == "" or password == "":
            error = "Enter Full Credentials"
        if users == 'True':


            session['user'] = username
            return redirect(url_for('admin'))
            #return render_template('upload.html', users=username)
        

        
        return render_template('login.html', error=error )
            


    return render_template('login.html')



  




@app.route('/admin')
def admin(): 
    if g.user:
        x = session['user']
        now = datetime.datetime.now()

        users = dbHandler.retrieve(x)
        companies = dbHandler.retrieveallcompany()
        startdate = dbHandler.retrievecompanystartdate()
        enddate = dbHandler.retrievecompanyenddate()
        curent_date = now.strftime("%Y-%m-%d %H:%M")


        #for row in users:
           # print ("Fucking user is ")
            #print (row[0])

            
        
        return render_template('upload.html', x = x, users = users, curent_date=curent_date, companies = companies, startdate=startdate, enddate=enddate)

    return redirect(url_for('home'))







@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'














@app.route('/deletecompany')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    con = sql.connect("EBL.db")
    cur = con.cursor()
    cur.execute("delete from bankname where id= ?", (a,))
    con.commit()
    
    # return jsonify(result=2 + 1)








@app.route('/displayprediction')
def displayprediction():
    a = request.args.get('a')
    b = request.args.get('b')

    # con = sql.connect("EBL.db")
    # cur = con.cursor()
    # cur.execute("delete from bankname where id= ?", (a,))
    # con.commit()


    con = sql.connect("EBL.db")
    cur = con.cursor()

    cur.execute("SELECT * from {} where date= ?".format(a), (b,))
    date = cur.fetchall()
    



    for row in date:
        
        # print ("Actual is  is")
        actual = row[2]
        # print ("Prediction is")
        prediction = row[6]
        id=row[0]
  
    cur.execute("SELECT * from {} where id= ?".format(a), (id-1,))
    date = cur.fetchall()





    for row in date:
        prevactual = row[2]
        prevprediction = row[6]


    print ("Actual")
    print (actual)
    status1 = 0;
    status2=0;
    if actual == 'None':
        statusprediction = prediction-prevprediction
        print ("Hurray")
        if (statusprediction>=0):
            status2=1;
        return jsonify(result1=actual, result2=prediction, status1=status1, status2=status2 )



    else:
    
        statusactual = actual - prevactual
        statusprediction = prediction-prevactual
        
        if (statusactual>=0):
            status1 = 1
        if (statusprediction>=0):
            status2=1;
    
    
        return jsonify(result1=actual, result2=prediction, status1=status1, status2=status2 )




















@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))



# serve all resources from static directory
@app.route('/js/<path:path>')
def js_proxy(path):
    return send_file(os.path.join('public/js/', path))
@app.route('/partials/<path:path>')
def partials_proxy(path):
    return send_file(os.path.join('public/partials/', path))
@app.route('/css/<path:path>')
def css_proxy(path):
    return send_file(os.path.join('public/css/', path))




APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route("/upload", methods = ['POST'])
def upload():

    

    name = request.form['name']
    types = request.form['type']

    file = request.files['file']
    image = request.files['image']

    
    #image = request.files['image']
        
       
       
    error = "File uploaded completely"
    
    fileerror = 1
    imageerror =1
    if  allowed_file(file.filename):
        fileerror = 0
        filenamee = secure_filename(file.filename)
        filename = os.path.splitext(filenamee)[0]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))


        #con = sql.connect("EBL.db")
        #cur = con.cursor()
        #cur.execute("insert into bankname (bankname) values (?)",  (filename,))
        #cur.execute("insert into bankname (name) values (55)")

        #con.commit()


    target = os.path.join(APP_ROOT, 'static/images/')
    print (target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for image in request.files.getlist("image"):
            print(image)
            imagename=image.filename
            if allowed_image(imagename):
                imageerror = 0
                destination="/".join([target,imagename])
                print ("Destination")
                print (destination)
                image.save(destination)




    if (fileerror==1 or imageerror ==1 ):
        error = "The file is not supported"
        
        return render_template("incomplete.html", error=error)
    #    return render_template("complete.html", file=filename)            
    
    else:
        error = "File Uploaded Successfully"
        con = sql.connect("EBL.db")
        cur = con.cursor()
        cur.execute("insert into bankname (filename, imagename, fullname, type) values (?, ?,?, ?)",  (filename, imagename, name, types))
        con.commit()

        #return redirect(url_for('admin'))




      

        fuck = 'training' + filename
        
        return redirect(fuck)
        #return render_template("complete.html", file=filename)


    

'''
APP_ROOTS = os.path.dirname(os.path.abspath(__file__))
@app.route("/upload", methods = ["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/imagess/')
    print (target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for image in request.files.getlist("image"):
            print(image)
            filename=image.filename
            destination="/".join([target,filename])
            print ("Destination")
            print (destination)
            image.save(destination)
    return render_template("complete.html")
'''







@app.route('/stockanalysis')
def stockanalysis():
    

    alljsondata = []
    con = sql.connect("EBL.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM bankname")
    data = cur.fetchall()

    i=-1;
    for row in data:
        
        print ("File Name is")
        print(row[1])
        jsondata = dbtojsonfunction(row[1])
        
        #alljsondata.append(jsondata)
        alljsondata += [jsondata]
        i=i+1
    print ("All Json Data is")
    print (alljsondata[1])
    key2 = dbtojsonfunction("individual")


    #print ("All JSON DATA is")
    #print (alljsondata)
   # key1 = dbtojsonfunction("individual") # Use this For stockanalysis.html
    #key2 = dbtojsonfunction("individual") #Use this for stockanalysis.html
    #key1 = 'fuck'
    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    #return render_template('stockanalysis.html', key1 = key1, key2=key2)

    return render_template('stockanalysis.html', alljsondata = alljsondata, key2=key2, i=i)


    #return render_template('insertinto.html', key1 = key1)




'''




@app.route('/analyzer')
def apiAnalyze2():
    
    return send_file('public/partials/analyze.html')

@app.route('/sanimabank')
def nepal ():
    key1 = analyzeSymbol()
    #return render_template('nepal.html')
    return render_template('sanimabank.html', key1=key1)
'''


# API routes
#@app.route('/himalayan/')
#def apiAnalyze():
    

#    key1 = json.dumps(analyzeSymbol())

     
 

    #return send_file('public/partials/analyze.html' ,key3)
    #return render_template('sanimabank.html', key1=key1)
 #   return render_template('sanimabank.html')


'''
@app.route('/rastriya')
def rastriya():
    #key1 = analyzeSymbol()
    key2 = "rastriya" #Put The name of bank here
    key1 = dbtojsonfunction("individual") # Use this to print graph in abcd.html inorder to print predict price and actual price
    #key1 = dbtojsonfunction("abcd") # Use this to print graph in bank.html
    #key1 = dbtojsonfunction("sanimabank") # Use this For stockanalysis.html
    #
    con = sql.connect("EBL.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM bankname")
    data = cur.fetchall()
   



    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    return render_template('rastriya.html', key1 = key1, key2=key2, data=data)


'''


@app.route('/<path:path>')

def individualbank(path):
    #key1 = analyzeSymbol()
   # key2 = path #Put The name of bank here
    key1 = dbtojsonfunction(path) # Use this to print graph in abcd.html inorder to print predict price and actual price
    #key1 = dbtojsonfunction("abcd") # Use this to print graph in bank.html
    #key1 = dbtojsonfunction("sanimabank") # Use this For stockanalysis.html
    #
    con = sql.connect("EBL.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM bankname")
    data = cur.fetchall()
    cur.execute("SELECT * FROM bankname where filename = ?", (path,))
    individualdata = cur.fetchall()

    startdate = dbHandler.retrievestartdate(path)
    enddate = dbHandler.retrieveenddate(path)

    print ("Start Date is")
    print (startdate)

    print ("End Dtae is")
    print (enddate)

   




    #name = cur.fetchall()

    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    return render_template('individual.html', key1 = key1, path=path, data=data, individualdata=individualdata, startdate=startdate, enddate=enddate)




@app.route('/training<variable>')
def training(variable):


    key1 = analyzeSymbol(variable)

    #key1 = dbtojsonfunction("abcd") # Use this to print graph in abcd.html inorder to print predict price and actual price
    #key1 = dbtojsonfunction("abcd") # Use this to print graph in bank.html
    #key1 = dbtojsonfunction("sanimabank") # Use this For stockanalysis.html
    #
   
    con = sql.connect("EBL.db")
    cur = con.cursor()
   
    cur.execute("SELECT * FROM {} ".format (variable,))
    individualdata = cur.fetchall()
    #name = cur.fetchall()

    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    return render_template('training.html',  variable=variable,  individualdata=individualdata)


    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    # return render_template('login.html', key1=key1)
    #return redirect(url_for('admin'))
    #return render_template('training.html')





@app.route('/about')
def miniproject():

   
    return render_template('about.html')


@app.route('/<path:path>')
def bank_index(path):
    #key1 = analyzeSymbol()

    #key1 = dbtojsonfunction("abcd") # Use this to print graph in abcd.html inorder to print predict price and actual price
    #key1 = dbtojsonfunction("abcd") # Use this to print graph in bank.html
    #key1 = dbtojsonfunction("sanimabank") # Use this For stockanalysis.html
    #
   



    #return render_template(os.path.join(path+'.html'), key1=key1, key2 = key2)
    #return render_template(os.path.join(path+'.html'), key1 = key1)
    return render_template(os.path.join(path+'.html'))




@app.route('/animation/<path:path>')
def animation_proxy(path):
    return send_from_directory(os.path.join('public/animation/', path))

@app.route('/results')
def apiAnalyze1():
    

    return send_file('public/partials/results.html')

@app.route('/analyzer')
def apiAnalyze2():
    
    return send_file('public/partials/analyze.html')


# @app.route('/index5', methods=['GET', 'POST'])
#def index5(): 
 #   return render_template('index5.html')




# leave frontend routing up to Angular
@app.route('/', defaults={'p': ''})
@app.route('/<path:p>')
def angularApp(p = None):
     #return send_file('public/miniproject.html')
     return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
