#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2019, Dmytro Sokil <dmytro.sokil@gmail.com>
# KOATUU database may be downloaded from http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip
#
# KOATUU format:
# 5320283602,С,ЗАПСІЛЛЯ
# where:
#   - 53: level 1 code
#   - 2:  level 2 type
#   - 02: level 2 code
#   - 8:  level 3 type
#   - 36: level 3 code
#   - 02: level 4 code
#

import argparse
import xlrd
import csv
import os
import io
import sys

LEVEL2_TYPE_DISTRICT_CITY = 1                   # міста обласного значення;
LEVEL2_TYPE_DISTRICT = 2                        # райони Автономної Республіки Крим, області;
LEVEL2_TYPE_SPECIAL_CITY_REGION = 3             # райони міст, що мають спеціальний статус.

LEVEL3_TYPE_REGION_CITY = 1                     # міста районного значення;
# Level 3 Code 2 is unused
LEVEL3_TYPE_DISTRICT_CITY_REGION = 3            # райони в містах обласного значення;
LEVEL3_TYPE_CITY_URBAN_SETTLEMENT = 4           # селища міського типу, що входять до складу міськради;
LEVEL3_TYPE_REGION_URBAN_SETTLEMENT = 5         # селища міського типу, що входять до складу райради;
LEVEL3_TYPE_CITY_REGION_URBAN_SETTLEMENT = 6    # селища міського типу, що входять до складу райради в місті;
LEVEL3_TYPE_CITY = 7                            # міста, що входять до складу міськради;
LEVEL3_TYPE_REGION_SETTLEMENT = 8               # сільради, що входять до складу райради;
LEVEL3_TYPE_CITY_SETTLEMENT = 9                 # сільради, села, що входять до складу райради міста, міськради.

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--source', help='Source file to convert', required=True)
parser.add_argument('--target', help='Target file to convert')
parser.add_argument('--format', help='Format of target file. Available values: mysql, postgres', default='mysql')
parser.add_argument('--level1Table', help='Name of level1 table', default='level1')
parser.add_argument('--level2Table', help='Name of level2 table', default='level2')
parser.add_argument('--level3Table', help='Name of level3 table', default='level3')
args = parser.parse_args()


# CSV reader
def create_csv_reader(filename):
    # open reader
    csv_file_handler = open(filename, 'rb')
    csv_reader = csv.reader(csv_file_handler)

    # skip first line
    csv_reader.next()

    for csv_row in csv_reader:
        yield (unicode(csv_row[0], 'utf8'), unicode(csv_row[1], 'utf8'), unicode(csv_row[2], 'utf8'))

    # close reader
    csv_file_handler.close()


def create_xls_reader(filename):
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    for row_id in range(1, sheet.nrows):
        xls_row = sheet.row_values(row_id)

        if not xls_row[0]:
            continue

        yield (xls_row[0], xls_row[1], xls_row[2])


def sql_insert_value_formatter(arguments):
    return u"('" + u"','".join(arguments) + "')"


# Create reader
source_format = os.path.splitext(args.source)[1]

if source_format == '.csv':
    reader = create_csv_reader(args.source)
elif source_format == '.xls':
    reader = create_xls_reader(args.source)
else:
    print("Source file not supported")
    sys.exit(0)

# Target format
if args.format in ["mysql", "postgres"]:
    target_format_template_file_path = 'template/{format}.sql'.format('', format=args.format)
    target_file_ext = 'sql'
    value_formatter = sql_insert_value_formatter
else:
    print("Target file format not supported")
    sys.exit(0)

# iterate
level1Values = []
level2Values = []
level3Values = []

for row in reader:
    koatuu_object_code = '{0:010d}'.format(int(row[0]))
    koatuu_object_category = row[1]  # С - село, Щ - селище, Т - селище міського типу, М - місто, Р - район міста
    koatuu_object_name = row[2]

    level1_code = koatuu_object_code[0:2]
    level2_type = int(koatuu_object_code[2])  # See LEVEL2_TYPE_* constants
    level2_code = koatuu_object_code[3:5]
    level3_type = int(koatuu_object_code[5])  # See LEVEL3_TYPE_* constants
    level3_code = koatuu_object_code[6:8]
    level4_code = koatuu_object_code[8:]

    is_level3_city = level2_type == LEVEL2_TYPE_DISTRICT_CITY and level2_code != '00' and level3_type == 0
    is_level3_settlement = level2_type in [LEVEL2_TYPE_DISTRICT, LEVEL2_TYPE_DISTRICT_CITY] and level3_type != 0 and level3_code != '00' and level4_code != '00'

    level1_table_row_id = level1_code
    level2_table_row_id = level1_code + level2_code

    # grab level1
    if level2_type == 0:
        level1Values.append(value_formatter([
            level1_table_row_id,
            koatuu_object_name.split('/')[0].lower().replace("'", '\\\'')
        ]))

    # grab level2
    elif level2_type == LEVEL2_TYPE_DISTRICT and level2_code != '00' and level3_type == 0:
        level2Values.append(value_formatter([
            level2_table_row_id,
            str(level2_type),
            level1_table_row_id,  # references level 1 table
            koatuu_object_name.split('/')[0].lower().replace("'", '\\\'')
        ]))

    elif is_level3_city or is_level3_settlement:
        level3Values.append(value_formatter([
            koatuu_object_code,
            str(level3_type),
            level2_table_row_id,  # references level 2 table
            str(level2_type),
            level1_table_row_id,  # references level 1 table
            koatuu_object_name.replace("'", '\\\'')
        ]))

# prepare target file template
template = open(target_format_template_file_path).read()

# prepare writer
if args.target:
    targetFile = args.target
else:
    targetFile = os.path.basename(args.source).split(".")[0] + "." + target_file_ext

target_file_handler = io.open(targetFile, "w", encoding="utf-8")

# write table creation instructions
target_file_handler.write(
    template.format(
        '',
        level1TableName=args.level1Table,
        level2TableName=args.level2Table,
        level3TableName=args.level3Table,
        level1Values=u",".join(level1Values),
        level2Values=u",".join(level2Values),
 add --all .        level3Values=u",".join(level3Values)
    )
)
