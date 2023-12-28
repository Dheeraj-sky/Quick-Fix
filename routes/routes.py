
from flask import  render_template ,flash,  request , redirect , session , jsonify

from  db.sqlUtilities import DbOperationCust
import random

set

# utils action
db = DbOperationCust()

res = {
    'error': '',
}
popupContent = {
    'heading': '',
    'description': '',
    'data': {},
    'btn1': {
        'url': '',
        'text': 'btn1'
    },
    'btn2': {
        'url': '',
        'text': 'btn2'
    }
}

def home():
    auth = isUserLogin()
    print(auth)
    if(len(auth) > 0 and auth[1] == 'admin'):
        return redirect('/admin')
    return render_template('pages/home.html' , auth=auth)

def login():
    auth = isUserLogin()
    isUser = authenticateUser(auth)
    if isUser:
        return isUser
    if request.method == 'POST':
        userid = request.form['userId']
        password = request.form['password']
        print(userid , password)
        users = db.get_cust_by_id_pass(userid , password)
        print(users)
        if users == None:
            popupContent["heading"] = "UserId and Password are Invalid"
            popupContent['description'] = ''
            popupContent['btn2']['url'] = '/login'
            popupContent['btn2']['text'] = 'Go Back'
            popupContent['data'] = {}
            return showPopup(res=popupContent)


        session['userId'] = users
        print(session['userId'])
        popupContent["heading"] = 'Hello ' + users[1] + ', You are login successfully'
        popupContent['description'] = ''
        popupContent['btn2']['url'] = '/' if users[1] != 'admin' else '/admin'
        popupContent['btn2']['text'] = 'Home' if users[1] != 'admin' else 'Dashboard'

        popupContent['data'] = {}
        return showPopup(res=popupContent)
    return render_template('auths/login.html' , auth = auth)


def register():
    auth = isUserLogin()
    isUser = authenticateUser(auth)
    if isUser:
        return isUser
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        contactnumber = request.form['contactNumber']
        users = db.get_cust_by_email(email)
        usersByPhone = db.get_cust_by_Number(contactnumber)
        if users != None:
            popupContent["heading"] = "Email id already exits"
            popupContent['description'] = ''
            popupContent['btn2']['url'] = '/register'
            popupContent['btn2']['text'] = 'Go Back'
            popupContent['data'] = {}
            return showPopup(res=popupContent)
        if usersByPhone != None:
            popupContent["heading"] = "Contact Number Is already exists"
            popupContent['description'] = ''
            popupContent['btn2']['url'] = '/register'
            popupContent['btn2']['text'] = 'Go Back'
            popupContent['data'] = {}
            return showPopup(res=popupContent)
        userId = int(str(random.randint(1000,3000)))
        isInserted = db.insert_cust_data([userId, username, email, password, address, contactnumber])

        if isInserted:
            popupContent["heading"] = 'Your registration is completed successfully'
            popupContent['description'] = "You can login by using your given userId and password"
            popupContent['data'] = {
                'User Id':userId,
                'User Name':username,
                'Email':email,
                'Address':address,
                'Contact Number':contactnumber
            }
            popupContent['btn2']['url'] = '/login'
            popupContent['btn2']['text'] = 'Login'
            return showPopup(res=popupContent)
        else:
            return showPopup(res=popupContent)

    return render_template('auths/register.html',res=res , auth = auth)


def admin():
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser
    return render_template('pages/admin.html' , auth=auth)

def showPopup(res):
    auth = isUserLogin()

    return render_template('pages/popup.html' , res=res , auth=auth)


def deleteServiceById(id):
    auth = isUserLogin()
    print('route', id)
    db.delete_bookings_by_id(id)

    popupContent["heading"] = 'Following Service is deleted successfully'
    popupContent['description'] = ""
    popupContent['data'] = {
        'Services': id,
    }
    popupContent['btn2']['url'] = '/service_list/0'
    popupContent['btn2']['text'] = 'Confirm'
    return showPopup(res=popupContent)
    # return render_template('pages/popup.html', res=res, auth=auth)
