-- Table: data.characters

-- DROP TABLE data.characters;

CREATE TABLE data.characters
(
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
  "corpKey" integer NOT NULL,
  CONSTRAINT pkey_characters PRIMARY KEY ("characterID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.characters
  OWNER TO spotmarketadmin;
