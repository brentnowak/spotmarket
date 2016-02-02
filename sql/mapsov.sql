-- Table: data.mapsov

-- DROP TABLE data.mapsov;

CREATE TABLE data.mapsov
(
  "systemsovID" serial NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  "allianceID" integer NOT NULL,
  "corporationID" integer NOT NULL,
  "solarSystemID" integer NOT NULL,
  CONSTRAINT pk_mapsov PRIMARY KEY ("systemsovID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.mapsov
  OWNER TO spotmarketadmin;

-- Index: data.idx_mapsov_timestamp

-- DROP INDEX data.idx_mapsov_timestamp;

CREATE INDEX idx_mapsov_timestamp
  ON data.mapsov
  USING btree
  ("timestamp" DESC NULLS LAST);