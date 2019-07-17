# Державний класифікатор об'єктів адміністративно-територіального устрою України (КОАТУУ)

State Classifier of objects of administrative and territorial structure of Ukraine

Converter from KOATUU database to SQL files.

Source database may be downloaded from:

* CSV, XLS: http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip
* JSON: https://data.gov.ua/dataset/d945de87-539c-45b4-932a-7dda57daf8d9/resource/296adb7a-476a-40c8-9de6-211327cb3aa1/download/koatuu.json

## Code structure

Code consists from 10 chars:

| Char number | Description |
| ---  | ------------- |
| 1,2  | Level 1 code  |
| 3    | Level 2 type  |
| 4,5  | Level 2 code  |
| 6    | Level 3 type  |
| 7,8  | Level 3 code  |
| 9,10 | Level 4 code  |

### Level 2 type (char 3)

| Char number | Description |
|---|---|
| 1 | міста обласного значення |
| 2 | райони Автономної Республіки Крим, області |
| 3 | райони міст, що мають спеціальний статус |

### Level 3 type (char 6)

| Char number | Description |
|---|---|
| 1 | міста районного значення |
| 2 | is unused |
| 3 | райони в містах обласного значення |
| 4 | селища міського типу, що входять до складу міськради |
| 5 | селища міського типу, що входять до складу райради |
| 6 | селища міського типу, що входять до складу райради в місті |
| 7 | міста, що входять до складу міськради |
| 8 | сільради, що входять до складу райради |
| 9 | сільради, села, що входять до складу райради міста, міськради |

### Example 

```
5320283602,С,ЗАПСІЛЛЯ
```
| Char number | Description | Value |
|---|---|---|
| 53 | level 1 code | ПОЛТАВСЬКА ОБЛАСТЬ/М.ПОЛТАВА)
| 2 | level 2 type | райони Автономної Республіки Крим, області)
| 02 | level 2 code | ВЕЛИКОБАГАЧАНСЬКИЙ РАЙОН/СМТ ВЕЛИКА БАГАЧКА)
| 8 | level 3 type | сільради, що входять до складу райради)
| 36 | level 3 code | ОСТАП'ЇВСЬКА/С.ОСТАП'Є |
| 02 | level 4 code | ЗАПСІЛЛЯ |

## Basic usage

1. Download new database from http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip and extract it;
2. Сonvert `KOATUU_xxxxxxxx.xls` file to `csv` format;
3. Run converter:
```
./convert.py --source KOATUU_26042018.csv --format=mysql --target "db.sql"
```

## See also

* [PHP library providing ISO codes with localization: country (ISO 3166-1), subdivision (ISO 3166-2), language (ISO 639-3), currency (ISO 4217) and scripts (ISO 15924)](https://github.com/sokil/php-isocodes)


