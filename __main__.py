from flask import Flask, request, render_template

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/")
def hello():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def login():
    if request.method == 'POST':
        # return do_the_login()
        return "hello"
    else:
        # return show_the_login_form()
        return "world"


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    # return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)