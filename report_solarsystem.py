#-----------------------------------------------------------------------------
# report_npckills.py - EVE Online Market Evaluator
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
# Version: 0.2
# - Added NPC charting
#-----------------------------------------------------------------------------

import time
from _utility import *

#
# Resampling Options
#
conversion = "4H"
v_window = 8
v_minperiods = 1


def main():
    # Track runtime
    start_time = time.time()

    df = getsolarsystemmapkills("30004468")
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('static/data/30004468_mapkills.csv', index=True, sep='\t', columns=list(df))

    df = getsolarsystemmapjumps("30004468")
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('static/data/30004468_mapjumps.csv', index=True, sep='\t', columns=list(df))

    df = getsolarsystemmapkills("30000182")
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('static/data/30000182_mapkills.csv', index=True, sep='\t', columns=list(df))

    df = getsolarsystemmapjumps("30000182")
    df = pd.rolling_mean(df.resample(conversion, fill_method='bfill'), window=v_window, min_periods=v_minperiods)
    df.to_csv('static/data/30000182_mapjumps.csv', index=True, sep='\t', columns=list(df))

    print("Runtime: %s seconds" % round((time.time() - start_time),2))

if __name__ == "__main__":
    main()
