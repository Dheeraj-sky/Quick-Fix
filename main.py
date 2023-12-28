from flask import Flask, render_template
from db.sqlUtilities import dbopertions_cust
app = Flask(__name__, template_folder='templates', static_folder='static')

# app.config('STATIC') = 'static'



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/test4')
def test1():
    d = dbopertions_cust()
    d.create_table()
    # # d.insertdetails(['2','test', 'email', 'pass', 'adtree', '1223'])
    data = d.getallusers()
    #
    print('this ', data)
    return render_template('test.html', name=data)

# def login():
#     pass

# test1()

# @app.route('/test')
# def test():
#     return 'fsdfsdf sdfsdf'


# app.add_url_rule('/login', 'user_login', login)

#
# @app.route('/test1')
# def test1():
#     return 'tefsdfs'


# @app.route('/register')
# def register():
#     return render_template('register.html')


# @app.route('/account_details')
# def account_details():
#     return render_template('account_details.html')

if __name__ == '__main__':
    app.run(debug=True , port=5001)