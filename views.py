from flask import Flask, render_template, request, redirect, url_for, json, flash, make_response
import common
from flask_login import login_user, login_required, logout_user
from flask_login import LoginManager, current_user
# from user import LoginForm, User
from login_form import LoginForm
from models import User
import util
from application import app, db
# from recommender import content_based
from recommender import hybrid_pipeline

# use login manager to manage session
login_manager = LoginManager()
# login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


# The callback to reload User object.
@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # print(this_function_name)
    if request.method == 'POST':
        form = LoginForm()
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)

        print(user_name, password)

        user = User(user_name, password)
        if user.verify_password(password):
            login_user(user)
            return redirect(url_for('homepage', title="logged in as {0}".format(user.username)))
        else:
            flash("username and password do not match!")
            return render_template('login.html', title="Log In")
    return render_template('login.html', title="Log In")


@app.route('/register', methods=['GET', 'POST'])
def register():
    # print(this_function_name)
    if request.method == 'GET':
        return render_template('register.html', title='Register Your Account')

    req_json = util.request_form_to_json(request)
    if req_json['password'] != "" and req_json['username'] != "":
        user = User(req_json['username'], req_json['password'])
        print(user)
        status, message = api.add_user(user)
        if status:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', warning=None)
    else:
        warning = "Username and password is empty"
        return render_template('register.html', title="Get Code", warning=warning)


@app.route('/logout')
@login_required
def logout():
    print("{0} is authenticated {1}".format(current_user, current_user.is_authenticated))
    logout_user()
    print("{0} is authenticated {1}".format(current_user, current_user.is_authenticated))
    return redirect(url_for('login'))


@app.route("/")
def homepage():
    items = []
    return render_template('search.html', items=items)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        inputs = _get_form_fields()
        print('/n')
        print({"inputs": inputs})
        result = hybrid_pipeline.hybrid_pipe(
            patent_id=None,
            after=inputs[common.AFTER],
            before=inputs[common.BEFORE],
            kind=inputs[common.KIND],
            cpc=inputs[common.CPC],
            inventor=inputs[common.INVENTOR],
            lawyer=inputs[common.LAWYER],
            assignee=inputs[common.ASSIGNEE],
            sentence=inputs[common.KEYWORDS])
        result = result.values.tolist()[:10]
        # print("result {0} {1}".format(type(result), result))
        return render_template('search.html', items=result, CPC_VALUES=common.CPC_VALUES)
    else:
        return redirect(url_for('homepage'))


@app.route('/more', methods=['POST'])
def save_clicked_items():
    if 'clicked_items' in request.cookies:
        items_in_string = request.cookies['clicked_items']
        clicked_items = get_distinct_items(items_in_string, '%2C')
        print(clicked_items)
        # GET MORE ITEMS FROM RECOMMENDATION SERVICE
        more_items = _refined_recommend_items("current_user", clicked_items)
        response = make_response(render_template('search.html', items=more_items, CPC_VALUES=common.CPC_VALUES))
        response.delete_cookie('clicked_items', path='/')
        return response
    return redirect('/')


def _get_form_fields():
    inputs = {}
    for key in common.SEARCH_FORM_FIELDS:
        if request.form.get(key):
            inputs[key] = request.form.get(key)
        else:
            inputs[key] = None
    return inputs


def _refined_recommend_items(username, clicked_items):
    result = list()
    for i in range(len(clicked_items)):
        result.append({})
    return result


def get_distinct_items(items_in_string, delimiter):
    items = items_in_string.split(delimiter)[:-1]
    return list(set(items))



