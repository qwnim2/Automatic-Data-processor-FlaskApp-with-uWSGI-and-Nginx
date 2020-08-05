from flask import Flask, make_response, request
from process import process_data

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def file_summer_page():
    if request.method == "POST":
        input_data = request.files["input_file"]
        #input_data = input_file.stream.read().decode("utf-8")
        output_data = process_data(input_data)
        response = make_response(output_data)
        response.headers["Content-Disposition"] = "attachment; filename=result.csv"
        return response

    return '''
        <html>
            <body>
                <h2>長片七日內銷售</h2>
                <h3>Select the file you want to extract:  </h3>
                <p>NOTE: File should come from <a href="https://mixpanel.com/s/XKjbb">HERE</a>.</p>
                <form method="post" action="." enctype="multipart/form-data">
                    <p><input type="file" name="input_file" /></p>
                    <p><input type="submit" value="Process the file" /></p>
                </form>
            </body>
        </html>
    '''

@app.route('/user/<username>')
def username(username):
    return 'i am ' + username
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')



