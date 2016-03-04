-- Table: data.characters

-- DROP TABLE data.characters;

CREATE TABLE data.characters
(
  "walletID" int NOT NULL,
  "characterID" integer NOT NULL,
  "characterName" character varying(255) NOT NULL,
  "keyID" int NOT NULL,
  "vCode" character varying(255) NOT NULL,
  "walletEnable" int NOT NULL,
  "journalEnable" int NOT NULL,
  "ordersEnabled" int NOT NULL,
  "displayOrders" int NOT NULL,
  "isCorpKey" int NOT NULL,
  CONSTRAINT characters_pkey PRIMARY KEY ("characterID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.characters
  OWNER TO spotmarketadmin;
