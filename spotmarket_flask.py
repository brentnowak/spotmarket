from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    title = "Test"
    paragraph = ['test1', 'test2']
    return render_template("index.html", title=title, paragraph=paragraph)


@app.route('/npckills')
def welcome():
    title = "NPC Kills"
    return render_template("npckills.html", title=title)


@app.route('/universe')
def reportsUniverse():
    return render_template("universe.html")


if __name__ == '__main__':
    app.run(debug=True)
