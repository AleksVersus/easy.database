#### edb.row.print

Вывод содержимого указанной строки.

Аргументы:

* `$args[0]` - идентификатор строки. Если не указан, используется идентификатор из указателя текущей строки.
* `$args[1]` - идентификатор таблицы данных. Если не указан, используется идентификатор из указателя текущей таблицы.

> [!example] Пример:
> 
> ```qsp
> @edb.row.print($i, 'objects')
> ```