# users action

def account_details():
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser
    return render_template('pages/account_details.html' , auth=auth)

def update_userData(id):
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser

    user = db.get_cust_by_id(id)
    if user == None:
        popupContent["heading"] = 'User Not exits'
        popupContent['description'] = ""
        popupContent['data'] = {
            'Services': id,
        }
        popupContent['btn2']['url'] = '/'
        popupContent['btn2']['text'] = 'Home'
        return showPopup(res=popupContent)

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        # password = request.form['password']
        address = request.form['address']
        contactnumber = request.form['contactNumber']
        print(username , email , address , contactnumber)
        db.update_details('name' , username , 'id' , id)
        db.update_details('email', email, 'id', id)
        db.update_details('address', address, 'id', id)
        db.update_details('phone_no', contactnumber, 'id', id)

        popupContent["heading"] = 'User Data is update Successfully'
        popupContent['description'] = ""
        popupContent['data'] = {
            'User Id': user[0],
            'User Name': username,
            'Email': email,
            'Address': address,
            'Contact Number': contactnumber
        }
        popupContent['btn2']['url'] = '/'
        popupContent['btn2']['text'] = 'Home'
        return showPopup(res=popupContent)
    return render_template('pages/update_userData.html' , auth=auth ,user=user)

def delete_userData(id):

    db.delete_details(id)
    popupContent["heading"] = 'Following user id user is deleted successfully'
    popupContent['description'] = ""
    popupContent['data'] = {
        'User Id': id,
    }
    popupContent['btn2']['url'] = '/userlist'
    popupContent['btn2']['text'] = 'Users'
    return showPopup(res=popupContent)

def userList(offset):
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser
    users = db.get_all_customers(int(offset)*4)
    print(users)
    return render_template('pages/userList.html' , auth=auth , users=users, offset=offset)

def searchUser():
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser
    if request.method == 'POST':
        searchParams = request.form['searchParams']

        print('search',searchParams)

        if searchParams == '':
            flash("Please enter valid input", 'error')
            return render_template('pages/userList.html', auth=auth, users=[])
        users = db.getconfirmation(searchParams)
        print(users)
        if len(users) == 0:
            flash("No data found", 'error')
            return render_template('pages/userList.html', auth=auth, users=[])
        return render_template('pages/userList.html', auth=auth, users=users)


    popupContent["heading"] = 'You can\'t access this page'
    popupContent['description'] = ''
    popupContent['btn2']['url'] = '/'
    popupContent['btn2']['text'] = 'Home'
    popupContent['data'] = {}
    return showPopup(res=popupContent)

# service action

def searchService():
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser
    if request.method == 'POST':
        searchParams = request.form['searchParams']
        print('search',searchParams)
        if searchParams == '':
            flash("Please enter valid input", 'error')
            return render_template('pages/serviceList.html', auth=auth, bookings=[], res=res , offset=0)
        bookings = db.search_bookings_by_id(searchParams)

        if len(bookings) == 0:
            flash("No data found", 'error')
            return render_template('pages/serviceList.html', auth=auth, bookings=[], res=res , offset=0)

        return render_template('pages/serviceList.html', auth=auth, bookings=bookings , res=res , offset=0)

    popupContent["heading"] = 'You can\'t access this page'
    popupContent['description'] = ''
    popupContent['btn2']['url'] = '/'
    popupContent['btn2']['text'] = 'Home'
    popupContent['data'] = {}
    return showPopup(res=popupContent)

# def services


