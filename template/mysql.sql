SET NAMES UTF8;

DROP TABLE IF EXISTS {level1TableName};

CREATE TABLE {level1TableName} (
    id char(2) not null,
    name varchar(255),
    PRIMARY KEY (id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;

DROP TABLE IF EXISTS {level2TableName};

CREATE TABLE {level2TableName} (
    id char(4) not null,
    type int not null,
    level1_id char(2) not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (level1_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;

DROP TABLE IF EXISTS {level3TableName};

CREATE TABLE {level3TableName} (
    id char(10) not null,
    type int not null,
    level2_id char(4) not null,
    level2_type int not null,
    level1_id char(2) not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (level2_id),
    KEY (level1_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;

INSERT INTO {level1TableName} VALUES {level1Values};

INSERT INTO {level2TableName} VALUES {level2Values};

INSERT INTO {level3TableName} VALUES {level3Values};