#### edb.list.first

Извлекает из списка первый элемент. Преимущество перед `em.str.getWord` в том, что функция не использует цикл.

* `$args[0]` - Список вида `aaaa|bbbb|....|zzzzz`. Обязательный аргумент.

Возвращает значение элемента до первого разделителя. Если разделителя в списке нет, возвращает исходное значение.

```qsp
@edb.list.first('id|body|count|place|include')	& ! 'id'
@edb.list.first('body|count|place|include')		& ! 'body'
@edb.list.first('count|place|include')			& ! 'count'
@edb.list.first('place|include')				& ! 'place'
@edb.list.first('include')						& ! 'include'
```