## на подумать:
- [ ] Почему не собрать словарь на базе одной переменной?
    ```qsp
    local $__dict__
    $__dict__['kind', 'type'] = 'str'
    $__dict__['kind', 'value'] = 'деревянная_булава'
	$__dict__['name', 'type'] = 'str'
	$__dict__['name', 'value'] = 'Дубина|Дубины|Дубине|Дубину|Дубиной|Дубине'
	$__dict__['np', 'type'] = 'str'
	$__dict__['np', 'value'] = 'оружие|одноручное|булава'
	$__dict__['color', 'type'] = 'str'
	$__dict__['color', 'value'] = '663300'
	$__dict__['number', 'type'] = 'num'
	__dict__['number', 'value'] = 1
	$__dict__['stoim', 'type'] = 'num'
	__dict__['stoim', 'value'] = 176
	$__dict__['weight', 'type'] = 'num'
	__dict__['weight', 'value'] = 50
	$__dict__['uron', 'type'] = 'dict'
	$__dict__['uron', 'value'] = {local $__dict__
	$__dict__['дробящий', 'type'] = 'num'
	$__dict__['дробящий', 'value'] = '1000'
	$__dict__['стрелковый', 'type'] = 'num'
	$__dict__['стрелковый', 'value'] = '125'
	}
	```
	Это упростит работу со словарём, хотя не его генерацию.