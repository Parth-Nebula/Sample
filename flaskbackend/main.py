### Data


Users = { "a" : "somepass" }                # usernames and passwords

UserSessions = { 1234 : "a" }               # active UserSessions and usenames

UserPcs = { "a" : { "mypc1" } }             # Pcs accessible per user

Permissions = { ("a","mypc1") : [0,0,0] }   # Permissions granted


Pcs = { "mypc1" : "somepass" }              # Pcs and passwords

PcSessions = { 4321 : "mypc1" }             # active PcSessions and Pcs

PcUsers = { "mypc1" : { "a" } }             # Users who can access a Pc

PcTasks = { "mypc1" : [ 0, 0, 0 ] }         # Remaining tasks in a Pc





import * from  flask

app = Flask("__main__")



### examples

@app.route("/")
def my_index() :
    return render_template("index.html",token = "Hello")



@app.route('/some/', methods = ['GET', 'POST'])
def example():
    if method == 'POST':
        exInput = request.form['exInput']

    return render_template('example.html',token = "some")






### for users

@app.route('/login/', methods = ['GET', 'POST'])
def some_request0():

    if method == 'GET':

        return render_template('loginpage.html')
    
    if method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if username not in Users or Users[username] != password :
            return render_template('error.html',code = "Credentials wrong" )

        for i in range ( 100000 ) :
            if i not in UserSessions and i not in PcSessions : break

        UserSessions[i] = username
        
        return render_template('home.html',code = "Login Successful" , sessionid = i )






@app.route('/getpcs/', methods = ['GET', 'POST'])
def some_request1():

    if method == 'GET':

        return render_template('getpcspage.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in UserSessions :
            return render_template('error.html',code = "Session expired" )

        username = Sessions[sessionid]
        
        return render_template('getpcspage.html', code = "Request successful" , pcs = UserPcs[username] )







@app.route('/perform/', methods = ['GET', 'POST'])
def some_request2():

    if method == 'GET':

        return render_template('doaction.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in UserSessions :
            return render_template('error.html',code = "Session expired" )

        username = Sessions[sessionid]

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
def now_request0():

    if method == 'GET':

        return render_template('pcloginpage.html')
    
    if method == 'POST':
        
        pc = request.form['pc']
        password = request.form['password']

        if pc not in PCs or Pcs[pc] != password :
            return render_template('error.html',code = "Credentials wrong" )

        for i in range ( 100000 ) :
            if i not in UserSessions and i not in PcSessions : break

        PcSessions[i] = pc
        
        return render_template('pchome.html',code = "Login Successful" , sessionid = i )





@app.route('/pcloginuser/', methods = ['GET', 'POST'])
def now_request1():

    if method == 'GET':

        return render_template('loginuserpage.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]

        username = request.form['username']

        password = request.form['password']

        if username not in Users or Users[username] != password :
            return render_template('error.html',code = "Credentials wrong" )

        UserPcs[username].add(pc)
        PcUsers[pc].add(username)
        Permissions[(username,pc)]=[0,0,0]

        return render_template('getuserspage.html', code = "Login successful"  )



    

@app.route('/getusers/', methods = ['GET', 'POST'])
def now_request2():

    if method == 'GET':

        return render_template('getuserspage.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]
        
        return render_template('getuserspage.html', code = "Request successful" , users = PcUsers[pc] )




@app.route('/getpermissions/', methods = ['GET', 'POST'])
def now_request3():

    if method == 'GET':

        return render_template('getpermissionsspage.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]

        username = request.form['username']

        if username not in PcUsers[pc] :
            return render_template('getpermissionsspage.html', code = "Access Denied"   )
        
        return render_template('getpermissionsspage.html', code = "Request successful" , permissions = PcUsers[pc][username]  )









@app.route('/changepermissions/', methods = ['GET', 'POST'])
def now_request4():

    if method == 'GET':

        return render_template('getpermissionsspage.html')
    
    if method == 'POST':
        
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
def now_request5():

    if method == 'GET':

        return render_template('pchome.html')
    
    if method == 'POST':
        
        sessionid = request.form['sessionid']

        if sessoinid not in PcSessions :
            return render_template('error.html',code = "Session expired" )

        pc = Sessions[sessionid]

        for i in range ( 3 ) :

            if PcTasks[pc][i] != 0 :

                PcTasks[pc][i] = 0
                
                return render_template('pchome.html',code = "Do action" , action = i + 1 )
        
        return render_template('pchome.html',code = "No action" , action = 0 )
            
       




app.run(debug = True )
