-- Table: data.charorders

-- DROP TABLE data.charorders;

CREATE TABLE data.charorders
(
  "characterID" integer NOT NULL,
  "orderID" bigint NOT NULL,
  "stationID" bigint NOT NULL,
  volentered integer NOT NULL,
  volremaining integer NOT NULL,
  minvolume integer NOT NULL,
  orderstate integer NOT NULL,
  "typeID" integer NOT NULL,
  range integer NOT NULL,
  accountkey integer NOT NULL,
  duration integer NOT NULL,
  escrow double precision NOT NULL,
  price double precision NOT NULL,
  bid boolean NOT NULL,
  issued timestamp without time zone NOT NULL,
  CONSTRAINT pk_charorders PRIMARY KEY ("characterID", "orderID")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE data.charorders
  OWNER TO spotmarketadmin;
