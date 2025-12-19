from flask import Flask,render_template,request,redirect, url_for, session
from datetime import datetime
import db
app = Flask(__name__, template_folder='', static_folder='')
app.secret_key = "你的隨機字串" 

# data = db.sel("students",1) 
# del
# db.delete("students",{"id":2})
# upd 
# db.upd("students",{"name":"帥哥"},{"id":4})
# sel
# db.sel("students",1) 
# db.sel("students",{"id":5})
# ins 
# db.ins("students",{"name":"大帥哥","score":50})


@app.route('/')
def home():
    room = db.sel("room",1,'booking_id')
    tables = db.selTables()
    return render_template("index.html", students=room, tables=tables, current_table="room")

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('booking',edit='3'))

    # tables = db.selTables()
    islogin = True
 
    return render_template("login.html",islogin =islogin)



@app.route('/booking')
def booking():
    if 'user' not in session:
        return  db.alert('未登入','/login.html')
    url = request.args.get('edit')or '3'

    room = db.sel("room",1,'booking_id')
    room_types = db.sel("room_type", 1)
    users = db.sel('users')
    print(session['user'])
    for all in room:
        price = db.sel('room_type',{'name':all['room_type']})[0]['price']
        all['price']= price*(all['check_outdate'] - all['check_indate']).days
        print(all)
    return render_template("booking.html", students=room,user= session['user'],url=url, room_types=room_types,users =users
)

@app.route('/login_check', methods=['POST'])
def login_check():
    acc = request.form.get('acc')
    ps = request.form.get('ps')
    checkAcc = db.sel('users',{'account':acc,'password':ps})
    if(checkAcc):
        user = checkAcc[0]
        session['user'] = user
        return redirect(url_for('booking',edit='3'))
    else:
        return db.alert("帳號或密碼錯誤",'login.html')
 
@app.route('/newAcc', methods=['POST'])
def newAcc():
    acc = request.form.get('acc')
    ps = request.form.get('ps')
    checkAcc = db.sel('users',{'account':acc})
    
    if(checkAcc):
        return db.alert("已有此帳號",'/login.html')
    db.ins('users',{'account':acc,'password':ps,'level':0})
    return db.alert("註冊成功",'/login.html')

@app.route('/UpdAndDelUsers', methods=['POST'])
def UpdAndDelUsers():
    id = request.form.get('upd') or request.form.get('del')

    if 'upd' in request.form:
        account = request.form.get('account')
        password = request.form.get('password')
        level = int(request.form.get('level'))
     
        db.upd("users", {
            "password": int(password),
            "account": account,
            "level": level,
        }, {"id": id})

    if 'del' in request.form:
        db.delete("users", {"id": id})

    return redirect(url_for('booking',edit='1'))

@app.route('/add_roomtype', methods=['POST'])
def add_roomtype():
    name = request.form.get('name')
    price = request.form.get('price')

    
    target = db.sel("room_type",{'name':name})
 
  
    if(target):
        return db.alert('已有此類型房間','/booking')

    db.ins("room_type", {
        "name": name,
        "price": int(price),
    })

    return redirect(url_for('booking',edit='2'))

@app.route('/UpdAndDelRoomType', methods=['POST'])
def UpdAndDelRoomType():
    id = request.form.get('upd') or request.form.get('del')

    if 'upd' in request.form:
        name = request.form.get('name')
        price = request.form.get('price')

        db.upd("room_type", {
            "name": name,
            "price": int(price),
        }, {"id": id})

    if 'del' in request.form:
        db.delete("room_type", {"id": id})

    return redirect(url_for('booking',edit='2'))

# ---------------- 新增房間預訂 ----------------
@app.route('/add_room', methods=['POST'])
def add_room():
    room_number = request.form.get('room_number')
    customer_name = request.form.get('customer_name')
    room_type_id=int( request.form.get('room_type_id'))
    contact_info = request.form.get('contact_info')
    check_indate = request.form.get('check_indate')
    check_outdate = request.form.get('check_outdate')
    room_type = db.sel('room_type',{'id':room_type_id})[0]['name']
    if not (room_number and customer_name and contact_info and check_indate and check_outdate):
        return db.alert("所有欄位都必須填寫")

    if not room_number.isdigit():
        return db.alert("房號必須是數字")
    
    target = db.sel("room",{'room_number':room_number},'booking_id')
 
    in_date = datetime.strptime(check_indate, '%Y-%m-%d').date()
    out_date = datetime.strptime(check_outdate, '%Y-%m-%d').date()
    if in_date >= out_date:
        return db.alert("退房日期必須晚於入住日期！")
    if(target):
        for booking in target:
            target_in_date = booking['check_indate'] 
            target_out_date = booking['check_outdate']
            if in_date < target_out_date and target_in_date < out_date :
                 return db.alert("該房間在您選擇的日期範圍內已被預訂，請重新選擇日期！")
    find_room = db.sel('room_type',{'name':room_type})
    db.ins("room", {
        "room_number": int(room_number),
        "room_type": room_type,
        "customer_name": customer_name,
        "contact_info": contact_info,
        "check_indate": check_indate,
        "check_outdate": check_outdate,
        "user_id":session['user']['id'],
    },"booking_id")

    return redirect(url_for('booking',edit='3'))


