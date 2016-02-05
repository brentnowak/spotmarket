-- Table: data.logs

-- DROP TABLE data.logs;

CREATE TABLE data.logs
(
  "logID" serial NOT NULL,
  "service" text NOT NULL,
  "severity" int NOT NULL,
  "detail" text NOT NULL,
  "timestamp" timestamp without time zone NOT NULL,
  CONSTRAINT pk_logs PRIMARY KEY ("logID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.logs
  OWNER TO spotmarketadmin;
