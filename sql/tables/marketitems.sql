-- Table: data.marketitems

-- DROP TABLE data.marketitems;

CREATE TABLE data.marketitems
(
  "marketitemsID" serial NOT NULL,
  "typeID" integer NOT NULL,
  "enabled" integer NOT NULL,
  "importResult" integer NULL,
  "importTimestamp" timestamp without time zone NULL,
  CONSTRAINT pk_marketitems PRIMARY KEY ("typeID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.marketitems
  OWNER TO spotmarketadmin;
