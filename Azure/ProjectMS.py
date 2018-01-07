"""
Routes and views for the flask application.
"""

# from FlaskWebProject1 import app
import pydocumentdb;
import pydocumentdb.document_client as document_client
from flask import Flask, render_template,request
from base64 import b64encode, b64decode
from time import clock
import os,csv
import werkzeug
import glob
from collections import Counter
import operator


config = {
    'ENDPOINT': 'https://sadhanadocumentdb.documents.azure.com',
    'MASTERKEY': 'vPLD5PfvVAdKZ761JhGS50KphL1ZLoZCjw1nfbTzvwm4XQ00RzxLPi6LCaNKROLKR7Fs4xSlLX0LgBFi89mgNw==',
    'DOCUMENTDB_DATABASE': 'dbFood',
    'DOCUMENTDB_COLLECTION': 'FoodCollection'
};
corpusroot = 'C:\Sadhana\CC\Assign9\data1'



app = Flask(__name__)
@app.route('/')
def hello_world():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    #  Initialize the Python DocumentDB client
    list=[]
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    #
    # #Create a database
    db = client.CreateDatabase({'id': config['DOCUMENTDB_DATABASE']})

     # Create a collection
    collection = client.CreateCollection(db['_self'], {'id': config['DOCUMENTDB_COLLECTION']})

    # The link for database with an id of Foo would be dbs/Foo
    database_link = 'dbs/' + 'dbFood'
    # database_link_counter = 'dbs/' + 'dbimagecsv'
    # The link for collection with an id of Bar in database Foo would be dbs/Foo/colls/Bar
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    # collection_link_counter = database_link_counter + '/colls/{0}'.format('sadcollectionnew')

    # Reading the documents in collection

    collection = client.ReadCollection(collection_link)
    # collection1 = client.ReadCollection(collection_link_counter)
    newlist = []
    for filename in os.listdir(corpusroot):
        # file = open(os.path.join(corpusroot, filename), "r", encoding='UTF-8')
        file1, file_ext = os.path.splitext(filename)
        fname = file1
        data=[]

        if file_ext == '.jpg':
            with open(corpusroot+'\\'+ file1 + '.jpg', 'rb') as f:
                Imagebinfile = f.read()
            image = (b64encode(Imagebinfile)).decode('UTF-8')
            l = []
            with open(corpusroot+'\\'+ file1 + '.csv') as csvfile:
                reader = csv.reader(csvfile)
                # print (reader)
                for row in reader:
                    data.append(row)
                d = {}
                calories = 0
                for i in range(0,len(data[0])):
                    try:
                        amount = int(data[0][i])
                    except ValueError:
                        amount = 0


                    d.update({data[1][i].replace(" ",""): amount})
                    calories = calories + amount
                    newlist.append(data[1][i].replace(" ",""))


            # print(newlist)

                # for i in range(0,len(data[0])):
                #     d={'name':data[1][i],'amount':data[0][i]}
                #     l.append(d)
                # print (l)

                document1 = client.CreateDocument(collection['_self'],
                                  {
                                      'id': fname,
                                      'image':image,
                                      'ingredients':d,
                                       'category':data[2][0],
                                      'TotalCalories': calories

                                  })


    end = clock()
    elapsed = end - start
    TimeTaken = str(elapsed)
    return TimeTaken



@app.route('/download', methods=['POST'])
def download():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    query = {'query': 'Select s.id,s.image, s.ingredients,s.category from server s'}
    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)
    end = clock()
    ela = end - start
    elap = str(ela)
    return render_template("display.html", image=results,time = elap)
b=[]
#query with 2 params
@app.route('/query', methods=['POST'])
def query():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    param1 = request.form['param1']

    query = {'query': 'Select s.id,s.image from server s where s.TotalCalories > ' + param1 + ''}

    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)

    for i in range(len(results)):
        a = results[i]['id']
        b.append(a)
    print(b)
    end = clock()
    ela = end - start
    elap = str(ela)
    # return str(results)
    return render_template("display.html", image=results[:3],time = elap)


@app.route('/delete', methods=['POST'])
def delete():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    param1 = request.form['param1']

    query = {'query': 'Select s.id from server s where s.TotalCalories > ' + param1 + ''}

    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)
    print (results)
    for i in range(len(results)):
        a = results[i]['id']
        b.append(a)
    print(b)
    for rows in b:
        document_link = collection_link + '/docs/{0}'.format(rows)
        document_del = client.DeleteDocument(document_link)

    end = clock()
    ela = end - start
    elap = str(ela)
    # return str(results)
    # return render_template("display.html", image=results,time = elap)
    return "Deleted"

