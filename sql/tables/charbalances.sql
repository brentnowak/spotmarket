-- Table: data.charbalances

-- DROP TABLE data.charbalances;

CREATE TABLE data.charbalances
(
  "balanceID" serial NOT NULL,
  "characterID" integer NOT NULL,
  balance real NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  CONSTRAINT pk_charbalances PRIMARY KEY ("characterID", balance, "timestamp")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charbalances
  OWNER TO spotmarketadmin;
