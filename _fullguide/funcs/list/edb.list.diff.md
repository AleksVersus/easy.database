#### edb.list.diff

Функция получения разницы между двумя списками.

* `$args[0]` - уменьшаемый список вида `aaaa|bbbb|....|zzzzz`.
* `$args[1]` - вычитаемый список вида `aaaa|bbbb|....|zzzzz`.
* `$args[2]` - разделитель. Если не указано: вертикальная черта `|`.
* `$args[3]` - управление:
	* `[union]` или `[un]` - в этом режиме из обоих списков исключаются совпадающие значения, а все оставшиеся возвращаются в виде нового списка.

Возвращает новый список.

**Внимание!!!** Удаляется только первое совпадение в списке. Ввиду того, что функция не используется в модуле, она не доработана. Вы можете самостоятельно написать похожую функцию, используя иные функции работы со списками.

Примеры:

```qsp
@edb.list.diff('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA|BBB|CCC')					 & ! 'AAA|BBB|DDD|EEE'
@edb.list.diff('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA|DDD|EEE')					 & ! 'BBB|CCC|AAA|BBB'
@edb.list.diff('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'JJJ|FFF|GGG')					 & ! 'AAA|BBB|CCC|AAA|BBB|DDD|EEE'
@edb.list.diff('AAA|BBB|CCC|AAA|BBB|DDD|EEE', 'AAA|FFF|GGG|EEE', '|', '[union]') & ! 'BBB|CCC|AAA|BBB|DDD|FFF|GGG'
```
