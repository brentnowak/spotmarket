from flask import render_template
from app import app
from _utility import *


#############################
# Main pages
#############################
@app.route('/login.html')
def login():
    return render_template('pages/login.html', title="Login")

@app.route('/')
@app.route('/dashboard')
def index():
    return render_template('pages/dashboard.html', title="Dashboard", header="Dashboard")

@app.route('/system/logs')
def system():
    return render_template('pages/logs.html', title="Logs", header="Logs")

@app.route('/system/settings')
def settings():
    return render_template('pages/settings.html', title="Settings", header="Settings")

@app.route('/trade/wallet')
def wallet():
    return render_template('pages/wallet.html', title="Wallet", header="Wallet")

@app.route('/blank.html')
def blank():
    return render_template('pages/blank.html', title="Blank", header="Blank", nav="Blank Page")

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

@app.route('/report/faction/angel')
def faction_report_angel():
    return render_template('pages/factionReports/angel.html', title="Angel Cartel", header="Angel Cartel", nav="Angel Cartel")

@app.route('/report/faction/blood')
def faction_report_blood():
    return render_template('pages/factionReports/blood.html', title="Blood Raiders", header="Blood Raiders", nav="Blood Raiders")

@app.route('/report/faction/guristas')
def faction_report_guristas():
    return render_template('pages/factionReports/guristas.html', title="Guristas", header="Guristas", nav="Guristas")

@app.route('/report/faction/sansha')
def faction_report_sansha():
    return render_template('pages/factionReports/sansha.html', title="Sansha's Nation", header="Sansha's Nation", nav="Sansha's Nation")

@app.route('/report/faction/serpentis')
def faction_report_serpentis():
    return render_template('pages/factionReports/serpentis.html', title="Serpentis", header="Serpentis", nav="Serpentis")

@app.route('/report/faction/mordu')
def faction_report_mordu():
    return render_template('pages/factionReports/mordu.html', title="Mordu's Legion Command", header="Mordu's Legion Command", nav="Mordu's Legion Command")

@app.route('/report/faction/sisters')
def faction_report_sisters():
    return render_template('pages/factionReports/sisters.html', title="Servant Sisters of EVE", header="Servant Sisters of EVE", nav="Servant Sisters of EVE")


#
#   securityReport
#
@app.route('/report/security/highsec')
def securityreporthighsec():
    return render_template('pages/securityReports/highsec.html', title="Highsec", header="Highsec", nav="Highsec")

@app.route('/report/security/lowsec')
def securityreportlowsec():
    return render_template('pages/securityReports/lowsec.html', title="Lowsec", header="Lowsec", nav="Lowsec")

@app.route('/report/security/nullsec')
def securityreportnullsec():
    return render_template('pages/securityReports/nullsec.html', title="Nullsec", header="Nullsec", nav="Nullsec")


#
# indexReports
#
@app.route('/report/index/universe')
def indexreport_universe():
    return render_template('pages/indexReports/universe.html', title="Universe", header="Universe", nav="Universe")

@app.route('/report/index/deadend')
def indexreport_deadend():
    return render_template('pages/indexReports/deadend.html',
                           title="Dead End Systems",
                           header="Dead End Systems",
                           nav="Dead End Systems",
                           systemList=json.loads(getdeadendsystems(1)))

@app.route('/report/index/pirateships')
def indexreport_pirateships():
    return render_template('pages/indexReports/pirateships.html', title="Pirate Ships", header="Pirate Ships", nav="Pirate Ships")


#
# regionReports
#
@app.route('/report/region/<regionID>')
def regionreport(regionID):
    return render_template('pages/regionReports/regionReport.html',
                           regionID=regionID,
                           title="Region 1",
                           header="Region 1",
                           nav="Region 1")


#
# jumpReports
#
@app.route('/report/jump/tradehubs')
def jumpreport_tradehubs():
    return render_template('pages/jumpReports/tradehubs.html',
                           title="Trade Hubs",
                           header="Trade Hubs",
                           nav="Trade Hubs")

#
# marketReports
#
@app.route('/report/market/pilotservices/')
def marketreport_pilotservices():
    return render_template('pages/marketReports/pilotservices.html',
                           title="Pilot Services",
                           header="Pilot Services",
                           nav="Pilot Services")

#
# moonReports
#
@app.route('/report/moon/sov')
def moonreport_sov():
    return render_template('pages/moonReports/sov.html', title="Sovereignty", header="Sovereignty", nav="Sovereignty")

@app.route('/report/moon/gases')
def moonreport_gases():
    return render_template('pages/moonReports/gases.html', title="Gasses", header="Gasses", nav="Gasses")

