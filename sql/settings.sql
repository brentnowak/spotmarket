-- Table: data.settings

-- DROP TABLE data.settings;

CREATE TABLE data.settings
(
  "settingID" serial NOT NULL,
  "version" text NOT NULL,
  CONSTRAINT pk_settings PRIMARY KEY ("settingID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.settings
  OWNER TO spotmarketadmin;

INSERT INTO data.settings("settingID", version)
VALUES (1, '0.3-dev');
