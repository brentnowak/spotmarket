0.6 Release
==================

- [ ] [bug] On most graphs, label for line appears to the left  
- [X] [bug] bootstrap-table table headers that contain icons do not align correctly with rows  
- [ ] [bug] Security reports have hardcoded time range for data that calculates ratting rate  
- [ ] [new] Create freighter security index based on killmails  
- [ ] [new] Character Orders table and page  
- [ ] [enhancement] Add functional buttons on Settings page to control imports  
- [ ] [enhancement] Learn how to use Classes and clean up utility scripts  
- [ ] [enhancement] Add second axis to d3js charts to denote Eve expansions  
- [ ] [enhancement] Add website favicon  
- [ ] [enhancement] Move API items to _api.py  

0.7 Release
==================
  
- [ ] [enhancement] Display tags rather than numbers for severity on log pages  
- [ ] [enhancement] Research replacing cron jobs with a better solution  
- [ ] [enhancement] Organize API endpoints into a more logical pattern  
- [ ] [enhancement] PostgreSQL 9.5.1 performance tuning  

0.8 Release
==================

- [ ] [enhancement] Create Docker image  

0.4 Release (Completed)
==================
  
- [x] [new] Creation of ship index report  
- [x] [bug] Change timestamp for zkillboard and markethistory consumer to use UTC for mental sanity   
- [x] [enhancement] Add 404 error page  
- [x] [enhancement] Change to postgres 9.5.1 to support jsonb  
- [x] [enhancement] Parameterize graph functions  
- [x] [enhancement] Change date format in graphs to ISO for mental sanity  
- [x] [enhancement] Standardize table formatting  
- [x] [enhancement] Supervisor to make Flask web service persistent  
- [x] [enhancement] Add jsonb index on data.killmails for typeID and solarSystemID
- [x] [enhancement] Add paging to zKillboard consumer
- [x] [enhancement] Add check to resume from last recorded page for zKillboard consumer  
- [x] [enhancement] Add basic exception handling to zKillboard consumer  

0.5 Release (Completed)
==================

- [x] [new] Character Blueprints table and page  
- [x] [new] Character Journal table and page  
- [x] [new] Character Wallet table and page  
- [x] [new] Work on data.killmails indexes to improve performance  
- [x] [new] Create process to fill in killmails that lack JSON data or zKb values    
- [x] [enhancement] Change graphs to exclude last 24 hours as it causes graphs to improperly trend  
- [x] [enhancement] Personalize 404 error page  
- [x] [enhancement] Change factionReport charts to be driven by JSON  
