-- Table: data.killmailssum

-- DROP TABLE data.killmailssum;

CREATE TABLE data.killmailssum
(
  "killmailssumID" serial NOT NULL,
  "killID" integer NOT NULL,
  "characterID" integer NOT NULL,
  "corporationID" integer,
  "typeID" integer NOT NULL,
  "attackerCount" integer NOT NULL,
  "damageTaken" integer NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  "solarSystemID" integer NOT NULL,
  x double precision,
  y double precision,
  z double precision,
  CONSTRAINT pk_killmailssum PRIMARY KEY ("killID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.killmailssum
  OWNER TO spotmarketadmin;
