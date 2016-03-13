-- Table: data.killmailsitems

-- DROP TABLE data.killmailsitems;

CREATE TABLE data.killmailsitems
(
  "killmailsitemsID" serial NOT NULL,
  "typeID" integer NOT NULL,
  enabled integer NOT NULL,
  "importResult" integer,
  "importTimestamp" timestamp without time zone,
  CONSTRAINT pk_killmailsitems PRIMARY KEY ("typeID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.killmailsitems
  OWNER TO spotmarketadmin;
