from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')

def home():
    title = "Title Test"
    paragraph = ['Paragraph 1', 'Paragraph 2', 'Paragraph 3']
    return render_template("index.html", title=title, paragraph=paragraph)


@app.route('/dashboard_overview')
def welcome():
    return render_template("dashboard_overview.html")

@app.route('/dashboard_npc_universe')
def dashboard_npc_universe():
    return render_template("dashboard_universe.html")

@app.route('/dashboard_npc_angel')
def dashboard_npc_angel():
    return render_template("dashboard_npc_angel.html")

@app.route('/dashboard_npc_blood')
def dashboard_npc_blood():
    return render_template("dashboard_npc_blood.html")

@app.route('/dashboard_npc_guristas')
def dashboard_npc_guristas():
    return render_template("dashboard_npc_guristas.html")

@app.route('/dashboard_npc_sanshas')
def dashboard_npc_sanshas():
    return render_template("dashboard_npc_sanshas.html")

@app.route('/dashboard_npc_serpentis')
def dashboard_npc_serpentis():
    return render_template("dashboard_npc_serpentis.html")

# Solar System Detail

@app.route('/30004468')
def solarSystemID_30004468():
    return render_template("30004468.html")

@app.route('/30000182')
def solarSystemID_30000182():
    return render_template("30000182.html")



if __name__ == '__main__':
    app.run(debug=True)
