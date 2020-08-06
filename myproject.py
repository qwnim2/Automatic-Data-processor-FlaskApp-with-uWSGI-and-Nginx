from flask import Flask, make_response, request
from flask import redirect, render_template, url_for
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
        output_data, min_date, max_date = flix_week_consumption(input_data)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = f"attachment; filename=Flix_week_consumption_{min_date}_{max_date}.csv"
        return response

    return render_template('seven.html')

@app.route("/CPchat_alert", methods=["GET", "POST"])
def CPchat_alert():   #TODO
    if request.method == "POST":
        input_data = request.files["input_file"]
        output_data, date = CPchat_difference(input_data)  #TODO
        response = make_response(output_data)   
        response.headers["Content-Disposition"] = f"attachment; filename=Chat_alert_{date}.csv"
        return response

    return render_template('CPchat_alert.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('hello', username=request.form.get('username')))

    return render_template('login.html')

@app.route('/hello/<username>')
def hello(username):
    return render_template('hello.html', username=username)
     
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')



