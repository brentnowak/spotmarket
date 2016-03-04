-- Table: data.killmails

-- DROP TABLE data.killmails;

CREATE TABLE data.killmails
(
  "killmailID" serial NOT NULL,
  "killID" integer NOT NULL,
  "killHash" text NOT NULL,
  "killData" json,
  CONSTRAINT pk_killmails PRIMARY KEY ("killID", "killHash")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.killmails
  OWNER TO spotmarketadmin;
