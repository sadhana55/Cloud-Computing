from flask import Flask,request,redirect,render_template,make_response
import MySQLdb
import csv
from time import clock
from flask import session
import os
from time import time
import random
mydb = MySQLdb.connect(host='dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com',
                       user='DBSadhana',passwd='***',db='Sadhanadb')


cursor = mydb.cursor()
cursor1=mydb.cursor()
cursor2=mydb.cursor()
app=Flask(__name__)
@app.route('/')
def main():
    return app.send_static_file('index1.html')
    #return render_template('login.html')


@app.route('/login', methods=['GET','POST'])
def login():

    uname=request.form['username']
    pwd=request.form['password']
    sql=("Select Username from Users where Username=%s and Password=%s")
    query_parameters=(uname,pwd)
    if(cursor.execute(sql,query_parameters)):
        result=cursor.fetchall()
        for row in result:
            user_name=row[0]
        print "user_name=%s "%user_name
        return app.send_static_file('index1.html')
    else:
        return "Login Failed"


@app.route('/schema', methods=['GET','POST'])
def schema():
    file = request.files['file']
    fileName = file.filename
    filePath = os.path.abspath(fileName)
    #tableName = os.path.splitext(file.filename)[0]
    #print tableName
    #cursor.execute("use Sadhanadb;")
    #serverfile = '/home/ubuntu/flaskapp/boat.csv'
    with open('C:/Sadhana/CC/Assign5/all_week.csv', "rb") as f:
    #with open(serverfile, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            rest = row
            break

    sql = "create table " + "Sadhanadb.all_week (" + rest[0] + " varchar(500),"
    n = len(rest) - 1
    for i in range(1, n):
        sql += rest[i] + " varchar(100),"
    sql += rest[n] + " varchar(100));"
    print(sql)
    cursor.execute(sql);
    return 'Schema created'

#Upload the csv file
    #link = 'C:/Sadhana/CC/Assign4/allweek.csv'
@app.route('/upload', methods=['GET','POST'])
def upload():
    start = clock()
    #serverfile = '/home/ubuntu/flaskapp/all_week.csv'
    op = 'mysqlimport -h dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u DBSadhana -p******! Sadhanadb C:/Sadhana/CC/Assign5/all_week.csv'
    #op = 'mysqlimport -h dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u DBSadhana -p*****! Sadhanadb /home/ubuntu/flaskapp/boat.csv'
    #op = 'mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u [user] -p [database] /path/to/address.csv'
    print op
    a=os.system(op)
    print  a
    end = clock()
    elapsed1 = end - start
    b = str(elapsed1)
    return 'time'+ b

@app.route('/query1', methods=['GET','POST'])
def query1():
    cursor= mydb.cursor()
    cursor.execute('use Sadhanadb;');
    param1 = request.form['param1']
    print param1
    param1_value = request.form['param1_value']

    param1_value2 = request.form['param1_value2']
    print param1_value
    start = time()
    clause = "" + str(param1_value)
    print clause

    sql1 = 'select name from Sadhanadb.boat where ' +param1+ ' between ' + clause+' and ' +param1_value2+ ' and survived = 1 ;'
                                        # +param1+ '=' +param1_value+ ';'
    print sql1
    cursor.execute(sql1)
    end = time()
    elap = end - start
    x = str(elap)
    result = cursor.fetchall()
    if len(result)>0:
        list = "<tr><td><h3>Results</h3></td>"
        for row in result:
            print row[0],
            list = list+ "<tr><td>"+str(row[0])+"</td></tr>"

        return '''<!DOCTYPE html>
        <html>
            <body>
            <head>
                    <title>Python Flask Application</title>
                    <h3> SQL Result</h3>
                </head>
                <body>
                    <table border = "1">''' + list + '''</table>
                </body>
            </html>'''


@app.route('/select_query', methods=['GET','POST'])
def select_query():
    cursor= mydb.cursor()
    cursor.execute('use Sadhanadb;');
    param1 = request.form['select_column']
    print param1
    param1_value = request.form['select_value']
    print param1_value
    start = time()


    sql1 = 'select * from Sadhanadb.all_week where ' +param1+ '=' + param1_value+' ;'
                                        # +param1+ '=' +param1_value+ ';'
    print sql1
    cursor.execute(sql1)
    end = time()
    elap = end - start
    x = str(elap)
    result = cursor.fetchall()
    return render_template('displaydepth.html', files=result)


