from flask import render_template
from app import app
from _api import *
from _dashboard import *
from _wallet import *
from _system import *
from _market import *
from _moon import *
from _map import *


#############################
# Main pages
#############################
@app.route('/')
@app.route('/dashboard')
def index():
    return render_template('pages/dashboard.html', title="Dashboard", header="Dashboard",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq(),
                           countdatakillmails="{:,.0f}".format(countdatakillmails()),
                           countdatamoonminerals="{:,.0f}".format(countdatamoonminerals()),
                           countdatamoonverify="{:,.0f}".format(countdatamoonverify()),
                           countlatestjitajump="{:,.0f}".format(countlatestjitajump()),
                           countdatamarkethistory="{:,.0f}".format(countdatamarkethistory()),
                           countdatawallet="{:,.0f}".format(countdatawallet()),
                           latestjumpdatatime=latestjumpdatatime().strftime('%Y-%m-%d %H:%M:%S'),
                           latestsovdatatime=latestsovdatatime().strftime('%Y-%m-%d %H:%M:%S'),
                           psutil_getmemory=psutil_getmemory(),
                           plexgetlatestprice="{:,.2f}".format(getlatestprice(29668, 10000002)),
                           plexgetlatestpricechange="{:,.2f}".format(getpricepercentchange(29668, 10000002)),
                           psutil_crestconnections=psutil_crestconnections(),
                           psutil_zkillboardconnections=psutil_zkillboardconnections(),
                           getwallettransactions=getwallettransactions(10),
                           getwalletbalances=getwalletbalances(),
                           getwalletbalancestotal=getwalletbalancestotal(),
                           getskillqueues=getskillqueues(),
                           getdbsize=getdbsize(),
                           countsovchangelastday=countsovchangelastday())

