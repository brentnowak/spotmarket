-- Table: data.alliances

-- DROP TABLE data.alliances;

CREATE TABLE data.alliances
(
  "allianceID" int NOT NULL,
  "ticker" text NOT NULL,
  "name" text NOT NULL,
  CONSTRAINT pk_alliances PRIMARY KEY ("allianceID", "ticker", "name")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.alliances
  OWNER TO spotmarketadmin;