@app.route('/top', methods=['POST'])
def top():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    newlist = []
    for filename in os.listdir(corpusroot):
        # file = open(os.path.join(corpusroot, filename), "r", encoding='UTF-8')
        file1, file_ext = os.path.splitext(filename)
        fname = file1
        data=[]

        if file_ext == '.jpg':
            with open(corpusroot+'\\'+ file1 + '.jpg', 'rb') as f:
                Imagebinfile = f.read()
            image = (b64encode(Imagebinfile)).decode('UTF-8')
            l = []
            with open(corpusroot+'\\'+ file1 + '.csv') as csvfile:
                reader = csv.reader(csvfile)
                # print (reader)
                for row in reader:
                    data.append(row)
                d = {}

                for i in range(0,len(data[0])):
                    try:
                        amount = int(data[0][i])
                    except ValueError:
                        amount = -1

                    d.update({data[1][i].replace(" ",""): amount})
                    newlist.append(data[1][i].replace(" ",""))

    print(newlist)
    uniquelist=[]
    for i in newlist:
        if i not in uniquelist:
            uniquelist.append(i)
    print(uniquelist)

    dict_count = {}

    for i in range(len(uniquelist)):
        dict_count.update({uniquelist[i]:newlist.count(uniquelist[i])})
        sorted_list = sorted(dict_count.items(),key=operator.itemgetter(1),reverse=True)

    print(sorted_list[:3])

    end = clock()
    elapsed = end - start
    TimeTaken = str(elapsed)
    return str(sorted_list[:5])

# dict_topsearch={}
# @app.route('/search', methods=['POST'])
# def search():
#     start = clock()
#     client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
#     database_link = 'dbs/' + 'dbFood'
#     collection_link = database_link + '/colls/{0}'.format('FoodCollection')
#     collection = client.ReadCollection(collection_link)
#     userinput = request.form['userinput']
#     search_count = 0
#     # dict_topsearch={}
#     print(dict_topsearch.keys())
#     if userinput in dict_topsearch.keys():
#         print(dict_topsearch.keys())
#         a=dict_topsearch[userinput]
#         dict_topsearch.update({userinput:a+1})
#     else:
#         dict_topsearch.update({userinput: 1})
#     print (dict_topsearch)
#
#     end = clock()
#     elapsed = end - start
#     TimeTaken = str(elapsed)
#     return TimeTaken

dict_newsearch={}
@app.route('/newsearch', methods=['POST'])
def newsearch():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbimagecsv'
    collection_link = database_link + '/colls/{0}'.format('searchcollection')
    collection = client.ReadCollection(collection_link)
    userinput = request.form['userinput']
    document_link = collection_link+'/docs/{0}'.format(userinput)

    try:
        document = client.ReadDocument(document_link)

    except Exception:
        document3 = client.CreateDocument(collection['_self'],
                                          {
                                              'id': userinput,
                                              'counts':0

                                          })

    document4 = client.ReadDocument(document_link)
    document1 = client.DeleteDocument(document_link)
    a = document4['count'] + 1
    document2 = client.CreateDocument(collection['_self'],
                                      {
                                          'id': userinput,
                                          'counts': a

                                      })



    end = clock()
    elapsed = end - start
    TimeTaken = str(elapsed)
    return TimeTaken

@app.route('/topsearch', methods=['POST'])
def topsearch():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbimagecsv'
    collection_link = database_link + '/colls/{0}'.format('searchcollection')
    collection = client.ReadCollection(collection_link)
    query = {'query': 'SELECT TOP 2(c.id) FROM server c where c.counts > 0'}
    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)
    end = clock()
    ela = end - start
    elap = str(ela)
    return str(results)


@app.route('/countquery', methods=['POST'])
def countquery():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)

    sprocs = 'dbs/dbFood/colls/FoodCollection/sprocs/SadhanaCountStoredProcedure'
    # d = request.form['condition']
    d=None
    results = client.ExecuteStoredProcedure(sprocs, params=d, options=None)
    end = clock()
    ela = end - start
    elap = str(ela)
    print(results)
    return str(results)
    # return render_template("display.html", image=results,time = elap)

#query with 1 params
@app.route('/query1', methods=['POST'])
def query1():
    start = clock()
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    param1 = request.form['param1']
    print(param1)
    query = {'query': 'Select s.image,s.id from server s where CONTAINS (s.id , "'+param1+'") ' }

    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)

    end = clock()
    ela = end - start
    elap = str(ela)
    # return str(results)
    return render_template("display.html", image=results,time = elap)


@app.route('/queryrange', methods=['POST'])
def queryrange():
    start = clock()
    param1 = request.form['param1']
    param2 = request.form['param2']
    # param3 = request.form['param3']
    client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})
    database_link = 'dbs/' + 'dbFood'
    collection_link = database_link + '/colls/{0}'.format('FoodCollection')
    collection = client.ReadCollection(collection_link)
    query = {'query': 'Select s.id,s.TotalCalories,s.image,s.category from server s where s.TotalCalories between '+param1+ ' and '+param2+''}
    result_iterable = client.QueryDocuments(collection['_self'], query)
    results = list(result_iterable)
    end = clock()
    ela = end - start
    elap = str(ela)
    return render_template("display.html", image=results,time = elap)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8082, debug=True)