from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect
from Elearningapp.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.http import FileResponse


import requests
import random
import uuid
import os
import json
import base64
import hashlib
import hmac
import mimetypes

from django.contrib.auth.models import User

from datetime import datetime, timedelta # Importing datetime and timedelta for handling time-related operations , such as setting OTP expiration time

import random

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from datetime import datetime, timedelta # Importing datetime and timedelta for handling time-related operations , such as setting OTP expiration time 

def home(request):
    return HttpResponse("hello world")
def master(request):
    return render(request,'master.html')  
def admindashboard(request):
    if request.session.has_key('adminemail'):
        eid=request.session['adminemail']# Get the email of the logged-in user from the session
        admin=Elearningadmin.objects.get(email=eid)# Retrieve the admin object based on the email
        stu=elearning_users.objects.count()
        Teacher=teacher.objects.count()
        Course=course.objects.count()
        return render(request,'admindashboard.html', {'admin': admin,'stu':stu,'Teacher':Teacher,'Course':Course})

    else:
        messages.success(request,'please login!')
        return redirect('/adminlogin')
def addadmin(request):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        gender=request.POST['gender']
        file=request.POST['file']
        city=request.POST['city']
        admin=Elearningadmin(name=name,email=email,mobile=mobile,password=password,gender=gender,file=file,city=city)
        admin.save()
        messages.success(request,'added successfully')
        return redirect('/addadmin')
    else:    
        return render(request,'addadmin.html',{'admin':admin})

def edit(request,id):
    admin=Elearningadmin.objects.get(id=id)
    if(request.method=="POST"):
        name=request.POST['name']
        mobile=request.POST['mobile']
        gender=request.POST['gender']
        file=request.FILES['file']
        city=request.POST['city']
        admin.name=name
        admin.mobile=mobile
        admin.gender=gender
        admin.file=file
        admin.city=city
        admin.save()
        messages.success(request,'edited successfull')
        return redirect('/addadmin')
    else:
        return render(request,'edit.html',{'admin':admin})

def delete(request,id): 
    admin=Elearningadmin.objects.get(id=id)  
    admin.delete()  
    return redirect('/addadmin')

def adminlogin(request):
    if request.method == "POST":
        email = request.POST['adminemail']
        password = request.POST['password']

        usercheck = Elearningadmin.objects.filter(
            email=email,
            password=password
        )

        if usercheck.exists():
            request.session['adminemail'] = email
            # Session expires when browser is closed
            request.session.set_expiry(0)
            messages.success(request, 'Login successfully')
            return redirect('/admindashboard')
        else:
            messages.error(request, 'Wrong password or username')
            return redirect('/adminlogin')
    return render(request, 'adminlogin.html')
def admin_logout(request):
    if request.session.has_key('adminemail'):
        del request.session['adminemail']  #loging out process
    messages.success(request,'logout successfully')
    return redirect('/')
def addcoursetype(request):
    coursetype1=coursetype.objects.all()
    if(request.method=='POST'):
        name=request.POST['name']
        file=request.FILES['file']
        coursetype1=coursetype(name=name,file=file)
        coursetype1.save()
        messages.success(request,'added successfully')
        return redirect('/addcoursetype')
    else:    
        return render(request,'addcoursetype.html',{'coursetype':coursetype1})

def addcoursetype_delete(request,id): 
    coursetype1=coursetype.objects.get(id=id)  
    coursetype1.delete()  
    return redirect('/addcoursetype')

def addcoursetype_edit(request,id):
    coursetype1=coursetype.objects.get(id=id)
    if(request.method=="POST"):
        name=request.POST['name']
        file=request.FILES['file']
        coursetype1.name=name
        coursetype1.file=file
        coursetype1.save()
        messages.success(request,'edited successfull')
        return redirect('/addcoursetype')
    else:
        return render(request,'addcoursetype_edit.html',{'coursetype':coursetype1})

def addcourse(request):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])    
    course1=course.objects.all()
    coursetype1=coursetype.objects.all()
    if(request.method=='POST'):
        coursetypes=request.POST['coursetypes']
        name=request.POST['name']
        duration=request.POST['duration']
        language=request.POST['language']
        price=request.POST['price']
        file=request.FILES['file']
        course1=course(coursetypes=coursetypes,name=name,duration=duration,language=language,price=price,file=file)
        course1.save()
        messages.success(request,'added successfully')
        return redirect('/addcourse')
    else:    
        return render(request,'addcourse.html',{'coursetype':coursetype1,'course':course1,'admin':admin})

def addcourse_edit(request,id):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])    
    course1=course.objects.get(id=id)
    coursetype1=coursetype.objects.all()
    if(request.method=="POST"):
        coursetypes=request.POST['coursetypes']
        name=request.POST['name']
        duration=request.POST['duration']
        language=request.POST['language']
        price=request.POST['price']
        file=request.FILES['file']
        Description=request.POST['Description']
        course1.name=name
        course1.duration=duration
        course1.language=language
        course1.price=price
        course1.file=file
        course1.Description=Description
        course1.save()
        messages.success(request,'edited successfull')
        return redirect('/addcourse')
    else:
        return render(request,'addcourse_edit.html',{'coursetype':coursetype1,'course':course1,'admin':admin})

def addcourse_delete(request,id): 
    course1=course.objects.get(id=id)  
    course1.delete()  
    return redirect('/addcourse')
def addteachers(request):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])    
    Teacher=teacher.objects.all()
    course2=course.objects.all()
    if(request.method=='POST'):
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        file=request.FILES['file']
        teacher1=teacher(name=name,phone=phone,email=email,password=password,file=file)
        teacher1.save()
        messages.success(request,'added successfully')
        return redirect('/addteachers')
    else:    
        return render(request,'addteachers.html',{'teacher':Teacher,'courses':course2,'admin':admin})
def addteachers_edit(request,id):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])
    teacher1=teacher.objects.get(id=id)
    if(request.method=="POST"):
        name=request.POST['name']
        phone=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']
        file=request.FILES['file']
        teacher1.name=name
        teacher1.phone=phone
        teacher1.email=email
        teacher1.password=password
        teacher1.file=file
        teacher1.save()
        messages.success(request,'edited successfull')
        return redirect('/addteachers')
    else:
        return render(request,'addteachers_edit.html',{'teacheredit':teacher1,'admin':admin})   
def addteachers_delete(request,id): 
    teacher1=teacher.objects.get(id=id)  
    teacher1.delete()  
    return redirect('/addteachers')            
