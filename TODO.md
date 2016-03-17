0.4 Release
==================

Completed
[enhancement] Add 404 error page 
[enhancement] Change to postgres 9.5.1 to support jsonb
[enhancement] Parameterize graph functions
[enhancement] Change date format in graphs to ISO for mental sanity
[enhancement] Standardize table formatting
[enhancement] Supervisor to make Flask web service persistent
[new] Creation of ship index report

To Do
[enhancement] Add paging to zKillboard consumer
[enhancement] Add jsonb index on data.killmails for:
    killmails."killData"->'victim'->'shipType'->'id'
    solarSystemID

0.5 Release
==================

To Do
[new] Create freighter security index
[new] Create process to fill in killmails that lack JSON data or zKb values
[enhancement] Personalize add 404 error page 
[enhancement] Add functional buttons on Settings page to control import status
[enhancement] Change factionReports to be driven by JSON
[enhancement] Learn how to use Classes and clean up utility scripts

0.6 Release
==================

To Do
[enhancement] Create Docker image
 