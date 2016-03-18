0.5 Release
==================

- [ ] [new] Create freighter security index based on killmails  
- [ ] [new] Work on indexes, add item destruction based on killmails  
- [ ] [new] Create process to fill in killmails that lack JSON data or zKb values  

- [ ] [bug] bootstrap-table table headers that contain icons do not align correctly with rows  
- [ ] [bug] Security reports have hardcoded time range for data that calculates ratting rate  

- [ ] [enhancement] Add second axis to d3js charts to denote Eve expansions  
- [ ] [enhancement] Personalize 404 error page  
- [ ] [enhancement] Add functional buttons on Settings page to control imports  
- [ ] [enhancement] Change factionReport charts to be driven by JSON  
- [ ] [enhancement] Learn how to use Classes and clean up utility scripts 
- [ ] [enhancement] Add website favicon  

0.6 Release
==================
  
- [ ] [enhancement] Create Docker image  
- [ ] [enhancement] Research replacing cron jobs with a better solution  

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
