#### edb.list.append

Добавляет новый элемент в конец списка.

* `$args[0]` - Список вида `aaaa|bbbb|....|zzzzz`. Обязательный аргумент.
* `$args[1]` - элемент, добавляемое значение. Обязательный аргумент.
* `$args[2]` - разделитель. Если не указано: вертикальная черта `|`.

Возвращает новый список с добавленным элементом, либо, если исходный список пуст, возвращает указанный элемент.

```qsp
@edb.list.append('', 'id')							& ! 'id'
@edb.list.append('id', 'body')						& ! 'id|body'
@edb.list.append('id|body', 'count')				& ! 'id|body|count'
@edb.list.append('id|body|count', 'place')			& ! 'id|body|count|place'
@edb.list.append('id|body|count|place', 'include')	& ! 'id|body|count|place|include'
```
