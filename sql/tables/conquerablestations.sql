-- Table: data.conquerablestations

-- DROP TABLE data.conquerablestations;

CREATE TABLE data.conquerablestations
(
  "solarSystemID" int NOT NULL,
  "stationID" int NOT NULL,
  "x" double precision NOT NULL,
  "y" double precision NOT NULL,
  "z" double precision NOT NULL,
  "name" text NOT NULL,
  CONSTRAINT pk_conquerablestations PRIMARY KEY ("solarSystemID", "stationID", "x", "y", "z", "name")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.conquerablestations
  OWNER TO spotmarketadmin;
