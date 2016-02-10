-- Table: data.wallet

-- DROP TABLE data.wallet;

CREATE TABLE data.wallet
(
  "transactionDateTime" timestamp without time zone NOT NULL,
  "transactionID" bigint NOT NULL,
  quantity bigint NOT NULL,
  "typeName" character varying(255) NOT NULL,
  "typeID" integer NOT NULL,
  price double precision NOT NULL,
  "clientID" bigint NOT NULL,
  "clientName" character varying(255) NOT NULL,
  "characterID" integer NOT NULL,
  "stationID" bigint NOT NULL,
  "stationName" character varying(255) NOT NULL,
  "transactionType" character varying(4) NOT NULL,
  personal smallint NOT NULL DEFAULT (0)::smallint,
  profit double precision NOT NULL DEFAULT (0)::double precision,
  CONSTRAINT wallet_pkey PRIMARY KEY ("transactionID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.wallet
  OWNER TO spotmarketadmin;