def website_index(request):
    ename=None
    user = None
    teacher1=None
    if request.session.has_key('email'):# Check if user is logged in
        eid=request.session['email']# Get the email of the logged-in user from the session 
        role=request.session.get('role')  # Get the role of the logged-in user from the session
        if role == 'student':
            user = elearning_users.objects.filter(email=eid).first()
            if user:
                ename = user.name
    admin=headlines.objects.all()
    Coursetype=coursetype.objects.all()
    course1=course.objects.all()
    return render(request,'website_index.html',{'admin':admin,'coursetype':Coursetype,'course':course1,'ename':ename}) 

def addheadlines(request):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])    
    Admin=headlines.objects.all()
    if(request.method=='POST'):
        heading1=request.POST['heading1']
        heading2=request.POST['heading2']
        heading3=request.POST['heading3']
        file=request.FILES['file']
        admin=headlines(heading1=heading1,heading2=heading2,heading3=heading3,file=file)
        admin.save()
        messages.success(request,'added successfully')
        return redirect('/addheadlines')
    else:    
        return render(request,'addheadlines.html',{'admin':admin,'Admin':Admin})
def addheadlines_delete(request,id): 
    admin=headlines.objects.get(id=id)  
    admin.delete()  
    return redirect('/addheadlines')        

def about(request):
    ename=None
    if request.session.has_key('email'):# Check if user is logged in
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user= elearning_users.objects.filter(email=eid).first()# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
    return render(request,'about.html',{'ename':ename})     

def contact(request):    
    ename=None
    if request.session.has_key('email'):# Check if user is logged in
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
        
    return render(request,'contact.html',{'ename':ename})

