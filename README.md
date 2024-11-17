# Easy.DataBase

Система управления базой данных "easy.database" — это модуль (библиотека), предназначенный для простого редактирования нереляционной базы данных на QSP.

Существует модуль Олегуса, реализующий то же самое, но через другие механизмы: https://forum.ifiction.ru/viewtopic.php?id=1522.

Исходный код "easy.database" всегда доступен по адресу: https://github.com/AleksVersus/easy.database

## Подключение

"easy.database" подключается как любой другой модуль QSP, то есть с использованием команды `inclib`. Скачайте архив со [страницы релизов](https://github.com/AleksVersus/easy.database/releases), распакуйте и скопируйте папку "`lib`" в папку с вашей игрой. Тогда на самой первой локации в игре достаточно будет прописать такую команду подключения:

```qsp
inclib 'lib/easy.database.qsp'
```

Для работы модуля требуется также подключить и библиотеку "easy.math". Она поставляется вместе с модулем. Подключение аналогичное:

```qsp
inclib 'lib/easy.math.qsp'
```

Если вы уже используете библиотеку "easy.math" в своей игре, убедитесь, что версия "easy.math" совместима с "easy.database". Для этого в первой строчке первой локации вашей игры используйте команду:

```qsp
@edb.em.version()
```

При запуске игры вы увидите на экране сообщение с номерами текущей и необходимой версий модуля "easy.math".

## Работа с исходниками

Если вы пишете игру, используя Sublime Text с подключённым пакетом QSP, у вас есть возможность самостоятельно собирать модуль из исходников.

В папке "`[source]`" размещены исходные тексты модуля, а так же файл "`qsp-project.json`", отредактировав который? вы наладите сборку модуля в папку с вашей игрой.

Так же вы можете собирать игру, напрямую включая в неё все локации модуля, если это необходимо. В этом случае вам не потребуется подключать модуль к игре — он уже будет в неё встроен.

В исходниках предусмотрены два режима сборки: без обработки препроцессором и с обработкой препроцессором.

- В первом случае модуль будет собран, как есть, включая все служебные комментарии и наборы "предохранителей" — сообщений в модальных окнах, которые предупреждают о некоторых наиболее распространённых ошибках при работе с модулем. Данный режим сборки необходим на этапе разработки, отладки и тестирования игры.
- Во втором случае необходимо включить препроцессор в "`qsp-project.json`", тогда из собранного модуля будут удалены все служебные комментарии, а так же блоки "предохранителей". Данный режим рекомендуется использовать при сборке релизной версии игры, когда большая часть ошибок уже отловлена.

Вы также можете включить препроцессор, но сохранить блоки предохранителей в конечной сборке модуля. Для этого в исходном файле "`00_edb.start.qsps`" в любом месте пропишите строку:

```qsp
!@pp:var(edb_fuse)
```

> [!warning] **Обратите внимание!**
> Исходники библиотеки "easy.math" необходимо скачивать отдельно: [easy.math на github](https://github.com/AleksVersus/easy.math.3)

## Подключение встроенного отладчика

Вы можете подключить отладочные команды модуля к командной строке (полю ввода), прописав в самом начале игры следующую команду:

```qsp
@edb.usercom('on')
```

Это добавит новый обработчик строки ввода к уже работающим. 

Все команды модуля должны начинаться с ключевого слова `edb`. Для вывода списка всех доступных команд, введите в строке ввода `edb help`.

Также список всех доступных команд для поля ввода представлен в разделе данной документации ["Команды отладки"](_fullguide/debug_commands.md).

## Особенности работы

Технически база данных представляет собой наборы массивов, описывающих таблицы данных, а так же массивы, реализующие поведение колонок в таблицах данных. Основные свойства базы данных записываются в массив `$EASY_DATABASE`.

Поскольку все массивы, входящие в базу данных являются глобальными, недопустимо использовать их в других местах игры. Ввиду чего необходимо чётко понимать, какие имена будут заняты под базу данных. Эту информацию можно проверить, воспользовавшись функцией `edb.print`, или через встроенный отладчик, введя команду `edb >`.

При создании таблицы данных инициализируется массив, название которого совпадает с названием идентификатора таблицы данных, поэтому требования к такому идентификатору такие же, как и к названию массива, плюс идентификатор не должен начинаться с символа `$` или `%`.

Также при создании таблицы данных автоматически генерируется колонка первичных ключей. Она является служебной, и с ней нельзя напрямую взаимодействовать (за исключением некоторых случаев), хотя технически это такой же массив, как и все прочие.

> [!abstract] Технически: 
> Колонка первичных ключей всегда представляет собой массив, название которого состоит из идентификатора таблицы данных и слова '`_id`'.
> > [!example] Примеры имён массивов, представляющих колонки первичных ключей для разных таблиц данных:
> > 
> > ```qsp
> > $objects_id
> > $dialogs_id
> > $potions_id
> > $temp_id
> > ```

Основные функции, реализующие работу с базой данных, представлены в виде локаций-функций. Названия всех таких локаций начинаются с `edb`. Для удобства чтения кода названия локаций содержат точки, это не мешает использовать их при неявном вызове `func`:

```qsp
@edb.row.fill('Старый меч', 'сумка', 1, [$i, 'objects'])
```

Также для улучшения семантики в названиях локаций-функций указывается сущность, с которой они работают, и только затем непосредственно названия функций. Исключение составляют функции, работающие непосредственно с сущностью базы данных:

```qsp
@edb.init()
@edb.print('[all arrays]')
```

В базе данных работает система указателей, которые позволяют не писать в каждой команде полностью, с какой строкой, колонкой и таблицей сейчас нужно работать. Указатели автоматически изменяются по последнему явно прописанному значению.

Некоторые функции требуют предварительного заполнения указателей.

## Содержание руководства

- [**Сущности**](_fullguide/entities/index.md)
	- [База Данных. Data Base](_fullguide/entities/data_base.md)
	- [data_table](_fullguide/entities/data_table.md)
	- [column](_fullguide/entities/column.md)
	- [row](_fullguide/entities/row.md)
	- [cell](../cell.md)
	- [list](_fullguide/entities/list.md)
- **Функции модуля**
	- Функции для работы с сущностями БД
		- База Данных
			- [edb.init](_fullguide/funcs/data_base/edb.init.md)
			- [edb.print](_fullguide/funcs/data_base/edb.print.md)
			- [edb.new_table](_fullguide/funcs/data_base/edb.new_table.md)
			- [edb.del_table](_fullguide/funcs/data_base/edb.del_table.md)
		- Таблица Данных
			- [edb.dt.set_cur](_fullguide/funcs/data_table/edb.dt.set_cur.md)
			- [edb.dt.print](_fullguide/funcs/data_table/edb.dt.print.md)
			- [edb.dt.new_col](_fullguide/funcs/data_table/edb.dt.new_col.md)
			- [edb.dt.del_col](_fullguide/funcs/data_table/edb.dt.del_col.md)
			- [edb.dt.new_row](_fullguide/funcs/data_table/edb.dt.new_row.md)
			- [edb.dt.del_row](_fullguide/funcs/data_table/edb.dt.del_row.md)
			- [edb.dt.height](_fullguide/funcs/data_table/edb.dt.height.md)
			- [edb.dt.width](_fullguide/funcs/data_table/edb.dt.width.md)
			- [edb.dt.find](_fullguide/funcs/data_table/edb.dt.find.md)
			- [edb.dt.clear](_fullguide/funcs/data_table/edb.dt.clear.md)
			- [edb.dt.clone](_fullguide/funcs/data_table/edb.dt.clone.md)
		- Колонка
			- [edb.col.set_cur](_fullguide/funcs/column/edb.col.set_cur.md)
			- [edb.col.print](_fullguide/funcs/column/edb.col.print.md)
			- [edb.col.set_next](_fullguide/funcs/column/edb.col.set_next.md)
		- Строка
			- [edb.row.set_cur](_fullguide/funcs/row/edb.row.set_cur.md)
			- [edb.row.fill](_fullguide/funcs/row/edb.row.fill.md)
			- [edb.row.print](_fullguide/funcs/row/edb.row.print.md)
			- [edb.row.set_next](_fullguide/funcs/row/edb.row.set_next.md)
			- [edb.row.exchange](_fullguide/funcs/row/edb.row.exchange.md)
			- [edb.row.extract](_fullguide/funcs/row/edb.row.extract.md)
			- [edb.row.inject](_fullguide/funcs/row/edb.row.inject.md)
			- [edb.row.clone](_fullguide/funcs/row/edb.row.clone.md)
		- Ячейка
			- [edb.cell.set_value](_fullguide/funcs/cell/edb.cell.set_value.md)
			- [edb.cell.get_value](_fullguide/funcs/cell/edb.cell.get_value.md)
			- [edb.cell.add](_fullguide/funcs/cell/edb.cell.add.md)
	- Вспомогательные функции
		- Функции работы со списками
			- [edb.list.remove](_fullguide/funcs/list/edb.list.remove.md)
			- [edb.list.is_el](_fullguide/funcs/list/edb.list.is_el.md)
			- [edb.list.first](_fullguide/funcs/list/edb.list.first.md)
			- [edb.list.last](_fullguide/funcs/list/edb.list.last.md)
			- [edb.list.append](_fullguide/funcs/list/edb.list.append.md)
			- [edb.list.diff](_fullguide/funcs/list/edb.list.diff.md)
			- [edb.list.for_each](_fullguide/funcs/list/edb.list.for_each.md)
			- [edb.list.length](_fullguide/funcs/list/edb.list.length.md)
		- 
## Команды отладки

[**Команды отладки можно посмотреть здесь.**](_fullguide/debug_commands.md)

## История версий

[**Историю версий можно посмотреть здесь.**](_fullguide/lib_versions.md)
