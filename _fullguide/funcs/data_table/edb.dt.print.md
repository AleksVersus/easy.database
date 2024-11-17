#### edb.dt.print

Выводит на печать или возвращает человекочитаемое описание таблицы данных.

Аргументы:

* `$args[0]` — идентификатор таблицы данных. Если не указывать, используется текущий.
* `$args[1]` — управление:
	* `[oi]`, `[only info]` — будет возвращена только информация о таблице данных
	* `[ot]`, `[only table]` — будет возвращёна только html-таблица с содержимым таблицы данных.
		* `[range:N-M]` — будут возвращены только строки с N по M включительно.
	* если предыдущие опции не указаны, возвращается и информация и html-таблица с содержимым.

Примеры вызова:

```qsp
@edb.dt.print('objects')
@edb.dt.print('objects', '[only info]')
@edb.dt.print('objects', '[ot] [range:2-4]')
```