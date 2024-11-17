#### edb.list.for_each

Функция перебора элементов списка с вызовом функции, переданной в виде текстового значения.

* `$args[0]` - список вида `aaaa|bbbb|....|zzzzz`.
* `$args[1]` - функция, применяющаяся к каждому элементу списка (условный колбэк).
* `$args[2]` - разделитель. Если не указано: вертикальная черта `|`.
* `$args[3]` ... `$args[18]` - аргументы, транслируемые в функцию-колбэк.

Данная функция циклически перебирает все элементы списка, вызывая переданную в виде текстового значения функцию (условный колбэк) через `$dyneval`. При этом в `$dyneval` в нулевом аргументе передаётся значение - элемент списка, а во все остальные аргументы транслируются значения из аргументов с 3-его по 18-ый. Это позволяет использовать переданную в виде текстового значения функцию, как колбэк, и таким образом гибко обрабатывать элементы списка.

`edb.list.for_each` может возвращать текстовое (только текстовое!) значение, получаемое путём склейки (конкатенация) полученных из колбэка значений. Если колбэк не возвращает никаких значений, `edb.list.for_each` так же ничего не вернёт.

Все аргументы, принимаемые колбэком, должны передаваться в текстовом виде, поэтому если вам нужно передать в колбэк число, сначала преобразуйте его в строковое значение. В колбэке строку снова можно преобразовать в число.

В колбэк всегда предаётся 16 аргументов от `$args[0]` до `$args[15]`, учитывайте это при оформлении колбэка. Соответствие аргументов, переданных в `edb.list.for_each`, аргументам в колбэке:

* `$args[0]` - значение, элемент списка,
* `$args[1] = $args[3]`
* `$args[2] = $args[4]`
* `$args[3] = $args[5]`
* `$args[4] = $args[6]`
* и т.д.

Примеры:

```qsp

$list_ = 'AAA|BBB|CCC|AAA|BBB|DDD|EEE'

! склейка значений списка, с исключением 'AAA':

$callback_ = { $result = iif($args[0] = 'AAA', '', $args[0]) }

*pl @edb.list.for_each($list_, $callback_)

! 'BBBCCCBBBDDDEEE'

! подсчёт числа элементов списка

$callback_ = { $result = '0' }
*pl len(@edb.list.for_each($list_, $callback_))

! 7

! реверс элементов списка

local $reverse_ = ''
$callback_ = { $reverse_ = '|' + $args[0] + $reverse_ }
@edb.list.for_each($list_, $callback_)
*pl $mid($reverse_, 2)

! 'EEE|DDD|BBB|AAA|CCC|BBB|AAA'
```