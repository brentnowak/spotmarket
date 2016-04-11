spotmarket - EVE Online Market Evaluator
==================

[https://github.com/brentnowak/spotmarket](https://github.com/brentnowak/spotmarket)

Development Blog [http://k162space.com/](http://k162space.com/) 

There are many projects out there that record historical data from the API and present it to you. 

We want to go a step further and build an analysis platform that can incorporate data from the API and use it to create relationships to fuel predictions.
 
This project is an attempt to aggregate various data sources and present them in a meaningful way in order to make decision about trading, potential targets, and to verify activity levels of different types of gameplay. 

Sample Images
==================

![Dashboard](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-02-16_dashboard.png)

![NPC Reports](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-01_npc1.png)

![Moon Reports](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-01_nullsec_1.png)

![Jump Reports](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-01_tradehubs_1.png)

![Moon Ownership](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-01_moons_1.png)

![Moon Details](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-01_moons_2.png)

![System Logs](https://github.com/brentnowak/spotmarket/blob/master/sampleImages/2016-03-03_logs_1.png)

Tested Platform
==================
* OS: ubuntu-14.04.3-server-amd64
* Database: PostgreSQL 9.5

External Packages
==================
* evelink 0.7.3 (https://github.com/eve-val/evelink)
* PyCrest (https://github.com/Dreae/PyCrest)
``

Stack
==================
* Web Server: Flask [http://flask.pocoo.org/](http://flask.pocoo.org/)
* Charting: D3.js [https://d3js.org/](https://d3js.org/)
* Statistics and Resampling: pandas [http://pandas.pydata.org/](http://pandas.pydata.org/)  
* Python 2.7
* Database: PostgreSQL

Services
==================

**consumer_alliance.py**

Input: XML API.  
Output: Populate 'meta.alliances' table with list of current Alliances.  

**consumer_conquerablestation.py**

Input: XML API.  
Output: Populate 'data.conquerablestations' with list of Conquerable Stations.    

**consumer_map.py**

Input: XML API.  
Output: Populate 'data.mapjumps', 'data.mapkills', and 'data.mapsov' with statistics.     

**consumer_markethistory.py**

Input: CREST API, list of typeIDs from 'data.marketitems' table.  
Output: Populate 'market.history' table with market data.  

**consumer_siphon.py**

Input: zKillboard API, CREST API  
Output: Populate 'data.moonverify' table with a list of CREST verified moons.    
Notes: Replace 'user-agent' value with your own custom string.  

**consumer_wallet.py *work in progress***

Input: XML API.  
Output: Populate 'data.wallet' table with a list of transactions per character.    

**consumer_zkillboard.py**

Input: zKillboard API, CREST API  
Output: Populate 'data.killmails' table with CREST killmails and value from zKillboard.    


Processes
==================

**process_updatemoons.py**

Output: Populate 'data.moonminerals' with CREST verified moons from 'data.moonverify' table.  

**process_validatekillmails.py**

Output: Check that each item in kill.mail has valid JSON and value from zKillboard.


Install Notes
==================

**PostgreSQL 9.5**

As root
```shell
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
apt-get update
apt-get install postgresql postgresql-contrib
```

**Dependencies**

As root
```shell 
apt-get build-dep python-psycopg2
apt-get install python-pip
apt-get install supervisor
apt-get install git
```

**Clone GitHub Project**
Clone in /home/ubuntu due to some hardcoded paths.
```shell
git clone https://github.com/brentnowak/spotmarket
cd spotmarket
sudo pip install -r requirements.txt
```

**Make Scripts Executable**
```shell
cd spotmarket
cd scripts/
chmod +x *
```

**PostgreSQL**
```shell
sudo su - postgres
psql
CREATE DATABASE spotmarket;
CREATE USER spotmarketadmin WITH PASSWORD 'changeme';
GRANT ALL PRIVILEGES ON DATABASE spotmarket TO spotmarketadmin;
\q
```

**Local and IPv4 Access to PostgreSQL**

As root
```shell
vim /etc/postgresql/9.5/main/pg_hba.conf
```
Change line 85 and 90 from 'peer' to 'md5'.
Under 'IPv4 local connections' add a line for your local network if you wish to connect to your database instance over your network.

As root
```shell
vim /etc/postgresql/9.5/main/postgresql.conf
```
Uncomment line 59 and change the 'listen_address' value to '*'

As root
```shell
service postgresql restart
```

**Test Database Connection**

```shell
psql -d spotmarket -U spotmarketadmin -W
\q
```

**Database Creation**
If you have setup the server instance correctly, you should be presented with a prompt that indicates you are connected.
```shell
psql (9.5.1)
Type "help" for help.

spotmarket=>
```
Create the schema by pasting in schema.sql located under *\sql* directory.  
You can connect to the database using the command listed above and create the tables or use a GUI tool such as pgAdmin.  

**Import Eve Static Data**

```shell
wget https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2
bzip2 -d postgres-latest.dmp.bz2
pg_restore -h localhost -p 5432 -U spotmarketadmin -d spotmarket -v "postgres-latest.dmp"
rm postgres-latest.dmp
```

**Modify config.ini with Database Details**
```shell
vim config.ini.change
mv config.ini.change config.ini
```

**Supervisor**

As root
```shell
cp supervisor/*.conf /etc/supervisor/conf.d/
service supervisor restart```

Reload conf files, as root
```shell
supervisorctl reread
supervisorctl update
```

Confirming supervisor and database settings are correct.
```shell
tail -f /var/log/spotmarket.error.log
```

If you see the following text displayed, then it is working.
```shell
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
 * Restarting with stat
```

Web Front End
==================
Browse to http://hostname


Tracking Tables - Work in Progress
==================
Currently the following tables have to be manually populated:
* kill.tracking - typeIDs that are used for zKillboard imports.
* market.tracking - typeIDs that are used for market prices.
* market.region - regionIDs that are used for market prices.


License Info
==================

Leverages public data sources and remains open source to comply with EULAs from [CCP](https://developers.eveonline.com/resource/license-agreement) and [eve-kill/zkillboard](https://beta.eve-kill.net/information/legal/)

EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. CCP hf. has granted permission to EVSCO to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, EVSCO. CCP is in no way responsible for the content on or functioning of this website, nor can it be liable for any damage arising from the use of this website.


MIT License
==================

Copyright © 2016 Brent Nowak

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
