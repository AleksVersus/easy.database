#### edb.dt.width

Функция для получения ширины таблицы данных.

Аргументы:

* `$args[0]` — идентификатор таблицы данных. Если не указан, используется идентификатор из указателя текущей таблицы.

Возвращает ширину таблицы данных (число), которое соответствует числу колонок. Работа этой функции основана на цикле.

> [!example] Пример:
> 
> ```qsp
> @edb.dt.width('objects')
> local width = @edb.dt.width()
> ```
