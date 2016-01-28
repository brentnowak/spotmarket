#-----------------------------------------------------------------------------
# consumer_markethistory.py - EVE Online CREST API consumer
# Brent Nowak <brent613@gmail.com>
#-----------------------------------------------------------------------------
# Version: 0.1
# - Initial release
#-----------------------------------------------------------------------------

from _utility import *


def main():

    # The Forge
    regionIDs = ['10000002']

    # marketGroupID = 1380
    # Pirate BS
    typeIDs = ['17736', '17738', '17740', '17918', '17920', '33472', '33820', '34151']

    # marketGroupID = 1371
    # Pirate Cruisers
    typeIDs = ['17715', '17718', '17720', '17722', '17922', '33470', '33818']
    getmarkethistory(regionIDs, typeIDs)

    # marketGroupID = 1365
    # Pirate Frigates
    typeIDs = ['17924', '17926', '17928', '17930', '17932', '33468', '33816']
    getmarkethistory(regionIDs, typeIDs)

    # To work on
    #18 	Mineral
    #423    Ice Product
    #427	Moon Materials
    #745	Cyber Learning
    #1136	Fuel Block
    #300	Cyberimplant
    #1042	Basic Commodities
    #1034	Refined Commodities
    #1040	Specialized Commidites
    #1041	Advanced Commodities


if __name__ == "__main__":
    main()