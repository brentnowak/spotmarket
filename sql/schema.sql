--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.0

-- Started on 2016-03-14 07:54:45

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 17001)
-- Name: data; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA data;


ALTER SCHEMA data OWNER TO spotmarketadmin;

SET search_path = data, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 285 (class 1259 OID 17053)
-- Name: alliances; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE alliances (
    "allianceID" integer NOT NULL,
    ticker text NOT NULL,
    name text NOT NULL
);


ALTER TABLE alliances OWNER TO spotmarketadmin;

--
-- TOC entry 286 (class 1259 OID 17061)
-- Name: characters; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE characters (
    "walletID" integer NOT NULL,
    "characterID" integer NOT NULL,
    "characterName" character varying(255) NOT NULL,
    "keyID" integer NOT NULL,
    "vCode" character varying(255) NOT NULL,
    "walletEnable" integer NOT NULL,
    "journalEnable" integer NOT NULL,
    "ordersEnabled" integer NOT NULL,
    "displayOrders" integer NOT NULL,
    "isCorpKey" integer NOT NULL
);


ALTER TABLE characters OWNER TO spotmarketadmin;

--
-- TOC entry 287 (class 1259 OID 17069)
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
-- TOC entry 289 (class 1259 OID 17079)
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
-- TOC entry 288 (class 1259 OID 17077)
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
-- TOC entry 2589 (class 0 OID 0)
-- Dependencies: 288
-- Name: killmails_killmailID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmails_killmailID_seq" OWNED BY killmails."killmailID";


--
-- TOC entry 291 (class 1259 OID 17090)
-- Name: killmailsitems; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE killmailsitems (
    "killmailsitemsID" integer NOT NULL,
    "typeID" integer NOT NULL,
    enabled integer NOT NULL,
    "importResult" integer,
    "importTimestamp" timestamp without time zone
);


ALTER TABLE killmailsitems OWNER TO spotmarketadmin;

--
-- TOC entry 290 (class 1259 OID 17088)
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
-- TOC entry 2590 (class 0 OID 0)
-- Dependencies: 290
-- Name: killmailsitems_killmailsitemsID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmailsitems_killmailsitemsID_seq" OWNED BY killmailsitems."killmailsitemsID";


--
-- TOC entry 276 (class 1259 OID 17004)
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
-- TOC entry 275 (class 1259 OID 17002)
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
-- TOC entry 2591 (class 0 OID 0)
-- Dependencies: 275
-- Name: logs_logID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "logs_logID_seq" OWNED BY logs."logID";