@app.route('/query2', methods=['GET','POST'])
def query2():
    cursor= mydb.cursor()
    cursor.execute('use Sadhanadb;');
    q2_param1 = request.form['q2_param1']
    q2_param2 = request.form['q2_param2']
    q2_param1_value = request.form['q2_param1_value']
    q2_param2_value = request.form['q2_param2_value']


    start = time()
    clause1 = "" + str(q2_param1_value)
    clause2 = "" + str(q2_param2_value)

    sql2 = 'select name from Sadhanadb.boat where ' +q2_param1+ '=' + q2_param1_value+' and ' +q2_param2+ ' = ' +q2_param2_value+ ';'

    print sql2
    cursor.execute(sql2)
    end = time()
    elap = end - start
    x = str(elap)
    result2 = cursor.fetchall()

    if len(result2)>0:
        list = "<tr><td>"+q2_param1+"</td><td>"+q2_param2+"</td></TR>"
        for row in result2:
            print row[0],row[1]
            list = list+ "<tr><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
        return '''<!DOCTYPE html>
        <html>
            <body>
            <head>
                    <title>Results</title>
                    <h3> SQL Result</h3>
                </head>
                <body>
                    <table border = "1">''' + list + '''</table>
                </body>
            </html>'''


@app.route('/query3_update', methods=['GET','POST'])
def query3_update():
    cursor= mydb.cursor()
    cursor.execute('use Sadhanadb;');
    q3_param1 = request.form['q3_param1']
    q3_param2 = request.form['q3_param2']
    q3_param1_value = request.form['q3_param1_value']
    q3_param2_value = request.form['q3_param2_value']

    #update Sadhanadb.all_week SET latitude = 100 where mag = 1.9;
    #select latitude, mag from Sadhanadb.all_week where mag = 1.9
    start = time()
    clause1 = "" + str(q3_param1_value)
    clause2 = "" + str(q3_param2_value)

    sql3 = 'update Sadhanadb.boat SET ' +q3_param1+ ' =' + clause1+' WHERE fare between ' +q3_param2+ ' and ' +clause2+ ';'
    sql4 = 'select '+q3_param1+ ', '+q3_param2+ ' from Sadhanadb.all_week where '+q3_param2+ '= '+clause2+ ';'
    print sql3
    print sql4
    cursor.execute(sql3)
    cursor1.execute(sql4)
    end = time()
    elap = end - start
    x = str(elap)
    result2 = cursor1.fetchall()

    cursor1.close()
    if len(result2)>0:
        list = "<tr><td>"+q3_param1+"</td><td>"+q3_param2+"</td></TR>"
        for row in result2:
            print row[0],row[1]
            list = list+ "<tr><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
        return '''<!DOCTYPE html>
        <html>
            <body>
            <head>
                    <title>Results</title>
                    <h3> SQL Result</h3>
                </head>
                <body>
                    <table border = "1">''' + list + '''</table>
                </body>
            </html>'''

@app.route('/query4_delete', methods=['GET','POST'])
def query4_delete():
    cursor= mydb.cursor()
    cursor.execute('use Sadhanadb;');
    q4_param1 = request.form['q4_param1']

    q4_value = request.form['q4_value']

    # select depth, mag from Sadhanadb.all_week where mag = 1.9;
    #delete from Sadhanadb.all_week where depth = 5.4 where mag = 1.9;
    #select depth, mag from Sadhanadb.all_week where mag = 1.9;
    start = time()
    clause2 = "" + str(q4_value)


    sql3 = 'delete from Sadhanadb.all_week where ' +q4_param1+ '=' + clause2+ ' ;'
    sql4 = 'select '+q4_param1+ ' from Sadhanadb.all_week where '+q4_param1+ '= '+clause2+ ';'
    print sql3
    print sql4
    cursor.execute(sql3)
    cursor1.execute(sql4)
    end = time()
    elap = end - start
    x = str(elap)
    result2 = cursor1.fetchall()

    if len(result2)>0:
        list = "<tr><td>"+q4_param1+"</td></TR>"
        for row in result2:
            print row[0]
            list = list+ "<tr><td>"+str(row[0])+"</td></tr>"
        return '''<!DOCTYPE html>
        <html>
            <body>
            <head>
                    <title>Results</title>
                    <h3> SQL Result</h3>
                </head>
                <body>
                    <table border = "1">''' + list + '''</table>
                </body>
            </html>'''
    else:
        return 'Values deleted'


@app.route('/queries', methods=['GET','POST'])
def queries():
    cursor.execute('use Sadhanadb;');
    x = request.form['upper']
    y = request.form['lower']
    x1 = x.upper()
    y1 = y.upper()

    f1 = float(x1)
    f2 = float(y1)
    random_number = random.uniform(f2, f1)
    rn = round(random_number, 2)
    print rn
    start = clock()
    for row in range(0, 10):
        random_number = random.uniform(f2, f1)
        rn = round(random_number, 2)
        clause = str(rn)
        sqlstmt = 'select * from Sadhanadb.all_week where depth = '+clause+ ';'
        print sqlstmt
        cursor.execute(sqlstmt);
    print sqlstmt
    end = clock()
    elapsed2 = end - start

    # print 'Time taken to run 5000 queries in seconds: ',elapsed2
    a = str(elapsed2)

    return "Time taken to run 10 queries: " + a


if __name__ == '__main__':
	#PORT = int(os.getenv('PORT', 8000))
    app.run(host='127.0.0.1', port=8082,debug=True)