-- Table: data.mapkills

-- DROP TABLE data.mapkills;

CREATE TABLE data.mapkills
(
  "systemkillID" serial NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  "factionKills" integer NOT NULL,
  "podKills" integer NOT NULL,
  "shipKills" integer NOT NULL,
  "solarSystemID" integer NOT NULL,
  CONSTRAINT pk_mapkills PRIMARY KEY ("systemkillID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.mapkills
  OWNER TO spotmarketadmin;

-- Index: data."idx_mapkills_systemkillID"

-- DROP INDEX data."idx_mapkills_systemkillID";

CREATE INDEX "idx_mapkills_systemkillID"
  ON data.mapkills
  USING btree
  ("systemkillID");

-- Index: data.idx_mapkills_timestamp

-- DROP INDEX data.idx_mapkills_timestamp;

CREATE INDEX idx_mapkills_timestamp
  ON data.mapkills
  USING btree
  ("timestamp" DESC NULLS LAST);

