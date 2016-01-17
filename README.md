spotmarket - EVE Online Market Evaluator
==================

[https://github.com/brentnowak/spotmarket](https://github.com/brentnowak/spotmarket)

Packages Used:
* evelink 0.7.3 (https://github.com/eve-val/evelink)


Recommended Platform
==================
* OS ubuntu-14.04.3-server-amd64
* Database PostgreSQL 9.3


Install Notes
==================

# Debian

**Dependencies**
```shell 
apt-get install postgresql postgresql-contrib  
apt-get build-dep python-psycopg2
pip install ConfigParser  
pip install psycopg2  
pip install arrow
```

**Install**
```shell
git clone https://github.com/brentnowak/spotmarket
chmod +x runjobs.sh
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

**Test database connection**

```shell
psql -d spotmarket -U spotmarketadmin -W
```

**Database creation**

Create database, tables, and indexes with the scripts located under \sql.  
You can connect to the database using the command listed above and create the tables or use a GUI tool such as pgAdmin.  

**Modify config.ini with database details**
```shell
vim config.ini.change
mv config.ini.change change.ini
```

**crontab**
```shell 
crontab -e
0,30 * * * * ubuntu /home/ubuntu/spotmarket/runjobs.sh > /dev/null 2>&1
```

License Info
==================

Leverages public data sources and remains open source to comply with EULAs from [CCP](https://developers.eveonline.com/resource/license-agreement) and [eve-kill/zkillboard](https://beta.eve-kill.net/information/legal/)

EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. CCP hf. has granted permission to EVSCO to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, EVSCO. CCP is in no way responsible for the content on or functioning of this website, nor can it be liable for any damage arising from the use of this website.