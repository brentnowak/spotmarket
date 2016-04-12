-- Table: meta."collation"

-- DROP TABLE meta."collation";

CREATE TABLE meta."collation"
(
  "collationID" integer NOT NULL,
  name text NOT NULL,
  ticker text NOT NULL,
  CONSTRAINT pk_meta_collation PRIMARY KEY (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE meta."collation"
  OWNER TO spotmarketadmin;
