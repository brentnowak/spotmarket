from flask import render_template
from app import app
from _utility import *

@app.route('/login.html')
def login():
    return render_template('pages/login.html', title="Login")

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('pages/index.html', title="Home", header="Home")

@app.route('/system.html')
def system():
    return render_template('pages/system.html', title="System", header="System")

@app.route('/settings.html')
def settings():
    return render_template('pages/settings.html', title="Settings", header="Settings")

@app.route('/wallet.html')
def wallet():
    return render_template('pages/wallet.html', title="Wallet", header="Wallet")

@app.route('/sovereignty.html')
def sovereignty():
    return render_template('pages/sovereignty.html', title="Sovereignty", header="Sovereignty")

@app.route('/blank.html')
def blank():
    return render_template('pages/blank.html', title="Blank", header="Blank", nav="Blank Page")

@app.route('/flot.html')
def flot():
    return render_template('pages/flot.html', title="Flot", header="Flot Charts", nav="Flot Page")

@app.route('/morris.html')
def morris():
    return render_template('pages/morris.html', title="Morris", header="Morris.js Charts", nav="Morris Page")

@app.route('/tables.html')
def tables():
    return render_template('pages/tables.html', title="Tables", header="Tables", nav="Tables Page")

@app.route('/forms.html')
def forms():
    return render_template('pages/forms.html', title="Forms", header="Forms", nav="Forms Page")

@app.route('/panels-wells.html')
def panels_wells():
    return render_template('pages/panels-wells.html', title="Panels and Wells", header="Panels and Wells", nav="Panels and Wells Page")

@app.route('/buttons.html')
def buttons():
    return render_template('pages/buttons.html', title="Buttons", header="Buttons", nav="Buttons Page")

@app.route('/notifications.html')
def notifications():
    return render_template('pages/notifications.html', title="Notifications", header="Notifications", nav="Notifications Page")

@app.route('/typography.html')
def typography():
    return render_template('pages/typography.html', title="Typography", header="Typography", nav="Typography Page")

@app.route('/icons.html')
def icons():
    return render_template('pages/icons.html', title="Icons", header="Icons", nav="Icons Page")

@app.route('/grid.html')
def grid():
    return render_template('pages/grid.html', title="Grid", header="Grid", nav="Grid Page")


#
#   factionReport
#

@app.route('/factionReport_angel.html')
def faction_report_angel():
    return render_template('pages/factionReports/angel.html', title="Angel Cartel", header="Angel Cartel", nav="Angel Cartel")

@app.route('/factionReport_blood.html')
def faction_report_blood():
    return render_template('pages/factionReports/blood.html', title="Blood Raiders", header="Blood Raiders", nav="Blood Raiders")

@app.route('/factionReport_guristas.html')
def faction_report_guristas():
    return render_template('pages/factionReports/guristas.html', title="Guristas", header="Guristas", nav="Guristas")

@app.route('/factionReport_sansha.html')
def faction_report_sansha():
    return render_template('pages/factionReports/sansha.html', title="Sansha's Nation", header="Sansha's Nation", nav="Sansha's Nation")

@app.route('/factionReport_serpentis.html')
def faction_report_serpentis():
    return render_template('pages/factionReports/serpentis.html', title="Serpentis", header="Serpentis", nav="Serpentis")


#
#   securityReport
#

@app.route('/securityReport_highsec.html')
def securityreporthighsec():
    return render_template('pages/securityReports/securityReport_highsec.html', title="Highsec", header="Highsec", nav="Highsec")

@app.route('/securityReport_lowsec.html')
def securityreportlowsec():
    return render_template('pages/securityReports/securityReport_lowsec.html', title="Lowsec", header="Lowsec", nav="Lowsec")

@app.route('/securityReport_nullsec.html')
def securityreportnullsec():
    return render_template('pages/securityReports/securityReport_nullsec.html', title="Nullsec", header="Nullsec", nav="Nullsec")


#
# indexReports
#

@app.route('/indexReport_universe.html')
def index_report_universe():
    return render_template('pages/indexReports/universe.html', title="Universe", header="Universe", nav="Universe")


#
# API
#
@app.route('/api/toprattingevents')
def api_toprattingevents():
    return toprattingevents()

@app.route('/api/topnullrattingsystems')
def api_topnullrattingsystems():
    return topnullrattingsystems()

# Highsec
@app.route('/api/gettoprattingregions_nullsec')
def api_gettoprattingregions_nullsec():
    df = gettoprattingregions_nullsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')


@app.route('/api/gettoprattingsystems_nullsec')
def api_gettoprattingsystemss_nullsec():
    df = gettoprattingsystems_nullsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')


# Lowsec
@app.route('/api/gettoprattingregions_lowsec')
def api_gettoprattingregions_lowsec():
    df = gettoprattingregions_lowsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')


@app.route('/api/gettoprattingsystems_lowsec')
def api_gettoprattingsystemss_lowsec():
    df = gettoprattingsystems_lowsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')


# Highsec
@app.route('/api/gettoprattingregions_highsec')
def api_gettoprattingregions_highsec():
    df = gettoprattingregions_highsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')


@app.route('/api/gettoprattingsystems_highsec')
def api_gettoprattingsystemss_highsec():
    df = gettoprattingsystems_highsec()
    df = addkillsperday(df)
    return df.reset_index().to_json(orient='records')

# System
@app.route('/api/system/log')
def api_systemlog():
    return getlog()

@app.route('/api/system/countmapkills')
def api_systemcountmapkills():
    return databasecountmapkills()

@app.route('/api/system/countmapjumps')
def api_systemcountmapjumps():
    return databasecountmapjumps()

@app.route('/api/system/countmapsov')
def api_systemcountmapsov():
    return databasecountmapsov()

@app.route('/api/system/countmarkethistory')
def api_systemcountmarkethistory():
    return databasecountmarkethistory()


# Market Items
@app.route('/api/marketitems')
def api_marketitems():
    return databasemarketitems()


# Wallet
@app.route('/api/wallet/transactions')
def api_wallettransactions():
    return getwallettransactions()


# Sovereignty
@app.route('/api/sov/events')
def api_getsovevents():
    return getsovevents()
