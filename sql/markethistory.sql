-- Table: data.markethistory

-- DROP TABLE data.markethistory;

CREATE TABLE data.markethistory
(
  "markethistoryID" serial NOT NULL,
  "regionID" integer NOT NULL,
  "typeID" integer NOT NULL,
  volume bigint NOT NULL,
  "orderCount" integer NOT NULL,
  "lowPrice" real NOT NULL,
  "highPrice" real NOT NULL,
  "avgPrice" real NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  CONSTRAINT pk_markethistory PRIMARY KEY ("markethistoryID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.markethistory
  OWNER TO spotmarketadmin;

-- Index: data.idx_mapjumps_timestamp

-- DROP INDEX data.idx_mapjumps_timestamp;

CREATE INDEX idx_markethistory_timestamp
  ON data.markethistory
  USING btree
  ("timestamp" DESC NULLS LAST);

CREATE INDEX idx_markethistory_regionID
  ON data.markethistory
  USING btree
  ("regionID" DESC NULLS LAST);
