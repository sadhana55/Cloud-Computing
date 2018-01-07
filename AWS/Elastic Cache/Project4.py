from flask import Flask,request,redirect,render_template,make_response
import MySQLdb
from time import clock
from time import time
import time
from random import *
from random import choice
import memcache
import redis
import csv
import os
import hashlib

mydb = MySQLdb.connect(host='dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com',
                       user='DBSadhana',passwd='****',db='Sadhanadb')
cursor = mydb.cursor()
cursor1=mydb.cursor()
cursor2=mydb.cursor()

app=Flask(__name__)
@app.route('/')
def main():
    return render_template('memcache.html')
    #return render_template('login.html')
    #return app.send_static_file('index1.html')


redis_client = redis.Redis(host='sadhana-redis.8fbkcw.0001.use2.cache.amazonaws.com',port=6379)
mc = memcache.Client(['sadhana-memcache.8fbkcw.0001.use2.cache.amazonaws.com:11211'],debug=0)

list_string = ["female","male"]

@app.route('/schema', methods=['GET','POST'])
def schema():
    file = request.files['file']
    fileName = file.filename
    print fileName
    filePath = os.path.abspath(fileName)
    tableName = os.path.splitext(file.filename)[0]
    print tableName
    #cursor.execute("use Sadhanadb;")
    #serverfile = 'C:/Sadhana/CC/Assign5/City.csv'
    with open(file.filename, "r") as f:
   # with open(serverfile, "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            rest = row
            break

    sql = "create table " + 'Sadhanadb.'+tableName + "(" + rest[0] + " varchar(500),"
    n = len(rest) - 1
    for i in range(1, n):
        sql += rest[i] + " varchar(100),"
    sql += rest[n] + " varchar(100));"
    print(sql)
    cursor.execute(sql);
    return 'Schema created'

    #link = 'C:/Sadhana/CC/Assign4/allweek.csv'
@app.route('/upload', methods=['GET','POST'])
def upload():
    start = clock()
    serverfile = '/home/ubuntu/flaskapp/all_week.csv'
    #op = 'mysqlimport -h dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u DBSadhana -p****! Sadhanadb /home/ubuntu/flaskapp/all_week.csv'
    op = 'mysqlimport -h dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u DBSadhana -p**** Sadhanadb C:/Sadhana/CC/Assign5/all_week.csv'
    op = 'mysqlimport -h dbsadhana.c96cydlesrgw.us-east-2.rds.amazonaws.com --fields-terminated-by=, --ignore-lines=1 --verbose --local -u DBSadhana -p**** Sadhanadb C:/Sadhana/CC/Assign5/all_week.csv'
    #op = 'mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u [user] -p [database] /path/to/address.csv'
    print op
    a=os.system(op)
    print  a
    end = clock()
    elapsed1 = end - start
    b = str(elapsed1)
    return 'time'+ b

@app.route('/with', methods=['GET','POST'])
def withmem():
    if request.form['withmem'] == 'WITH MEMCACHE':
        return render_template('withmemcache.html')
    else:
        return render_template('withoutmem.html')

@app.route('/without', methods=['GET','POST'])
def withoutmem():
    if request.form['withoutmem'] == 'WITHOUT MEMCACHE':
        return render_template('withoutmem.html')
    else:
        return render_template('withmemcache.html')


@app.route('/query1withoutmem', methods=['GET', 'POST'])
def query1withoutmem():
    cursor.execute('use Sadhanadb');
    parameter1 = request.form['parameter']
    processed_colname = parameter1.upper()
    upper_range = request.form['upper_range']
    processed_upper = upper_range.upper()
    print processed_upper
    lower_range = request.form['lower_range']
    processed_lower = lower_range.upper()
    print processed_lower

    x = int(processed_upper)
    y = int(processed_lower)
    random_number = randint(y, x)
    rn = str(random_number)
    print rn
    start = clock()
    res1 = []
    for row in range(0, 10):
        #random_number = randint(y, x)
        #rn = str(random_number)
        random_number = uniform(y, x)
        rn = round(random_number, 2)
        rns = str(rn)
        sqlstmt = 'select latitude from Sadhanadb.all_week where ' + processed_colname + ' = ' + rns + ';'
        print sqlstmt
        cursor.execute(sqlstmt);
        result = cursor.fetchall()
        print  result
        res1.append(result)
    print res1
    print sqlstmt
    end = clock()
    elapsed2 = end - start
    cursor.close();
    print res1
    print 'Time taken to run 1000 queries in seconds: ', elapsed2
    a = str(elapsed2)
    return a


@app.route('/query1withmem', methods=['GET', 'POST'])
def query1withmem():
    cursor = mydb.cursor()
    cursor.execute('use Sadhanadb');
    parameter1 = request.form['parameter']
    processed_colname = parameter1.upper()
    upper_range = request.form['upper_range']
    processed_upper = upper_range.upper()
    print processed_upper
    lower_range = request.form['lower_range']
    processed_lower = lower_range.upper()
    print processed_lower
    #key_parameter = request.form['key_param']
   # x = int(processed_upper)
   # y = int(processed_lower)
    x = float(processed_upper)
    y = float(processed_lower)
    #random_number = randint(y, x)
    start = clock()
    print start
    res = []
    counter=0
    for row in range(0, 5):
        random_number = randint(y, x)
        rns = str(random_number)
        #random_number = uniform(y, x)
        #rn = round(random_number, 2)
        #rns = str(rn)
        print rns
        cursor.execute('use Sadhanadb');
        sqlstmt = 'select place from all_week where ' + processed_colname + ' = ' + rns
        h = hashlib.md5(sqlstmt)
        ah =h.hexdigest()
        print (ah)
        print sqlstmt
        cursor.execute(sqlstmt);
        result1 = cursor.fetchall()
        if len(result1)>0:
            counter = counter +1
        print result1
        mc.set(ah, result1)
        res.append(result1)
    print counter
    print res
    end = clock()
    elapsed_mem1 = end - start
    print'!!!!!!!!!!!!!!!!!!!!!!!!!!to db : ', elapsed_mem1
    print res
    b= str(elapsed_mem1)
    return str(counter)


