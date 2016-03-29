-- Table: data.charblueprints

-- DROP TABLE data.charblueprints;

CREATE TABLE data.charblueprints
(
  "characterID" integer NOT NULL,
  "itemID" bigint NOT NULL,
  "locationID" bigint NOT NULL,
  "typeID" integer NOT NULL,
  quantity bigint NOT NULL,
  "flagID" bigint NOT NULL,
  timeefficiency integer NOT NULL,
  materialefficiency integer NOT NULL,
  runs bigint NOT NULL,
  CONSTRAINT pk_charblueprints PRIMARY KEY ("characterID", "itemID", "locationID", "typeID", quantity, "flagID", timeefficiency, materialefficiency, runs)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charblueprints
  OWNER TO spotmarketadmin;
