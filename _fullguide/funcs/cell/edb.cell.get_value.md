#### edb.cell.get_value

Возвращает значение ячейки.

Аргументы:

* `$args[0]` - идентификатор строки. Если не указан, используется идентификатор из указателя текущей строки.
* `$args[1]` - идентификатор колонки. Если не указан, используется идентификатор из указателя текущей колонки.
* `$args[2]` - идентификатор таблицы данных. Если не указан, используется идентификатор из указателя текущей таблицы.

> [!example] Пример:
> 
> ```qsp
> @edb.cell.get_value($i, 'place', 'objects')
> @edb.cell.get_value($s, 'place')
> @edb.cell.get_value()
> ```