@app.route('/report/moon/r8')
def moonreport_r8():
    return render_template('pages/moonReports/r8.html', title="Rarity 8", header="Rarity 8", nav="Rarity 8")

@app.route('/report/moon/r16')
def moonreport_r16():
    return render_template('pages/moonReports/r16.html', title="Rarity 16", header="Rarity 16", nav="Rarity 16")

@app.route('/report/moon/r32')
def moonreport_r32():
    return render_template('pages/moonReports/r32.html', title="Rarity 32", header="Rarity 32", nav="Rarity 32")

@app.route('/report/moon/r64')
def moonreport_r64():
    return render_template('pages/moonReports/r64.html', title="Rarity 64", header="Rarity 64", nav="Rarity 64")

#
# Map
#
@app.route('/map/sovereignty')
def map_sovereignty():
    return render_template('pages/mapReports/sovereignty.html', title="Sovereignty", header="Sovereignty")

@app.route('/map/conquerablestations')
def map_conquerablestations():
    return render_template('pages/mapReports/conquerablestations.html', title="Conquerable Stations", header="Conquerable Stations")


#############################
# API
#############################
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
    return getsystemlogs()

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


# Settings
@app.route('/api/marketitems')
def api_marketitems():
    return databasemarketitems()

@app.route('/api/characters')
def api_characters():
    return getcharacters()


# Wallet
@app.route('/api/wallet/transactions')
def api_wallettransactions():
    return getwallettransactions()


# Sovereignty
@app.route('/api/sov/events')
def api_getsovevents():
    return getsovevents()


# Simple Lookups
@app.route('/api/regionName/<regionID>')
def api_regionID(regionID):
    return regionName(regionID)

# Market
@app.route('/api/typeName/<typeID>')
def api_typeID(typeID):
    return getmarkethistory_typeid(typeID)

@app.route('/api/market/avgprice/<typeID>')
def api_marketavgprice(typeID):
    return getmarkethistory_avgprice(typeID)


# Region
@app.route('/api/region/sovereignty/<regionID>')
def api_regionsovereignty(regionID):
    return getsovbyregion(regionID)

@app.route('/api/gettoprattingbyregion/<regionID>')
def api_gettoprattingbyregion(regionID):
    df = gettoprattingbyregion(regionID)
    return df.reset_index().to_json(orient='records')

# Moons
@app.route('/api/moonminerals/regionid/<regionID>')
def api_moonmineralsbyregion(regionID):
    return getmoonmineralsbyregion(regionID)

@app.route('/api/moonminerals/typeid/<typeID>')
def api_moonmineralsbytype(typeID):
    return getmoonmineralsbytypeid(typeID)

@app.route('/api/moonminerals/alliance/<typeID>')
def api_moonmineralsbyalliance(typeID):
    return getmoonmineralsbyalliance(typeID)

@app.route('/api/moonminerals/alliance/')
def api_moonmineralsbyallalliance():
    return getmoonmineralsbysov()

# Index
@app.route('/api/report/index/deadend/<gateCountLimit>')
def api_getdeadendsystems(gateCountLimit):
    return getdeadendsystems(gateCountLimit)

@app.route('/api/report/index/sovchanges')
def indexreport_sovchanges():
    return getsoveventsumbyday()

@app.route('/api/report/index/pirateships/<shipclass>')
def indexreport_indexpirateships(shipclass):
    if shipclass == "battleship":
        return getindexpirateships(17918, 17740, 17736, 17738, 17920)
    if shipclass == "cruiser":
        return getindexpirateships(17720, 17922, 17715, 17718, 17722)
    if shipclass == "frigate":
        return getindexpirateships(17932, 17926, 17930, 17924, 17928)

# Map
@app.route('/api/map/conquerablestations')
def api_conquerablestations():
    return getconquerablestationslist()

@app.route('/api/map/jumps/<solarSystemID>')
def api_mapjumps_solarsystemID(solarSystemID):
    return mapjumps_solarsystemID(solarSystemID)

@app.route('/api/map/jumps/tradehubs')
def api_mapjumps_tradehubs():
    return mapjumps_tradehubs()

@app.route('/api/map/npckills/region/<regionID>')
def api_mapkills_npckillsbyregion(regionID):
    return mapkills_npckillsbyregion(regionID)

@app.route('/api/map/shipkills/region/<regionID>')
def api_mapkills_shipkillsbyregion(regionID):
    return mapkills_shipkillsbyregion(regionID)

@app.route('/api/map/podkills/region/<regionID>')
def api_mapkills_podkillsbyregion(regionID):
    return mapkills_podkillsbyregion(regionID)

@app.route('/api/map/jumps/region/<regionID>')
def api_mapkills_jumpsbyregion(regionID):
    return mapkills_jumpsbyregion(regionID)
