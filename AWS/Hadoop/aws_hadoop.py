from flask import Flask, request, render_template, request, make_response, session,send_from_directory
import os, json
from time import clock
import commands

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('mapreduce_prog.html')
   # return app.send_static_file('index.html')

@app.route('/select',methods=['POST'])
def mapreduce_program():
    start = clock()
    mp = request.form['map']
    red = request.form['red']
    arg1 = request.form['arg1']
    arg2 = request.form['arg2']
    zip = request.form['zip']
    #print argument1,argument2
    #os.system("hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D stream.map.output.field.separator=',' -files /home/ubuntu/mapper.py,/home/ubuntu/reducer.py -input /input3/allweek.csv -output /input5/week_output_new11 -mapper mapper.py -reducer reducer.py")

    #os.system("sudo /home/ubuntu/dataout.csv")

    #os.system("sudo -S -u -ubuntu hdfs dfs -mkdir /input1")

    #Simple hadoop command for 1 mapper and 1 reducer
    #output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hadoop jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -input /input1/air.csv -output /output117 -mapper "python /home/ubuntu/mapper_air.py" -reducer "python /home/ubuntu/reducer_air.py"')

    #========================================
    #take input from user and run
    # output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hadoop jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D mapred.map.tasks=5 -D mapred.reduce.tasks=2 -input /input1/air.csv -output /output30 -mapper "python /home/ubuntu/mapper_air.py" -reducer "python /home/ubuntu/reducer_air.py"')
    output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hadoop jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -D mapred.map.tasks='+mp+' -D mapred.reduce.tasks='+red+' -input /input1/data3.csv -output /output36 -mapper "python /home/ubuntu/mapper_arg_pexam.py ' + arg1 + ' ' + arg2 + '" -reducer "python /home/ubuntu/reducer_arg_exam.py"')
    print ("Hello")
    final_output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hdfs dfs -cat /output36/*')

    #==========================================================
    #take arguments

    # output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hadoop jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -input /input3/data3.csv -output /output7 -mapper "python /home/ubuntu/mapper.py ' + arg1 + ' ' + arg2 + '" -reducer "python /home/ubuntu/reducer_arg_exam.py"')
    # print ("Hello")
    # final_output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hdfs dfs -cat /output4/*')

    #==============================================
    #Getting the files
    #==============================================
    # get_files = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hdfs dfs -get /output196/* /home/ubuntu/')
    # data = [line.strip('\t') for line in open("/home/ubuntu/part-00000","rb")]
    # # return str(finalDisplay)
    # newData = data.split("\t")

    #taking arguments and mapper and reducer:

    # output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hadoop jar /home/ubuntu/hadoop-2.7.3/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -input /input1/air.csv -output /output4 -mapper "python /home/ubuntu/mapper_arg_pexam.py ' + arg1 + ' ' + arg2 + '" -reducer "python /home/ubuntu/reducer_arg_exam.py"')
    # print ("Hello")
    # final_output = commands.getoutput('sudo -S -u ubuntu home/ubuntu/hadoop-2.7.3/bin/hdfs dfs -cat /output4/*')

    end = clock()
    elapsed = end - start
    #return str(elapsed)
    return str(final_output)
    #return str(elapsed)


port = os.getenv('VCAP_APP_PORT', '8000')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=int(port), debug=True)