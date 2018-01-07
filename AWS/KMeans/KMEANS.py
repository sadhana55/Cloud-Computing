from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from collections import Counter
import copy
import matplotlib.pyplot as plt
from scipy.spatial import distance
from flask import Flask, request, redirect, render_template, make_response
from matplotlib import style
import time
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

from time import clock
# Bar Chart
@app.route('/exec_query',methods=['GET','POST'])
def query():
    # Reading Data
    start = clock()
    p = pd.read_csv("data2.csv")
    #p = pd.read_csv("/home/ubuntu/flaskapp/data.csv")
    #cluster_number = 5
    cluster_number = int(request.form['clusters'])
    a1 = request.form['att1']
    a2 = request.form['att2']
    clusters = int(request.form['clusters'])
    #Attribute1 = request.form["District"]
    # Attribute2 = request.form["House"]
    # headers= list(p.columns.values)

    # Taking Age column
    features = [a1, a2]
    p_features = p[features]
    lst2 = []
    lst3 = []
    lst4 = []
    lst2 = copy.deepcopy(p_features[a1].tolist())
    lst3 = copy.deepcopy(p_features[a2].tolist())
    lst4.append(lst2)
    lst4.append(lst3)

    KM = KMeans(n_clusters=cluster_number).fit(p_features)
    lbl = KM.labels_
    centroids = KM.cluster_centers_
    label_list = []
    label_list = copy.deepcopy(lbl.tolist())
    # Counting the number of occurences in the list
    x = Counter(label_list)

    # finding distance between 2 points
    dist1 = []
    result = []
    for i in range(cluster_number):
        for j in range(i + 1, cluster_number):
            dst = distance.euclidean(centroids[i], centroids[j])
            # print(dst, centroids[i],centroids[j])
            result.append(dst)
    print(result)
    print(max(result))
    z = []
    data_x = []
    data_y = []
    for i in range(cluster_number):
        b = []
        c = []
        s = []
        for j in range(0, len(lbl)):
            if lbl[j] == i:
                variable1 = lst2[j]
                variable2 = lst3[j]
                pt = (variable1, variable2)
                pt1 = (variable1)
                pt2 = (variable2)
                b.append(pt)
                c.append(pt1)
                s.append(pt2)
        z.append(b)
        data_x.append(c)
        data_y.append(s)

    max_value = []
    # for i in range(5):
    #     max_value.append(max(data_x[i]))
    # print(max_value)

    num = []
    for x in range(0, cluster_number):
        num.append(label_list.count(x))

    color_data = ['red', 'yellow', 'purple', 'green', 'black','violet']
    # # can plot specifically, after just showing the defaults:
    for i in range(cluster_number):
        plt.scatter(data_x[i], data_y[i], linewidth=3, color=color_data[i])
    #     # plt.scatter(data_x[1], data_y[1], linewidth=3, color='red')
    #     # plt.scatter(data_x[2], data_y[2], linewidth=3, color='blue')
    #     # plt.scatter(data_x[3], data_y[3], linewidth=3, color='yellow')
    #     # plt.scatter(data_x[4], data_y[4], linewidth=3, color='orange')
    #
    plt.scatter(centroids[:, 0], centroids[:, 1], color='red', marker='*')

    plt.title('Data Clustering')
    plt.ylabel('Y axis')
    plt.xlabel('X axis')
    print (lbl)
    #plt.show()
    end = clock()
    #return render_template('cluster.html', data=num)
    #return str(centroids)
    # return render_template('cluster.html', data=num)




    return render_template('pie.html',data = num)
    # elap = end-start
    #return str(z)
   #return str(elap)

# Distance between  Centroids
@app.route('/distance1', methods=['GET', 'POST'])
def distance1():
    # Reading Data
    # p = pd.read_csv("data.csv")
    # p = pd.read_csv("/home/ubuntu/flaskapp/data.csv")
    # cluster_number = 5
    p = pd.read_csv("data2.csv")
    # p = pd.read_csv("/home/ubuntu/flaskapp/data.csv")
    # cluster_number = 5
    cluster_number = int(request.form['Cluster'])
    Attribute1 = request.form["District"]
    Attribute2 = request.form["House"]
    headers= list(p.columns.values)
    q = p[0:200]
    # Taking Age column
    features = ['Age', 'Centimeters']
    p_features = q[features]
    lst2 = []
    lst3 = []
    lst4 = []
    lst2 = copy.deepcopy(p_features['Age'].tolist())
    lst3 = copy.deepcopy(p_features['Centimeters'].tolist())
    lst4.append(lst2)
    lst4.append(lst3)

    KM = KMeans(n_clusters=cluster_number).fit(p_features)
    lbl = KM.labels_
    centroids = KM.cluster_centers_
    label_list = []
    label_list = copy.deepcopy(lbl.tolist())
    # Counting the number of occurences in the list
    x = Counter(label_list)

    # finding distance between 2 points
    dist1 = []
    result = []
    for i in range(cluster_number):
        for j in range(i + 1, cluster_number):
            dst = distance.euclidean(centroids[i], centroids[j])
            # print(dst, centroids[i],centroids[j])
            result.append(str(dst))
    print(result)
    print(max(result))
    return (str(result))
    # return render_template('distance.html',data = result)


@app.route('/CentroidLoc', methods=['GET', 'POST'])
def CentroidLoc():
    # Reading Data
    # p = pd.read_csv("data.csv")
    p = pd.read_csv("/home/ubuntu/flaskapp/data2.csv")
    cluster_number = 5
    # cluster_number = request.form['cluster_number']
    # headers= list(p.columns.values)
    q = p[0:200]
    # Taking Age column
    features = ['District', 'House']
    p_features = q[features]
    lst2 = []
    lst3 = []
    lst4 = []
    lst2 = copy.deepcopy(p_features['District'].tolist())
    lst3 = copy.deepcopy(p_features['House'].tolist())
    lst4.append(lst2)
    lst4.append(lst3)

    KM = KMeans(n_clusters=cluster_number).fit(p_features)
    lbl = KM.labels_
    centroids = KM.cluster_centers_

    return (str(lst4))


# Bar Chart
@app.route('/Counter1', methods=['GET', 'POST'])
def Counter1():
    # Reading Data
    p = pd.read_csv("data2.csv")
    #p = pd.read_csv("/home/ubuntu/flaskapp/data.csv")
    cluster_number = 6
    # cluster_number = request.form['cluster_number']
    # headers= list(p.columns.values)
    q = p[0:200]
    # Taking Age column
    features = ['Age', 'Centimeters']
    p_features = q[features]
    lst2 = []
    lst3 = []
    lst4 = []
    lst2 = copy.deepcopy(p_features['Age'].tolist())
    lst3 = copy.deepcopy(p_features['Centimeters'].tolist())
    lst4.append(lst2)
    lst4.append(lst3)

    KM = KMeans(n_clusters=cluster_number).fit(p_features)
    lbl = KM.labels_
    centroids = KM.cluster_centers_
    label_list = []
    label_list = copy.deepcopy(lbl.tolist())
    # Counting the number of occurences in the list
    x = Counter(lbl)
    print(x)
    return str(x)


if __name__ == '__main__':
    # PORT = int(os.getenv('PORT', 8000))
    app.run(host='127.0.0.1', port=8082, debug=True)








