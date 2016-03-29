-- Table: data.charwallet

-- DROP TABLE data.charwallet;

CREATE TABLE data.charwallet
(
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
  "transactionType" character varying(4) NOT NULL,
  personal int NOT NULL DEFAULT,
  transactionFor integer NOT NULL,
  journalTransactionID bitint NOT NULL,
  profit double precision NOT NULL DEFAULT (0)::double precision,
  CONSTRAINT pkey_charwallet PRIMARY KEY ("transactionID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charwallet
  OWNER TO spotmarketadmin;