@app.route('/query1withmemcheck', methods=['GET', 'POST'])
def query1withmemcheck():
    cursor = mydb.cursor()
    cursor.execute('use Sadhanadb');
    parameter1 = request.form['parameter']
    processed_colname = parameter1.upper()
    upper_range = request.form['upper_range']
    processed_upper = upper_range.upper()
    print processed_upper
    lower_range = request.form['lower_range']
    processed_lower = lower_range.upper()
    print processed_lower
    key_parameter = request.form['key_param']
    # x = int(processed_upper)
    # y = int(processed_lower)
    x = float(processed_upper)
    y = float(processed_lower)
    # random_number = randint(y, x)
    start = clock()
    res = []
    count_cache = 0
    count_db = 0
    for row in range(0, 5):
        random_number = randint(y, x)
        rns = str(random_number)
        # random_number = uniform(y, x)
        # rn = round(random_number, 2)
        # rns = str(rn)
        print rns
        cursor.execute('use Sadhanadb');
        sqlstmt = 'select place from all_week where ' + processed_colname + ' = ' + rns
        h = hashlib.md5(sqlstmt)
        ah = h.hexdigest()
        print (ah)
        print sqlstmt
        obj1 = mc.get(ah)
        
        if obj1:
            obj1 = mc.get(ah)
            print 'cache'
            count_cache = count_cache +1
        else:
            cursor.execute(sqlstmt);
            result1 = cursor.fetchall()
            print 'db'
            mc.set(ah, result1)
            count_db = count_db +1
        # res.append(result1)
    #print res
    print count_cache
    print count_db
    end = clock()
    elapsed_mem1_set = end - start
    print'!!!!!!!!!!!!!!!!!!!!!!!!!!to db : ', elapsed_mem1_set
    b = str(elapsed_mem1_set)
    return b

@app.route('/queryforsec', methods=['GET', 'POST'])
def query4sec():
    cursor = mydb.cursor()
    time_end = time.time() + 10*1
    count = 0
    print "queryforonetenthsecond"
    while time.time() < time_end:
        random_number = randint(10, 90)
        rns = str(random_number)
        # random_number = uniform(y, x)
        # rn = round(random_number, 2)
        # rns = str(rn)
        print rns
        cursor.execute('use Sadhanadb');
        sqlstmt = 'select name from boat where ' + 'age ' + ' = ' + rns
        h = hashlib.md5(sqlstmt)
        ah = h.hexdigest()
        cursor.execute(sqlstmt)
        print (ah)
        print sqlstmt
        count = count +1
        print count
    return str(count)


@app.route('/query1withmem_str', methods=['GET', 'POST'])
def query1withmem_str():
    cursor = mydb.cursor()
    cursor.execute('use Sadhanadb');
    list_string = ['male','female']
    start = clock()
    print start
    res = []

    for row in range(0, 10):
        rn = choice(list_string)

        print rn
        cursor.execute('use Sadhanadb');
        sqlstmt = 'select name from boat where sex  = "' + str(rn) + '"'
        h = hashlib.md5(sqlstmt)
        ah =h.hexdigest()
        print (ah)
        print sqlstmt
        cursor.execute(sqlstmt);
        result1 = cursor.fetchall()
        print result1
        mc.set(ah, result1)
        res.append(result1)
    print res
    end = clock()
    elapsed_mem1 = end - start
    print'!!!!!!!!!!!!!!!!!!!!!!!!!!to db : ', elapsed_mem1
    """start1 = clock()
    print'start clock %f' % start
    mc.get(ah)
    end1 = clock()
    print'end clock %f' % end
    elapsed2 = end1 - start1
    print'!!!!!!!!!!!!!!!!!!!!!!!!!!to memcache : ', elapsed2"""
    print res
    b= str(elapsed_mem1)
    #c = str(elapsed2)
    return str(res)+b

@app.route('/query1withmemcheck_str', methods=['GET', 'POST'])
def query1withmemcheck_str():
    cursor = mydb.cursor()
    cursor.execute('use Sadhanadb');
    start = clock()

    for row in range(0, 10):
        rn = choice(list_string)
        #rns = str(random_number)
        # random_number = uniform(y, x)
        # rn = round(random_number, 2)
        rns = str(rn)
        print rns
        cursor.execute('use Sadhanadb');
        sqlstmt = 'select place from all_week where mag = "' +rns+ '"'
        h = hashlib.md5(sqlstmt)
        ah = h.hexdigest()
        print (ah)
        print sqlstmt
        obj1 = mc.get(ah)
        #diff_get=0
        if obj1:
            obj1 = mc.get(ah)
            print 'cache'
        else:
            cursor.execute(sqlstmt);
            result1 = cursor.fetchall()
            print 'db'
            mc.set(ah, result1)
        # res.append(result1)
    #print res
    end = clock()
    elapsed_mem1_set = end - start
    print'!!!!!!!!!!!!!!!!!!!!!!!!!!to db : ', elapsed_mem1_set
    b = str(elapsed_mem1_set)

    return b

if __name__ == '__main__':
    #app.run()
    app.run(host='127.0.0.1', port=8050,debug=True)