--
-- TOC entry 282 (class 1259 OID 17034)
-- Name: mapjumps; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE mapjumps (
    "systemjumpID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "shipJumps" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE mapjumps OWNER TO spotmarketadmin;

--
-- TOC entry 281 (class 1259 OID 17032)
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
-- TOC entry 2592 (class 0 OID 0)
-- Dependencies: 281
-- Name: mapjumps_systemjumpID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapjumps_systemjumpID_seq" OWNED BY mapjumps."systemjumpID";


--
-- TOC entry 280 (class 1259 OID 17024)
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
-- TOC entry 279 (class 1259 OID 17022)
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
-- TOC entry 2593 (class 0 OID 0)
-- Dependencies: 279
-- Name: mapkills_systemkillID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapkills_systemkillID_seq" OWNED BY mapkills."systemkillID";


--
-- TOC entry 278 (class 1259 OID 17015)
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
-- TOC entry 277 (class 1259 OID 17013)
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
-- TOC entry 2594 (class 0 OID 0)
-- Dependencies: 277
-- Name: mapsov_systemsovID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "mapsov_systemsovID_seq" OWNED BY mapsov."systemsovID";


--
-- TOC entry 293 (class 1259 OID 17098)
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
-- TOC entry 292 (class 1259 OID 17096)
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
-- TOC entry 2595 (class 0 OID 0)
-- Dependencies: 292
-- Name: markethistory_markethistoryID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "markethistory_markethistoryID_seq" OWNED BY markethistory."markethistoryID";


--
-- TOC entry 295 (class 1259 OID 17108)
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
-- TOC entry 294 (class 1259 OID 17106)
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
-- TOC entry 2596 (class 0 OID 0)
-- Dependencies: 294
-- Name: marketitems_marketitemsID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "marketitems_marketitemsID_seq" OWNED BY marketitems."marketitemsID";


--
-- TOC entry 296 (class 1259 OID 17114)
-- Name: moonminerals; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE moonminerals (
    "moonID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE moonminerals OWNER TO spotmarketadmin;

--
-- TOC entry 298 (class 1259 OID 17121)
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
-- TOC entry 297 (class 1259 OID 17119)
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
-- TOC entry 2597 (class 0 OID 0)
-- Dependencies: 297
-- Name: moonverify_moonverifyID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "moonverify_moonverifyID_seq" OWNED BY moonverify."moonverifyID";


--
-- TOC entry 284 (class 1259 OID 17044)
-- Name: settings; Type: TABLE; Schema: data; Owner: spotmarketadmin
--

CREATE TABLE settings (
    "settingID" integer NOT NULL,
    version text NOT NULL
);


ALTER TABLE settings OWNER TO spotmarketadmin;

--
-- TOC entry 283 (class 1259 OID 17042)
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
-- TOC entry 2598 (class 0 OID 0)
-- Dependencies: 283
-- Name: settings_settingID_seq; Type: SEQUENCE OWNED BY; Schema: data; Owner: spotmarketadmin
--

ALTER SEQUENCE "settings_settingID_seq" OWNED BY settings."settingID";


--
-- TOC entry 299 (class 1259 OID 17129)
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
-- TOC entry 2425 (class 2604 OID 17082)
-- Name: killmailID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmails ALTER COLUMN "killmailID" SET DEFAULT nextval('"killmails_killmailID_seq"'::regclass);


--
-- TOC entry 2426 (class 2604 OID 17093)
-- Name: killmailsitemsID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailsitems ALTER COLUMN "killmailsitemsID" SET DEFAULT nextval('"killmailsitems_killmailsitemsID_seq"'::regclass);


--
-- TOC entry 2420 (class 2604 OID 17007)
-- Name: logID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY logs ALTER COLUMN "logID" SET DEFAULT nextval('"logs_logID_seq"'::regclass);


--
-- TOC entry 2423 (class 2604 OID 17037)
-- Name: systemjumpID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapjumps ALTER COLUMN "systemjumpID" SET DEFAULT nextval('"mapjumps_systemjumpID_seq"'::regclass);


--
-- TOC entry 2422 (class 2604 OID 17027)
-- Name: systemkillID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapkills ALTER COLUMN "systemkillID" SET DEFAULT nextval('"mapkills_systemkillID_seq"'::regclass);


--
-- TOC entry 2421 (class 2604 OID 17018)
-- Name: systemsovID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapsov ALTER COLUMN "systemsovID" SET DEFAULT nextval('"mapsov_systemsovID_seq"'::regclass);


--
-- TOC entry 2427 (class 2604 OID 17101)
-- Name: markethistoryID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY markethistory ALTER COLUMN "markethistoryID" SET DEFAULT nextval('"markethistory_markethistoryID_seq"'::regclass);


--
-- TOC entry 2428 (class 2604 OID 17111)
-- Name: marketitemsID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY marketitems ALTER COLUMN "marketitemsID" SET DEFAULT nextval('"marketitems_marketitemsID_seq"'::regclass);


--
-- TOC entry 2429 (class 2604 OID 17124)
-- Name: moonverifyID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonverify ALTER COLUMN "moonverifyID" SET DEFAULT nextval('"moonverify_moonverifyID_seq"'::regclass);


--
-- TOC entry 2424 (class 2604 OID 17047)
-- Name: settingID; Type: DEFAULT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings ALTER COLUMN "settingID" SET DEFAULT nextval('"settings_settingID_seq"'::regclass);


--
-- TOC entry 2450 (class 2606 OID 17068)
-- Name: characters_pkey; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY characters
    ADD CONSTRAINT characters_pkey PRIMARY KEY ("characterID");


--
-- TOC entry 2448 (class 2606 OID 17060)
-- Name: pk_alliances; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY alliances
    ADD CONSTRAINT pk_alliances PRIMARY KEY ("allianceID", ticker, name);


--
-- TOC entry 2452 (class 2606 OID 17076)
-- Name: pk_conquerablestations; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY conquerablestations
    ADD CONSTRAINT pk_conquerablestations PRIMARY KEY ("solarSystemID", "stationID", x, y, z, name);


--
-- TOC entry 2454 (class 2606 OID 17087)
-- Name: pk_killmails; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmails
    ADD CONSTRAINT pk_killmails PRIMARY KEY ("killID", "killHash");


--
-- TOC entry 2456 (class 2606 OID 17095)
-- Name: pk_killmailsitems; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmailsitems
    ADD CONSTRAINT pk_killmailsitems PRIMARY KEY ("typeID");


--
-- TOC entry 2433 (class 2606 OID 17012)
-- Name: pk_logs; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY logs
    ADD CONSTRAINT pk_logs PRIMARY KEY ("logID");


--
-- TOC entry 2444 (class 2606 OID 17039)
-- Name: pk_mapjumps; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapjumps
    ADD CONSTRAINT pk_mapjumps PRIMARY KEY ("timestamp", "shipJumps", "solarSystemID");


--
-- TOC entry 2440 (class 2606 OID 17029)
-- Name: pk_mapkills; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapkills
    ADD CONSTRAINT pk_mapkills PRIMARY KEY ("timestamp", "factionKills", "podKills", "shipKills", "solarSystemID");


--
-- TOC entry 2436 (class 2606 OID 17020)
-- Name: pk_mapsov; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY mapsov
    ADD CONSTRAINT pk_mapsov PRIMARY KEY ("systemsovID");


--
-- TOC entry 2460 (class 2606 OID 17103)
-- Name: pk_markethistory; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY markethistory
    ADD CONSTRAINT pk_markethistory PRIMARY KEY ("markethistoryID");


--
-- TOC entry 2462 (class 2606 OID 17113)
-- Name: pk_marketitems; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY marketitems
    ADD CONSTRAINT pk_marketitems PRIMARY KEY ("typeID");


--
-- TOC entry 2464 (class 2606 OID 17118)
-- Name: pk_moonminerals; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonminerals
    ADD CONSTRAINT pk_moonminerals PRIMARY KEY ("moonID", "typeID");


--
-- TOC entry 2468 (class 2606 OID 17126)
-- Name: pk_moonverify; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY moonverify
    ADD CONSTRAINT pk_moonverify PRIMARY KEY ("moonID", "killID", "typeID");


--
-- TOC entry 2446 (class 2606 OID 17052)
-- Name: pk_settings; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT pk_settings PRIMARY KEY ("settingID");


--
-- TOC entry 2470 (class 2606 OID 17138)
-- Name: wallet_pkey; Type: CONSTRAINT; Schema: data; Owner: spotmarketadmin
--

ALTER TABLE ONLY wallet
    ADD CONSTRAINT wallet_pkey PRIMARY KEY ("transactionID");


--
-- TOC entry 2441 (class 1259 OID 17041)
-- Name: idx_mapjumps_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapjumps_solarsystemid ON mapjumps USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2442 (class 1259 OID 17040)
-- Name: idx_mapjumps_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapjumps_timestamp ON mapjumps USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2437 (class 1259 OID 17031)
-- Name: idx_mapkills_solarsystemid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapkills_solarsystemid ON mapkills USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2438 (class 1259 OID 17030)
-- Name: idx_mapkills_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapkills_timestamp ON mapkills USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2434 (class 1259 OID 17021)
-- Name: idx_mapsov_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_mapsov_timestamp ON mapsov USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2457 (class 1259 OID 17105)
-- Name: idx_markethistory_regionid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_markethistory_regionid ON markethistory USING btree ("regionID" DESC NULLS LAST);


--
-- TOC entry 2458 (class 1259 OID 17104)
-- Name: idx_markethistory_timestamp; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_markethistory_timestamp ON markethistory USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2465 (class 1259 OID 17127)
-- Name: idx_moonverify_moonid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_moonverify_moonid ON moonverify USING btree ("moonID" DESC NULLS LAST);


--
-- TOC entry 2466 (class 1259 OID 17128)
-- Name: idx_moonverify_typeid; Type: INDEX; Schema: data; Owner: spotmarketadmin
--

CREATE INDEX idx_moonverify_typeid ON moonverify USING btree ("typeID" DESC NULLS LAST);


-- Completed on 2016-03-14 07:54:46

--
-- PostgreSQL database dump complete
--

