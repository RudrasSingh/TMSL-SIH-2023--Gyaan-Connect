from flask import *
from pyrebase import *
from algorithm import Algorithm
import database as db
from authlib.integrations.flask_client import OAuth
import youtube as yt #self made module
# import requests
import time 
from datetime import timedelta
from flask_socketio import SocketIO, emit
from threading import Thread, Event
import os
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from config import Config


#---------------initializeing application------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
socketio = SocketIO(app)

#Oauth Configuration
app.secret_key = Config.FLASK_SECRET

oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=Config.OAUTH2_CLIENT_ID,
    client_secret=Config.OAUTH2_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=Config.OAUTH2_META_URL
)

#---------------configuring firebase----------------------------
firebase = initialize_app(Config.FIREBASE_CONFIG)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.permanent_session_lifetime = timedelta(days=31)
auth = firebase.auth()

#-------------------------security key (do not change/remove this code)---------------------------------------

app.secret_key = "SECRET_KEY"


#-----------------------page routes-----------------------------------------
#time calculation
def calculate_total_time():
    if 'user' in session and 'start_time' in session:
        elapsed_time = time.time() - session['start_time']
        total_time_spent = session.get('total_time_spent', 0) + elapsed_time
        session['total_time_spent'] = total_time_spent
      ##  print(f"Total Time Spent: {total_time_spent} seconds")
        session.pop('start_time', None)
        return total_time_spent
       
#time calculation
@app.before_request
def before_request():
    if 'user' in session and 'start_time' not in session:
        session['start_time'] = time.time()
        
#time calculation
@app.teardown_request
def teardown_request(exception=None):
    calculate_total_time()




@app.route('/')
def home():
    
    if 'user' in session:

        #signed user

        try:
            print(session['user'])
            button1id = "hello"
            video1 = "https://www.youtube.com/watch?v=vLqTf2b6GZw&pp=ygUGcHl0aG9u"
            like1="1000"
            view1="10K"
            thumbnail1="Python tutorial for beginners"
            channel1="Code with Harry"
            cardimage1="https://i.ytimg.com/vi/fr1f84rg4Nw/hqdefault.jpg"
            title1 = "Python Full Course for free 🐍"

            button2id = "hello"
            video2 = "https://www.youtube.com/watch?v=DInMru2Eq6E&pp=ygUGcHl0aG9u"
            title2 = "15 Minute Python Tutorial For Beginners In Hindi (Full &amp; Complete Python Crash Course)"
            like2="1000"
            view2="20K"
            thumbnail2="DSA Foundation Course"
            channel2="PW"
            cardimage2="https://i.ytimg.com/vi/_uQrJ0TkZlc/hqdefault.jpg"
            
            return render_template('index.html',video2=video2, button2id=button2id,
                                   title2=title2, video1=video1, button1id=button1id, title1=title1,like1=like1,like2=like2,channel1=channel1,view1=view1,thumbnail1=thumbnail1,view2=view2,thumbnail2=thumbnail2,channel2=channel2,cardimage1=cardimage1,cardimage2=cardimage2)
        except Exception as e:
            print(f"Error getting account info: {e}")
            # Handle the error, for now, redirect to the login page
            return redirect('/login')
    else:
        #unsigned user
        return render_template('index2.html')



#Google Login
@app.route("/callback/<flow>")
def googleCallback(flow):
    # fetch access token and id token using authorization code
    token = oauth.myApp.authorize_access_token()
    token = dict(token)
    userinfo = token.get('userinfo')

    if not userinfo:
        # Handle the case where user info is not available
        abort(400, "Failed to fetch user information")

    user_info = {
        "name": userinfo.get('name'),
        "email": userinfo.get('email'),
        "id_token": token.get('id_token')
    }

    # Set complete user information in the session
    session["user"] = user_info

    # Redirect based on the flow type (login or signup)
    if flow == "login":
        return redirect("/")  # Redirect to the home page after login
    elif flow == "signup":
        return redirect("/")  # Redirect to a welcome page after signup
    else:
        abort(400, "Invalid flow type")



@app.route("/google-login")
def googleLogin():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", flow="login", _external=True))


@app.route("/google-signup")
def googleSignup():
    if "user" in session:
        abort(404)
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", flow="signup", _external=True))