def serviceList(offset):
    limit = 3
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    print(offset)
    if isUser:
        return isUser
    print(request.method)
    # if request.method == 'POST':
    #     data = request.json
    #     res = data.get('res')
    #     print(res)
    #     # bookings = db.get_booking_by_userId((auth[0]), res['limit'], res['offset']) if auth[1] != 'admin' else db.get_booking_all(res['limit'], res['offset'])
    #     # return render_template('pages/serviceList.html', auth=auth, bookings=bookings, res=res)
    #     # auth = auth, bookings = []
    #     return redirect('/service_list' )

    bookings = db.get_booking_by_userId((auth[0]) , limit , int(offset) * 4) if auth[1] != 'admin' else db.get_booking_all(limit , int(offset)*4)
    print(bookings)
    return render_template('pages/serviceList.html' , auth=auth , bookings=bookings , offset=offset)


def service(type):
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser

    services = {
        'ac':{
            'name': 'Ac & Appliances repair Services',
            'subServices': ['Ac repair', 'Fridge repair' , 'Tv repair' , 'Washing machine repair'],
            'amount': [100, 500, 800, 1000, 1500]
        },
       'house_cleaning': {
            'name': 'House cleaning Services',
            'subServices': ['1-BHK', '2-BHK' , '3-BHK' ,'Bathroom Cleaning'],
            'amount': [100, 500, 800, 1000, 1500]
        },
        'vihicle_service': {
            'name': 'Vehicle Services',
            'subServices': ['2-weeler', '3-weeler' , '4-weeler'],
            'amount': [100, 500, 800, 1000, 1500]
        },
        'pickup_service': {
            'name': 'Pickup/Drop Services',
            'subServices': ['Vehicle Delivery', 'Furniture Delivery' , 'Groceries Delivery' ],
            'amount': [100, 500, 800, 1000, 1500]
        }
    }
    if request.method == 'POST':
        for _ in request.form:
            print(_)
        service = request.form['service']
        subService = request.form['subservice']
        date = request.form['date']
        address = request.form['address']
        vender = request.form['vender']
        amount = request.form['amount']

        print(services[type]['name'] )
        serviceId = 'SERV'+ str(random.randint(1000, 3000))
        serviceData = (serviceId ,
                       auth[0],
                       service ,
                       subService,
                       date ,
                       address ,
                       vender ,
                       amount,
                       'Pending')
        print(serviceData)
        db.insert_table(serviceData)

        popupContent["heading"] = 'Your serives booked Successfully'
        popupContent['description'] = ''
        popupContent['data'] = {
            'Service' : service,
            'Sub Service': subService,
            'Date': date,
            'Vender': vender,
            'Address': address,
            'Amount': amount
        }
        popupContent['btn2']['url'] = '/service_list/0'
        popupContent['btn2']['text'] = 'Services'
        # serviceData = (  )
        return showPopup(res=popupContent)

    return render_template('pages/service.html' , type=type, services=services[type] , auth=auth)

def serviceUpdate():
    auth = isUserLogin()
    isUser = beforeUserLogin(auth)
    if isUser:
        return isUser

    data = request.json
    res = data.get('res')
    print('request.json', res)
    db.update_booking_status('status', res['status'], 'service_id' , res['service_id'])
    return jsonify({'payload':res})
# utilities

def authenticateUser(user):
    print(user)
    if(user):
        popupContent["heading"] = 'You can\'t access this page'
        popupContent['description'] = ''
        popupContent['btn2']['url'] = '/'
        popupContent['btn2']['text'] = 'Home'
        popupContent['data'] = {}
        return showPopup(res=popupContent)
    return False

def beforeUserLogin(user):
    if (  len(user) == 0 ):
        popupContent["heading"] = 'You need to login'
        popupContent['description'] = ''
        popupContent['btn2']['url'] = '/login'
        popupContent['btn2']['text'] = 'Login'
        popupContent['data'] = {}
        return showPopup(res=popupContent)

def isUserLogin():
    return session['userId'] if 'userId' in session else ()

def logout():
    session.pop('userId' , None)
    popupContent["heading"] = 'You are successfully logout'
    popupContent['description'] = ''
    popupContent['btn2']['url'] = '/'
    popupContent['btn2']['text'] = 'Home'
    popupContent['data'] = {}
    return showPopup(res=popupContent)
