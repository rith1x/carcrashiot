from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase
import requests

config = {
  'apiKey': "AIzaSyDDfwD09XHVNZ0o1xBmf1LJQV3XJ7NGCqY",
  'authDomain': "carcollision-16d52.firebaseapp.com",
  'databaseURL': "https://carcollision-16d52-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "carcollision-16d52",
  'storageBucket': "carcollision-16d52.appspot.com",
  'messagingSenderId': "781096938120",
  'appId': "1:781096938120:web:d1587c4677713ff7284d3d"
}












firebase = pyrebase.initialize_app(config)

database = firebase.database()
auth = firebase.auth()
global local_id


def signIn(request):
    return render(request, "login.html",{"msg":"enter credentials"})


global name

def postSignIn(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            if user is not None and "idToken" in user:
                idtoken = user["idToken"]
                user_info = auth.get_account_info(idtoken)
                email_verified = user_info['users'][0]['emailVerified']
                if email_verified:
                    userid = user_info["users"][0]["localId"]
                    name = database.child("users").child(userid).child("details").child("name").get().val()
                    
                    return render(request,"welcome.html", {"name":name})
                else:
                    message = "Email is not verified, kindly verify your Email before signing in!"
                    return render(request, "login.html",{"msg":message})
            else:
                message = "User not found"
                return render(request, "login.html", {"msg": message})
        except Exception as e:
            
            msg = str(e)
            if "INVALID_LOGIN_CREDENTIALS" in msg:
                message = "Invalid Login Credentials, Forgot your password?"
                return render(request, "login.html", {"msg": message})
            elif "TOO_MANY_ATTEMPTS_TRY_LATER" in msg:
                message = "Too many Attempts, Try again later!"
                return render(request, "login.html", {"msg": message})
            else:
                message = "Internal Error!, Try Later"
                return render(request, "auth.html", {"msg": message})
    return render(request, "login.html",{"msg":"Server Down"})


def signUp(request):
    return render(request, "signup.html")


def postSignUp(request):
    
    global local_id
    name = request.POST.get("name")
    email = request.POST.get("email")
    passw = request.POST.get("password")
    try:
        user = auth.create_user_with_email_and_password(email, passw)
        auth.send_email_verification(user["idToken"])
        uid = user["localId"]
        local_id = uid
        data = {
        "name": name,
        "email": email,
        }
        msg = "An verification Email has been sent to your email, Verify your email and proceed to login"
        database.child("users").child(uid).child("details").set(data)
        return render(request, "login.html",{"msg":msg})
    except Exception as e:
        msg = "Unable to create account. Try again"
        return render(request, "login.html", {"msg":msg})
    
    
    
    
    
    
    
    
    
    
    
    
    
  