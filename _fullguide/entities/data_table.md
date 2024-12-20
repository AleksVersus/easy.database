### Таблица Данных. Data Table

Таблица данных — это наибольшая структурная единица базы данных. Именно из множества таблиц данных состоит вся база данных игры.

Технически Таблица Данных — это набор массивов, каждый из которых является столбцом такой таблицы. Соответственно строкой можно считать ряд записей во все массивы Таблицы Данных под одним индексом.

Непосредственно, как сущность, Таблица Данных представлена в виде массива, имя которого совпадает с названием идентификатора таблицы данных. В этом массиве хранятся некоторые настройки, позволяющие управлять таблицей данных.

#### Методы

Методы Таблицы Данных представлены в виде соответствующих функций. С подробным описанием можно ознакомиться в разделе ["Функции модуля"](#).

* `set_cur` - устанавливает указанную таблицу данных в качестве текущей. (`edb.dt.set_cur`).
* `print` - выводит на экран, или возвращает в виде результата, человекочитаемую информацию об указанной таблице данных. (`edb.dt.`).
* `new_col` - создаёт в таблице данных колонку с указанным идентификатором. (`edb.dt.new_col`).
* `del_col` - удаляет из таблицы данных колонку с указанным идентификатором. (`edb.dt.del_col`).
* `new_row` - создаёт в таблице данных строку и возвращает её идентификатор. (`edb.dt.new_row`).
* `del_row` - удаляет из таблицы данных строку с указанным идентификатором. (`edb.dt.del_row`).
* `height` - возвращает высоту таблицы данных, то есть число строк. (`edb.dt.height`).
* `width` - возвращает ширину таблицы данных, то есть число колонок. (`edb.dt.width`).
* `find` - возвращает идентификатор строки, в которой найдено указанное значение. Данный метод позволяет использовать дополнительные фильтры для более точного поиска информации в таблице данных. (`edb.dt.find`).
* `clear` - удаляет все строки в указанной таблице данных. (`edb.dt.clear`).
* `clone` - копирует таблицу данных, или её часть, в новую таблицу данных. (`edb.dt.clone`).

#### Свойства

Свойства таблицы данных соответствуют значениям в массиве, имя которого совпадает с идентификатором таблицы данных. См. функцию [`edb.new_table`](#edb.new_table). Помимо этого механизмы "easy.database" используют не обозначенные в данном массиве свойства:

* высота таблицы данных — определяется числом строк в таблице данных. Технически получается из размера массива, соответствующего колонке первичных ключей.
* ширина таблицы данных — число колонок в таблице данных.
* последний первичный ключ — индекс последней в таблице данных строки.
