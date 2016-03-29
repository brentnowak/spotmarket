-- Table: data.charskillqueues

-- DROP TABLE data.charskillqueues;

CREATE TABLE data.charskillqueues
(
  "characterID" integer NOT NULL,
  endtime timestamp without time zone NOT NULL,
  level integer NOT NULL,
  "typeID" integer NOT NULL,
  starttime timestamp without time zone NOT NULL,
  endsp integer NOT NULL,
  startsp integer NOT NULL,
  queueposition integer NOT NULL,
  CONSTRAINT pk_charskillqueues PRIMARY KEY ("characterID", endtime, level, "typeID", starttime, endsp, startsp, queueposition)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charskillqueues
  OWNER TO spotmarketadmin;
