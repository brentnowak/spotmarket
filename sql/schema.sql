--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.1
-- Dumped by pg_dump version 9.5.0

-- Started on 2016-04-11 17:11:43

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 11 (class 2615 OID 1061174)
-- Name: character; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA "character";


ALTER SCHEMA "character" OWNER TO spotmarketadmin;

--
-- TOC entry 14 (class 2615 OID 1074253)
-- Name: kill; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA kill;


ALTER SCHEMA kill OWNER TO spotmarketadmin;

--
-- TOC entry 12 (class 2615 OID 1061179)
-- Name: map; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA map;


ALTER SCHEMA map OWNER TO spotmarketadmin;

--
-- TOC entry 10 (class 2615 OID 1061168)
-- Name: market; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA market;


ALTER SCHEMA market OWNER TO spotmarketadmin;

--
-- TOC entry 9 (class 2615 OID 1008770)
-- Name: meta; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA meta;


ALTER SCHEMA meta OWNER TO spotmarketadmin;

--
-- TOC entry 13 (class 2615 OID 1061183)
-- Name: moon; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA moon;


ALTER SCHEMA moon OWNER TO spotmarketadmin;

--
-- TOC entry 8 (class 2615 OID 1008764)
-- Name: system; Type: SCHEMA; Schema: -; Owner: spotmarketadmin
--

CREATE SCHEMA system;


ALTER SCHEMA system OWNER TO spotmarketadmin;

