#### edb.dt.new_row

Создаёт строку в таблице данных, не заполняя её значениями.

Аргументы:

* `$args[0]` - идентификатор таблицы данных. Если не указан, используется идентификатор из указтеля текущей колонки.

Функция возвращает идентификатор созданной строки, для дальнейшего использования.

Генерируется первичный ключ, а затем происходит заполнение всех массивов, соответствующих колонкам таблицы данных, пустыми значениями, при этом индексы заполняемых ячеек равны сгенерированному первичному ключу.

> [!example] Пример:
> 
> ```qsp
> @edb.dt.new_row('objects')
> local $r = @edb.dt.new_row('objects')
> local $i = @edb.dt.new_row()
> @edb.dt.new_row()
> @edb.dt.new_row()
> ```