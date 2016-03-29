-- Table: data.moonevemoonsitems

-- DROP TABLE data.moonevemoonsitems;

CREATE TABLE data.moonevemoonsitems
(
  "solarSystemID" integer NOT NULL,
  "result" integer NOT NULL,
  CONSTRAINT pk_moonevemoonsitems PRIMARY KEY ("solarSystemID", "result")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.moonevemoonsitems
  OWNER TO spotmarketadmin;
