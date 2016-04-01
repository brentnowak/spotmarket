-- Table: data.killmails

-- DROP TABLE data.killmails;

CREATE TABLE data.killmails
(
  "killmailID" serial NOT NULL,
  "killID" integer NOT NULL,
  "killHash" text NOT NULL,
  "killData" jsonb,
  "totalValue" real,
  CONSTRAINT pk_killmails PRIMARY KEY ("killID", "killHash")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.killmails
  OWNER TO spotmarketadmin;

-- Index: data.idx_killmails_solarsystemid

-- DROP INDEX data.idx_killmails_solarsystemid;

CREATE INDEX idx_killmails_solarsystemid
  ON data.killmails
  USING btree
  (((("killData" -> 'solarSystem'::text) ->> 'id'::text)::integer));

-- Index: data.idx_killmails_timestamp

-- DROP INDEX data.idx_killmails_timestamp;

CREATE INDEX idx_killmails_timestamp
  ON data.killmails
  USING btree
  (("killData" -> 'killTime'::text) DESC);

-- Index: data.idx_killmails_typeid

-- DROP INDEX data.idx_killmails_typeid;

CREATE INDEX idx_killmails_typeid
  ON data.killmails
  USING btree
  ((((("killData" -> 'victim'::text) -> 'shipType'::text) ->> 'id'::text)::integer));

