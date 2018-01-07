# ASSIGNMENT FOR CREATING UPLOADING DELETING LISTING FILE ON S3
#http://docs.ceph.com/docs/master/radosgw/s3/python/
from flask import Flask, request, render_template, request, make_response, session,send_from_directory
import os, json, boto3
import cgi

# connection established between s3
s3 = boto3.resource(service_name='s3', aws_access_key_id='AKIAJHSSGXZG5UXFONDA',
                aws_secret_access_key='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',
                region_name='us-east-2')


#Creating the Flask application
app = Flask(__name__)
app.secret_key='any string'
#APP_ROOT = os.path.dirname(os.path.abspath(file))


@app.route("/")
def main():
    # return render_template('login.html')
   return app.send_static_file('index.html')


from time import clock

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        #bucket_name = 'bucket-sadhana'
        file = request.files['file']
        fileName = file.filename
        file1,file_ext = os.path.splitext(fileName)
        bucket = request.form['bucket']
        #filePath = os.path.abspath(fileName)
        if file_ext == '.txt':
            data = file.read()
            fileSize = int(len(data))
            #if os.path.getsize(file) > 200000:
            #print fileSize
            if fileSize > 30:
                bucket_name=bucket + '-text'
                s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
                s3.Bucket(bucket_name).put_object(Key=fileName, Body=data)
                return 'Text File Uploaded correctly'
            else:
                return 'Not uploaded due to exceeded quota for text'
        else:
            data = file.read()
            fileSize = int(len(data))
            if fileSize > 30:
                bucket_name = bucket+ '-others'
                s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
                s3.Bucket(bucket_name).put_object(Key=fileName, Body=data)
                return 'Image File Uploaded correctly'
            else:
                return 'Not uploaded due to exceeded quota for text'





@app.route( '/download', methods=['POST'] )
def download():
    file_name = request.form['file']
    bucket = request.form['bucket']
    number = request.form['number']
    file1, file_ext = os.path.splitext(file_name)
    if number in file1:
        file = s3.meta.client.get_object( Bucket=bucket, Key=file_name )
        contents = file['Body'].read()
        response = make_response( contents )
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        return response

@app.route('/displayfile',methods=['POST', 'GET'])
def display():
    content = []
    file_name = request.form['file']
    number = request.form['number']
    bucket = request.form['bucket']
    file = s3.meta.client.get_object(Bucket=bucket, Key=file_name)
    file1, file_ext = os.path.splitext(file_name)

    if number in file1:
        print number
        contents = file['Body'].read()
        response = make_response(contents)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        filenameD = 'output.txt'
        with open(filenameD, 'w') as my_example:
            my_example.write(contents)
        with open(filenameD) as f:
            for i in xrange(2):
                content.append(f.readline())
        return render_template("display.html", content=content)
    else:
        contents = file['Body'].read()
        response = make_response(contents)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % file_name
        return response


@app.route('/login',methods=['POST'])
def login():
   global bucket,bucket_name
   user_name=request.form['username']
   session['bucket_name']=user_name
   result = s3.meta.client.get_object(Bucket='bucket-sadhana-login', Key='login.txt')
   content= result['Body'].read()
   #print content
   user=user_name
   #print user
   if user in content:
       return app.send_static_file('index.html')
   else:
       return 'No Acess'

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return 'Logged Out'

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    files = request.form['file']
    bucket = request.form['bucket']
    s3.Object(bucket, files).delete()
    return 'file deleted'

####LISTING FILES
@app.route('/list_files', methods=['POST','GET'])
def list():
    if request.method == 'GET':
        # listing the buckets and files
        mylist = []
        for bucket in s3.buckets.all():
            for key in bucket.objects.all():
                mylist.append(key.key)
        print(mylist)
        return render_template('list.html', files = mylist)


port = os.getenv('VCAP_APP_PORT', '8000')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=int(port), debug=True)