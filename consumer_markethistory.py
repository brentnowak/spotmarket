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

    # Angel Ships
    typeIDs = ['17738', '17720', '17932']

    # marketGroupID = 1380
    # Pirate BS
    #typeIDs = ['17736', '17738', '17740', '17918']
    #typeIDs = ['17920', '33472', '33820', '34151']

    # marketGroupID = 1371
    # Pirate Cruisers
    #typeIDs = ['17715', '17718', '17720']
    #typeIDs = ['17722', '17922', '33470', '33818']

    # marketGroupID = 1365
    # Pirate Frigates
    #typeIDs = ['17924', '17926', '17928', '17930']
    #typeIDs = ['17932', '33468', '33816']

    # marketGroupID = 1857
    # Minerals
    #typeIDs = ['34', '35', '36', '36', '38', '39', '40', '11399']

    # marketGroupID = 1334, 1033
    # Ice Products
    #typeIDs = ['3645', '3683', '16272', '16273', '16274', '16275', '17887', '17888', '17889']

    # marketGroupID = 501
    # Moon Materials
    #typeIDs = ['16633', '16634', '16635', '16636', '16637', '16638']
    #typeIDs = ['16639', '16640', '16641', '16642', '16643', '16644']
    #typeIDs = ['16646', '16647', '16648', '16649', '16650', '16651']
    #typeIDs = ['16652', '16653']

    # marketGroupID = 1870
    # Fuel Block
    #typeIDs = ['4051', '4246', '4247', '4312']

    # groupID = 898
    # Black Ops
    #typeIDs = ['22428', '22436', '22430', '22440']

    # groupID = 1202
    # Blockade Runner
    #typeIDs = ['12729', '12733', '12735', '12743']

    #745	Cyber Learning
    #300	Cyberimplant
    #1042	Basic Commodities
    #1034	Refined Commodities
    #1040	Specialized Commidites
    #1041	Advanced Commodities

    # Special Interest
    # Small EMP Smartbomb II
    #typeIDs = ['1565']

    getmarkethistory(regionIDs, typeIDs)


if __name__ == "__main__":
    main()