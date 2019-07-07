from flask import Flask, request, render_template
import common

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/")
def hello():
    items = [{}, {}, {}]
    return render_template('search.html', items=items)


@app.route('/search', methods=['POST'])
def login():
    if request.method == 'POST':
        inputs = _get_form_fields()
        return inputs
    else:
        return "hello world"


def _get_form_fields():
    inputs = {}
    for key in common.SEARCH_FORM_FIELDS:
        if request.form.get(key):
            print({'key': key})
            inputs[key] = request.form.get(key)
    return inputs


if __name__ == '__main__':
    app.run(debug=True)