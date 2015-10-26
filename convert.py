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
parser.add_argument('--districtsTable', metavar='districts', help='name of districts table', default='districts')
parser.add_argument('--regionsTable', metavar='regions', help='name of regions table', default='regions')
parser.add_argument('--citiesTable', metavar='cities', help='name of cities table', default='cities')
args = parser.parse_args()

# open reader
csv_file_handler = open(args.csv, 'rb')
csv_reader = csv.reader(csv_file_handler)

# skip first line
csv_reader.next()


# iterate
districts = []
regions = []
cities = []

for row in csv_reader:
    name = row[2]
    code = '{0:010d}'.format(int(row[0]))
    level1_code = code[0:2]
    level2_type = int(code[2])
    level2_code = code[3:5]
    level3_type = int(code[5])
    level3_code = code[6:8]
    level4_code = code[8:]

    is_district = level2_type == 0
    is_region = level2_type == LEVEL2_TYPE_DISTRICT and level2_code != '00' and level3_type == 0
    is_city = level2_type == LEVEL2_TYPE_DISTRICT_CITY and level2_code != '00' and level3_type == 0
    is_settlement = level2_type in [LEVEL2_TYPE_DISTRICT, LEVEL2_TYPE_DISTRICT_CITY] and level3_type != 0 and level3_code != '00' and level4_code != '00'

    district_id = level1_code
    region_id = level1_code + level2_code
    city_id = level1_code + level2_code + level3_code + level4_code

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

    # grab districts
    if is_district:
        district_name = name.split('/')[0].lower().replace("'", '\\\'')
        districts.append("('" + "','".join([
            district_id,
            district_name
        ]) + "')")

    # grab regions
    elif is_region:
        region_name = name.split('/')[0].lower().replace("'", '\\\'')
        regions.append("('" + "','".join([
            region_id,
            district_id,
            region_name
        ]) + "')")

    elif is_city or is_settlement:
        cities.append("('" + "','".join([
            code,
            region_id,
            district_id,
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
DROP TABLE IF EXISTS {districtsTable};
CREATE TABLE {districtsTable} (
    id int not null,
    name varchar(255),
    PRIMARY KEY (id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', districtsTable = args.districtsTable))

sql_file_handler.write(
"""
DROP TABLE IF EXISTS {regionsTable};
CREATE TABLE {regionsTable} (
    id int not null,
    district_id int not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (district_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', regionsTable = args.regionsTable))

sql_file_handler.write(
"""
DROP TABLE IF EXISTS {citiesTable};
CREATE TABLE {citiesTable} (
    id bigint not null,
    region_id int not null,
    district_id int not null,
    name varchar(255),
    PRIMARY KEY (id),
    KEY (region_id),
    KEY (district_id)
) DEFAULT CHARSET=UTF8 Engine=InnoDB;
""".format('', citiesTable = args.citiesTable))

# write district insert operations
sql_file_handler.write("""
INSERT INTO {districtsTable} VALUES {districts};
""".format('', districtsTable = args.districtsTable, districts = ",".join(districts)))

# write region insert operations
sql_file_handler.write("""
INSERT INTO {regionsTable} VALUES {regions};
""".format('', regionsTable = args.regionsTable, regions = ",".join(regions)))

# write region insert operations
sql_file_handler.write("""
INSERT INTO {citiesTable} VALUES {cities};
""".format('', citiesTable = args.citiesTable, cities = ",".join(cities)))
