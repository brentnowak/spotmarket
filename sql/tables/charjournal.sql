-- Table: data.charjournal

-- DROP TABLE data.charjournal;

CREATE TABLE data.charjournal
(
  "transactionDateTime" timestamp without time zone NOT NULL,
  "refID" bigint NOT NULL,
  "refTypeID" real NOT NULL,
  "ownerName1" text NOT NULL,
  "ownerID1" integer NOT NULL,
  "ownerName2" text,
  "ownerID2" integer,
  "argName1" text,
  "argID1" integer,
  amount real,
  balance real,
  reason text,
  "taxReceiverID" integer,
  "taxAmount" real,
  CONSTRAINT pkey_charjournal PRIMARY KEY ("refID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charjournal
  OWNER TO spotmarketadmin;

-- Index: data.idx_charjournal_ownerid1

-- DROP INDEX data.idx_charjournal_ownerid1;

CREATE INDEX idx_charjournal_ownerid1
  ON data.charjournal
  USING btree
  ("ownerID1" DESC NULLS LAST);

-- Index: data.idx_charjournal_ownerid2

-- DROP INDEX data.idx_charjournal_ownerid2;

CREATE INDEX idx_charjournal_ownerid2
  ON data.charjournal
  USING btree
  ("ownerID2" DESC NULLS LAST);

-- Index: data.idx_charjournal_taxreceiverid

-- DROP INDEX data.idx_charjournal_taxreceiverid;

CREATE INDEX idx_charjournal_taxreceiverid
  ON data.charjournal
  USING btree
  ("taxReceiverID" DESC NULLS LAST);