@app.route('/system/logs')
def systemsettings_logs():
    return render_template('pages/systemSettings/logs.html',
                           title="Logs",
                           header="Logs",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/system/market')
def systemsettings_settings():
    return render_template('pages/systemSettings/market.html',
                           title="Market",
                           header="Market",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/system/characters')
def systemsettings_characters():
    return render_template('pages/systemSettings/characters.html',
                           title="Characters",
                           header="Characters",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/system/zkillboard')
def systemsettings_zkillboard():
    return render_template('pages/systemSettings/zkillboard.html',
                           title="zKillboard",
                           header="zKillboard",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/system/database')
def systemsettings_database():
    return render_template('pages/systemSettings/database.html',
                           title="Database",
                           header="Database",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

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

@app.route('/forms.html')
def forms():
    return render_template('pages/forms.html', title="Forms", header="Forms", nav="Forms Page")

@app.route('/tables.html')
def tables():
    return render_template('pages/tables.html', title="Tables", header="Tables", nav="Tables Page")


#############################
# Error Handling
#############################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


#############################
#   factionReport
#############################
@app.route('/report/faction/overview')
def faction_report_overview():
    return render_template('pages/factionReports/overview.html',
                           title="Overview",
                           header="Overview",
                           nav="Overview",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/angel')
def faction_report_angel():
    return render_template('pages/factionReports/angel.html',
                           title="Angel Cartel",
                           header="Angel Cartel",
                           nav="Angel Cartel",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/blood')
def faction_report_blood():
    return render_template('pages/factionReports/blood.html',
                           title="Blood Raiders",
                           header="Blood Raiders",
                           nav="Blood Raiders",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/guristas')
def faction_report_guristas():
    return render_template('pages/factionReports/guristas.html',
                           title="Guristas",
                           header="Guristas",
                           nav="Guristas",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/sansha')
def faction_report_sansha():
    return render_template('pages/factionReports/sansha.html',
                           title="Sansha's Nation",
                           header="Sansha's Nation",
                           nav="Sansha's Nation",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/serpentis')
def faction_report_serpentis():
    return render_template('pages/factionReports/serpentis.html',
                           title="Serpentis",
                           header="Serpentis",
                           nav="Serpentis",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/mordu')
def faction_report_mordu():
    return render_template('pages/factionReports/mordu.html',
                           title="Mordu's Legion Command",
                           header="Mordu's Legion Command",
                           nav="Mordu's Legion Command",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/faction/sisters')
def faction_report_sisters():
    return render_template('pages/factionReports/sisters.html',
                           title="Servant Sisters of EVE",
                           header="Servant Sisters of EVE",
                           nav="Servant Sisters of EVE",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


#############################
#   securityReport
#############################
@app.route('/report/security/highsec')
def securityreporthighsec():
    return render_template('pages/securityReports/highsec.html',
                           title="Highsec",
                           header="Highsec",
                           nav="Highsec",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/security/lowsec')
def securityreportlowsec():
    return render_template('pages/securityReports/lowsec.html',
                           title="Lowsec",
                           header="Lowsec",
                           nav="Lowsec",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/security/nullsec')
def securityreportnullsec():
    return render_template('pages/securityReports/nullsec.html',
                           title="Nullsec",
                           header="Nullsec",
                           nav="Nullsec",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

#############################
#   characterReport
#############################
@app.route('/report/character/blueprints')
def characterreport_blueprints():
    return render_template('pages/characterReports/blueprints.html',
                           title="Blueprints",
                           header="Blueprints",
                           nav="Blueprints",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


@app.route('/report/character/orders')
def characterreport_orders():
    return render_template('pages/characterReports/orders.html',
                           title="Orders",
                           header="Orders",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


@app.route('/report/character/wallet')
def characterreport_wallet():
    return render_template('pages/characterReports/wallet.html',
                           title="Wallet",
                           header="Wallet",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


#############################
# indexReports
#############################
@app.route('/report/index/universe')
def indexreport_universe():
    return render_template('pages/indexReports/universe.html', title="Universe", header="Universe", nav="Universe")

@app.route('/report/index/deadend')
def indexreport_deadend():
    return render_template('pages/indexReports/deadend.html',
                           title="Dead End Systems",
                           header="Dead End Systems",
                           nav="Dead End Systems",
                           systemList=json.loads(getdeadendsystems(1)),
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/index/pirateships')
def indexreport_pirateships():
    return render_template('pages/indexReports/pirateships.html',
                           title="Pirate Ships",
                           header="Pirate Ships",
                           nav="Pirate Ships",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/index/boosters')
def indexreport_boosters():
    return render_template('pages/indexReports/boosters.html',
                           title="Boosters",
                           header="Boosters",
                           nav="Boosters",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/index/pilotservices')
def indexreport_pilotservices():
    return render_template('pages/indexReports/pilotservices.html',
                           title="Pilot Services",
                           header="Pilot Services",
                           nav="Pilot Services",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/index/capitalships')
def indexreport_capitalships():
    return render_template('pages/indexReports/capitalships.html',
                           title="Capital Ships",
                           header="Capital Ships",
                           nav="Capital Ships",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/index/goldenroute')
def indexreport_goldenroute():
    return render_template('pages/indexReports/goldenroute.html',
                           title="Golden Route",
                           header="Golden Route",
                           nav="Golden Route",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


#############################
# regionReports
#############################
@app.route('/report/region/<regionID>')
def regionreport(regionID):
    if regionID == "north":
        return render_template('pages/regionReports/north.html',
                               header="The North",
                               regionName=regionID,
                               timeutc=timeutc(),
                               userstq="{:,.0f}".format(countuserstq()),
                               statustq=statustq())
    else:
        regionName = getregionName(regionID)
        return render_template('pages/regionReports/regionReport.html',
                           regionID=regionID,
                           regionName=regionName,
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())



#############################
# jumpReports
#############################
@app.route('/report/jump/tradehubs')
def jumpreport_tradehubs():
    return render_template('pages/jumpReports/tradehubs.html',
                           title="Trade Hubs",
                           header="Trade Hubs",
                           nav="Trade Hubs",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


#############################
# marketReports
#############################
@app.route('/report/market/pilotservices/')
def marketreport_pilotservices():
    return render_template('pages/marketReports/pilotservices.html',
                           title="Pilot Services",
                           header="Pilot Services",
                           nav="Pilot Services",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


@app.route('/report/market/item/<typeID>')
def marketreport_item(typeID):
    return render_template('pages/marketReports/item.html',
                           typeID=typeID,
                           typeName=gettypeName(typeID),
                           getprofitpersolarsystem=getprofitpersolarsystem(typeID),
                           getregionalstats=getregionalstats(typeID),
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


@app.route('/report/market/speculation')
def marketreport_speculation():
    return render_template('pages/marketReports/speculation.html',
                           title="Speculation",
                           header="Speculation",
                           nav="Speculation",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq(),
                           market_speculationtotals=market_speculationtotals())


#############################
# moonReports
#############################
@app.route('/report/moon/sov')
def moonreport_sov():
    return render_template('pages/moonReports/sov.html',
                           title="Sovereignty",
                           header="Sovereignty",
                           nav="Sovereignty",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/moon/gases')
def moonreport_gases():
    return render_template('pages/moonReports/gases.html',
                           title="Gasses",
                           header="Gasses",
                           nav="Gasses",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/moon/r8')
def moonreport_r8():
    return render_template('pages/moonReports/r8.html',
                           title="Rarity 8",
                           header="Rarity 8",
                           nav="Rarity 8",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/moon/r16')
def moonreport_r16():
    return render_template('pages/moonReports/r16.html',
                           title="Rarity 16",
                           header="Rarity 16",
                           nav="Rarity 16",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/moon/r32')
def moonreport_r32():
    return render_template('pages/moonReports/r32.html',
                           title="Rarity 32",
                           header="Rarity 32",
                           nav="Rarity 32",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/report/moon/r64')
def moonreport_r64():
    return render_template('pages/moonReports/r64.html',
                           title="Rarity 64",
                           header="Rarity 64",
                           nav="Rarity 64",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


@app.route('/report/moon/item/<typeID>')
def moonreport_item(typeID):
    return render_template('pages/moonReports/item.html',
                           title="Rarity 64",
                           header="Rarity 64",
                           nav="Rarity 64",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq(),
                           typeID=typeID,
                           typeName=gettypeName(typeID))


#############################
# mapReports
#############################
@app.route('/map/sovereignty')
def map_sovereignty():
    return render_template('pages/mapReports/sovereignty.html',
                           title="Sovereignty",
                           header="Sovereignty",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())

@app.route('/map/conquerablestations')
def map_conquerablestations():
    return render_template('pages/mapReports/conquerablestation.html',
                           title="Conquerable Stations",
                           header="Conquerable Stations",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


#############################
# warReports
#############################
@app.route('/report/war/worldwarbee')
def warreport_worldwarbee():
    return render_template('pages/warReports/worldwarbee.html',
                           title="World War Bee",
                           header="World War Bee",
                           timeutc=timeutc(),
                           userstq="{:,.0f}".format(countuserstq()),
                           statustq=statustq())


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
def api_getmarketitems():
    return getmarketitems()

@app.route('/api/characters')
def api_getcharacters():
    return getcharacters()

@app.route('/api/zkillboarditems')
def api_getzkillboarditems():
    return getzkillboarditems()


# Wallet
@app.route('/api/wallet/transactions')
def api_getallwallettransactions():
    return getallwallettransactions()

@app.route('/api/wallet/typeid/<typeID>/<transactionType>')
def api_getwallet_typeid(typeID, transactionType):
    return getwallet_typeid(typeID, transactionType)


# Sovereignty
@app.route('/api/sov/events')
def api_getsovevents():
    return getsovevents()


# Simple Lookups
@app.route('/api/regionName/<regionID>')
def api_regionID(regionID):
    return getregionName(regionID)

# Market
@app.route('/api/typeName/<typeID>')
def api_typeID(typeID):
    return getmarkethistory_typeID(typeID)

@app.route('/api/market/avgprice/<typeID>')
def api_marketavgprice(typeID):
    return getmarkethistory_avgprice(typeID)

@app.route('/api/market/regional/<typeID>/hubs/<hubTypes>')
def api_market_getregionalprices(typeID, hubTypes):
    if hubTypes == "major":
        return market_getregionalprices(typeID, tradeHubsmajor)

# Region
@app.route('/api/region/sovereignty/<regionID>')
def api_regionsovereignty(regionID):
    return getsovbyregion(regionID)

@app.route('/api/gettoprattingbyregion/<regionID>')
def api_gettoprattingbyregion(regionID):
    df = gettoprattingbyregion(regionID)
    return df.reset_index().to_json(orient='records')

@app.route('/api/killmails/region/<regionID>')
def api_getkillmailsbyregion(regionID):
    return getkillmailsbyregion(regionID)

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

@app.route('/api/moonminerals/region/pie/<typeID>')
def api_moon_regionsummarypie(typeID):
    return moon_regionsummarypie(typeID)

@app.route('/api/moonminerals/alliance/')
def api_moonmineralsbyallalliance():
    return getmoonmineralsbysov()

@app.route('/api/moonminerals/region/<typeID>')
def api_moon_regionsummary(typeID):
    return moon_regionsummary(typeID)

# Index
@app.route('/api/report/index/deadend/<gateCountLimit>')
def api_getdeadendsystems(gateCountLimit):
    return getdeadendsystems(gateCountLimit)

@app.route('/api/report/index/sovchanges')
def indexreport_sovchanges():
    return getsoveventsumbyday()

@app.route('/api/report/index/typeids/<typenames>')
def indexreport_indexitems(typenames):
    if typenames == "battleship":
        return getindextypeids((17918, 17740, 17736, 17738, 17920), 30000000000)
    if typenames == "cruiser":
        return getindextypeids((17720, 17922, 17715, 17718, 17722), 30000000000)
    if typenames == "frigate":
        return getindextypeids((17932, 17926, 17930, 17924, 17928), 30000000000)
    if typenames == "sisters":
        return getindextypeids((33468, 33470, 33472), 30000000000)
    if typenames == "mordu":
        return getindextypeids((33816, 33818, 33820), 30000000000)
    if typenames == "antipharmakon":
        return getindextypeids((36908, 36909, 36910, 36911, 36912), 30000)
    if typenames == "quafezero":
        return getindextypeids((3898,), 100000000000)
    if typenames == "plex":
        return getindextypeids((29668,), 50000000000000)
    if typenames == "carriers":
        return getindextypeids((23757, 23915, 23911, 22852), 100000000)
    if typenames == "faux":
        return getindextypeids((23757, 23915, 23911, 22852), 100000000)
        #return getindextypeids((37604, 37605, 37606, 37607), 30000000000)  # Placeholder
    if typenames == "dreadnoughts":
        return getindextypeids((19720, 19726, 19724, 19722), 300000000)
    if typenames == "freighters":
        return getindextypeids((20183, 20189, 20187, 20183, ), 5000000000)
    if typenames == "jumpfreighters":
        return getindextypeids(jumpFreighters, 5000000000)
    if typenames == "ore":
        return getindextypeids((34328, 28606), 300000000)

@app.route('/api/report/index/goldenroute/<typenames>')
def api_goldenroute(typenames):
    if typenames == "freighters":
        return getkillmails_typeid_solarsystem(freighters, golden_route)
    if typenames == "jumpfreighters":
        return getkillmails_typeid_solarsystem(jumpFreighters, golden_route)
    if typenames == "allfreighters":
        return getkillmails_typeid_solarsystem(allFreighters, golden_route)
    if typenames == "ore":
        return getkillmails_typeid_solarsystem(oreFreighters, golden_route)

@app.route('/api/npckills/universe')
def api_npckillsuniverse():
    return getnpckills_byuniverse()

@app.route('/api/npckills/security')
def api_npckillssecurity():
    return getnpckills_byallsecurity()

@app.route('/api/npckills/faction/totals/<factionName>')
def api_getnpckills_totalbyregions(factionName):
    if factionName == "all":
        return getnpckills_byallfactions()
    if factionName == "angel":
        df = getnpckills_byregions(regions_angel, "Angel Cartel")
        return df.reset_index().to_json(orient='records',date_format='iso')
    if factionName == "blood":
        df = getnpckills_byregions(regions_blood, "Blood Raiders")
        return df.reset_index().to_json(orient='records',date_format='iso')
    if factionName == "guristas":
        df = getnpckills_byregions(regions_guristas, "Guristas")
        return df.reset_index().to_json(orient='records', date_format='iso')
    if factionName == "sansha":
        df = getnpckills_byregions(regions_sanshas, "Sansha's Nation")
        return df.reset_index().to_json(orient='records', date_format='iso')
    if factionName == "serpentis":
        df = getnpckills_byregions(regions_serpentis, "Serpentis")
        return df.reset_index().to_json(orient='records', date_format='iso')

@app.route('/api/npckills/faction/<factionName>')
def api_getnpckills_byregions(factionName):
    if factionName == "angel":
        return getnpckills_byfaction(regions_angel)
    if factionName == "blood":
        return getnpckills_byfaction(regions_blood)
    if factionName == "guristas":
        return getnpckills_byfaction(regions_guristas)
    if factionName == "sansha":
        return getnpckills_byfaction(regions_sanshas)
    if factionName == "serpentis":
        return getnpckills_byfaction(regions_serpentis)

@app.route('/api/npckills/war/<warName>')
def api_getnpckills_bywar(warName):
    if warName == "worldwarbee":
        return getnpckills_bywar(warName)


# Map
@app.route('/api/map/conquerablestation')
def api_conquerablestations():
    return meta_conquerablestationslist()

@app.route('/api/map/jumps/<solarSystemID>')
def api_mapjumps_solarsystemID(solarSystemID):
    return mapjumps_solarsystemID(solarSystemID)

@app.route('/api/map/jumps/tradehubs')
def api_mapjumps_tradehubs():
    return mapjumps_tradehubs()

@app.route('/api/map/npckills/region/<regionID>')
def api_mapkills_npckillsbyregion(regionID):
    if regionID == "north":
        return getnpckills_byregionsname(regions_north, "The North")
    else:
        return mapkills_npckillsbyregion(regionID)

@app.route('/api/map/shipkills/region/<regionID>')
def api_mapkills_shipkillsbyregion(regionID):
    return mapkills_shipkillsbyregion(regionID)

@app.route('/api/map/podkills/region/<regionID>')
def api_mapkills_podkillsbyregion(regionID):
    return mapkills_podkillsbyregion(regionID)

@app.route('/api/map/jumps/region/<regionID>')
def api_mapkills_jumpsbyregion(regionID):
    if regionID == "north":
        return getjumps_byregionsname(regions_north, "The North")
    else:
        return mapkills_jumpsbyregion(regionID)

@app.route('/api/character/blueprints')
def api_characterblueprints():
    return getcharacterblueprints()

@app.route('/api/character/orders')
def api_characterorders():
    return getcharacterorders()

# System
@app.route('/api/system/size/<element>')
def api_systemdatabasesizes(element):
    if element == "tables":
        return getdbtablesizes()

# Inventory
@app.route('/api/inventory/add/<transactionID>')
def api_market_inventoryadd(transactionID):
    return market_inventoryadd(transactionID)

# Spectulation
@app.route('/api/speculation/add/<transactionID>')
def api_market_speculationadd(transactionID):
    return market_speculationadd(transactionID)

@app.route('/api/market/speculation')
def api_market_speculationpricechange():
    return market_speculationpricechange()

# Force
@app.route('/api/force/region/<regionID>')
def api_force_region(regionID):
    return force_region(regionID)
