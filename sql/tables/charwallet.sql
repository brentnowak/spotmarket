-- Table: data.charwallet

-- DROP TABLE data.charwallet;

CREATE TABLE data.charwallet
(
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
  personal integer NOT NULL,
  transactionfor integer,
  journaltransactionid bigint,
  profit real,
  CONSTRAINT pkey_charwallet PRIMARY KEY ("transactionID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charwallet
  OWNER TO spotmarketadmin;

-- Index: data.idx_charwallet_stationid

-- DROP INDEX data.idx_charwallet_stationid;

CREATE INDEX idx_charwallet_stationid
  ON data.charwallet
  USING btree
  ("stationID" DESC NULLS LAST);

-- Index: data.idx_charwallet_typeid

-- DROP INDEX data.idx_charwallet_typeid;

CREATE INDEX idx_charwallet_typeid
  ON data.charwallet
  USING btree
  ("typeID" DESC NULLS LAST);

