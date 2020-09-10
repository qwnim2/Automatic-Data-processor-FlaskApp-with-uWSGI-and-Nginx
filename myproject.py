from flask import Flask, make_response, request
from flask import redirect, render_template, url_for, send_file
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
def CPchat_alert():   
    if request.method == "POST":
        input_data = request.files["input_file"]
        output_data, date = CPchat_difference(input_data)  
        response = make_response(output_data)   
        response.headers["Content-Disposition"] = f"attachment; filename=Chat_alert_{date}.csv"
        return response

    return render_template('CPchat_alert.html')

@app.route('/Dating_List', methods=["GET", "POST"])
def dating_list():
    if request.method == "POST":
        input_data = request.files["input_file"]
        output, date = Dating_list(input_data)  
        # response = make_response(output_data)   
        # response.headers["Content-Disposition"] = f"attachment; filename={date}甜蜜約會.csv" 
        # return response
        return send_file(output, attachment_filename=f"{date}甜蜜約會.xlsx", as_attachment=True)


    return render_template('Dating_List.html')

@app.route('/CPonline_List', methods=["GET", "POST"])
def CPonline_List():
    if request.method == "POST":
        input_data = request.files["input_file"]
        output = CPonline_List_func(input_data)  
        # response = make_response(output_data)   
        # response.headers["Content-Disposition"] = f"attachment; filename={date}甜蜜約會.csv" 
        # return response
        return send_file(output, attachment_filename=f"CP在線數量監測.xlsx", as_attachment=True)

    return render_template('CPonline_List.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('hello', username=request.form.get('username')))

    return render_template('login.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

# REPORT part
@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/stream_diamond_diff_report')
def stream_diamond_diff_report():
    return render_template('diamond_diff_stream_debut.html')

@app.route('/flix_wordcloud_report')
def flix_worldcloud_report():
    return render_template('Flix_WordCloud.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')