@app.route('/signup', methods = ['GET','POST'])
def signup():

    if request.method == 'POST':

        newname = request.form['newname']
        newemail = request.form['newemail']
        newpassword = request.form['newpassword']
        is_teacher = 'flag' in request.form

        try: 
            user = auth.create_user_with_email_and_password(newemail, newpassword)
            
            if is_teacher==True :
                db.create_login(newemail, newname, newpassword, 1)
                return(render_template('teacher_login.html'))
            else:
                return(render_template('personal_details.html'))
           
        except Exception as e:
            message = json.loads(e.args[1])['error']['message']

            if message == "EMAIL_EXISTS":
                return render_template('login.html', signup_error = "Email already exists. Login with you registered email or register with a new one.", signup_display_error = True)
            else:
                return render_template('login.html', signup_error = "Something is not right. Please try again later or contact the administrator", signup_display_error = True)

    else:
        signup_error_message = "Something is not right. Please try again later or contact the administrator"
        return render_template('login.html', signup_error = signup_error_message, signup_display_error = True)


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            idToken = user["idToken"]
            user = auth.get_account_info(user['idToken'])
            session['user'] = {
                "name":user["users"][0]["displayName"],
                "email":user["users"][0]["email"],
                "emailVerified":user["users"][0]["emailVerified"],
                "idToken":idToken
            }
            return redirect('/')
        
        except Exception as e:
            login_error = "Invalid email or password. Please try again."
            return render_template('login.html', login_error = login_error, login_display_error = True)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():


    print(calculate_total_time())
    session.pop('user', None)
    session.clear() 


    return redirect('/')




@app.route('/dashboard')
def dashboard():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = "Utsav Tiwari"
        login_name="Utsav"
        login_email="kkk.@"
        login_phone="123456789"
        login_mobile="032145687"
        login_address="abcdefgh"
        gyx_credits=5
        login_full_name="Utsav Tiwari"
        login_address="Student"
        login_course="Btech"


        



        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('teachers_dashboard.html', first=first_name,login=login_name,login_email=login_email,login_phone=login_phone, login_mobile=login_mobile,login_address=login_address,gyx_credit=gyx_credits,login_full_name=login_full_name,login_course=login_course)


    else:

        return redirect('/login')


@app.route('/teachers_dashboard')

def teachers_dashboard():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        teachers_name="Prof HC verma"
        teachers_website="aboututsav.netlify.app"
        teachers_github="github.com"
        teachers_twitter="twitter.com"
        teachers_instagram="instagram.com"
        teachers_facebook="facebook.com"


        teachers_login_name="Prof HC verma"
        teachers_login_phone="123456789"
        teachers_login_expertise="Physics "
        teachers_login_address="Kolkata"
        teachers_login_email="profverma@gmail.com"
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('teachers_dashboard.html', first=first_name, teachers_github=teachers_github,teachers_facebook=teachers_facebook,teachers_instagram=teachers_instagram,teachers_twitter=teachers_twitter,teachers_website=teachers_website,teachers_name=teachers_name, teachers_login_name=teachers_login_name,teachers_login_phone=teachers_login_phone,teachers_login_expertise=teachers_login_expertise,teachers_login_address=teachers_login_address,teachers_login_email=teachers_login_email)


    else:

        return redirect('/login')
    

    





@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        try:
            auth.send_password_reset_email(email)
            message = "Success! Password reset link has been sent to your email"
            return render_template('login.html', message=message, display_alert=True)
        except Exception as e:
            message = json.loads(e.args[1])['error']['message']
            
            if message == "EMAIL_NOT_FOUND":


                return render_template('forgot_password.html', message = "Email does not exists. Enter your registered email id!", display_error = True)
            
            
            else:

                return render_template('forgot_password.html', message = "Something is not right. Please try again later or contact the administrator", display_error = True)
    else:
        return render_template('forgot_password.html')

# @app.route('/livechat')
# def livechat():
#     if 'user' in session:

#         #signed user
        
#         user_id_token = session['user']["idToken"]
        
#         auth.refresh(session['user']['refreshToken'])

#         user = auth.get_account_info(user_id_token)['users'][0]
        
#         first_name = ""
        
#         if "displayName" not in user:
#             first_name = "!"
#         else:
#             first_name = user['displayName'].split()[0]

#         return render_template('working.html', first_name=first_name)

#     else:
#         return render_template('homee.html')
    



@app.route('/personal_details', methods = ['GET','POST'])
def personal_details():

    return render_template('personal_details.html')

