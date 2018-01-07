#THIS PROGRAM SELECTS ALL THE FILES ON THE FOLDER AND UPLOAD IT ON THE CLOUD
import swiftclient
import keystoneclient
import simplejson
import os
import pyDes
from pyDes import *
import glob, os

PORT = int(os.getenv('VCAP_APP_PORT', 8000))

auth_url = 'https://identity.open.softlayer.com' + '/v3'  #authorization URL
password = 'bE=v.46JV]2h{or}' #password
project_id = 'd926bf21115e423cb69dc208a31acc3e' #project id
user_id = '6a46fcfb2c4b43d28b4bfada080d6ee1' #user id
region_name = 'dallas' #region name
conn = swiftclient.Connection(key=password,
                               authurl=auth_url,
                               auth_version='3',
                               os_options={"project_id": project_id,
                                           "user_id": user_id,
                                           "region_name": region_name})

# CONNECTION IS ESTABLISHED

# Create a new container
container_name = 'container'
conn.put_container(container_name)
print "nContainer %s created successfully." % container_name

# creating the menu options for users
def print_menu():
    print "Welcome to Cloud Storage Service."
    print "1. List local Files"
    print "2. Upload to cloud and delete from local"
    print "3. List files"
    print "4. Download from cloud"
    print "5. Delete from cloud"
    print "6. Exit"

path = "C:\Sadhana\Assign1"
dirs = os.listdir(path)
os.chdir(path)
loop = True
while loop:
    print_menu()
    choice = input("Enter your choice")
    if choice ==1:
        path = "C:\Sadhana\your path"
        dirs = os.listdir(path)
        print(dirs)
        loop = 'false'

    if choice ==2:
        print("Enter the encryption key")
        encryptionkey = raw_input()
        print("Enter the file name to be uploaded")
        filename = raw_input()
        file = open(filename,'rb')
        hashcode = hashlib.md5(file.filename).hexdigest()
        data = file.read()
        # data = "Please encrypt my strinhdskfhdsfhldsafadfdf"
        k = pyDes.des(encryptionkey, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        d = k.encrypt(data)
        # print(d)
        with open(filename, 'wb') as f:
            f.write(d)

        # UPLOADING THE FILES ON DIFFERENT FOLDER
        file1, file_ext = os.path.splitext(filename)
        if file_ext == '.txt':
            print(file1)
            container_text = 'containertext'
            conn.put_container(container_text)
            with open(filename, 'r') as example_file:
                conn.put_object(container_text, filename, contents=example_file.read(), content_type='text/plain')
                print("File uploaded")

        else:
            container_others = 'containerothers'
            conn.put_container(container_others)
            with open(filename, 'r') as example_file:
                conn.put_object(container_others, filename, contents=example_file.read(), content_type='text/plain')
                print("File uploaded")

        #DELETING THE FILE FROM LOCAL
        if os.path.exists(filename):
            file.close()
            print("Hi")
            os.remove(filename)
        else:
            print("sorry no file as the entered name")

    if choice ==3:
        print ("nObject List from container:")
        for container in conn.get_account()[1]:
            for data in conn.get_container(container['name'])[1]:
                print 'object: {0} size: {1} date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

    if choice ==4:
        print("Enter the file name to be downloaded from the cloud")
        print("Enter the encryption key")
        encryptionkey = raw_input()
        filename_download = raw_input()
        file1, file_ext = os.path.splitext(filename_download)
        if file_ext == '.txt':
            container = 'containertext'
        if file_ext = '.jpg'
            container = 'container'

            obj = conn.get_object(container_text, filename_download)
            with open(filename_download, 'w') as my_example:
                my_example.write(obj[1])
                print "text file downloaded"
        else:
            container_others = 'containerothers'
            obj = conn.get_object(container_others, filename_download)
            with open(filename_download, 'w') as my_example:
                my_example.write(obj[1])
                print "other file downloaded"


        # DECRYPTING THE FILES
        #file = open(filenameD)
        #data = file.read()
        # print(data)
        k = pyDes.des(encryptionkey, CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        dec_content = k.decrypt(d)  # DECRYPTING THE STORED DATA IN D VARIABLE
        # print(dec_content)
        with open(filename_download, 'wb') as f:
            f.write(dec_content)

    if choice == 5:
       print("Enter the file size")
       size = raw_input()
       for container in conn.get_account()[1]:
            for data in conn.get_container(container['name'])[1]:
                print data['bytes']
                print (size)
                if (data['bytes'] < size):
                    conn.delete_object(container_name, data['name'])
                    print('file deleted')

    if choice == 6:
        loop = False
        exit(0)