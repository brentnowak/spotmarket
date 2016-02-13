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
  CONSTRAINT pk_mapkills PRIMARY KEY ("timestamp, factionKills, podKills, solarSystemID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.mapkills
  OWNER TO spotmarketadmin;

-- Index: data.idx_mapkills_timestamp

-- DROP INDEX data.idx_mapkills_timestamp;

CREATE INDEX idx_mapkills_timestamp
  ON data.mapkills
  USING btree
  ("timestamp" DESC NULLS LAST);

CREATE INDEX idx_mapkills_solarsystemid
  ON data.mapkills
  USING btree
  ("solarSystemID" DESC NULLS LAST);