def join_now(request):
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone'].strip()  # Remove leading and trailing whitespace from the phone number 
        password=request.POST['password']
        school_college=request.POST['school_college']
        address=request.POST['address']

         # Validate Indian phone number
        phone = phone.replace(" ", "")
        phone = phone.replace("-", "")
        phone = phone.replace("(", "")
        phone = phone.replace(")", "")

        # Convert +91XXXXXXXXXX to XXXXXXXXXX
        if phone.startswith("+91"):
            phone = phone[3:]

        # Convert 91XXXXXXXXXX to XXXXXXXXXX
        elif phone.startswith("91") and len(phone) == 12:
            phone = phone[2:]

        # Check for valid 10-digit Indian mobile number
        if len(phone) != 10 or not phone.isdigit() or phone[0] not in "6789":
            messages.error(
                request,
                "Please enter a valid 10-digit Indian mobile number."
            )
            return redirect("join_now")
        # Check if email already exists
        if elearning_users.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("join_now")

        otp = str(random.randint(100000, 999999))

        # Store registration details in session
        request.session['reg_name'] = name
        request.session['reg_email'] = email
        request.session['reg_phone'] = phone
        request.session['reg_password'] = password
        request.session['reg_school'] = school_college
        request.session['reg_address'] = address
        request.session['register_otp'] = otp

        expiry = datetime.now() + timedelta(minutes=2)
        request.session['register_otp_expiry'] = expiry.strftime('%Y-%m-%d %H:%M:%S')# Store the OTP expiry time in session for later verification 

        send_mail(
            "Email Verification OTP",
            f"Welcome to EdunoVa.Verifying email for creating account.\n\nYour OTP is: {otp}\n\nIt is valid for 2 minutes.",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False, 
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("joining_otp_verification")
    
    return render(request,'join_now.html')    

def joining_otp_verification(request):
    expiry = request.session.get("register_otp_expiry")
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        saved_otp = request.session.get("register_otp")
        expiry = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")#
        if datetime.now() > expiry:
            messages.error(request, "OTP expired. Please register again.")
            request.session.flush()  # Clear session data
            return redirect("join_now")
        if user_otp == saved_otp:
            # Retrieve registration details from session
            name = request.session.get("reg_name")
            email = request.session.get("reg_email")
            phone = request.session.get("reg_phone")
            password = request.session.get("reg_password")
            school_college = request.session.get("reg_school")
            address=request.session.get("reg_address")
            # Create a new user in the database
            new_user = elearning_users(
                name=name,
                email=email,
                phone=phone,
                password=password,
                school_college=school_college,
                address=address
            )
            new_user.save()

            # Clear session data after successful registration
            request.session.flush()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect("join_now") 
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            request.session.flush()  # Clear session data
            return redirect("join_now")
    return render(request, "joining_otp_verification.html", {"expiry": expiry})        

def user_login(request): 
    if request.session.has_key('email'):
        del request.session['email']  #loging out process
    if(request.method=="POST"):
        email=request.POST['email']
        password=request.POST['password']
        usercheck=elearning_users.objects.filter(email=email,password=password).first()
        if(usercheck):
            request.session['email']=email
            request.session['role'] = 'student'
            messages.success(request,'login successfully')
            return redirect('/')
        else:
            messages.success(request,'wrong password or username')
            return redirect('/user_login')
    else:
        return render(request,'user_login.html')

def user_logout(request):
    if request.session.has_key('email'):
        del request.session['email']  #loging out process
    messages.success(request,'logout successfully')
    return redirect('/')

# def courses(request):
#     course1=course.objects.all()
#     return render(request,'courses.html',{'course':course1})        
def course_details(request,id):
    course1=course.objects.get(id=id)
    coursename=course1.name
    course_assign1=courseassign.objects.filter(course_assigned=coursename)
    teacherid_list = [assign.teacherid for assign in course_assign1] # Get a list of teacher IDs assigned to this course
    Teachers = teacher.objects.filter(id__in=teacherid_list) # Get the teacher objects based on the list of IDs
    return render(request,'course_details.html',{'course':course1, 'teachers': Teachers})

def course_assign(request,id):
    if not request.session.get('adminemail'):
        messages.error(request, 'Please login first')
        return redirect('adminlogin')
    admin=Elearningadmin.objects.get(email=request.session['adminemail'])
    course1=course.objects.all()
    teacher1=teacher.objects.get(id=id)
    course_assign1 = courseassign.objects.filter(teacherid=id)
    if(request.method=="POST"):
        assigncourse=request.POST['assigncourse']
        course_assign1=courseassign(course_assigned=assigncourse,teacherid=teacher1.id)
        course_assign1.save()
        messages.success(request,'assigned successfully')
        return redirect('/addteachers')
    else:
        return render(request,'course_assign.html',{'teachere':teacher1,'courses':course1,'course_assign':course_assign1,'admin':admin}) 
def course_remove(request,id):
    course_assign1=courseassign.objects.get(id=id)  # Get the course assignment object based on the provided id 
    course_assign1.delete()  # Delete the course assignment object from the database
    messages.success(request,'course removed successfully')  # Display a success message to the user
    return redirect('/addteachers')           

def forgot_password(request):
    if(request.method=="POST"):
        email=request.POST['email']
        usercheck=elearning_users.objects.filter(email=email)
        if(usercheck):
            otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
            request.session['reset_otp'] = otp  # Store OTP in session for later verification 
            request.session['reset_email'] = email  # Store email in session for later use in password reset process
            
            expiry_time = datetime.now() + timedelta(minutes=1)# Set OTP expiry time to 1 minute from now 
            request.session['otp_expiry'] = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
            # Send OTP via email
            send_mail( # Subject of the email, message body, sender's email address, recipient list, and fail_silently flag for error handling 
                'Password Reset OTP',
                f'Your OTP for EdunoVa password reset is: {otp}',
                settings.EMAIL_HOST_USER, # Sender email address (configured in settings.py)
                [email], # Recipient email address 
                fail_silently=False, # Raise an exception if email sending fails, allowing for error handling and debugging 
            )

            messages.success(request,'OTP sent to your email') # Display a success message to the user indicating that the OTP has been sent to their email 
            return redirect('/verify_user_otp')
        else:
            messages.success(request,'email not found')
            return redirect('/forgot_password')
    else:
        return render(request,'forgot_password.html')    

def verify_user_otp(request):
    expiry_time = request.session.get('otp_expiry') # Retrieve the OTP expiry time stored in the session during the forgot password process 
    if request.method == "POST":
        user_otp = request.POST.get('otp') # Get the OTP entered by the user from the form 
        saved_otp = request.session.get('reset_otp') # Retrieve the OTP stored in the session during the forgot password process 
        print("User OTP:", user_otp)  # Debugging: Print the OTP entered by the user
        print("Saved OTP:", saved_otp)  # Debugging: Print the OTP stored

       
        expiry_time = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S') # Convert the expiry time string back to a datetime object for comparison 
        if datetime.now() > expiry_time: # Check if the current time has exceeded the OTP expiry time 
            messages.error(request, "OTP expired")
            return redirect('user_login') # Redirect the user to the login page if the OTP has expired

        if user_otp == saved_otp:
            messages.success(request, "OTP verified")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")
        return render(request, 'verify_user_otp.html',{'otp_expiry': expiry_time})
    return render(request, 'verify_user_otp.html')    

def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('reset_email')
            if not email:
                messages.error(request, "Session expired")
                return redirect('forgot_password')
            user = elearning_users.objects.filter(email=email).first()
            if not user:
                messages.error(request, "User not found")
                return redirect('forgot_password')
            user.password = new_password
            user.save()
            request.session.flush()
            messages.success(request, "Password reset successfully")
            return redirect('user_login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'reset_password.html')    

def before_payment(request,id):
    course1=course.objects.get(id=id) # Get the course object based on the provided id 
    user=elearning_users.objects.all()
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        if(request.method=="POST"):
            user_email=request.POST['email']
            course_taken_date=datetime.now().strftime('%Y-%m-%d')  # Get the current date and time as the course taken date
            my_batch1=my_batch(course_id=id,user_email=user_email,course_taken_date=course_taken_date,status="Active")# Create a new instance of the my_batch model with the provided course and user details
            my_batch1.save()
            messages.success(request,'batch added successfully')  # Display a success message to the user
            return redirect('/user_dashboard')
        return render(request, 'before_payment.html',{'course': course1,'user': user})
    
    else:  
        return redirect('/user_login')  # Redirect to login page if user is not logged in      
    
def create_cashfree_order(request, id):

    if not request.session.has_key('email'):
        return redirect('/user_login')

    course1 = get_object_or_404(course, id=id)

    eid = request.session['email']
    user = get_object_or_404(elearning_users, email=eid)

    # Check if user already purchased this course
    existing_batch = my_batch.objects.filter(
        course_id=id,
        user_email=user.email,
        status="Active"
    ).exists()

    if existing_batch:
        return JsonResponse({
            "success": False,
            "already_purchased": True,
            "message": "You have already purchased this course."
        }, status=400)

    order_id = "edunova_" + uuid.uuid4().hex[:20]

    url = "https://sandbox.cashfree.com/pg/orders"

    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2025-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY,
        "x-idempotency-key": str(uuid.uuid4())
    }

    payload = {
        "order_id": order_id,
        "order_amount": float(course1.price),
        "order_currency": "INR",

        "customer_details": {
            "customer_id": str(user.id),
            "customer_name": user.name,
            "customer_email": user.email,
            "customer_phone": str(user.phone)
        },

        "order_meta": {
            "return_url": (
                request.build_absolute_uri(
                    "/cashfree/payment-success/"
                ) + "?order_id={order_id}"
            ),
            "notify_url": "https://tuition-recycled-felt-tip.ngrok-free.dev/cashfree/webhook/"
        },

        "order_note": "EduNova Course Payment"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code not in [200, 201]:
        print("CASHFREE ORDER ERROR:", response.status_code)
        print("CASHFREE RESPONSE:", response.text)

        return JsonResponse({
            "success": False,
            "error": response.text
        }, status=response.status_code)

    data = response.json()
    # Save payment information in database
    payment.objects.create(
        order_id=data['order_id'],
        user_email=user.email,
        course_id=id,
        amount=course1.price,
        payment_status="PENDING"
    )

    request.session['cashfree_order_id'] = data['order_id']
    # request.session['cashfree_course_id'] = id
    # request.session['cashfree_user_email'] = user.email

    return JsonResponse({
        "success": True,
        "order_id": data['order_id'],
        "payment_session_id": data['payment_session_id']
    })

@csrf_exempt
def cashfree_webhook(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Only POST requests are allowed"
        }, status=405)

    # Get Cashfree webhook headers
    signature = request.headers.get("x-webhook-signature")
    timestamp = request.headers.get("x-webhook-timestamp")

    if not signature or not timestamp:
        return JsonResponse({
            "success": False,
            "message": "Missing webhook signature"
        }, status=400)

    # Get raw request body
    raw_body = request.body.decode("utf-8")

    # Create signature using Cashfree secret key
    signed_payload = timestamp + raw_body

    generated_signature = base64.b64encode(
        hmac.new(
            settings.CASHFREE_SECRET_KEY.encode("utf-8"),
            signed_payload.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode("utf-8")

    # Verify webhook signature
    if not hmac.compare_digest(
        generated_signature,
        signature
    ):
        return JsonResponse({
            "success": False,
            "message": "Invalid webhook signature"
        }, status=401)

    # Convert JSON into Python dictionary
    data = json.loads(raw_body)

    # Get webhook data
    webhook_data = data.get("data", {})

    order_data = webhook_data.get("order", {})
    payment_data = webhook_data.get("payment", {})

    order_id = order_data.get("order_id")
    payment_status = payment_data.get("payment_status")
    payment_amount = payment_data.get("payment_amount")
    cf_payment_id = payment_data.get("cf_payment_id")

    # Validate required data
    if not order_id:
        return JsonResponse({
            "success": False,
            "message": "Order ID missing"
        }, status=400)

    if not payment_status:
        return JsonResponse({
            "success": False,
            "message": "Payment status missing"
        }, status=400)

    # Find our Payment record
    payment_record = payment.objects.filter(
        order_id=order_id
    ).first()

    if not payment_record:
        return JsonResponse({
            "success": False,
            "message": "Payment record not found"
        }, status=404)

    # Idempotency:
    # If this payment was already processed successfully,
    # do nothing again.
    if payment_record.payment_status == "SUCCESS":
        return JsonResponse({
            "success": True,
            "message": "Payment already processed",
            "order_id": order_id
        })

    # Handle failed payment
    if payment_status == "FAILED":

        payment_record.payment_status = "FAILED"
        payment_record.cf_payment_id = cf_payment_id
        payment_record.save()

        return JsonResponse({
            "success": True,
            "message": "Payment marked as failed",
            "order_id": order_id
        })

    # Only process successful payments
    if payment_status != "SUCCESS":

        payment_record.payment_status = "PENDING"
        payment_record.save()

        return JsonResponse({
            "success": True,
            "message": "Payment status received",
            "order_id": order_id
        })

    # Make sure payment amount exists
    if payment_amount is None:
        return JsonResponse({
            "success": False,
            "message": "Payment amount missing"
        }, status=400)

    # Verify amount
    if float(payment_amount) != float(payment_record.amount):
        return JsonResponse({
            "success": False,
            "message": "Payment amount mismatch"
        }, status=400)

    # Payment is valid and successful
    payment_record.payment_status = "SUCCESS"
    payment_record.cf_payment_id = cf_payment_id
    payment_record.save()

    # Get course and user information from our database
    course_id = payment_record.course_id
    user_email = payment_record.user_email

    course1 = get_object_or_404(
        course,
        id=course_id
    )

    # Check whether the student is already enrolled
    existing_batch = my_batch.objects.filter(
        course_id=course_id,
        user_email=user_email
    ).first()

    # Create enrollment only once
    if not existing_batch:

        course_taken_date = datetime.now().strftime(
            '%Y-%m-%d'
        )

        my_batch1 = my_batch(
            course_id=course_id,
            user_email=user_email,
            course_taken_date=course_taken_date,
            status="Active"
        )

        my_batch1.save()

    return JsonResponse({
        "success": True,
        "message": "Payment processed successfully",
        "order_id": order_id
    })

def cashfree_payment_success(request):

    order_id = request.GET.get("order_id")

    if not order_id:
        return JsonResponse({
            "success": False,
            "message": "Order ID is missing"
        }, status=400)

    # Get payment information stored when order was created
    session_order_id = request.session.get("cashfree_order_id")

    # Make sure this order belongs to this browser session
    if session_order_id != order_id:
        return JsonResponse({
            "success": False,
            "message": "Invalid payment session"
        }, status=403)

    # Get payment record from database
    payment_record = payment.objects.filter(
        order_id=order_id
    ).first()

    if not payment_record:
        return JsonResponse({
            "success": False,
            "message": "Payment record not found"
        }, status=404)

    # Prevent processing the same successful payment again
    if payment_record.payment_status == "SUCCESS":
        return redirect('/user_dashboard')

    # Ask Cashfree for payment status
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/payments"

    headers = {
        "Content-Type": "application/json",
        "x-api-version": "2025-01-01",
        "x-client-id": settings.CASHFREE_APP_ID,
        "x-client-secret": settings.CASHFREE_SECRET_KEY
    }

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        return JsonResponse({
            "success": False,
            "message": "Unable to verify payment",
            "error": response.json()
        }, status=response.status_code)

    payments = response.json()

    # Find payment status
    successful_payment = None
    failed_payment = None
    pending_payment = None

    for Pay in payments:

        status = Pay.get("payment_status")

        if status == "SUCCESS":
            successful_payment = Pay
            break

        elif status == "FAILED":
            failed_payment = Pay

        elif status == "PENDING":
            pending_payment = Pay

    # =====================================================
    # PAYMENT SUCCESS
    # =====================================================

    if successful_payment:

        cashfree_amount = successful_payment.get("payment_amount")

        if cashfree_amount is None:
            return JsonResponse({
                "success": False,
                "payment_verified": False,
                "message": "Payment amount not found"
            }, status=400)

        # Verify payment amount
        if float(cashfree_amount) != float(payment_record.amount):
            return JsonResponse({
                "success": False,
                "payment_verified": False,
                "message": "Payment amount mismatch"
            }, status=400)

        # Update payment record
        payment_record.payment_status = "SUCCESS"
        payment_record.cf_payment_id = successful_payment.get(
            "cf_payment_id"
        )
        payment_record.save()

        # Get course and user information
        course_id = payment_record.course_id
        user_email = payment_record.user_email

        course1 = get_object_or_404(
            course,
            id=course_id
        )

        # Check whether this course is already enrolled
        existing_batch = my_batch.objects.filter(
            course_id=course_id,
            user_email=user_email
        ).first()

        # Create enrollment only once
        if not existing_batch:

            course_taken_date = datetime.now().strftime(
                '%Y-%m-%d'
            )

            my_batch1 = my_batch(
                course_id=course_id,
                user_email=user_email,
                course_taken_date=course_taken_date,
                status="Active"
            )

            my_batch1.save()

        # Remove temporary payment information
        request.session.pop(
            'cashfree_order_id',
            None
        )

        request.session.pop(
            'cashfree_course_id',
            None
        )

        request.session.pop(
            'cashfree_user_email',
            None
        )

        return redirect('/user_dashboard')

    # =====================================================
    # PAYMENT FAILED
    # =====================================================

    if failed_payment:

        payment_record.payment_status = "FAILED"
        payment_record.cf_payment_id = failed_payment.get(
            "cf_payment_id"
        )
        payment_record.save()

        return render(
            request,
            "payment_faield.html",
            {
                "order_id": order_id,
                "course_id": payment_record.course_id
            }
        )

    # =====================================================
    # PAYMENT PENDING
    # =====================================================

    if pending_payment:

        payment_record.payment_status = "PENDING"
        payment_record.save()

        return render(
            request,
            "pending_payment.html",
            {
                "order_id": order_id,
                "course_id": payment_record.course_id
            }
        )

    # =====================================================
    # UNKNOWN / NO PAYMENT STATUS
    # =====================================================

    payment_record.payment_status = "PENDING"
    payment_record.save()

    return render(
        request,
        "payment_pending.html",
        {
            "order_id": order_id,
            "course_id": payment_record.course_id
        }
    )

def user_profile_master(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
        return render(request, 'user_profile_master.html', {'ename':ename, 'user': user})
    else:
        messages.success(request,'please login!')
        return redirect('/user_login')

def user_dashboard(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
        return render(request, 'user_dashboard.html', {'ename':ename, 'user': user})
    else:
        messages.success(request,'please login!')
        return redirect('/user_login')


def My_Batch(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
        batches=my_batch.objects.filter(user_email=eid)  # Retrieve all batches associated with the logged-in user's email
        course_list=[] # Create an empty list to store course objects corresponding to the user's batches
        for batch in batches:
            try:
                c = course.objects.get(id=int(batch.course_id))
                course_list.append(c)
            except course.DoesNotExist: # Handle the case where the course with the given ID does not exist 
                pass
        return render(request, 'My_Batch.html', {'ename':ename,'my_batches':batches,'courses':course_list, 'user': user})
    else:
        messages.success(request,'please login!')
        return redirect('/user_login')
def update_profile(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        user=elearning_users.objects.get(email=eid)# Retrieve the user object based on the email
        ename=user.name # Get the name of the logged-in user from the user object 
        if request.method == "POST":
            print(request.FILES.get('profile_pic'))
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            user.address = request.POST.get('address')
            user.gender = request.POST.get('gender')
            # Update profile picture only if a new one is selected
            if 'profile_pic' in request.FILES:
                user.img = request.FILES['profile_pic']
            user.save()
            messages.success(request, "Profile updated successfully.")
        return render(request, 'user_my_profile.html', {'ename':ename,'user':user})
    else:
        messages.success(request,'please login!')
        return redirect('/user_login')
from datetime import datetime

def student_view_batch(request, id):

    if request.session.has_key('email'):

        eid = request.session['email']

        # Get logged-in student
        user = elearning_users.objects.get(email=eid)

        ename = user.name

        # Get the selected course
        batche = course.objects.get(id=id)

        materials=StudyMaterial.objects.filter(course=batche).order_by('-uploaded_at')  # Get study materials for this course, ordered by upload date

        # Check student's enrollment in this course
        batch = my_batch.objects.filter(
            user_email=eid,
            course_id=id,
            status='Active'
        ).first()

        # Get live classes for this course
        live_classes = LiveClass.objects.filter(
            course=batche
        ).order_by(
            'scheduled_date',
            'start_time'
        )

        # Calculate live class status
        now = datetime.now()

        for live in live_classes:

            start_datetime = datetime.combine(
                live.scheduled_date,
                live.start_time
            )

            end_datetime = datetime.combine(
                live.scheduled_date,
                live.end_time
            )

            if now < start_datetime:
                live.class_status = "Upcoming"

            elif start_datetime <= now <= end_datetime:
                live.class_status = "Live Now"

            else:
                live.class_status = "Ended"

        return render(
            request,
            'student_view_batch.html',
            {
                'ename': ename,
                'user': user,
                'batche': batche,
                'batch': batch,
                'live_classes': live_classes,
                'materials': materials
            }
        )
    else:
        messages.success(request, 'Please login!')
        return redirect('/user_login')       

def view_study_material(request, id):
    material = get_object_or_404(StudyMaterial, id=id)

    if not material.file:
        raise Http404("Study material file not found.")

    filename = os.path.basename(material.file.name)

    # Detect the file type automatically.
    content_type, _ = mimetypes.guess_type(filename)

    if not content_type:
        content_type = "application/octet-stream"

    try:
        file_handle = material.file.open("rb")

        response = FileResponse(
            file_handle,
            content_type=content_type
        )

        # Ask the browser to display the file inline if supported.
        response["Content-Disposition"] = (
            f'inline; filename="{filename}"'
        )

        # Prevent browsers from guessing a different content type.
        response["X-Content-Type-Options"] = "nosniff"

        return response

    except (FileNotFoundError, OSError, ValueError):
        raise Http404("Study material file could not be opened.")


def teachers_login(request): 
    if request.session.has_key('email'):
        del request.session['email']  #loging out process
    if(request.method=="POST"):
        email=request.POST['email']
        password=request.POST['password']
        usercheck=teacher.objects.filter(email=email,password=password).first()
        if(usercheck):
            request.session['email']=email
            request.session['role']='teacher'
            # Session expires when browser is closed
            request.session.set_expiry(0)
            messages.success(request,'login successfully')
            return redirect('/teacherdashboard')
        else:
            messages.success(request,'wrong password or username')
            return redirect('/teachers_login')
    else:
        return render(request,'teachers_login.html')        
def teachers_master(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session 
        Teacher=teacher.objects.get(email=eid)# Retrieve the user object based on the email
        ename=Teacher.name # Get the name of the logged-in user from the user object 
        return render(request, 'teachers_master.html', {'ename':ename, 'Teacher': Teacher})
    else:
        messages.success(request,'please login!')
        return redirect('/teachers_login')        
def teacherdashboard(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session
        Teacher=teacher.objects.get(email=eid)# Retrieve the user object based on the email
        return render(request,'teacherdashboard.html',{'Teacher':Teacher})
    else:
        messages.success(request,'please login!')
        return redirect('/teachers_login')         
def teacher_logout(request):
    if request.session.has_key('email'):
        del request.session['email']  #loging out process
    messages.success(request,'logout successfully')
    return redirect('/')
def teacher_my_batch(request):

    if request.session.has_key('email'):

        eid = request.session['email']
        # Get logged-in teacher
        Teacher = teacher.objects.get(email=eid)
        # Get courses assigned to this teacher
        batches = courseassign.objects.filter(
            teacherid=int(Teacher.id)
        )
        course_list = []

        for batch in batches:

            try:
                # course_assigned contains course ID as a string
                c = course.objects.get(
                    name=batch.course_assigned
                )

                course_list.append(c)

            except (course.DoesNotExist, ValueError, TypeError):
                pass

        return render(
            request,
            'teacher_my_batch.html',
            {
                'my_batches': batches,
                'courses': course_list,
                'Teacher': Teacher
            }
        )

    else:
        messages.success(request, 'Please login!')
        return redirect('/teachers_login')        
def admin_master(request):
    if request.session.has_key('email'):
        eid=request.session['email']# Get the email of the logged-in user from the session
        admin=Elearningadmin.objects.get(email=eid)# Retrieve the user object based on the email
        return render(request,'admin_master.html',{'admin':admin})
    else:
        messages.success(request,'please login!')
        return redirect('/adminlogin')    

def admin_viewalldetails_teachers(request):
    if request.session.has_key('adminemail'):
        eid=request.session['adminemail']# Get the email of the logged-in user from the session
        admin=Elearningadmin.objects.get(email=eid)# Retrieve the user object based on the email
        Teacher=teacher.objects.all()
        return render(request,'admin_viewalldetails_teachers.html',{'admin':admin,'Teacher':Teacher})
    else:
        messages.success(request,'please login!')
        return redirect('/adminlogin')  

def teacher_view_batch(request, id):
    if request.session.has_key('email'):
        eid = request.session['email']
        Teacher = teacher.objects.get(email=eid)
        batche=course.objects.get(id=id)  # Retrieve the course object based on the provided ID
        total_students = my_batch.objects.filter(course_id=id, status='Active').count()  # Count the number of active students in the batch with the given course ID
        # Check whether this teacher is assigned to this course
        assigned = courseassign.objects.filter(
            teacherid=str(Teacher.id),
            course_assigned=batche.name
        ).exists()

        if not assigned:
            messages.error(
                request,
                'You are not assigned to this course and cannot upload study materials.'
            )
            return redirect('teacherdashboard')
        # Get live classes for this course and teacher
        live_classes = LiveClass.objects.filter(
            course=batche,
            teacher=Teacher
        ).order_by(
            '-scheduled_date',
            '-start_time'
        )
        # Check status of every live class
        now = datetime.now()

        for live in live_classes:

            start_datetime = datetime.combine(
                live.scheduled_date,
                live.start_time
            )

            end_datetime = datetime.combine(
                live.scheduled_date,
                live.end_time
            )

            if now < start_datetime:

                live.class_status = "Upcoming"

            elif start_datetime <= now <= end_datetime:

                live.class_status = "Live Now"

            else:

                live.class_status = "Ended"
        return render(request, 'teacher_view_batch.html',{'total_students': total_students, 'Teacher': Teacher,'batche': batche, 'live_classes': live_classes})
    else:
        messages.success(request, 'Please login!')
        return redirect('/teachers_login')

# def Upload_leacture(request, id):
#     if request.session.has_key('email'):
#         eid = request.session['email']
#         Teacher = teacher.objects.get(email=eid)
#         batche=course.objects.get(id=id)  # Retrieve the course object based on the provided ID
#         if request.method == "POST":
#             lecture_title = request.POST['lecture_title']
#             lecture_file = request.FILES['lecture_file']
#             lecture = upload_lecture(course_id=id, lecture_title=lecture_title, lecture_file=lecture_file,teacher_email=eid) # Create a new instance of the recorded_lectures model with the provided course ID, lecture title, lecture file, and teacher email
#             lecture.save()
#             messages.success(request, 'Lecture uploaded successfully')
#             return redirect('/teacher_my_batch')
#         return render(request, 'teacher_view_batch.html', {'Teacher': Teacher, 'batche': batche, 'all_ready_exist_lectures': all_ready_exist_lectures})
#     else:
#         messages.success(request, 'Please login!')
#         return redirect('/teachers_login')

def create_live_class(request, id):

    if request.session.has_key('email'):

        eid = request.session['email']

        # Get logged-in teacher
        Teacher = teacher.objects.get(email=eid)

        # Get course
        batche = course.objects.get(id=id)

        if request.method == 'POST':

            title = request.POST.get('title')
            scheduled_date = request.POST.get('scheduled_date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            # Generate a unique room ID
            room_id = uuid.uuid4().hex
            LiveClass.objects.create(
                course=batche,
                teacher=Teacher,
                title=title,
                scheduled_date=scheduled_date,
                start_time=start_time,
                end_time=end_time,
                room_id=room_id
            )

            messages.success(
                request,
                'Live class created successfully!'
            )

            return redirect('/teacher_view_batch/' + str(id))

        return render(
            request,
            'create_live_class.html',
            {
                'batche': batche,
                'Teacher': Teacher
            }
        )

    else:

        messages.success(request, 'Please login!')

        return redirect('/teachers_login')

# def teacher_live_class(request, id):
#     # Check teacher login
#     if not request.session.has_key('email'):
#         messages.error(request, 'Please login!')
#         return redirect('/teachers_login')

#     # Get logged-in teacher
#     email = request.session['email']

#     try:
#         Teacher = teacher.objects.get(email=email)
#     except teacher.DoesNotExist:
#         messages.error(request, 'Teacher account not found!')
#         return redirect('/teachers_login')

#     # Get live class belonging to this teacher
#     try:
#         live_class = LiveClass.objects.get(
#             id=id,
#             teacher=Teacher
#         )
#     except LiveClass.DoesNotExist:
#         messages.error(request, 'Live class not found!')
#         return redirect('/teachers_login')

#     # Check live class timing
#     now = datetime.now()

#     start_datetime = datetime.combine(
#         live_class.scheduled_date,
#         live_class.start_time
#     )

#     end_datetime = datetime.combine(
#         live_class.scheduled_date,
#         live_class.end_time
#     )

#     # Class has already ended
#     if now > end_datetime:

#         messages.error(
#             request,
#             'This live class has already ended.'
#         )

#         return redirect(
#             '/teacher_view_batch/' + str(live_class.course.id)
#         )

#     # Open teacher live class page
#     return render(
#         request,
#         'teacher_live_class.html',
#         {
#             'Teacher': Teacher,
#             'live_class': live_class
#         }
#     )
def teacher_live_class(request, id):
    if 'email' not in request.session:
        return redirect('teachers_login')

    try:
        Teacher = teacher.objects.get(email=request.session['email'])
        live_class = LiveClass.objects.get(id=id, teacher=Teacher)
    except (teacher.DoesNotExist, LiveClass.DoesNotExist):
        return redirect('teacherdashboard')

    room_name = f"EduNovaLive_{live_class.id}"

    return render(
        request,
        'teacher_live_class.html',
        {
            'Teacher': Teacher,
            'live_class': live_class,
            'room_name': room_name,
        }
    )
# def student_live_class(request, id):

#     # Check student login
#     if not request.session.has_key('email'):
#         messages.error(request, 'Please login!')
#         return redirect('/user_login')

#     # Get logged-in student
#     email = request.session['email']

#     try:
#         User = elearning_users.objects.get(email=email)
#     except elearning_users.DoesNotExist:
#         messages.error(request, 'Student account not found!')
#         return redirect('/user_login')

#     # Get live class
#     try:
#         live_class = LiveClass.objects.get(id=id)
#     except LiveClass.DoesNotExist:
#         messages.error(request, 'Live class not found!')
#         return redirect('/my_batch')

#     # Check whether student is enrolled in this course
#     enrolled = my_batch.objects.filter(
#         user_email=email,
#         course_id=str(live_class.course.id),
#         status='Active'
#     ).exists()

#     if not enrolled:
#         messages.error(request, 'You are not enrolled in this course!')
#         return redirect('/my_batch')
#     # Check live class timing
#     now = datetime.now()

#     start_datetime = datetime.combine(
#         live_class.scheduled_date,
#         live_class.start_time
#     )

#     end_datetime = datetime.combine(
#         live_class.scheduled_date,
#         live_class.end_time
#     )

#     # Allow joining only while class is live
#     if not (start_datetime <= now <= end_datetime):
#         messages.error(
#             request,
#             'This live class is not currently running.'
#         )
#         return redirect(
#             '/student_view_batch/' + str(live_class.course.id)
#         )
#     return render(
#         request,
#         'student_live_class.html',
#         {
#             'user': User,
#             'live_class': live_class
#         }
#     )  

def student_live_class(request, id):

    if 'email' not in request.session:
        return redirect('website_index')

    try:
        live_class = LiveClass.objects.get(id=id)
    except LiveClass.DoesNotExist:
        return redirect('my_batch')

    room_name = f"EduNovaLive_{live_class.id}"
    user=elearning_users.objects.get(email=request.session['email'])
    return render(
        request,
        'student_live_class.html',
        {
            'live_class': live_class,
            'room_name': room_name,
            'user': user
        }
    )

def upload_study_material(request, id):
    if not request.session.has_key('email'):
        messages.success(request,'please login!')
        return redirect('/teachers_login')
    Teacher=get_object_or_404(teacher,email=request.session['email'])
    batch=get_object_or_404(course,id=id)
    # Check whether this teacher is assigned to this course
    assigned = courseassign.objects.filter(
        teacherid=str(Teacher.id),
        course_assigned=batch.name
    ).exists()

    if not assigned:
        return redirect('teacherdashboard')
    if request.method == 'POST':
        title=request.POST['title']
        file=request.FILES.get('file')
        StudyMaterial.objects.create(
            course=batch,
            teacher=Teacher,
            title=title,
            file=file
        )
        messages.success(request, 'Study material uploaded successfully!')
    materials=StudyMaterial.objects.filter(course=batch,teacher=Teacher)    
    return render(request,'upload_study_material.html',{'batch': batch,'Teacher': Teacher,'materials': materials})

def delete_study_material(request,id):
    if not request.session.has_key('email'):
        messages.success(request,'please login!')
        return redirect('/teachers_login')
    Teacher=get_object_or_404(teacher,email=request.session['email'])
    material=get_object_or_404(StudyMaterial,id=id) # Get the study material object based on the provided ID
    batch=material.course # Get the course associated with the study material
    if material.teacher != Teacher:
        messages.error(request,'You are not the owner of this material!')
        return redirect('/upload_study_material/'+str(batch.id))
    material.delete()
    messages.success(request,'Study material deleted successfully!')
    return redirect('/upload_study_material/'+str(batch.id))

def conduct_test(request, id):

    batche = get_object_or_404(course, id=id)

    teacher_email = request.session.get('email')

    if not teacher_email:
        return redirect('teachers_login')

    Teacher = get_object_or_404(
        teacher,
        email=teacher_email
    )

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')

        # Start date and time
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        start_ampm = request.POST.get('start_ampm')

        # End date and time
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        end_ampm = request.POST.get('end_ampm')

        duration = request.POST.get('duration')

        # Combine date + time + AM/PM
        start_datetime_string = (
            f"{start_date} {start_time} {start_ampm}"
        )

        end_datetime_string = (
            f"{end_date} {end_time} {end_ampm}"
        )

        # Convert to Python datetime
        start_datetime = datetime.strptime(
            start_datetime_string,
            '%Y-%m-%d %I:%M %p'
        )

        end_datetime = datetime.strptime(
            end_datetime_string,
            '%Y-%m-%d %I:%M %p'
        )

        # Make timezone-aware using Asia/Kolkata
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)

        # Make sure end time is after start time
        if end_datetime <= start_datetime:
            return render(
                request,
                'conduct_test.html',
                {
                    'batche': batche,
                    'Teacher': Teacher,
                    'error': 'End time must be after start time.'
                }
            )

        test=PracticeTest.objects.create(
            course=batche,
            title=title,
            description=description,
            start_time=start_datetime,
            end_time=end_datetime,
            duration=duration,
            created_by=teacher_email
        )

        return redirect( 'add_question', test_id=test.id )

    return render(
        request,
        'conduct_test.html',
        {
            'batche': batche,
            'Teacher': Teacher
        }
    )

def add_question(request, test_id):

    test = get_object_or_404(
        PracticeTest,
        id=test_id
    )

    teacher_email = request.session.get('email')

    if not teacher_email:
        return redirect('teachers_login')

    Teacher = get_object_or_404(
        teacher,
        email=teacher_email
    )

    if request.method == 'POST':

        question = request.POST.get('question')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_answer = request.POST.get('correct_answer')
        marks = request.POST.get('marks')

        TestQuestion.objects.create(
            test=test,
            question=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            marks=marks
        )

        # Recalculate total marks
        total_marks = sum(
            q.marks for q in test.questions.all()
        )

        test.total_marks = total_marks
        test.save()

        return redirect(
            'add_question',
            test_id=test.id
        )

    questions = test.questions.all()

    return render(
        request,
        'add_question.html',
        {
            'test': test,
            'questions': questions,
            'Teacher': Teacher
        }
    )

def edit_question(request, question_id):

    question = get_object_or_404(
        TestQuestion,
        id=question_id
    )

    teacher_email = request.session.get('email')

    if not teacher_email:
        return redirect('teachers_login')

    Teacher = get_object_or_404(
        teacher,
        email=teacher_email
    )

    if request.method == 'POST':

        question.question = request.POST.get('question')
        question.option_a = request.POST.get('option_a')
        question.option_b = request.POST.get('option_b')
        question.option_c = request.POST.get('option_c')
        question.option_d = request.POST.get('option_d')
        question.correct_answer = request.POST.get('correct_answer')
        question.marks = request.POST.get('marks')

        question.save()

        test = question.test

        # Recalculate total marks
        total_marks = sum(
            q.marks for q in test.questions.all()
        )

        test.total_marks = total_marks
        test.save()

        return redirect(
            'add_question',
            test_id=test.id
        )

    return render(
        request,
        'edit_question.html',
        {
            'question': question,
            'Teacher': Teacher
        }
    )


def delete_question(request, question_id):

    question = get_object_or_404(
        TestQuestion,
        id=question_id
    )

    test = question.test

    teacher_email = request.session.get('email')

    if not teacher_email:
        return redirect('teachers_login')

    if request.method == 'POST':

        question.delete()

        # Recalculate total marks
        total_marks = sum(
            q.marks for q in test.questions.all()
        )

        test.total_marks = total_marks
        test.save()

    return redirect(
        'add_question',
        test_id=test.id
    )

def student_practice_tests(request):

    student_email = request.session.get('email')
    user=elearning_users.objects.get(email=student_email)
    if not student_email:
        return redirect('user_login')

    # Get courses purchased by the student
    batches = my_batch.objects.filter(
        user_email=student_email,
        status='Active'
    )

    course_ids = [
        int(batch.course_id)
        for batch in batches
    ]

    # Get tests for those courses
    tests = PracticeTest.objects.filter(
        course_id__in=course_ids
    ).order_by('start_time')

    return render(
        request,
        'student_practice_tests.html',
        {
            'tests': tests,'user': user
        }
    )

def start_practice_test(request, test_id):

    student_email = request.session.get('email')
    user=elearning_users.objects.get(email=student_email)
    if not student_email:
        return redirect('adminlogin')

    test = get_object_or_404(
        PracticeTest,
        id=test_id
    )

    now = timezone.now()

    # Test has not started yet
    if now < test.start_time:

        return render(
            request,
            'test_message.html',
            {
                'message': 'This test has not started yet.',
                'test': test,
                'user': user,
            }
        )

    # Test has ended
    if now >= test.end_time:
        TestQuestion.objects.filter(test=test).delete();
        return render(
            request,
            'test_message.html',
            {
                'message': 'This test has already ended.',
                'test': test,
                'user': user,
            }
        )

    # Check student enrollment
    enrolled = my_batch.objects.filter(
        user_email=student_email,
        course_id=str(test.course.id), # Filter by course ID 
        status='Active'
    ).exists()

    if not enrolled:

        return render(
            request,
            'test_message.html',
            {
                'message': 'You are not enrolled in this course.',
                'test': test,
                'user': user,
            }
        )

    # Check whether the test has questions
    questions = test.questions.all()

    if not questions.exists():

        return render(
            request,
            'test_message.html',
            {
                'message': 'This test does not have any questions yet.',
                'test': test,
                'user': user,
            }
        )

    # Check if student already has an attempt
    attempt = TestAttempt.objects.filter(
        student_email=student_email,
        test=test
    ).first()

    # Student already submitted
    if attempt and attempt.completed:

        return redirect(
            'test_result',
            attempt_id=attempt.id
        )

    # Create attempt if this is the first time
    if not attempt:

        attempt = TestAttempt.objects.create(
            student_email=student_email,
            test=test,
            started_at=now
        )

    # Calculate student's personal deadline
    duration_seconds = test.duration * 60

    personal_deadline = (
        attempt.started_at +
        timedelta(seconds=duration_seconds)
    )

    # Test closing time has priority
    if test.end_time < personal_deadline:
        deadline = test.end_time
    else:
        deadline = personal_deadline

    # Student's time is already over
    if now >= deadline:

        return redirect(
            'submit_practice_test',
            attempt_id=attempt.id
        )

    return render(
        request,
        'take_test.html',
        {
            'test': test,
            'questions': questions,
            'attempt': attempt,
            'deadline': deadline,
            'user': user,
        }
    )

def submit_practice_test(request, attempt_id):

    student_email = request.session.get('email')
    user=elearning_users.objects.get(email=student_email)
    if not student_email:
        return redirect('adminlogin')

    attempt = get_object_or_404(
        TestAttempt,
        id=attempt_id,
        student_email=student_email
    )

    # Prevent submitting the same test again
    if attempt.completed:
        return redirect(
            'test_result',
            attempt_id=attempt.id
        )

    test = attempt.test

    questions = test.questions.all()

    score = 0

    if request.method == 'POST':

        for question in questions:

            selected_answer = request.POST.get(
                f'question_{question.id}'
            )

            if selected_answer == question.correct_answer:

                score += question.marks

    else:

        # Timer expired
        score = 0

    attempt.score = score
    attempt.submitted_at = timezone.now()
    attempt.completed = True

    attempt.save()

    return redirect(
        'test_result',
        attempt_id=attempt.id,
    )

def test_result(request, attempt_id):

    student_email = request.session.get('email')
    user=elearning_users.objects.get(email=student_email)
    if not student_email:
        return redirect('adminlogin')

    attempt = get_object_or_404(
        TestAttempt,
        id=attempt_id,
        student_email=student_email
    )

    test = attempt.test

    percentage = 0

    if test.total_marks > 0:

        percentage = (
            attempt.score / test.total_marks
        ) * 100

    return render(
        request,
        'test_result.html',
        {
            'attempt': attempt,
            'test': test,
            'percentage': round(percentage, 2),
            'user': user
        }
    )
