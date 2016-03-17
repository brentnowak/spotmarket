0.4 Release
==================

**Completed**  
[bug] Change timestamp for zkillboard and markethistory consumer to use UTC for mental sanity   
[enhancement] Add 404 error page  
[enhancement] Change to postgres 9.5.1 to support jsonb  
[enhancement] Parameterize graph functions  
[enhancement] Change date format in graphs to ISO for mental sanity  
[enhancement] Standardize table formatting  
[enhancement] Supervisor to make Flask web service persistent  
[enhancement] Add jsonb index on data.killmails for typeID and solarSystemID
[enhancement] Add paging to zKillboard consumer
[enhancement] Add check to resume from last recorded page for zKillboard consumer  
[enhancement] Add basic exception handling to zKillboard consumer  
[new] Creation of ship index report  

0.5 Release
==================

**Completed**  

**To Do**  
[bug] bootstrap-table table headers that contain icons do not align correctly with rows  
[bug] Security reports have hardcoded time range for data that calculates ratting rate    
[new] Create freighter security index  
[new] Work on indexes, add item destruction based on killmails  
[new] Create process to fill in killmails that lack JSON data or zKb values  
[enhancement] Add second axis to d3js charts to denote Eve expansions  
[enhancement] Personalize 404 error page  
[enhancement] Add functional buttons on Settings page to control import status  
[enhancement] Change factionReports to be driven by JSON  
[enhancement] Learn how to use Classes and clean up utility scripts 
[enhancement] Add favicon  

0.6 Release
==================

**To Do**  
[enhancement] Create Docker image  
[enhancement] Research replacing cron jobs with a better solution  
