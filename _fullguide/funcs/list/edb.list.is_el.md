#### edb.list.is_el

Проверяет наличие указанного элемента в списке.

Аргументы:

* `$args[0]` - Список вида `aaaa|bbbb|....|zzzzz`. Обязательный аргумент.
* `$args[1]` - элемент, искомое значение. Обязательный аргумент.

Возвращает единицу, если элемент в списке присутствует. Если элемента в списке нет, возвращает 0.

> [!example] Примеры:
> 
> ```qsp
> @edb.list.is_el('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA') & ! 1
> @edb.list.is_el('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'BBB') & ! 1
> @edb.list.is_el('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'FFF') & ! 0
> @edb.list.is_el('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'EEE') & ! 1
> ```
