#### edb.list.last

Извлекает из списка последний элемент. Преимущество перед `em.str.getWord` в том, что функция не использует цикл.

* `$args[0]` - Список вида `aaaa|bbbb|....|zzzzz`. Обязательный аргумент.
* `$args[1]` - разделитель. Если не указано: вертикальная черта `|`.

Возвращает значение элемента после последнего разделителя. Если разделителя в списке нет, возвращает исходное значение.

```qsp
@edb.list.last('id|body|count|place|include')	& ! 'include'
@edb.list.last('body|count|place|include')		& ! 'include'
@edb.list.last('count|place|include')			& ! 'include'
@edb.list.last('place|include')					& ! 'include'
@edb.list.last('include')						& ! 'include'
```
