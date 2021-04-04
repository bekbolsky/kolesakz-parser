# kolesakz-parser

Парсер грузовых автомобилей с kolesa.kz, с выгрузкой данных в формате csv

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
![GitHub](https://img.shields.io/github/license/bekbolsky/kolesakz-parser)

## Установка

Используйте пакетный менеджер `pip`

```sh
python3 -m pip install -r requirements.txt
```

## Запуск

```sh
python3 parser.py
```

## Пример выгружаемых данных

Парсер собирает такие данные:

- vehicle - Название техники
- year - Год выпуска
- price - Цена (₸)
- emergency - Техническое состояние техники
- fuel_type - Тип топлива
- engine_volume - Объем двигателя
- vehicle_type - Тип техники

_Если какая-то информация в объявлении не указана, то она будет пропущена и при выгрузке_

| vehicle                 | year    | price    | emergency  | fuel_type | engine_volume | vehicle_type |
| ----------------------- | ------- | -------- | ---------- | --------- | ------------- | ------------ |
| Mercedes-Benz           | 2008 г. | 7770000  | с пробегом | дизель    | 2.9 л         | фургон       |
| DAF 95                  | 2005 г. | 17000000 | с пробегом | дизель    | 4.8 л         |              |
| Mercedes-Benz 814       | 1992 г. | 5100000  | с пробегом | дизель    | 6 л           | фургон       |
| ЗиЛ 130                 | 1985 г. | 1250000  | с пробегом | бензин    | 5 л           | самосвал     |
| MAN                     | 1997 г. | 7000000  | с пробегом | дизель    |               | тягач        |
| Mercedes-Benz Варио 814 | 2000 г. | 5500000  | с пробегом | дизель    | 4.3 л         | фургон       |

## Лицензия

[MIT](https://choosealicense.com/licenses/mit/)
