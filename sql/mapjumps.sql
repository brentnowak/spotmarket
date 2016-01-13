-- Table: data.mapjumps

-- DROP TABLE data.mapjumps;

CREATE TABLE data.mapjumps
(
  "systemjumpID" serial NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  "shipJumps" integer NOT NULL,
  "solarSystemID" integer NOT NULL,
  CONSTRAINT pk_mapjumps PRIMARY KEY ("systemjumpID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.mapjumps
  OWNER TO spotmarketadmin;

-- Index: data."idx_mapjumps_systemkillID"

-- DROP INDEX data."idx_mapjumps_systemkillID";

CREATE INDEX "idx_mapjumps_systemjumpID"
  ON data.mapjumps
  USING btree
  ("systemjumpID");

-- Index: data.idx_mapjumps_timestamp

-- DROP INDEX data.idx_mapjumps_timestamp;

CREATE INDEX idx_mapjumps_timestamp
  ON data.mapjumps
  USING btree
  ("timestamp" DESC NULLS LAST);

