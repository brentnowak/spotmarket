#-----------------------------------------------------------------------------
# report_npckills.py - EVE Online Market Evaluator
# https://github.com/brentnowak/spotmarket
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.2
# - Added NPC charting
# Version: 0.3
# - Resampling
# - CSV, HTML outputs from dataframes
#-----------------------------------------------------------------------------

import time
from _utility import *
from _globals import *

#
# Resampling Options
#

def main():
    # Track runtime
    start_time = time.time()

    #
    df_faction = pd.DataFrame()

    # Universe
    df = getnpckills_byallsecurity()
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_universe.csv', index=True, sep='\t', columns=['high', 'low', 'null'])

    # Guristas Pirates
    # Tenal, Branch, Venal, Deklein, Pure Blind, Geminate, Vale of the Silent, Tribute
    # Tenal         10000015
    # Branch        10000055
    # Venal         10000045
    # Deklein       10000035
    # Pure Blind    10000023
    # Geminate      10000029
    # Vale of the Silent 10000003
    # Tribute       10000010
    df = getnpckills_byregions(regions_guristas)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_regions_guristas_pirate.csv', index=True, sep='\t', columns=list(df))
    df['total'] = df.sum(axis=1)
    df_faction['Guristas Pirates'] = df['total']
    df.to_csv('app/data/npckills_regions_guristas_pirates_sum.csv', index=True, sep='\t', columns=['total'])

    # Sansha's Nation
    # Stain, Paragon Soul, Esoteria, Catch, Providence
    # Stain         10000022
    # Paragon Soul  10000059
    # Esoteria      10000039
    # Catch         10000014
    # Providence    10000047
    df = getnpckills_byregions(regions_sanshas)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_regions_sanshas_nation.csv', index=True, sep='\t', columns=list(df))
    df['total'] = df.sum(axis=1)
    df_faction["Sansha's Nation"] = df['total']
    #df_faction['sansha'] = df_faction.combine_first(df['total'])
    df.to_csv('app/data/npckills_regions_sanshas_nation_sum.csv', index=True, sep='\t', columns=['total'])


    # Angel Cartel
    # Impass, Feythabolis, Omist, Tenerifis, Immensea, Curse, Scalding Pass, Wicked Creek, Detorid, Insmother, Great Wildlands, Cache
    # Impass        10000031
    # Feythabolis   10000056
    # Omist         10000062
    # Tenerifis     10000061
    # Immensea      10000025
    # Curse         10000012
    # Scalding Pass 10000008
    # Wicked Creek  10000006
    # Detorid       10000005
    # Insmother     10000009
    # Great Wildlands   10000011
    # Cache         10000014
    df = getnpckills_byregions(regions_angel)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_regions_angel_cartel.csv', index=True, sep='\t', columns=list(df))
    df['total'] = df.sum(axis=1)
    df_faction['Angel Cartel'] = df['total']
    df.to_csv('app/data/npckills_regions_angel_cartel_sum.csv', index=True, sep='\t', columns=['total'])


    # Blood Raiders
    # Delve, Querious, Period Basis
    # Delve         10000060
    # Querious      10000050
    # Period Basis  10000063
    df = getnpckills_byregions(regions_blood)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_regions_blood_raiders.csv', index=True, sep='\t', columns=list(df))
    df['total'] = df.sum(axis=1)
    df_faction['Blood Raiders'] = df['total']
    df.to_csv('app/data/npckills_regions_blood_raiders_sum.csv', index=True, sep='\t', columns=['total'])


    # Serpentis Corporation
    # Fade, Outer Ring, Cloud Ring, Syndicate, Fountain
    # Fade          10000046
    # Outer Ring    10000057
    # Cloud Ring    10000051
    # Syndicate     10000041
    # Fountain      10000058
    df = getnpckills_byregions(regions_serpentis)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('app/data/npckills_regions_serpentis_corporation.csv', index=True, sep='\t', columns=list(df))
    df['total'] = df.sum(axis=1)
    df_faction['Serpentis Corporation'] = df['total']
    df.to_csv('app/data/npckills_regions_serpentis_corporation_sum.csv', index=True, sep='\t', columns=['total'])


    # NPC Kill totals by Faction
    df_faction.to_csv('app/data/npckills_factions.csv', index=True, sep='\t')


    # Top Nullsec Ratting Regions
    df = gettoprattingregions_nullsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingregions_nullsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingregions_nullsec.html")


    # Top Nullsec Ratting Systems
    df = gettoprattingsystems_nullsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingsystems_nullsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['solarSystemName', 'security', 'regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingsystems_nullsec.html")

    # Top Lowsec Ratting Regions
    df = gettoprattingregions_lowsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingregions_lowsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingregions_lowsec.html")


    # Top Lowsec Ratting Systems
    df = gettoprattingsystems_lowsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingsystems_lowsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['solarSystemName', 'security', 'regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingsystems_lowsec.html")


    # Top Highsec Ratting Regions
    df = gettoprattingregions_highsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingregions_highsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingregions_highsec.html")


    # Top Highsec Ratting Systems
    df = gettoprattingsystems_highsec()
    df = df.head(20)
    df = addkillsperday(df)
    df.to_html('app/data/npckills_toprattingsystems_highsec.html', header=True, index=True, float_format=lambda x: '%10.2f' % x,classes='table table-striped', columns=['solarSystemName', 'security', 'regionName', 'SUM_factionKills', 'killsPerDay'])
    cleartableborder("app/data/npckills_toprattingsystems_highsec.html")

    # Track Runtime
    print("Runtime: %s seconds" % round((time.time() - start_time),2))

if __name__ == "__main__":
    main()