@app.route('/UpdAndDelRoom', methods=['POST'])
def UpdAndDelRoom():
    booking_id = request.form.get('upd') or request.form.get('del')

    if 'upd' in request.form:
        room_number = request.form.get('room_number')
        customer_name = request.form.get('customer_name')
        contact_info = request.form.get('contact_info')
        check_indate = request.form.get('check_indate')
        check_outdate = request.form.get('check_outdate')
        room_type_id = int(request.form.get('room_type_id'))
        room_type = db.sel('room_type',{'id':room_type_id})[0]['name']
        if not room_number.isdigit():
            return db.alert("房號必須是數字",'/booking')
        target = db.sel("room",{'room_number':room_number},'booking_id')
    
        in_date = datetime.strptime(check_indate, '%Y-%m-%d').date()
        out_date = datetime.strptime(check_outdate, '%Y-%m-%d').date()
        if in_date >= out_date:
            return db.alert("退房日期必須晚於入住日期！",'/booking')
        if(target):
            for booking in target:
                target_in_date = booking['check_indate'] 
                target_out_date = booking['check_outdate']
                print( target[0]['booking_id'],booking_id)
                print(booking_id,in_date ,out_date ,booking['booking_id'], target_in_date , target_out_date )
                if booking['booking_id'] == int(booking_id):
                    continue
                if in_date < target_out_date and target_in_date < out_date :
                    return db.alert("該房間在您選擇的日期範圍內已被預訂，請重新選擇日期！",'/booking')
            db.upd("room", {
                "room_number": int(room_number),
                "customer_name": customer_name,
                "contact_info": contact_info,
                "check_indate": check_indate,
                "check_outdate": check_outdate,
                "room_type": room_type
            }, {"booking_id": booking_id})

    if 'del' in request.form:
        db.delete("room", {"booking_id": booking_id})

    return redirect(url_for('booking',edit='3'))



@app.route('/selData', methods=['POST'])
def selData():
    selectData = request.form.get('select')
    option = int(request.form.get('option'))
    tables = db.selTables()
    room_types = db.sel("room_type", 1)
    users = db.sel('users')
    url = request.args.get('edit', '3')

    if not selectData:
        students = db.sel("room", 1,'booking_id')
        for all in students:
            price = db.sel('room_type',{'name':all['room_type']})[0]['price']
            all['price']= price*(all['check_outdate'] - all['check_indate']).days
        return render_template("booking.html",url=url, students=students, tables=tables,users=users, user= session['user'], option=str(option), room_types=room_types)

    if option == 0:  # Booking_ID
        if not selectData.isdigit():
            return db.alert("Booking_ID 必須是數字")
        students = db.sel("room", {"booking_id": selectData},'booking_id')
    elif option == 1:  # Room_Number
        if not selectData.isdigit():
            return db.alert("Room_Number 必須是數字")
        students = db.sel("room", {"room_number": selectData},'booking_id')
    elif option == 2:  # Customer_Name
        students = db.sel("room", {"customer_name": selectData},'booking_id')
    elif option == 3:
        students = db.sel("room", {"room_type": selectData},'booking_id')

    for all in students:
        price = db.sel('room_type',{'name':all['room_type']})[0]['price']
        all['price']= price*(all['check_outdate'] - all['check_indate']).days
    return render_template("booking.html",url=url, students=students, tables=tables,user= session['user'],users=users, option=str(option), room_types=room_types)




@app.route('/add_table', methods=['POST'])

def add_table():
    table_name = request.form.get('table_name')  # 前端新增資料表名稱
    col_names = request.form.getlist('col_name[]')
    col_types = request.form.getlist('col_type[]')

    if not table_name or not col_names or not col_types:
        return db.alert("資料表名稱或欄位不能為空")

    if len(col_names) != len(col_types):
        return db.alert("欄位名稱與型別數量不一致")

    columns_dict = {name.strip(): typ.strip() for name, typ in zip(col_names, col_types)}

  
    db.create_table(table_name, columns_dict)

    return redirect(url_for('home'))



@app.route('/DelTable', methods=['POST'])
def DelTable():
    table_name = request.form.get('del')
    if table_name:
        db.drop_table(table_name)
    return redirect(url_for('home'))

# @app.route('/switch_table', methods=['POST'])
# def switch_table():
#     table_name = request.form.get('table_name')
#     if not table_name:
#         return db.alert("請選擇資料表")

#     # 查出該資料表的所有資料
#     try:
#         rows = db.sel(table_name, 1)  # 這裡假設 table 有 id 欄位，如果沒有可以修改 sel 函式
#     except Exception as e:
#         return db.alert(f"讀取資料表 {table_name} 失敗: {e}")

#     tables = db.selTables()
#     return render_template("index.html", students=rows, tables=tables, current_table=table_name)

    


# @app.route("/aboutme.html")
# def about():
#     return render_template(
#         "aboutme.html",
#         title="關於我",
#         img_src="img/烏一一阿一.png",
#         img_alt="烏一一阿一",
#         left_list=[
#             {"label": "科系/年級", "value": "資工二"},
#             {"label": "名字", "value": "褚昀澔"},
#             {"label": "Email", "value": "t113590010@ntut.org.tw"},
#         ],
#         right_list=[
#             {"label": "學校", "value": "台北科技大學"},
#             {"label": "科系", "value": "資訊工程系"},
#             {"label": "興趣", "value": "遊戲、編程"},
#             {"label": "最近在做的事1", "value": "重寫網頁，之前的網頁是php無法放到github"},
#             {"label": "最近在做的事2", "value": "花兩天把整個網頁改大半，終於完成了！"},
#         ],
#     )

if __name__=='__main__':
    app.run(debug = True)