@app.route('/searchQuery', methods = ['GET','POST'])
def searchQuery():
    if request.method == 'POST':
        query = request.form["query"]
           
        api_key = 'AIzaSyAMtysCv1YSFqck6UOtdpZWYuZ1qzGGNWY'
        search_results = youtube_search_topic(api_key, query)

        for result in search_results:
            print(f'Title: {result["title"]}')
            print(f'Video ID: {result["video_id"]}')
            print(f'URL: {result["url"]}')
            print('\n')

    return render_template('index.html')



@app.route('/chatbot', methods = ["GET","POST"])
def chatbot():
    
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('chatbot.html', first_name=first_name)

    else:
        return render_template('chatbot.html')



@app.route('/working')
def working():
    if 'user' in session:

        #signed user    
        
        user_id_token = session['user']["idToken"]
        
        auth.refresh(session['user']['refreshToken'])

        user = auth.get_account_info(user_id_token)['users'][0]
        
        first_name = ""
        
        if "displayName" not in user:
            first_name = "!"
        else:
            first_name = user['displayName'].split()[0]

        return render_template('working.html', first_name=first_name)
        return redirect('working.html')


@app.route("/teaher_login", methods = ['GET'])
def teacher_login():
    print(request.get_data())
    return render_template('teacher_login.html')


#time function
@app.route('/update_total_time', methods=['POST'])
def update_total_time():
    print( calculate_total_time())
    return jsonify(success=True)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['inputUsername']
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        university_name = request.form['inputOrgName']
        gender = request.form['selectedGender']
        location = request.form['inputLocation']
        email = request.form['inputEmailAddress']
        phone_number = request.form['inputPhone']
        birthday = request.form['inputBirthday']
        course_enrolled = request.form['inputenrolled']
        topics_interested = request.form['topics']
        level = request.form['selectedLevel']


        # Do something with the data (e.g., save to a database)
        # For now, just print the data

        # Return a response (you can customize this based on your needs)
        print('successful')
        return render_template('login.html')



'''@app.route('/livechat')
def livechat():
    if 'user' in session:
        user_id_token = session['user']["idToken"]
        auth.refresh(session['user']['refreshToken'])
        user = auth.get_account_info(user_id_token)['users'][0]
        first_name = "" if "displayName" not in user else user['displayName'].split()[0]

        return render_template('live_server.html', first_name=first_name)
    else:
        return redirect('/login')'''

@app.route('/submit_teacher_form', methods=['POST'])
def submit_teacher_form():
    
        # Fetch form data
        username = request.form['inputUsername']
        first_name = request.form['inputFirstName']
        last_name = request.form['inputLastName']
        expertise = request.form['inputexpertise']
        website = request.form.get('inputwebsite', '')  # Use get() to handle optional fields
        github = request.form.get('inputgithub', '')
        twitter = request.form.get('inputtwitter', '')
        facebook = request.form.get('inputfacebook', '')
        instagram = request.form.get('inputinstagram', '')
        university_name = request.form.get('inputOrgName', '')
        experience = request.form['inputExperience']  # Convert to int assuming it's a number
        gender = request.form['selectGender']
        location = request.form.get('inputLocation', '')
        email = request.form['inputEmailAddress']
        phone = request.form['inputPhone']
        birthday = request.form['inputBirthday']
        language = request.form['selectLang']
        agree_terms = request.form.get('flag', '')

        # Print the values for debugging
        print(f"Username: {username}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Expertise: {expertise}")
        print(f"Website: {website}")
        print(f"GitHub: {github}")
        print(f"Twitter: {twitter}")
        print(f"Facebook: {facebook}")
        print(f"Instagram: {instagram}")
        print(f"University Name: {university_name}")
        print(f"Experience: {experience}")
        print(f"Gender: {gender}")
        print(f"Location: {location}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Birthday: {birthday}")
        print(f"Language: {language}")
        print(f"Agree to Terms: {agree_terms}")

        return render_template('index.html')  # You can create a success page



'''@app.route('/search', methods=['POST'])
def search_route():
    # Handle the form submission here
    # You can access form data using request.form
   

    # Perform any necessary actions with the form data

    # For example, you can render a template with the search results
    return render_template('suggestions.html')'''


rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

@app.route("/homee", methods=["POST", "GET"])
def homee():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("homee.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("homee.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("homee.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("homee.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("homee"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")  


if __name__ == '__main__':
    app.run(debug=True)
    # socketio.run(app, debug=True)
    