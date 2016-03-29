-- Table: data.moonminerals

-- DROP TABLE data.moonminerals;

CREATE TABLE data.moonminerals
(
  "moonID" integer NOT NULL,
  "typeID" integer NOT NULL,
  CONSTRAINT pk_moonminerals PRIMARY KEY ("moonID", "typeID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.moonminerals
  OWNER TO spotmarketadmin;
