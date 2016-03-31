--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.0

-- Started on 2016-03-30 19:39:29

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 17000)
-- Name: data; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA data;


ALTER SCHEMA data OWNER TO spotmarketadmin;

SET search_path = data, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 275 (class 1259 OID 17003)
-- Name: alliances; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE alliances (
    "allianceID" integer NOT NULL,
    ticker text NOT NULL,
    name text NOT NULL
);


ALTER TABLE alliances OWNER TO spotmarketadmin;

--
-- TOC entry 303 (class 1259 OID 653601)
-- Name: characters; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE characters (
    "walletID" integer NOT NULL,
    "characterID" integer NOT NULL,
    "characterName" character varying(255) NOT NULL,
    "keyID" integer NOT NULL,
    "vCode" character varying(255) NOT NULL,
    "enableWallet" integer NOT NULL,
    "enableJournal" integer NOT NULL,
    "enableOrders" integer NOT NULL,
    "enableBlueprints" integer NOT NULL,
    "displayWallet" integer NOT NULL,
    "displayOrders" integer NOT NULL,
    "displayBlueprints" integer NOT NULL,
    "corpKey" integer NOT NULL
);


ALTER TABLE characters OWNER TO spotmarketadmin;

--
-- TOC entry 308 (class 1259 OID 653626)
-- Name: charbalances; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE charbalances (
    "balanceID" integer NOT NULL,
    "characterID" integer NOT NULL,
    balance real NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE charbalances OWNER TO spotmarketadmin;

--
-- TOC entry 307 (class 1259 OID 653624)
-- Name: charbalances_balanceID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "charbalances_balanceID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "charbalances_balanceID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2652 (class 0 OID 0)
-- Dependencies: 307
-- Name: charbalances_balanceID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "charbalances_balanceID_seq" OWNED BY charbalances."balanceID";


--
-- TOC entry 304 (class 1259 OID 653609)
-- Name: charblueprints; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE charblueprints (
    "characterID" integer NOT NULL,
    "itemID" bigint NOT NULL,
    "locationID" bigint NOT NULL,
    "typeID" integer NOT NULL,
    quantity bigint NOT NULL,
    "flagID" bigint NOT NULL,
    timeefficiency integer NOT NULL,
    materialefficiency integer NOT NULL,
    runs bigint NOT NULL
);


ALTER TABLE charblueprints OWNER TO spotmarketadmin;

--
-- TOC entry 305 (class 1259 OID 653614)
-- Name: charorders; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE charorders (
    "characterID" integer NOT NULL,
    "orderID" bigint NOT NULL,
    "stationID" bigint NOT NULL,
    volentered integer NOT NULL,
    volremaining integer NOT NULL,
    minvolume integer NOT NULL,
    orderstate integer NOT NULL,
    "typeID" integer NOT NULL,
    range integer NOT NULL,
    accountkey integer NOT NULL,
    duration integer NOT NULL,
    escrow double precision NOT NULL,
    price double precision NOT NULL,
    bid boolean NOT NULL,
    issued timestamp without time zone NOT NULL
);


ALTER TABLE charorders OWNER TO spotmarketadmin;

--
-- TOC entry 306 (class 1259 OID 653619)
-- Name: charskillqueues; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE charskillqueues (
    "characterID" integer NOT NULL,
    endtime timestamp without time zone NOT NULL,
    level integer NOT NULL,
    "typeID" integer NOT NULL,
    starttime timestamp without time zone NOT NULL,
    endsp integer NOT NULL,
    startsp integer NOT NULL,
    queueposition integer NOT NULL
);


ALTER TABLE charskillqueues OWNER TO spotmarketadmin;

--
-- TOC entry 276 (class 1259 OID 17015)
-- Name: conquerablestations; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE conquerablestations (
    "solarSystemID" integer NOT NULL,
    "stationID" integer NOT NULL,
    x double precision NOT NULL,
    y double precision NOT NULL,
    z double precision NOT NULL,
    name text NOT NULL
);


ALTER TABLE conquerablestations OWNER TO spotmarketadmin;

--
-- TOC entry 277 (class 1259 OID 17021)
-- Name: killmails; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE killmails (
    "killmailID" integer NOT NULL,
    "killID" integer NOT NULL,
    "killHash" text NOT NULL,
    "killData" jsonb,
    "totalValue" real
);


ALTER TABLE killmails OWNER TO spotmarketadmin;

--
-- TOC entry 278 (class 1259 OID 17027)
-- Name: killmails_killmailID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "killmails_killmailID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "killmails_killmailID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2653 (class 0 OID 0)
-- Dependencies: 278
-- Name: killmails_killmailID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmails_killmailID_seq" OWNED BY killmails."killmailID";


--
-- TOC entry 279 (class 1259 OID 17029)
-- Name: killmailsitems; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE killmailsitems (
    "killmailsitemsID" integer NOT NULL,
    "typeID" integer NOT NULL,
    enabled integer NOT NULL,
    "importResult" integer,
    "importTimestamp" timestamp without time zone,
    "lastPage" integer
);


ALTER TABLE killmailsitems OWNER TO spotmarketadmin;

--
-- TOC entry 280 (class 1259 OID 17032)
-- Name: killmailsitems_killmailsitemsID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "killmailsitems_killmailsitemsID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "killmailsitems_killmailsitemsID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2654 (class 0 OID 0)
-- Dependencies: 280
-- Name: killmailsitems_killmailsitemsID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmailsitems_killmailsitemsID_seq" OWNED BY killmailsitems."killmailsitemsID";


--
-- TOC entry 310 (class 1259 OID 763016)
-- Name: killmailssum; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE killmailssum (
    "killmailssumID" integer NOT NULL,
    "killID" integer NOT NULL,
    "characterID" integer NOT NULL,
    "corporationID" integer,
    "typeID" integer NOT NULL,
    "attackerCount" integer NOT NULL,
    "damageTaken" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "solarSystemID" integer NOT NULL,
    x double precision,
    y double precision,
    z double precision
);


ALTER TABLE killmailssum OWNER TO spotmarketadmin;

--
-- TOC entry 309 (class 1259 OID 763014)
-- Name: killmailssum_killmailssumID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "killmailssum_killmailssumID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "killmailssum_killmailssumID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2655 (class 0 OID 0)
-- Dependencies: 309
-- Name: killmailssum_killmailssumID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmailssum_killmailssumID_seq" OWNED BY killmailssum."killmailssumID";


--
-- TOC entry 281 (class 1259 OID 17034)
-- Name: logs; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE logs (
    "logID" integer NOT NULL,
    service text NOT NULL,
    severity integer NOT NULL,
    detail text NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE logs OWNER TO spotmarketadmin;

--
-- TOC entry 282 (class 1259 OID 17040)
-- Name: logs_logID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "logs_logID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "logs_logID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2656 (class 0 OID 0)
-- Dependencies: 282
-- Name: logs_logID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "logs_logID_seq" OWNED BY logs."logID";


--
-- TOC entry 283 (class 1259 OID 17042)
-- Name: mapfaction; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE mapfaction (
    "systemfactionID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "factionID" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE mapfaction OWNER TO spotmarketadmin;

--
-- TOC entry 284 (class 1259 OID 17045)
-- Name: mapfaction_systemfactionID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "mapfaction_systemfactionID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "mapfaction_systemfactionID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2657 (class 0 OID 0)
-- Dependencies: 284
-- Name: mapfaction_systemfactionID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapfaction_systemfactionID_seq" OWNED BY mapfaction."systemfactionID";


--
-- TOC entry 285 (class 1259 OID 17047)
-- Name: mapjumps; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE mapjumps (
    "systemjumpID" integer NOT NULL,
    "solarSystemID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "shipJumps" integer NOT NULL
);


ALTER TABLE mapjumps OWNER TO spotmarketadmin;

--
-- TOC entry 286 (class 1259 OID 17050)
-- Name: mapjumps_systemjumpID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "mapjumps_systemjumpID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "mapjumps_systemjumpID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2658 (class 0 OID 0)
-- Dependencies: 286
-- Name: mapjumps_systemjumpID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapjumps_systemjumpID_seq" OWNED BY mapjumps."systemjumpID";


--
-- TOC entry 287 (class 1259 OID 17052)
-- Name: mapkills; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE mapkills (
    "systemkillID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "factionKills" integer NOT NULL,
    "podKills" integer NOT NULL,
    "shipKills" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE mapkills OWNER TO spotmarketadmin;

--
-- TOC entry 288 (class 1259 OID 17055)
-- Name: mapkills_systemkillID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "mapkills_systemkillID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "mapkills_systemkillID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2659 (class 0 OID 0)
-- Dependencies: 288
-- Name: mapkills_systemkillID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapkills_systemkillID_seq" OWNED BY mapkills."systemkillID";


--
-- TOC entry 289 (class 1259 OID 17057)
-- Name: mapsov; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE mapsov (
    "systemsovID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "allianceID" integer NOT NULL,
    "corporationID" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE mapsov OWNER TO spotmarketadmin;

--
-- TOC entry 290 (class 1259 OID 17060)
-- Name: mapsov_systemsovID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "mapsov_systemsovID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "mapsov_systemsovID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2660 (class 0 OID 0)
-- Dependencies: 290
-- Name: mapsov_systemsovID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapsov_systemsovID_seq" OWNED BY mapsov."systemsovID";


--
-- TOC entry 291 (class 1259 OID 17062)
-- Name: markethistory; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE markethistory (
    "markethistoryID" integer NOT NULL,
    "regionID" integer NOT NULL,
    "typeID" integer NOT NULL,
    volume bigint NOT NULL,
    "orderCount" integer NOT NULL,
    "lowPrice" real NOT NULL,
    "highPrice" real NOT NULL,
    "avgPrice" real NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE markethistory OWNER TO spotmarketadmin;

--
-- TOC entry 292 (class 1259 OID 17065)
-- Name: markethistory_markethistoryID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "markethistory_markethistoryID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "markethistory_markethistoryID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2661 (class 0 OID 0)
-- Dependencies: 292
-- Name: markethistory_markethistoryID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "markethistory_markethistoryID_seq" OWNED BY markethistory."markethistoryID";


--
-- TOC entry 293 (class 1259 OID 17067)
-- Name: marketitems; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE marketitems (
    "marketitemsID" integer NOT NULL,
    "typeID" integer NOT NULL,
    enabled integer NOT NULL,
    "importResult" integer,
    "importTimestamp" timestamp without time zone
);


ALTER TABLE marketitems OWNER TO spotmarketadmin;

--
-- TOC entry 294 (class 1259 OID 17070)
-- Name: marketitems_marketitemsID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "marketitems_marketitemsID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "marketitems_marketitemsID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2662 (class 0 OID 0)
-- Dependencies: 294
-- Name: marketitems_marketitemsID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "marketitems_marketitemsID_seq" OWNED BY marketitems."marketitemsID";


--
-- TOC entry 295 (class 1259 OID 17072)
-- Name: moonevemoons; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE moonevemoons (
    "moonID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE moonevemoons OWNER TO spotmarketadmin;

--
-- TOC entry 296 (class 1259 OID 17075)
-- Name: moonevemoonsitems; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE moonevemoonsitems (
    "solarSystemID" integer NOT NULL,
    result integer NOT NULL
);


ALTER TABLE moonevemoonsitems OWNER TO spotmarketadmin;

--
-- TOC entry 297 (class 1259 OID 17078)
-- Name: moonminerals; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE moonminerals (
    "moonID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE moonminerals OWNER TO spotmarketadmin;

--
-- TOC entry 298 (class 1259 OID 17081)
-- Name: moonverify; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE moonverify (
    "moonverifyID" integer NOT NULL,
    "moonID" integer NOT NULL,
    "killID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE moonverify OWNER TO spotmarketadmin;

--
-- TOC entry 299 (class 1259 OID 17084)
-- Name: moonverify_moonverifyID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "moonverify_moonverifyID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "moonverify_moonverifyID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2663 (class 0 OID 0)
-- Dependencies: 299
-- Name: moonverify_moonverifyID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "moonverify_moonverifyID_seq" OWNED BY moonverify."moonverifyID";


--
-- TOC entry 300 (class 1259 OID 17086)
-- Name: settings; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE settings (
    "settingID" integer NOT NULL,
    version text NOT NULL
);


ALTER TABLE settings OWNER TO spotmarketadmin;

--
-- TOC entry 301 (class 1259 OID 17092)
-- Name: settings_settingID_seq; Type: SEQUENCE; Schema: data; Owner: spotmarketadmin
--

CREATE SEQUENCE "settings_settingID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "settings_settingID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2664 (class 0 OID 0)
-- Dependencies: 301
-- Name: settings_settingID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "settings_settingID_seq" OWNED BY settings."settingID";


--
-- TOC entry 302 (class 1259 OID 17094)
-- Name: wallet; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE wallet (
    "transactionDateTime" timestamp without time zone NOT NULL,
    "transactionID" bigint NOT NULL,
    quantity bigint NOT NULL,
    "typeName" character varying(255) NOT NULL,
    "typeID" integer NOT NULL,
    price double precision NOT NULL,
    "clientID" bigint NOT NULL,
    "clientName" character varying(255) NOT NULL,
    "walletID" integer NOT NULL,
    "stationID" bigint NOT NULL,
    "stationName" character varying(255) NOT NULL,
    "transactionType" character varying(4) NOT NULL,
    personal smallint DEFAULT (0)::smallint NOT NULL,
    profit double precision DEFAULT (0)::double precision NOT NULL
);


ALTER TABLE wallet OWNER TO spotmarketadmin;

--
-- TOC entry 2471 (class 2604 OID 653629)
-- Name: balanceID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY charbalances ALTER COLUMN "balanceID" SET DEFAULT nextval('"charbalances_balanceID_seq"'::regclass);


--
-- TOC entry 2458 (class 2604 OID 17110)
-- Name: killmailID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmails ALTER COLUMN "killmailID" SET DEFAULT nextval('"killmails_killmailID_seq"'::regclass);


--
-- TOC entry 2459 (class 2604 OID 17111)
-- Name: killmailsitemsID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailsitems ALTER COLUMN "killmailsitemsID" SET DEFAULT nextval('"killmailsitems_killmailsitemsID_seq"'::regclass);


--
-- TOC entry 2472 (class 2604 OID 763019)
-- Name: killmailssumID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailssum ALTER COLUMN "killmailssumID" SET DEFAULT nextval('"killmailssum_killmailssumID_seq"'::regclass);


--
-- TOC entry 2460 (class 2604 OID 17112)
-- Name: logID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY logs ALTER COLUMN "logID" SET DEFAULT nextval('"logs_logID_seq"'::regclass);


--
-- TOC entry 2461 (class 2604 OID 17113)
-- Name: systemfactionID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapfaction ALTER COLUMN "systemfactionID" SET DEFAULT nextval('"mapfaction_systemfactionID_seq"'::regclass);


--
-- TOC entry 2462 (class 2604 OID 17114)
-- Name: systemjumpID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapjumps ALTER COLUMN "systemjumpID" SET DEFAULT nextval('"mapjumps_systemjumpID_seq"'::regclass);


--
-- TOC entry 2463 (class 2604 OID 17115)
-- Name: systemkillID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapkills ALTER COLUMN "systemkillID" SET DEFAULT nextval('"mapkills_systemkillID_seq"'::regclass);


--
-- TOC entry 2464 (class 2604 OID 17116)
-- Name: systemsovID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapsov ALTER COLUMN "systemsovID" SET DEFAULT nextval('"mapsov_systemsovID_seq"'::regclass);


--
-- TOC entry 2465 (class 2604 OID 17117)
-- Name: markethistoryID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY markethistory ALTER COLUMN "markethistoryID" SET DEFAULT nextval('"markethistory_markethistoryID_seq"'::regclass);


--
-- TOC entry 2466 (class 2604 OID 17118)
-- Name: marketitemsID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY marketitems ALTER COLUMN "marketitemsID" SET DEFAULT nextval('"marketitems_marketitemsID_seq"'::regclass);


--
-- TOC entry 2467 (class 2604 OID 17119)
-- Name: moonverifyID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonverify ALTER COLUMN "moonverifyID" SET DEFAULT nextval('"moonverify_moonverifyID_seq"'::regclass);


--
-- TOC entry 2468 (class 2604 OID 17120)
-- Name: settingID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings ALTER COLUMN "settingID" SET DEFAULT nextval('"settings_settingID_seq"'::regclass);


--
-- TOC entry 2491 (class 2606 OID 23588)
-- Name: mapjumps_pkey; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapjumps
    ADD CONSTRAINT mapjumps_pkey PRIMARY KEY ("timestamp", "solarSystemID", "shipJumps");


--
-- TOC entry 2474 (class 2606 OID 23590)
-- Name: pk_alliances; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY alliances
    ADD CONSTRAINT pk_alliances PRIMARY KEY ("allianceID", ticker, name);


--
-- TOC entry 2528 (class 2606 OID 653631)
-- Name: pk_charbalances; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY charbalances
    ADD CONSTRAINT pk_charbalances PRIMARY KEY ("characterID", balance, "timestamp");


--
-- TOC entry 2522 (class 2606 OID 653613)
-- Name: pk_charblueprints; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY charblueprints
    ADD CONSTRAINT pk_charblueprints PRIMARY KEY ("characterID", "itemID", "locationID", "typeID", quantity, "flagID", timeefficiency, materialefficiency, runs);


--
-- TOC entry 2524 (class 2606 OID 653618)
-- Name: pk_charorders; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY charorders
    ADD CONSTRAINT pk_charorders PRIMARY KEY ("characterID", "orderID");


--
-- TOC entry 2526 (class 2606 OID 653623)
-- Name: pk_charskillqueues; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY charskillqueues
    ADD CONSTRAINT pk_charskillqueues PRIMARY KEY ("characterID", endtime, level, "typeID", starttime, endsp, startsp, queueposition);


--
-- TOC entry 2476 (class 2606 OID 23592)
-- Name: pk_conquerablestations; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY conquerablestations
    ADD CONSTRAINT pk_conquerablestations PRIMARY KEY ("solarSystemID", "stationID", x, y, z, name);


--
-- TOC entry 2480 (class 2606 OID 23594)
-- Name: pk_killmails; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmails
    ADD CONSTRAINT pk_killmails PRIMARY KEY ("killID", "killHash");


--
-- TOC entry 2482 (class 2606 OID 23596)
-- Name: pk_killmailsitems; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailsitems
    ADD CONSTRAINT pk_killmailsitems PRIMARY KEY ("typeID");


--
-- TOC entry 2533 (class 2606 OID 763021)
-- Name: pk_killmailssum; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailssum
    ADD CONSTRAINT pk_killmailssum PRIMARY KEY ("killID");


--
-- TOC entry 2484 (class 2606 OID 23598)
-- Name: pk_logs; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY logs
    ADD CONSTRAINT pk_logs PRIMARY KEY ("logID");


--
-- TOC entry 2487 (class 2606 OID 23600)
-- Name: pk_mapfaction; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapfaction
    ADD CONSTRAINT pk_mapfaction PRIMARY KEY ("systemfactionID");


--
-- TOC entry 2495 (class 2606 OID 23602)
-- Name: pk_mapkills; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapkills
    ADD CONSTRAINT pk_mapkills PRIMARY KEY ("timestamp", "factionKills", "podKills", "shipKills", "solarSystemID");


--
-- TOC entry 2498 (class 2606 OID 23604)
-- Name: pk_mapsov; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapsov
    ADD CONSTRAINT pk_mapsov PRIMARY KEY ("systemsovID");


--
-- TOC entry 2502 (class 2606 OID 23606)
-- Name: pk_markethistory; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY markethistory
    ADD CONSTRAINT pk_markethistory PRIMARY KEY ("markethistoryID");


--
-- TOC entry 2504 (class 2606 OID 23608)
-- Name: pk_marketitems; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY marketitems
    ADD CONSTRAINT pk_marketitems PRIMARY KEY ("typeID");


--
-- TOC entry 2506 (class 2606 OID 23610)
-- Name: pk_moonevemoons; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonevemoons
    ADD CONSTRAINT pk_moonevemoons PRIMARY KEY ("moonID", "typeID");


--
-- TOC entry 2508 (class 2606 OID 23612)
-- Name: pk_moonevemoonsitems; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonevemoonsitems
    ADD CONSTRAINT pk_moonevemoonsitems PRIMARY KEY ("solarSystemID", result);


--
-- TOC entry 2510 (class 2606 OID 23614)
-- Name: pk_moonminerals; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonminerals
    ADD CONSTRAINT pk_moonminerals PRIMARY KEY ("moonID", "typeID");


--
-- TOC entry 2514 (class 2606 OID 23616)
-- Name: pk_moonverify; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonverify
    ADD CONSTRAINT pk_moonverify PRIMARY KEY ("moonID", "killID", "typeID");


--
-- TOC entry 2516 (class 2606 OID 23618)
-- Name: pk_settings; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT pk_settings PRIMARY KEY ("settingID");


--
-- TOC entry 2520 (class 2606 OID 653608)
-- Name: pkey_characters; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY characters
    ADD CONSTRAINT pkey_characters PRIMARY KEY ("characterID");


--
-- TOC entry 2518 (class 2606 OID 23620)
-- Name: wallet_pkey; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY wallet
    ADD CONSTRAINT wallet_pkey PRIMARY KEY ("transactionID");


--
-- TOC entry 2477 (class 1259 OID 33890)
-- Name: idx_killmails_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_killmails_solarsystemid 
  ON killmails ((("killData"->'solarSystem')->>'id'::int));


--
-- TOC entry 2478 (class 1259 OID 33794)
-- Name: idx_killmails_typeid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_killmails_typeid 
  ON killmails (((("killData"->'victim')->'shipType')->>'id'::int));
  
CREATE INDEX idx_killmails_timestamp
  ON killmails ((("killData"->'killTime')) DESC)


--
-- TOC entry 2529 (class 1259 OID 767464)
-- Name: idx_killmailssum_corporationid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_killmailssum_corporationid ON killmailssum USING btree ("corporationID" DESC NULLS LAST);


--
-- TOC entry 2530 (class 1259 OID 767451)
-- Name: idx_killmailssum_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_killmailssum_solarsystemid ON killmailssum USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2531 (class 1259 OID 767433)
-- Name: idx_killmailssum_typeid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_killmailssum_typeid ON killmailssum USING btree ("typeID" DESC NULLS LAST);


--
-- TOC entry 2485 (class 1259 OID 23623)
-- Name: idx_mapfaction_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapfaction_timestamp ON mapfaction USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2488 (class 1259 OID 23624)
-- Name: idx_mapjumps_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapjumps_solarsystemid ON mapjumps USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2489 (class 1259 OID 23625)
-- Name: idx_mapjumps_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapjumps_timestamp ON mapjumps USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2492 (class 1259 OID 23626)
-- Name: idx_mapkills_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapkills_solarsystemid ON mapkills USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2493 (class 1259 OID 23627)
-- Name: idx_mapkills_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapkills_timestamp ON mapkills USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2496 (class 1259 OID 23628)
-- Name: idx_mapsov_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapsov_timestamp ON mapsov USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2499 (class 1259 OID 23629)
-- Name: idx_markethistory_regionid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_markethistory_regionid ON markethistory USING btree ("regionID" DESC NULLS LAST);


--
-- TOC entry 2500 (class 1259 OID 23630)
-- Name: idx_markethistory_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_markethistory_timestamp ON markethistory USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2511 (class 1259 OID 23631)
-- Name: idx_moonverify_moonid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_moonverify_moonid ON moonverify USING btree ("moonID" DESC NULLS LAST);


--
-- TOC entry 2512 (class 1259 OID 23632)
-- Name: idx_moonverify_typeid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_moonverify_typeid ON moonverify USING btree ("typeID" DESC NULLS LAST);


-- Completed on 2016-03-30 19:39:29

--
-- PostgreSQL database dump complete
--

