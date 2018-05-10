# Державний класифікатор об'єктів адміністративно-територіального устрою України (КОАТУУ)

State Classifier of objects of administrative and territorial structure of Ukraine

Converts CSV database to SQL files.

Database may be downloaded from http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip

Last update: 26.04.2018

Basic useage
------------

Download new database from http://www.ukrstat.gov.ua/klasf/st_kls/koatuu.zip, convert `KOATUU_xxxxxxxx.csv` file to `csv` format, and run converter:

```
./convert.py --csv KOATUU_26042018.csv
```

See also
--------

* [PHP library providing ISO codes with localization: country (ISO 3166-1), subdivision (ISO 3166-2), language (ISO 639-3), currency (ISO 4217) and scripts (ISO 15924)](https://github.com/sokil/php-isocodes)


