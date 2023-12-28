from datetime import timedelta
from flask import Flask, render_template, jsonify
# from actions.auth import login , register
from db.sqlUtilities import DbOperationCust
from routes.routes import register, serviceUpdate, searchUser, searchService, delete_userData, login, home, deleteServiceById, account_details, serviceList, update_userData, showPopup, admin, userList, service, logout

app = Flask(__name__, template_folder='templates', static_folder='static')


app.permanent_session_lifetime = timedelta(minutes=5)

app.secret_key = 'hello'
# app.add_url_rule('/test', 'test', test)
# utils
db = DbOperationCust()
db.create_cust_table()
db.create_booking_table()

app.add_url_rule('/', 'home', home)
app.add_url_rule('/login', 'user_login', login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'user_register',
                 register, methods=['GET', 'POST'])
app.add_url_rule('/popup', 'popup', showPopup)
# app.add_url_rule('/showpopup/<type>', 'showpopup', showPopupType)
app.add_url_rule('/admin', 'admin', admin)
app.add_url_rule('/logout', 'logout', logout)

# user actions
app.add_url_rule('/account_details', 'account_details', account_details)
app.add_url_rule('/update_userData/<id>', 'update_userData',
                 update_userData, methods=['GET', 'POST'])
app.add_url_rule('/delete_userData/<id>', 'delete_userData',
                 delete_userData, methods=['GET', 'POST'])
app.add_url_rule('/userlist/<offset>', 'userlist', userList)


# Services actions
app.add_url_rule('/service_list/<offset>', 'serviceList',
                 serviceList, methods=['GET', 'POST'])
app.add_url_rule('/service/<type>', 'service',
                 service,  methods=['GET', 'POST'])
app.add_url_rule('/service/update', 'serviceUpdate',
                 serviceUpdate, methods=['GET', 'POST'])
app.add_url_rule('/service/delete/<id>', 'serviceDelete',
                 deleteServiceById, methods=['GET', 'POST'])
app.add_url_rule('/searchService', 'searchService',
                 searchService,  methods=['GET', 'POST'])
app.add_url_rule('/searchUser', 'searchUser',
                 searchUser, methods=['GET', 'POST'])
if __name__ == '__main__':

    app.run(debug=True, port=5001)
