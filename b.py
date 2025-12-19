from flask import Flask,render_template,request,redirect, url_for
import db
app = Flask(__name__, template_folder='', static_folder='')
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
    students = db.sel("students", 1)
    tables = db.selTables()
    return render_template("index.html", students=students, tables=tables)

@app.route('/add_student', methods=['POST'])
def addStudent():
    name = request.form.get('name')
    score = request.form.get('score')
    if not score.isdigit():
        return db.alert('別搞我，分數只能放數字')
      
    target = db.sel("students",{"name":name})
    
    if (target):
        return db.alert('已有相同名字')
     
    else:
        db.ins("students",{"name":name,"score":score})  

    return render_template("index.html", students= db.sel("students",1))

@app.route('/UpdAndDel', methods=['POST'])
def UpdAndDel():
    name = request.form.get('name')
    score =int( request.form.get('score'))
    target = db.sel("students",{"name":name})
    
    if 'upd' in request.form:
        sid = request.form.get('upd')
        if(target and str(target[0]['id'])!= sid):
            return db.alert('已有其他使用者')
        if not str(score).isdigit():
            return db.alert('別搞我，分數只能放數字')
        db.upd("students",{"name":name,"score":score},{"id":sid})

    if 'del' in request.form:
        sid = request.form.get('del')
        db.delete("students",{"id":sid})
        
    return render_template("index.html", students= db.sel("students",1))


@app.route('/selData', methods=['POST'])
def selData():
    selectData = request.form.get('select')
    option = int(request.form.get('option'))
    students = ""
    tables = db.selTables() 
    if(not selectData):
        students = db.sel("students",1)
        return render_template("index.html", students=students, option=str(option), tables=tables)
        

    if option == 0:
        if not selectData.isdigit():
            return db.alert('別搞我，分數只能放數字')
        students = db.sel("students",{"id":selectData})
        print(selectData,students[0]['id'])
    elif option == 1:
        students = db.sel("students",{"name":selectData})
    elif option == 2:
        if not selectData.isdigit():
            return db.alert('別搞我，分數只能放數字')
        students = db.sel("students",{"score":selectData})
   

    return render_template("index.html", students=students,option=str(option), tables=tables)


@app.route('/add_table', methods=['POST'])

def add_table():
    table_name = request.form.get('table_name')  # 前端新增資料表名稱
    col_names = request.form.getlist('col_name[]')
    col_types = request.form.getlist('col_type[]')

    if not table_name or not col_names or not col_types:
        return db.alert("資料表名稱或欄位不能為空")

    if len(col_names) != len(col_types):
        return db.alert("欄位名稱與型別數量不一致")

    # 把兩個 list 合併成 dict
    columns_dict = {name.strip(): typ.strip() for name, typ in zip(col_names, col_types)}

    # 呼叫 create_table
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