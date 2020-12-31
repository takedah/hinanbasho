# 旭川市避難場所検索

旭川市ホームページからダウンロードした指定避難場所一覧CSVから、旭川市の指定避難場所を検索できるようにしたサービスです。

## Description

ToDo

## Requirement

- PostgreSQL
- flask
- gunicorn
- numpy
- pandas
- psycopg2
- requests

## Install

```bash
$ export HINANBASHO_DB_URL=postgresql://{user_name}:{password}@{host_name}/{db_name}
$ psql -f db/schema.sql -U {user_name} -d {db_name} -h {host_name}
$ make
```

## Usage

```bash
$ gunicorn run:app
```

## Lisence

Copyright (c) 2020 Hiroki Takeda
[MIT](http://opensource.org/licenses/mit-license.php)
