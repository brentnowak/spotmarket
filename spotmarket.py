#-----------------------------------------------------------------------------
# spotmarket.py - EVE Online Market Evaluator
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------


from _utility import *

#
# Resampling Options
#
value_window = 3
value_min_periods = 1

def main():
    # Universe
    df = getnpckills_byuniverse()
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_universe.csv', index=True, sep='\t', columns=['SUM_factionKills'])

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
    regions = ['10000015', '10000055', '10000045', '10000035', '10000023', '10000029', '10000003', '10000010']
    df = getnpckills_byregions(regions)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_regions_guristas_pirate.csv', index=True, sep='\t', columns=list(df))
    df['sum'] = df.sum(axis=1)
    df.to_csv('npckills_regions_guristas_pirates_sum.csv', index=True, sep='\t', columns=['sum'])

    # Sansha's Nation
    # Stain, Paragon Soul, Esoteria, Catch, Providence
    # Stain         10000022
    # Paragon Soul  10000059
    # Esoteria      10000039
    # Catch         10000014
    # Providence    10000047
    regions = ['10000022', '10000059', '10000039', '10000014', '10000047']
    df = getnpckills_byregions(regions)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_regions_sanshas_nation.csv', index=True, sep='\t', columns=list(df))
    df['sum'] = df.sum(axis=1)
    df.to_csv('npckills_regions_sanshas_nation_sum.csv', index=True, sep='\t', columns=['sum'])


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
    regions = ['10000031', '10000056', '10000062', '10000061', '10000025', '10000012', '10000008', '10000006', '10000005', '10000009', '10000011', '10000014']
    df = getnpckills_byregions(regions)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_regions_angel_cartel.csv', index=True, sep='\t', columns=list(df))
    df['sum'] = df.sum(axis=1)
    df.to_csv('npckills_regions_angel_cartel_sum.csv', index=True, sep='\t', columns=['sum'])


    # Blood Raiders
    # Delve, Querious, Period Basis
    # Delve         10000060
    # Querious      10000050
    # Period Basis  10000063
    regions = ['10000060', '10000050', '10000063']
    df = getnpckills_byregions(regions)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_regions_blood_raiders.csv', index=True, sep='\t', columns=list(df))
    df['sum'] = df.sum(axis=1)
    df.to_csv('npckills_regions_blood_raiders_sum.csv', index=True, sep='\t', columns=['sum'])


    # Serpentis Corporation
    # Fade, Outer Ring, Cloud Ring, Syndicate, Fountain
    # Fade          10000046
    # Outer Ring    10000057
    # Cloud Ring    10000051
    # Syndicate     10000041
    # Fountain      10000058
    regions = ['10000046', '10000057', '10000051', '10000041', '10000058']
    df = getnpckills_byregions(regions)
    df = df.pivot(index='timestamp', columns='regionName', values='SUM_factionKills')
    df = pd.rolling_mean(df.resample("6H", fill_method='bfill'), window=value_window, min_periods=value_min_periods)
    df.to_csv('npckills_regions_serpentis_corporation.csv', index=True, sep='\t', columns=list(df))
    df['sum'] = df.sum(axis=1)
    df.to_csv('npckills_regions_serpentis_corporation_sum.csv', index=True, sep='\t', columns=['sum'])


if __name__ == "__main__":
    main()


