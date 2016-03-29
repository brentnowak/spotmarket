-- Table: data.moonverify

-- DROP TABLE data.moonverify;

CREATE TABLE data.moonverify
(
  "moonverifyID" serial NOT NULL,
  "moonID" integer NOT NULL,
  "killID" integer NOT NULL,
  "typeID" integer NOT NULL,
  CONSTRAINT pk_moonverify PRIMARY KEY ("moonID", "killID", "typeID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.moonverify
  OWNER TO spotmarketadmin;

-- Index: data.idx_moonverify_moonid

-- DROP INDEX data.idx_mapjumps_moonid;

CREATE INDEX idx_moonverify_moonid
  ON data.moonverify
  USING btree
  ("moonID" DESC NULLS LAST);

-- Index: data.idx_moonverify_typeID

-- DROP INDEX data.idx_moonverify_typeID;

CREATE INDEX idx_moonverify_typeid
  ON data.moonverify
  USING btree
  ("typeID" DESC NULLS LAST);

