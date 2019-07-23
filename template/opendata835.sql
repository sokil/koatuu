CREATE SCHEMA opendata;

CREATE TABLE opendata.ukrstatOD17region (
	id                   char(2)  NOT NULL ,
	name                 varchar(100)  NOT NULL ,
	CONSTRAINT Pk_ukrstatOD17koatuu_0_id PRIMARY KEY ( id )
 );

COMMENT ON TABLE opendata.ukrstatOD17region IS 'Довідник областей';

COMMENT ON COLUMN opendata.ukrstatOD17region.id IS 'Level 1 code';

COMMENT ON COLUMN opendata.ukrstatOD17region.name IS 'Назва області або міста';

CREATE TABLE opendata.ukrstatOD17district (
	id                   char(4)  NOT NULL ,
	type                 integer  NOT NULL ,
	regionId             char(2)  NOT NULL ,
	name                 varchar(100)  NOT NULL ,
	CONSTRAINT Pk_ukrstatOD17district_id PRIMARY KEY ( id )
 );

COMMENT ON TABLE opendata.ukrstatOD17district IS 'Райони';

CREATE TABLE opendata.ukrstatOD17locality (
	koatuu               char(10)  NOT NULL ,
	type                 integer  NOT NULL ,
	districtId           char(4)  NOT NULL ,
	districtType         integer  NOT NULL ,
	regionId             char(2)  NOT NULL ,
	name                 varchar(255)  NOT NULL ,
	CONSTRAINT Pk_ukrstatOD17locality_koatuu PRIMARY KEY ( koatuu )
 );

CREATE INDEX Idx_ukrstatOD17locality_district ON opendata.ukrstatOD17locality ( districtId );

CREATE INDEX Idx_ukrstatOD17locality_region ON opendata.ukrstatOD17locality ( regionId );

ALTER TABLE opendata.ukrstatOD17district ADD CONSTRAINT Fk_ukrstatOD17district_ukrstatOD17region FOREIGN KEY ( regionId ) REFERENCES opendata.ukrstatOD17region( id );

ALTER TABLE opendata.ukrstatOD17locality ADD CONSTRAINT Fk_ukrstatOD17locality_ukrstatOD17district_district FOREIGN KEY ( districtId ) REFERENCES opendata.ukrstatOD17district( id );

ALTER TABLE opendata.ukrstatOD17locality ADD CONSTRAINT Fk_ukrstatOD17locality_ukrstatOD17region_region FOREIGN KEY ( regionId ) REFERENCES opendata.ukrstatOD17region( id );

INSERT INTO opendata.ukrstatOD17region VALUES {level1Values};

INSERT INTO opendata.ukrstatOD17district VALUES {level2Values};

INSERT INTO opendata.ukrstatOD17locality VALUES {level3Values};