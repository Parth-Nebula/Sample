### Data


Users = { "a" : "somepass" }                # usernames and passwords

UserSessions = { 1234 : "a" }               # active UserSessions and usenames

UserPcs = { "a" : { "mypc1" } }             # Pcs accessible per user

Permissions = { ("a","mypc1") : [0,0,0] }   # Permissions granted


Pcs = { "mypc1" : "somepass" }              # Pcs and passwords

PcSessions = { 4321 : "mypc1" }             # active PcSessions and Pcs

PcUsers = { "mypc1" : { "a" } }             # Users who can access a Pc

PcTasks = { "mypc1" : [ 0, 0, 0 ] }         # Remaining tasks in a Pc





from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

### examples

@app.route("/", methods=["GET"])
@cross_origin()
def my_index() :
    response = jsonify(message="Simple server is running")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response



@app.route('/some/', methods = ['GET', 'POST'])
def example():
    if request.method == 'POST':
        return "Req recieved"

    return render_template('example.html',token = "some")






### for users

@app.route('/login/', methods = ['GET', 'POST'])
@cross_origin()
def some_request0():
    if request.method == 'GET':
        response = jsonify(message="Simple server is running")
        return response
    
    if request.method == 'POST':
        print(request.get_json())
        username = request.get_json()['username']
        password = request.get_json()['password']
        print(username)
        if username not in Users or Users[username] != password :
            return "Error: Wrong Credentials"

        for i in range ( 100000 ) :
            if i not in UserSessions and i not in PcSessions : break

        UserSessions[i] = username
        
        return jsonify({'status': 'success', 'data': {'sessionid': i}})






@app.route('/getpcs/', methods = ['GET', 'POST'])
@cross_origin()
def some_request1():

    if request.method == 'GET':
        return render_template('getpcspage.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessionid not in UserSessions :
            return render_template('error.html',code = "Session expired" )

        username = UserSessions[sessionid]
        
        return jsonify({'status': 'success', 'data': {'pcs': UserPcs[username] }})







@app.route('/perform/', methods = ['GET', 'POST'])
@cross_origin()
def some_request2():

    if request.method == 'GET':

        return render_template('doaction.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessionid not in UserSessions :
            return render_template('error.html',code = "Session expired" )

        username = UserSessions[sessionid]

        pc = request.form['pc']

        action = request.form['action']

        if pc not in UserPcs[username] :
            return render_template('error.html',code = "Access denied" )

        if Permissions[(username,pc)][action-1] == 0 :
            return render_template('getpcspage.html',code = "Permission denied" )

        PcTasks[pc][action-1] = 1
        
        return render_template('getpcspage.html', code = "Action performed" )




### for pcs

@app.route('/pclogin/', methods = ['GET', 'POST'])
@cross_origin()
def now_request0():

    if request.method == 'GET':

        return render_template('pcloginpage.html')
    
    if request.method == 'POST':
        
        pc = request.form['pc']
        password = request.form['password']

        if pc not in Pcs or Pcs[pc] != password :
            return render_template('error.html',code = "Credentials wrong" )

        for i in range ( 100000 ) :
            if i not in UserSessions and i not in PcSessions : break

        PcSessions[i] = pc
        
        return render_template('pchome.html',code = "Login Successful" , sessionid = i )





@app.route('/pcloginuser/', methods = ['GET', 'POST'])
@cross_origin()
def now_request1():

    if request.method == 'GET':

        return render_template('loginuserpage.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessionid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = UserSessions[sessionid]

        username = request.form['username']

        password = request.form['password']

        if username not in Users or Users[username] != password :
            return render_template('error.html',code = "Credentials wrong" )

        UserPcs[username].add(pc)
        PcUsers[pc].add(username)
        Permissions[(username,pc)]=[0,0,0]

        return render_template('getuserspage.html', code = "Login successful"  )



    

@app.route('/getusers/', methods = ['GET', 'POST'])
@cross_origin()
def now_request2():

    if request.method == 'GET':

        return render_template('getuserspage.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessionid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = UserSessions[sessionid]
        
        return render_template('getuserspage.html', code = "Request successful" , users = PcUsers[pc] )




@app.route('/getpermissions/', methods = ['GET', 'POST'])
@cross_origin()
def now_request3():

    if request.method == 'GET':

        return render_template('getpermissionsspage.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessionid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = UserSessions[sessionid]

        username = request.form['username']

        if username not in PcUsers[pc] :
            return render_template('getpermissionsspage.html', code = "Access Denied"   )
        
        return render_template('getpermissionsspage.html', code = "Request successful" , permissions = PcUsers[pc][username]  )









@app.route('/changepermissions/', methods = ['GET', 'POST'])
@cross_origin()
def now_request4():

    if request.method == 'GET':

        return render_template('getpermissionsspage.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]

        username = request.form['username']

        if username not in PcUsers[pc] :
            return render_template('getpermissionsspage.html', code = "Access Denied"   )

        change = request.form['change']

        if change > 0 :
            PcUsers[pc][username][change-1] = 1
        else :
            PcUsers[pc][username][-1*(change+1)] = 0
        
        return render_template('getpermissionsspage.html', code = "Request successful" , permissions = PcUsers[pc][username]  )





@app.route('/isaction/', methods = ['GET', 'POST'])
@cross_origin()
def now_request5():

    if request.method == 'GET':

        return render_template('pchome.html')
    
    if request.method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]

        for i in range ( 3 ) :

            if PcTasks[pc][i] != 0 :

                PcTasks[pc][i] = 0
                
                return render_template('pchome.html',code = "Do action" , action = i + 1 )
        
        return render_template('pchome.html',code = "No action" , action = 0 )
            
       



app.run(host="0.0.0.0", port="5001", debug=True)
