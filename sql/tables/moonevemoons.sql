-- Table: data.moonevemoons

-- DROP TABLE data.moonevemoons;

CREATE TABLE data.moonevemoons
(
  "moonID" integer NOT NULL,
  "typeID" integer NOT NULL,
  CONSTRAINT pk_moonevemoons PRIMARY KEY ("moonID", "typeID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.moonevemoons
  OWNER TO spotmarketadmin;
