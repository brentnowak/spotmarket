-- Table: data.mapfaction

-- DROP TABLE data.mapfaction;

CREATE TABLE data.mapfaction
(
  "systemfactionID" serial NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  "factionID" integer NOT NULL,
  "solarSystemID" integer NOT NULL,
  CONSTRAINT pk_mapfaction PRIMARY KEY ("systemfactionID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.mapfaction
  OWNER TO spotmarketadmin;

-- Index: data.idx_mapfaction_timestamp

-- DROP INDEX data.idx_mapfaction_timestamp;

CREATE INDEX idx_mapfaction_timestamp
  ON data.mapfaction
  USING btree
  ("timestamp" DESC NULLS LAST);
