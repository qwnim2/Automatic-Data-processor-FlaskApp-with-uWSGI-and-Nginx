from flask import Flask, make_response, request, render_template
from process import *

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/seven", methods=["GET", "POST"])
def seven():
    if request.method == "POST":
        input_data = request.files["input_file"]
        #input_data = input_file.stream.read().decode("utf-8")
        output_data = process_data(input_data)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        return response

    return render_template('seven.html')

@app.route("/CPchat", methods=["GET", "POST"])
def CPchat():
    if request.method == "POST":
        input_data = request.files["input_file"]
        output_data = process_data(input_data)  #TODO
        response = make_response(output_data)   
        #TODO response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        return response

    return render_template('CPchat.html')

@app.route('/login', methods=['GET', 'POST']) 
def login():
    #  利用request取得使用者端傳來的方法為何
    if request.method == 'POST':
                          #  利用request取得表單欄位值
        return 'Hello ' + request.values['username']
    
    #  非POST的時候就會回傳一個空白的模板
    return render_template('login.html')

           
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')



