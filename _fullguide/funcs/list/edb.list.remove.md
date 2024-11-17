#### edb.list.remove

Заменяет в списке первое вхождение, или все вхождения, указанного значения на новое значение, если указанное значение присутствует в списке.

Аргументы:

* `$args[0]` - Список вида `aaaa|bbbb|....|zzzzz`. Обязательный аргумент.
* `$args[1]` - старое значение.
* `$args[2]` - новое начение. Если не указано, элемент удаляется из списка.
* `$args[3]` - управление:
	* `[nclr]` или `[no clear]` - пустые значения между разделителями не удаляются.
	* `[of]` или `[only first]` - заменяется только первое вхождение указанного значения.

Возвращает видоизменённый список.

> [!example] Примеры:
> 
> ```qsp
> @edb.list.remove('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA')
> !                    'BBB|CCC|BBB|DDD|EEE'
> @edb.list.remove('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA', 'aaa')
> !                'aaa|BBB|CCC|aaa|BBB|DDD|EEE'
> @edb.list.remove('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA', '', '[no clear]')
> !                   '|BBB|CCC||BBB|DDD|EEE'
> @edb.list.remove('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA', '', '[only first]')
> !                    'BBB|CCC|AAA|BBB|DDD|EEE'
> ```