SET search_path = "character", pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 296 (class 1259 OID 1070904)
-- Name: balance; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE balance (
    "balanceID" integer NOT NULL,
    "characterID" integer NOT NULL,
    balance real NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE balance OWNER TO spotmarketadmin;

--
-- TOC entry 295 (class 1259 OID 1070902)
-- Name: balance_balanceID_seq; Type: SEQUENCE; Schema: character; Owner: spotmarketadmin
--

CREATE SEQUENCE "balance_balanceID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "balance_balanceID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2679 (class 0 OID 0)
-- Dependencies: 295
-- Name: balance_balanceID_seq; Type: SEQUENCE OWNED BY; Schema: character; Owner: spotmarketadmin
--

ALTER SEQUENCE "balance_balanceID_seq" OWNED BY balance."balanceID";


--
-- TOC entry 297 (class 1259 OID 1070917)
-- Name: blueprint; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE blueprint (
    "characterID" integer NOT NULL,
    "itemID" bigint NOT NULL,
    "locationID" bigint NOT NULL,
    "typeID" integer NOT NULL,
    quantity bigint NOT NULL,
    "flagID" bigint NOT NULL,
    "timeEfficiency" integer NOT NULL,
    "materialEfficiency" integer NOT NULL,
    runs integer NOT NULL
);


ALTER TABLE blueprint OWNER TO spotmarketadmin;

--
-- TOC entry 298 (class 1259 OID 1070928)
-- Name: characters; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE characters (
    "walletID" integer NOT NULL,
    "characterID" integer NOT NULL,
    "characterName" text NOT NULL,
    "keyID" integer NOT NULL,
    "vCode" text NOT NULL,
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
-- TOC entry 299 (class 1259 OID 1070940)
-- Name: journal; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE journal (
    "transactionDateTime" timestamp without time zone NOT NULL,
    "refID" bigint NOT NULL,
    "refTypeID" real NOT NULL,
    "ownerName1" text NOT NULL,
    "ownerID1" integer NOT NULL,
    "ownerName2" text,
    "ownerID2" integer,
    "argName1" text,
    "argID1" integer,
    amount real,
    balance real,
    reason text,
    "taxReceiverID" integer,
    "taxAmount" real
);


ALTER TABLE journal OWNER TO spotmarketadmin;

--
-- TOC entry 308 (class 1259 OID 2481729)
-- Name: orders; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE orders (
    "characterID" integer NOT NULL,
    "orderID" bigint NOT NULL,
    "stationID" bigint,
    "volEntered" integer,
    "volRemaining" integer,
    "minVolume" integer,
    "orderState" text,
    "typeID" integer,
    range integer,
    "accountKey" integer,
    duration integer,
    escrow real,
    price real,
    bid text,
    issued timestamp without time zone
);


ALTER TABLE orders OWNER TO spotmarketadmin;

--
-- TOC entry 301 (class 1259 OID 1071178)
-- Name: skillqueue; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE skillqueue (
    "characterID" integer NOT NULL,
    "endTime" timestamp without time zone NOT NULL,
    level integer NOT NULL,
    "typeID" integer NOT NULL,
    "startTime" timestamp without time zone NOT NULL,
    "endSP" integer NOT NULL,
    "startSP" integer NOT NULL,
    "queuePosition" integer NOT NULL
);


ALTER TABLE skillqueue OWNER TO spotmarketadmin;

--
-- TOC entry 300 (class 1259 OID 1070972)
-- Name: wallet; Type: TABLE; Schema: character; Owner: spotmarketadmin
--

CREATE TABLE wallet (
    "transactionDateTime" timestamp without time zone NOT NULL,
    "transactionID" bigint NOT NULL,
    quantity bigint NOT NULL,
    "typeName" text NOT NULL,
    "typeID" integer NOT NULL,
    price real NOT NULL,
    "clientID" bigint NOT NULL,
    "clientName" text NOT NULL,
    "characterID" integer NOT NULL,
    "stationID" bigint NOT NULL,
    "transactionType" text NOT NULL,
    personal integer,
    "journalTransactionID" bigint,
    profit real,
    "transactionFor" text
);


ALTER TABLE wallet OWNER TO spotmarketadmin;

SET search_path = kill, pg_catalog;

--
-- TOC entry 305 (class 1259 OID 1074272)
-- Name: mail; Type: TABLE; Schema: kill; Owner: spotmarketadmin
--

CREATE TABLE mail (
    "killmailID" integer NOT NULL,
    "killID" integer NOT NULL,
    "killHash" text NOT NULL,
    "killData" jsonb,
    "totalValue" real
);


ALTER TABLE mail OWNER TO spotmarketadmin;

--
-- TOC entry 304 (class 1259 OID 1074270)
-- Name: mail_killmailID_seq; Type: SEQUENCE; Schema: kill; Owner: spotmarketadmin
--

CREATE SEQUENCE "mail_killmailID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "mail_killmailID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2680 (class 0 OID 0)
-- Dependencies: 304
-- Name: mail_killmailID_seq; Type: SEQUENCE OWNED BY; Schema: kill; Owner: spotmarketadmin
--

ALTER SEQUENCE "mail_killmailID_seq" OWNED BY mail."killmailID";


--
-- TOC entry 303 (class 1259 OID 1074264)
-- Name: tracking; Type: TABLE; Schema: kill; Owner: spotmarketadmin
--

CREATE TABLE tracking (
    "killmailsitemsID" integer NOT NULL,
    "typeID" integer NOT NULL,
    enabled integer NOT NULL,
    "importResult" integer,
    "lastPage" integer,
    "importTimestamp" timestamp without time zone
);


ALTER TABLE tracking OWNER TO spotmarketadmin;

--
-- TOC entry 302 (class 1259 OID 1074262)
-- Name: tracking_killmailsitemsID_seq; Type: SEQUENCE; Schema: kill; Owner: spotmarketadmin
--

CREATE SEQUENCE "tracking_killmailsitemsID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "tracking_killmailsitemsID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2681 (class 0 OID 0)
-- Dependencies: 302
-- Name: tracking_killmailsitemsID_seq; Type: SEQUENCE OWNED BY; Schema: kill; Owner: spotmarketadmin
--

ALTER SEQUENCE "tracking_killmailsitemsID_seq" OWNED BY tracking."killmailsitemsID";


SET search_path = map, pg_catalog;

--
-- TOC entry 313 (class 1259 OID 3145222)
-- Name: jump; Type: TABLE; Schema: map; Owner: spotmarketadmin
--

CREATE TABLE jump (
    "systemjumpID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "shipJumps" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE jump OWNER TO spotmarketadmin;

--
-- TOC entry 312 (class 1259 OID 3145220)
-- Name: jump_systemjumpID_seq; Type: SEQUENCE; Schema: map; Owner: spotmarketadmin
--

CREATE SEQUENCE "jump_systemjumpID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "jump_systemjumpID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2682 (class 0 OID 0)
-- Dependencies: 312
-- Name: jump_systemjumpID_seq; Type: SEQUENCE OWNED BY; Schema: map; Owner: spotmarketadmin
--

ALTER SEQUENCE "jump_systemjumpID_seq" OWNED BY jump."systemjumpID";


--
-- TOC entry 315 (class 1259 OID 3145292)
-- Name: kill; Type: TABLE; Schema: map; Owner: spotmarketadmin
--

CREATE TABLE kill (
    "systemkillID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "factionKills" integer NOT NULL,
    "podKills" integer NOT NULL,
    "shipKills" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE kill OWNER TO spotmarketadmin;

--
-- TOC entry 314 (class 1259 OID 3145290)
-- Name: kill_systemkillID_seq; Type: SEQUENCE; Schema: map; Owner: spotmarketadmin
--

CREATE SEQUENCE "kill_systemkillID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "kill_systemkillID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2683 (class 0 OID 0)
-- Dependencies: 314
-- Name: kill_systemkillID_seq; Type: SEQUENCE OWNED BY; Schema: map; Owner: spotmarketadmin
--

ALTER SEQUENCE "kill_systemkillID_seq" OWNED BY kill."systemkillID";


--
-- TOC entry 311 (class 1259 OID 3145134)
-- Name: sov; Type: TABLE; Schema: map; Owner: spotmarketadmin
--

CREATE TABLE sov (
    "systemsovID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    "allianceID" integer NOT NULL,
    "corporationID" integer NOT NULL,
    "solarSystemID" integer NOT NULL
);


ALTER TABLE sov OWNER TO spotmarketadmin;

--
-- TOC entry 310 (class 1259 OID 3145132)
-- Name: sov_systemsovID_seq; Type: SEQUENCE; Schema: map; Owner: spotmarketadmin
--

CREATE SEQUENCE "sov_systemsovID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "sov_systemsovID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2684 (class 0 OID 0)
-- Dependencies: 310
-- Name: sov_systemsovID_seq; Type: SEQUENCE OWNED BY; Schema: map; Owner: spotmarketadmin
--

ALTER SEQUENCE "sov_systemsovID_seq" OWNED BY sov."systemsovID";


SET search_path = market, pg_catalog;

--
-- TOC entry 294 (class 1259 OID 1062456)
-- Name: history; Type: TABLE; Schema: market; Owner: spotmarketadmin
--

CREATE TABLE history (
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


ALTER TABLE history OWNER TO spotmarketadmin;

--
-- TOC entry 293 (class 1259 OID 1062454)
-- Name: history_markethistoryID_seq; Type: SEQUENCE; Schema: market; Owner: spotmarketadmin
--

CREATE SEQUENCE "history_markethistoryID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "history_markethistoryID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2685 (class 0 OID 0)
-- Dependencies: 293
-- Name: history_markethistoryID_seq; Type: SEQUENCE OWNED BY; Schema: market; Owner: spotmarketadmin
--

ALTER SEQUENCE "history_markethistoryID_seq" OWNED BY history."markethistoryID";


--
-- TOC entry 307 (class 1259 OID 2217798)
-- Name: inventory; Type: TABLE; Schema: market; Owner: spotmarketadmin
--

CREATE TABLE inventory (
    "marketinventoryID" integer NOT NULL,
    "transactionID" bigint NOT NULL,
    "typeID" integer NOT NULL,
    quantity integer NOT NULL,
    remaining integer NOT NULL,
    price real NOT NULL
);


ALTER TABLE inventory OWNER TO spotmarketadmin;

--
-- TOC entry 306 (class 1259 OID 2217796)
-- Name: inventory_marketinventoryID_seq; Type: SEQUENCE; Schema: market; Owner: spotmarketadmin
--

CREATE SEQUENCE "inventory_marketinventoryID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "inventory_marketinventoryID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2686 (class 0 OID 0)
-- Dependencies: 306
-- Name: inventory_marketinventoryID_seq; Type: SEQUENCE OWNED BY; Schema: market; Owner: spotmarketadmin
--

ALTER SEQUENCE "inventory_marketinventoryID_seq" OWNED BY inventory."marketinventoryID";


--
-- TOC entry 290 (class 1259 OID 1061340)
-- Name: region; Type: TABLE; Schema: market; Owner: spotmarketadmin
--

CREATE TABLE region (
    "marketregionID" integer NOT NULL,
    "regionID" integer NOT NULL,
    enabled integer NOT NULL,
    rank integer,
    "timestamp" timestamp without time zone,
    "importResult" integer
);


ALTER TABLE region OWNER TO spotmarketadmin;

--
-- TOC entry 289 (class 1259 OID 1061338)
-- Name: region_marketregionID_seq; Type: SEQUENCE; Schema: market; Owner: spotmarketadmin
--

CREATE SEQUENCE "region_marketregionID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "region_marketregionID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2687 (class 0 OID 0)
-- Dependencies: 289
-- Name: region_marketregionID_seq; Type: SEQUENCE OWNED BY; Schema: market; Owner: spotmarketadmin
--

ALTER SEQUENCE "region_marketregionID_seq" OWNED BY region."marketregionID";


--
-- TOC entry 292 (class 1259 OID 1061372)
-- Name: tracking; Type: TABLE; Schema: market; Owner: spotmarketadmin
--

CREATE TABLE tracking (
    "marketitemID" integer NOT NULL,
    "typeID" integer NOT NULL,
    enabled integer NOT NULL,
    "importResult" integer,
    "importTimestamp" timestamp without time zone
);


ALTER TABLE tracking OWNER TO spotmarketadmin;

--
-- TOC entry 291 (class 1259 OID 1061370)
-- Name: tracking_marketitemID_seq; Type: SEQUENCE; Schema: market; Owner: spotmarketadmin
--

CREATE SEQUENCE "tracking_marketitemID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "tracking_marketitemID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2688 (class 0 OID 0)
-- Dependencies: 291
-- Name: tracking_marketitemID_seq; Type: SEQUENCE OWNED BY; Schema: market; Owner: spotmarketadmin
--

ALTER SEQUENCE "tracking_marketitemID_seq" OWNED BY tracking."marketitemID";


SET search_path = meta, pg_catalog;

--
-- TOC entry 286 (class 1259 OID 1008815)
-- Name: alliances; Type: TABLE; Schema: meta; Owner: spotmarketadmin
--

CREATE TABLE alliances (
    "allianceID" integer NOT NULL,
    ticker text NOT NULL,
    name text NOT NULL
);


ALTER TABLE alliances OWNER TO spotmarketadmin;

--
-- TOC entry 309 (class 1259 OID 2493287)
-- Name: conquerablestation; Type: TABLE; Schema: meta; Owner: spotmarketadmin
--

CREATE TABLE conquerablestation (
    "solarSystemID" integer,
    "stationID" integer NOT NULL,
    x double precision,
    y double precision,
    z double precision,
    name text NOT NULL
);


ALTER TABLE conquerablestation OWNER TO spotmarketadmin;

--
-- TOC entry 319 (class 1259 OID 3180513)
-- Name: tranquility; Type: TABLE; Schema: meta; Owner: spotmarketadmin
--

CREATE TABLE tranquility (
    "tranquilityID" integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    players integer NOT NULL,
    status boolean NOT NULL
);


ALTER TABLE tranquility OWNER TO spotmarketadmin;

--
-- TOC entry 318 (class 1259 OID 3180511)
-- Name: tranquility_tranquilityID_seq; Type: SEQUENCE; Schema: meta; Owner: spotmarketadmin
--

CREATE SEQUENCE "tranquility_tranquilityID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "tranquility_tranquilityID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2689 (class 0 OID 0)
-- Dependencies: 318
-- Name: tranquility_tranquilityID_seq; Type: SEQUENCE OWNED BY; Schema: meta; Owner: spotmarketadmin
--

ALTER SEQUENCE "tranquility_tranquilityID_seq" OWNED BY tranquility."tranquilityID";


SET search_path = moon, pg_catalog;

--
-- TOC entry 322 (class 1259 OID 3190178)
-- Name: killmail; Type: TABLE; Schema: moon; Owner: spotmarketadmin
--

CREATE TABLE killmail (
    "moonverifyID" integer NOT NULL,
    "moonID" integer NOT NULL,
    "killID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE killmail OWNER TO spotmarketadmin;

--
-- TOC entry 321 (class 1259 OID 3190176)
-- Name: killmail_moonverifyID_seq; Type: SEQUENCE; Schema: moon; Owner: spotmarketadmin
--

CREATE SEQUENCE "killmail_moonverifyID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "killmail_moonverifyID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2690 (class 0 OID 0)
-- Dependencies: 321
-- Name: killmail_moonverifyID_seq; Type: SEQUENCE OWNED BY; Schema: moon; Owner: spotmarketadmin
--

ALTER SEQUENCE "killmail_moonverifyID_seq" OWNED BY killmail."moonverifyID";


--
-- TOC entry 320 (class 1259 OID 3189674)
-- Name: mineral; Type: TABLE; Schema: moon; Owner: spotmarketadmin
--

CREATE TABLE mineral (
    "moonID" integer NOT NULL,
    "typeID" integer NOT NULL
);


ALTER TABLE mineral OWNER TO spotmarketadmin;

SET search_path = system, pg_catalog;

--
-- TOC entry 317 (class 1259 OID 3148258)
-- Name: log; Type: TABLE; Schema: system; Owner: spotmarketadmin
--

CREATE TABLE log (
    "logID" integer NOT NULL,
    service text NOT NULL,
    severity integer NOT NULL,
    detail text NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE log OWNER TO spotmarketadmin;

--
-- TOC entry 316 (class 1259 OID 3148256)
-- Name: log_logID_seq; Type: SEQUENCE; Schema: system; Owner: spotmarketadmin
--

CREATE SEQUENCE "log_logID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "log_logID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2691 (class 0 OID 0)
-- Dependencies: 316
-- Name: log_logID_seq; Type: SEQUENCE OWNED BY; Schema: system; Owner: spotmarketadmin
--

ALTER SEQUENCE "log_logID_seq" OWNED BY log."logID";


--
-- TOC entry 288 (class 1259 OID 1009285)
-- Name: settings; Type: TABLE; Schema: system; Owner: spotmarketadmin
--

CREATE TABLE settings (
    "settingID" integer NOT NULL,
    version text NOT NULL
);


ALTER TABLE settings OWNER TO spotmarketadmin;

--
-- TOC entry 287 (class 1259 OID 1009283)
-- Name: settings_settingID_seq; Type: SEQUENCE; Schema: system; Owner: spotmarketadmin
--

CREATE SEQUENCE "settings_settingID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "settings_settingID_seq" OWNER TO spotmarketadmin;

--
-- TOC entry 2692 (class 0 OID 0)
-- Dependencies: 287
-- Name: settings_settingID_seq; Type: SEQUENCE OWNED BY; Schema: system; Owner: spotmarketadmin
--

ALTER SEQUENCE "settings_settingID_seq" OWNED BY settings."settingID";


SET search_path = "character", pg_catalog;

--
-- TOC entry 2484 (class 2604 OID 1070907)
-- Name: balanceID; Type: DEFAULT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY balance ALTER COLUMN "balanceID" SET DEFAULT nextval('"balance_balanceID_seq"'::regclass);


SET search_path = kill, pg_catalog;

--
-- TOC entry 2486 (class 2604 OID 1074275)
-- Name: killmailID; Type: DEFAULT; Schema: kill; Owner: spotmarketadmin
--

ALTER TABLE ONLY mail ALTER COLUMN "killmailID" SET DEFAULT nextval('"mail_killmailID_seq"'::regclass);


--
-- TOC entry 2485 (class 2604 OID 1074267)
-- Name: killmailsitemsID; Type: DEFAULT; Schema: kill; Owner: spotmarketadmin
--

ALTER TABLE ONLY tracking ALTER COLUMN "killmailsitemsID" SET DEFAULT nextval('"tracking_killmailsitemsID_seq"'::regclass);


SET search_path = map, pg_catalog;

--
-- TOC entry 2489 (class 2604 OID 3145225)
-- Name: systemjumpID; Type: DEFAULT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY jump ALTER COLUMN "systemjumpID" SET DEFAULT nextval('"jump_systemjumpID_seq"'::regclass);


--
-- TOC entry 2490 (class 2604 OID 3145295)
-- Name: systemkillID; Type: DEFAULT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY kill ALTER COLUMN "systemkillID" SET DEFAULT nextval('"kill_systemkillID_seq"'::regclass);


--
-- TOC entry 2488 (class 2604 OID 3145137)
-- Name: systemsovID; Type: DEFAULT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY sov ALTER COLUMN "systemsovID" SET DEFAULT nextval('"sov_systemsovID_seq"'::regclass);


SET search_path = market, pg_catalog;

--
-- TOC entry 2483 (class 2604 OID 1062459)
-- Name: markethistoryID; Type: DEFAULT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY history ALTER COLUMN "markethistoryID" SET DEFAULT nextval('"history_markethistoryID_seq"'::regclass);


--
-- TOC entry 2487 (class 2604 OID 2217801)
-- Name: marketinventoryID; Type: DEFAULT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY inventory ALTER COLUMN "marketinventoryID" SET DEFAULT nextval('"inventory_marketinventoryID_seq"'::regclass);


--
-- TOC entry 2481 (class 2604 OID 1061343)
-- Name: marketregionID; Type: DEFAULT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY region ALTER COLUMN "marketregionID" SET DEFAULT nextval('"region_marketregionID_seq"'::regclass);


--
-- TOC entry 2482 (class 2604 OID 1061375)
-- Name: marketitemID; Type: DEFAULT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY tracking ALTER COLUMN "marketitemID" SET DEFAULT nextval('"tracking_marketitemID_seq"'::regclass);


SET search_path = meta, pg_catalog;

--
-- TOC entry 2492 (class 2604 OID 3180516)
-- Name: tranquilityID; Type: DEFAULT; Schema: meta; Owner: spotmarketadmin
--

ALTER TABLE ONLY tranquility ALTER COLUMN "tranquilityID" SET DEFAULT nextval('"tranquility_tranquilityID_seq"'::regclass);


SET search_path = moon, pg_catalog;

--
-- TOC entry 2493 (class 2604 OID 3190181)
-- Name: moonverifyID; Type: DEFAULT; Schema: moon; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmail ALTER COLUMN "moonverifyID" SET DEFAULT nextval('"killmail_moonverifyID_seq"'::regclass);


SET search_path = system, pg_catalog;

--
-- TOC entry 2491 (class 2604 OID 3148261)
-- Name: logID; Type: DEFAULT; Schema: system; Owner: spotmarketadmin
--

ALTER TABLE ONLY log ALTER COLUMN "logID" SET DEFAULT nextval('"log_logID_seq"'::regclass);


--
-- TOC entry 2480 (class 2604 OID 1009288)
-- Name: settingID; Type: DEFAULT; Schema: system; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings ALTER COLUMN "settingID" SET DEFAULT nextval('"settings_settingID_seq"'::regclass);


SET search_path = "character", pg_catalog;

--
-- TOC entry 2508 (class 2606 OID 1070909)
-- Name: pk_character_balance; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY balance
    ADD CONSTRAINT pk_character_balance PRIMARY KEY ("characterID", balance, "timestamp");


--
-- TOC entry 2512 (class 2606 OID 1070921)
-- Name: pk_character_blueprint; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY blueprint
    ADD CONSTRAINT pk_character_blueprint PRIMARY KEY ("characterID", "itemID", "locationID", "typeID", quantity, "flagID", "timeEfficiency", "materialEfficiency", runs);


--
-- TOC entry 2537 (class 2606 OID 2481736)
-- Name: pk_character_orders; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY orders
    ADD CONSTRAINT pk_character_orders PRIMARY KEY ("characterID", "orderID");


--
-- TOC entry 2525 (class 2606 OID 1071182)
-- Name: pk_character_skillqueue; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY skillqueue
    ADD CONSTRAINT pk_character_skillqueue PRIMARY KEY ("characterID", "endTime", level, "typeID", "startTime", "endSP", "startSP", "queuePosition");


--
-- TOC entry 2514 (class 2606 OID 1070935)
-- Name: pkey_character_characters; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY characters
    ADD CONSTRAINT pkey_character_characters PRIMARY KEY ("characterID");


--
-- TOC entry 2519 (class 2606 OID 1070947)
-- Name: pkey_character_journal; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY journal
    ADD CONSTRAINT pkey_character_journal PRIMARY KEY ("refID");


--
-- TOC entry 2523 (class 2606 OID 1070979)
-- Name: pkey_character_wallet; Type: CONSTRAINT; Schema: character; Owner: spotmarketadmin
--

ALTER TABLE ONLY wallet
    ADD CONSTRAINT pkey_character_wallet PRIMARY KEY ("transactionID");


SET search_path = kill, pg_catalog;

--
-- TOC entry 2532 (class 2606 OID 2277110)
-- Name: pk_kill_mail; Type: CONSTRAINT; Schema: kill; Owner: spotmarketadmin
--

ALTER TABLE ONLY mail
    ADD CONSTRAINT pk_kill_mail PRIMARY KEY ("killID");


--
-- TOC entry 2527 (class 2606 OID 1074269)
-- Name: pk_kill_tracking; Type: CONSTRAINT; Schema: kill; Owner: spotmarketadmin
--

ALTER TABLE ONLY tracking
    ADD CONSTRAINT pk_kill_tracking PRIMARY KEY ("typeID");


SET search_path = map, pg_catalog;

--
-- TOC entry 2546 (class 2606 OID 3145227)
-- Name: pk_map_jump; Type: CONSTRAINT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY jump
    ADD CONSTRAINT pk_map_jump PRIMARY KEY ("timestamp", "solarSystemID");


--
-- TOC entry 2550 (class 2606 OID 3145297)
-- Name: pk_map_kill; Type: CONSTRAINT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY kill
    ADD CONSTRAINT pk_map_kill PRIMARY KEY ("timestamp", "solarSystemID");


--
-- TOC entry 2542 (class 2606 OID 3145139)
-- Name: pk_map_sov; Type: CONSTRAINT; Schema: map; Owner: spotmarketadmin
--

ALTER TABLE ONLY sov
    ADD CONSTRAINT pk_map_sov PRIMARY KEY ("systemsovID");


SET search_path = market, pg_catalog;

--
-- TOC entry 2503 (class 2606 OID 2200589)
-- Name: history_pkey; Type: CONSTRAINT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY history
    ADD CONSTRAINT history_pkey PRIMARY KEY ("regionID", "typeID", "timestamp");


--
-- TOC entry 2535 (class 2606 OID 2217803)
-- Name: pk_market_inventory; Type: CONSTRAINT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY inventory
    ADD CONSTRAINT pk_market_inventory PRIMARY KEY ("transactionID");


--
-- TOC entry 2499 (class 2606 OID 1061345)
-- Name: pk_market_region; Type: CONSTRAINT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY region
    ADD CONSTRAINT pk_market_region PRIMARY KEY ("regionID");


--
-- TOC entry 2501 (class 2606 OID 1061377)
-- Name: pk_market_tracking; Type: CONSTRAINT; Schema: market; Owner: spotmarketadmin
--

ALTER TABLE ONLY tracking
    ADD CONSTRAINT pk_market_tracking PRIMARY KEY ("typeID");


SET search_path = meta, pg_catalog;

--
-- TOC entry 2495 (class 2606 OID 1008822)
-- Name: pk_alliances; Type: CONSTRAINT; Schema: meta; Owner: spotmarketadmin
--

ALTER TABLE ONLY alliances
    ADD CONSTRAINT pk_alliances PRIMARY KEY ("allianceID", ticker, name);


--
-- TOC entry 2539 (class 2606 OID 2493294)
-- Name: pk_meta_conquerablestation; Type: CONSTRAINT; Schema: meta; Owner: spotmarketadmin
--

ALTER TABLE ONLY conquerablestation
    ADD CONSTRAINT pk_meta_conquerablestation PRIMARY KEY ("stationID");


--
-- TOC entry 2554 (class 2606 OID 3180518)
-- Name: pk_meta_tranquility; Type: CONSTRAINT; Schema: meta; Owner: spotmarketadmin
--

ALTER TABLE ONLY tranquility
    ADD CONSTRAINT pk_meta_tranquility PRIMARY KEY ("timestamp", players, status);


SET search_path = moon, pg_catalog;

--
-- TOC entry 2560 (class 2606 OID 3190183)
-- Name: pk_moon_killmail; Type: CONSTRAINT; Schema: moon; Owner: spotmarketadmin
--

ALTER TABLE ONLY killmail
    ADD CONSTRAINT pk_moon_killmail PRIMARY KEY ("moonID", "killID", "typeID");


--
-- TOC entry 2556 (class 2606 OID 3189678)
-- Name: pk_moon_mineral; Type: CONSTRAINT; Schema: moon; Owner: spotmarketadmin
--

ALTER TABLE ONLY mineral
    ADD CONSTRAINT pk_moon_mineral PRIMARY KEY ("moonID", "typeID");


SET search_path = system, pg_catalog;

--
-- TOC entry 2497 (class 2606 OID 1009293)
-- Name: pk_settings; Type: CONSTRAINT; Schema: system; Owner: spotmarketadmin
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT pk_settings PRIMARY KEY ("settingID");


--
-- TOC entry 2552 (class 2606 OID 3148266)
-- Name: pk_system_log; Type: CONSTRAINT; Schema: system; Owner: spotmarketadmin
--

ALTER TABLE ONLY log
    ADD CONSTRAINT pk_system_log PRIMARY KEY ("logID");


SET search_path = "character", pg_catalog;

--
-- TOC entry 2506 (class 1259 OID 1070910)
-- Name: idx_character_balance_characterid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_balance_characterid ON balance USING btree ("characterID" DESC NULLS LAST);


--
-- TOC entry 2509 (class 1259 OID 1070922)
-- Name: idx_character_blueprint_characterid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_blueprint_characterid ON blueprint USING btree ("characterID" DESC NULLS LAST);


--
-- TOC entry 2510 (class 1259 OID 1070923)
-- Name: idx_character_blueprint_typeid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_blueprint_typeid ON blueprint USING btree ("typeID" DESC NULLS LAST);


--
-- TOC entry 2515 (class 1259 OID 1070948)
-- Name: idx_character_journal_ownerid1; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_journal_ownerid1 ON journal USING btree ("ownerID1" DESC NULLS LAST);


--
-- TOC entry 2516 (class 1259 OID 1070949)
-- Name: idx_character_journal_ownerid2; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_journal_ownerid2 ON journal USING btree ("ownerID2" DESC NULLS LAST);


--
-- TOC entry 2517 (class 1259 OID 1070950)
-- Name: idx_character_journal_taxreceiverid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_journal_taxreceiverid ON journal USING btree ("taxReceiverID" DESC NULLS LAST);


--
-- TOC entry 2520 (class 1259 OID 1070980)
-- Name: idx_character_wallet_stationid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_wallet_stationid ON wallet USING btree ("stationID" DESC NULLS LAST);


--
-- TOC entry 2521 (class 1259 OID 1070981)
-- Name: idx_character_wallet_typeid; Type: INDEX; Schema: character; Owner: spotmarketadmin
--

CREATE INDEX idx_character_wallet_typeid ON wallet USING btree ("typeID" DESC NULLS LAST);


SET search_path = kill, pg_catalog;

--
-- TOC entry 2528 (class 1259 OID 1074281)
-- Name: idx_kill_mail_solarsystemid; Type: INDEX; Schema: kill; Owner: spotmarketadmin
--

CREATE INDEX idx_kill_mail_solarsystemid ON mail USING btree ((((("killData" -> 'solarSystem'::text) ->> 'id'::text))::integer));


--
-- TOC entry 2529 (class 1259 OID 1074282)
-- Name: idx_kill_mail_timestamp; Type: INDEX; Schema: kill; Owner: spotmarketadmin
--

CREATE INDEX idx_kill_mail_timestamp ON mail USING btree ((("killData" -> 'killTime'::text)) DESC);


--
-- TOC entry 2530 (class 1259 OID 1074283)
-- Name: idx_kill_mail_typeid; Type: INDEX; Schema: kill; Owner: spotmarketadmin
--

CREATE INDEX idx_kill_mail_typeid ON mail USING btree (((((("killData" -> 'victim'::text) -> 'shipType'::text) ->> 'id'::text))::integer));


SET search_path = map, pg_catalog;

--
-- TOC entry 2543 (class 1259 OID 3145228)
-- Name: idx_map_jump_solarsystemid; Type: INDEX; Schema: map; Owner: spotmarketadmin
--

CREATE INDEX idx_map_jump_solarsystemid ON jump USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2544 (class 1259 OID 3145229)
-- Name: idx_map_jump_timestamp; Type: INDEX; Schema: map; Owner: spotmarketadmin
--

CREATE INDEX idx_map_jump_timestamp ON jump USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2547 (class 1259 OID 3145298)
-- Name: idx_map_kill_solarsystemid; Type: INDEX; Schema: map; Owner: spotmarketadmin
--

CREATE INDEX idx_map_kill_solarsystemid ON kill USING btree ("solarSystemID" DESC NULLS LAST);


--
-- TOC entry 2548 (class 1259 OID 3145299)
-- Name: idx_map_kill_timestamp; Type: INDEX; Schema: map; Owner: spotmarketadmin
--

CREATE INDEX idx_map_kill_timestamp ON kill USING btree ("timestamp" DESC NULLS LAST);


--
-- TOC entry 2540 (class 1259 OID 3145140)
-- Name: idx_map_sov_timestamp; Type: INDEX; Schema: map; Owner: spotmarketadmin
--

CREATE INDEX idx_map_sov_timestamp ON sov USING btree ("timestamp" DESC NULLS LAST);


SET search_path = market, pg_catalog;

--
-- TOC entry 2504 (class 1259 OID 1062462)
-- Name: idx_market_history_regionid; Type: INDEX; Schema: market; Owner: spotmarketadmin
--

CREATE INDEX idx_market_history_regionid ON history USING btree ("regionID" DESC NULLS LAST);


--
-- TOC entry 2505 (class 1259 OID 1062464)
-- Name: idx_market_history_typeid; Type: INDEX; Schema: market; Owner: spotmarketadmin
--

CREATE INDEX idx_market_history_typeid ON history USING btree ("typeID" DESC NULLS LAST);


--
-- TOC entry 2533 (class 1259 OID 2217804)
-- Name: idx_market_inventory_typeid; Type: INDEX; Schema: market; Owner: spotmarketadmin
--

CREATE INDEX idx_market_inventory_typeid ON inventory USING btree ("typeID" DESC NULLS LAST);


SET search_path = moon, pg_catalog;

--
-- TOC entry 2557 (class 1259 OID 3190184)
-- Name: idx_moon_killmail_moonid; Type: INDEX; Schema: moon; Owner: spotmarketadmin
--

CREATE INDEX idx_moon_killmail_moonid ON killmail USING btree ("moonID" DESC NULLS LAST);


--
-- TOC entry 2558 (class 1259 OID 3190185)
-- Name: idx_moon_killmail_typeid; Type: INDEX; Schema: moon; Owner: spotmarketadmin
--

CREATE INDEX idx_moon_killmail_typeid ON killmail USING btree ("typeID" DESC NULLS LAST);


-- Completed on 2016-04-11 17:11:43

--
-- PostgreSQL database dump complete
--

