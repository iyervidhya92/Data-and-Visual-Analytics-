from flask import Flask,render_template,request,json,redirect,url_for
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('hello.html')


@app.route("/", methods=['POST'])
def redirectUser():
    return redirect(url_for("signUp"))


@app.route('/signUp')
def signUp():
    return render_template('signup.html')


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user = request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user': user, 'pass': password});


if __name__ == "__main__":
    app.run(debug=True)