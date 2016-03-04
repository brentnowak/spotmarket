#-----------------------------------------------------------------------------
# report_market.py
# https://github.com/brentnowak/spotmarket
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *
from _globals import *

def main():
    # Track runtime
    start_time = time.time()

    headvalue = 90

    # Machariel, Cynabal, Dramiel
    typeIDs = ['17738', '17720', '17932']

    df = pd.DataFrame()
    df = getmarkethistory_typeid(17738)
    df = df.head(headvalue)
    df = df.pivot(index='timestamp', columns='typeName', values='avgPrice')
    dfkills = getfactionkills_byfaction()
    dfkills = dfkills.resample(rule='24H', how='sum')
    dfkills = dfkills.combine_first(df)
    dfkills = dfkills.dropna()

    print(dfkills)

    #for typeID in typeIDs:
    #    dftmp = getmarkethistory_typeid(typeID)
    #    dftmp = dftmp.head(90)
    #    dftmp = dftmp.pivot(index='timestamp', columns='typeName', values='avgPrice')
    #    df = df.combine_first(dftmp)
    #df['mean'] = df.mean(axis=1)
    #df.to_csv('static/data/market_faction_angel.csv', index=True, sep='\t', columns=list(df))
    #print(dffaction)
    #dffaction.to_csv('static/data/market_faction_angel_kills.csv', index=True, sep='\t', columns=['SUM_factionKills', 'mean'])
    #print(dffaction)




    print("Runtime: %s seconds" % round((time.time() - start_time),2))

if __name__ == "__main__":
    main()