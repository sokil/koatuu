#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2014, Dmytro Sokil <dmytro.sokil@gmail.com>
# KOATUU database may be downloaded from http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.rar

import argparse
import csv
import os

LEVEL2_TYPE_DISTRICT_CITY = 1                   # міста обласного значення;
LEVEL2_TYPE_DISTRICT = 2                        # райони Автономної Республіки Крим, області;
LEVEL2_TYPE_SPECIAL_CITY_REGION = 3             # райони міст, що мають спеціальний статус.

LEVEL3_TYPE_REGION_CITY = 1                     # міста районного значення;
# Code 2 is unused
LEVEL3_TYPE_DISTRICT_CITY_REGION = 3            # райони в містах обласного значення;
LEVEL3_TYPE_CITY_URBAN_SETTLEMENT = 4           # селища міського типу, що входять до складу міськради;
LEVEL3_TYPE_REGION_URBAN_SETTLEMENT = 5         # селища міського типу, що входять до складу райради;
LEVEL3_TYPE_CITY_REGION_URBAN_SETTLEMENT = 6    # селища міського типу, що входять до складу райради в місті;
LEVEL3_TYPE_CITY = 7                            # міста, що входять до складу міськради;
LEVEL3_TYPE_REGION_SETTLEMENT = 8               # сільради, що входять до складу райради;
LEVEL3_TYPE_CITY_SETTLEMENT = 9                 # сільради, села, що входять до складу райради міста, міськради.

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--csv', metavar='csv_file', help='csv file to convert', required=True)
parser.add_argument('--sql', metavar='sql_file', help='sql file to export')
parser.add_argument('--level1Table', metavar='level1', help='name of level1 table', default='level1')
parser.add_argument('--level2Table', metavar='level2', help='name of level2 table', default='level2')
parser.add_argument('--level3Table', metavar='level3', help='name of level3 table', default='level3')
args = parser.parse_args()

# open reader
csv_file_handler = open(args.csv, 'rb')
csv_reader = csv.reader(csv_file_handler)

# skip first line
csv_reader.next()


# iterate
level1 = []
level2 = []
level3 = []

for row in csv_reader:
    name = row[2]
    code = '{0:010d}'.format(int(row[0]))
    level1_code = code[0:2]
    level2_type = int(code[2])
    level2_code = code[3:5]
    level3_type = int(code[5])
    level3_code = code[6:8]
    level4_code = code[8:]

    is_level1 = level2_type == 0
    is_level2 = level2_type == LEVEL2_TYPE_DISTRICT and level2_code != '00' and level3_type == 0
    is_level3_city = level2_type == LEVEL2_TYPE_DISTRICT_CITY and level2_code != '00' and level3_type == 0
    is_level3_settlement = level2_type in [LEVEL2_TYPE_DISTRICT, LEVEL2_TYPE_DISTRICT_CITY] and level3_type != 0 and level3_code != '00' and level4_code != '00'

    level1_id = level1_code
    level2_id = level1_code + level2_code
    level3_id = level1_code + level2_code + level3_code + level4_code

    # print " ".join([
    #     code,
    #     level1_code,
    #     str(level2_type),
    #     level2_code,
    #     str(level3_type),
    #     level3_code,
    #     level4_code,
    #     name
    # ])

    # grab level1
    if is_level1:
        level1_name = name.split('/')[0].lower().replace("'", '\\\'')
        level1.append("('" + "','".join([
            level1_id,
            level1_name
        ]) + "')")

    # grab level2
    elif is_level2:
        level2_name = name.split('/')[0].lower().replace("'", '\\\'')
        level2.append("('" + "','".join([
            level2_id,
            level1_id,
            level2_name
        ]) + "')")

    elif is_level3_city or is_level3_settlement:
        level3.append("('" + "','".join([
            code,
            level2_id,
            level1_id,
            name.replace("'", '\\\'')
        ]) + "')")



# close reader
csv_file_handler.close()

# prepare writer
if args.sql:
    sqlFile = args.sql
else:
    sqlFile = os.path.basename(args.csv).split(".")[0] + ".sql"

sql_file_handler = open(sqlFile, "w")
sql_file_handler.write("SET NAMES UTF8;")

# write table creation instructions
sql_file_handler.write(
"""
DROP TABLE IF EXISTS {level1Table};
CREATE TABLE {level1Table} (
    id int not null,
    name varchar(255),
    PRIMARY KEY (id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', level1Table = args.level1Table))

sql_file_handler.write(
"""
DROP TABLE IF EXISTS {level2Table};
CREATE TABLE {level2Table} (
    id int not null,
    level1_id int not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (level1_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', level2Table = args.level2Table))

sql_file_handler.write(
"""
DROP TABLE IF EXISTS {level3Table};
CREATE TABLE {level3Table} (
    id bigint not null,
    level2_id int not null,
    level1_id int not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (level2_id),
    KEY (level1_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', level3Table = args.level3Table))

# write level1 insert operations
sql_file_handler.write("""
INSERT INTO {level1Table} VALUES {level1};
""".format('', level1Table = args.level1Table, level1 = ",".join(level1)))

# write level2 insert operations
sql_file_handler.write("""
INSERT INTO {level2Table} VALUES {level2};
""".format('', level2Table = args.level2Table, level2 = ",".join(level2)))

# write level2 insert operations
sql_file_handler.write("""
INSERT INTO {level3Table} VALUES {level3};
""".format('', level3Table = args.level3Table, level3 = ",".join(level3)))
