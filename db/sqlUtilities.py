from  db.sqlContext import SqliteConnection

class DbOperationCust:
    def create_cust_table(self):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""create table if not exists customers 
            (id integer primary key, 
            name text, 
            email text,
            password text, 
            address text, 
            phone_no text)
            """)

    def insert_cust_data(self, cust_list):
        with SqliteConnection('data.db') as connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""insert into customers 
                (id, name, email,password, address, phone_no) 
                values (?, ?, ?, ?, ?,?)""", cust_list)
                return True
            except:
                return False

    def get_all_customers(self ,offset):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            print('sfs',offset)
            cursor.execute("select * from customers limit ?,4" , (offset,))
            customers = cursor.fetchall()
            return customers

    def get_cust_by_id(self, cust_id):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select * from customers where id = ?", (cust_id,))
            cust = cursor.fetchone()
            return cust
    def get_cust_by_email(self, email):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select * from customers where email = ?", (email,))
            cust = cursor.fetchone()
            return cust
    def get_cust_by_Number(self, number):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select * from customers where phone_no = ?", (number,))
            cust = cursor.fetchone()
            return cust
    def count_cus_details(self):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select count(*) from customers")
            cust = cursor.fetchone()
            return cust[0]

    def get_cust_by_id_pass(self, cust_id, password):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select * from customers where id = ? and password=?", (cust_id, password))
            cust = cursor.fetchone()

            return cust

    def get_by_mobile_no(self, mobile_no):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            # mobile_no=str(mobile_no)
            cursor.execute("select * from customers  where phone_no=? ", (mobile_no,))
            cust = cursor.fetchall()
            print(cust)
            return cust

    def delete_details(self, custid):
        with SqliteConnection('data.db') as con:
            cursor = con.cursor()
            cursor.execute("""delete from customers where id=?""", (custid,))

    def update_details(self, colName , colValue , searchCol , searchValue):
        with SqliteConnection('data.db') as con:
            cursor = con.cursor()
            cursor.execute("update customers set " + colName + "=? where " + searchCol + "=?", (colValue, searchValue,))

    def getconfirmation(self, custid):
        with SqliteConnection('data.db') as con:
            cursor = con.cursor()
            cursor.execute("""select * from customers where id=?""", (custid,))
            cust = cursor.fetchall()
            return  cust

    def create_booking_table(self):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''create table if not exists booking
            (service_id text primary key, 
            cus_id int ,
            service_name text ,
            subservice text ,
            date text,
            address text,
            vender_selection text,
            amount int,
            status text
            )''')

    def insert_table(self, book_list):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''insert into booking (service_id,cus_id,service_name,subservice,date,address,
            vender_selection,amount , status ) values(?,?,?, ?, ?, ?, ?,?,?)''', book_list)

    def get_booking_by_userId(self, id ,  limit , offset):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            # mobile_no=str(mobile_no)
            cursor.execute("""select 
            service_id,b.service_name,subservice,date,b.address,
            vender_selection,amount, status 
            from 
            booking b 
            inner join customers c
            on b.cus_id = c.id
              where cus_id=? 
              LIMIT ?, ? """, (id,offset , limit))
            cust = cursor.fetchall()
            return cust

    def get_booking_all(self , limit , offset):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            # mobile_no=str(mobile_no)
            print(offset)
            cursor.execute("""select 
            service_id, c.name,service_name,subservice,date,b.address,
            vender_selection,amount, status 
            from 
            booking b 
            inner join customers c
            on b.cus_id = c.id
            LIMIT ?, ?""" , (offset , limit))
            cust = cursor.fetchall()
            return cust
    def update_booking_status(self , setcol , value , searchCol , searchValue):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            # mobile_no=str(mobile_no)
            cursor.execute("update booking set " + setcol + "=? where " + searchCol + "=?",( value ,searchValue,))


    def delete_bookings_by_id(self, id):
        with SqliteConnection('data.db') as con:
            print(id)
            cursor = con.cursor()
            cursor.execute("""delete from booking where service_id=?""", (id,))

    def search_bookings_by_id(self, id):
        with SqliteConnection('data.db') as con:
            print(id)
            cursor = con.cursor()
            print("sql" , id)
            try:
                cursor.execute("""select * from booking where service_id =? """, (id,))
                cust = cursor.fetchall()
                return  cust
            except:
                return []

    def paginate_bookings(self, limit , offset):
        with SqliteConnection('data.db') as con:
            print(id)
            cursor = con.cursor()
            print("sql" , id)
            try:
                cursor.execute("""select * from booking where service_id =? """, (id,))
                cust = cursor.fetchall()
                return  cust
            except:
                return []

    def cus_by_service_type(self, service_type):
        with SqliteConnection('data.db') as connection:
            cursor = connection.cursor()
            cursor.execute("select * from booking where service_name=?", (service_type,))
            cust = cursor.fetchall()
            return cust
