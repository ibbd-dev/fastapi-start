# Python开发最佳实践

## 1. 基础规范

- [PEP8规范](https://pep8.org/)
- [PEP8中文版（版本略旧）](https://alvinzhu.xyz/2017/10/07/python-pep-8/)
- [遵循Google的开源项目风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)

补充：

- Python版本选择3.8或者以上；
- 在pep8中代码行的字符串限制为80个字符，这个在有点少，我们放宽到110个字符。

### 1.1 一些之前不太注意的规范

以下几个规范来源官方文档：

- 不要讲lambda定义的匿名函数赋值给一个变量

Yes:

```python
def f(x): return 2*x
```

No:

```python
f = lambda x: 2*x
```

- 不要讲return语句也放在`try...except`中

Yes:

```python
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```

No:

```python
try:
    # Too broad!
    return handle_value(collection[key])
except KeyError:
    # Will also catch KeyError raised by handle_value()
    return key_not_found(key)
```

- 优先使用`startswith`, `endswith`, `isinstance`等

Yes:

```python
if foo.startswith('bar'):
```

No:

```python
if foo[:3] == 'bar':
```

## 2. 类型提示

- [Python Type Checking (Guide)](https://realpython.com/python-type-checking/)

### 2.1 简单类型

Python的简单类型包括：布尔值，整型，浮点型，字符串。

```python
from typing import Optional

# 定义一个字符串类型
name: str = 'world'
# 待缺省值的字符串
name: Optional[str] = None
```

还有些特殊的用法：

- 对于不定的类型可以使用`Any`
- 如果一个变量可以同时是多个类型，则可以使用`Union`，例如`Union[str, int]`

语法上可以这样使用，不过我们并建议这样子使用，一个变量应该只有一个类型。对于不确定的类型，在使用时，应该先进行类型判断，如：

```python
from typing import Any

def test(var: Any = None) -> None:
    if var is None:
        var = 'world'
    if type(var) == str:
        print(f'Hello {var}')
    elif type(var) == int:
        print(20 + var)
    else:
        # do somethings...
```

### 2.2 复杂类型

所说的复杂类型，主要包括元组，列表，组合，字典等。对于这些类型，我们应该定义清楚每一个值。

```python
from typing import Tuple, List, Set, Dict, Optional

# 对于元组应该定义清楚每个元素的类型
data1: Tuple[str, int, int] = ('date', 2021, 6)

# 在python中列表中的元素可以是不一样的，
# 不过我们列表的元素应该是只有一种类型的，
# 元素包含多种类型的列表，会让列表变得很复杂
# 集合也是类似。
data2: List[int] = [1, 2, 3]

# 对于字典，我们应该定义清楚每个键和值的类型
# 以下定义一个键为str，值为int的字典
data3: Dict[str, int] = {'age': 23}

# 下面这个规范是不符合规范的
data4: Dict[str, int] = {'age': 23.5}
```

### 2.3 枚举类型

枚举类型通常在数据表的字段中，定义的时候应该使用明确的枚举类型。枚举类型简单用法如下：

```python
from enum import Enum, IntEnum

class Color(IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Status(Enum):
    SUCC = 'succ'
    FAIL = 'fail'

# 获取键和值
print(Color.RED.value)
print(Status.SUCC.value)
print(Color.RED.name)
print(Status.SUCC.name)
```

枚举类型的派生类型：

```python
from enum import Flag, auto
class Color(Flag):
    RED = auto()
    BLUE = auto()
    GREEN = auto()

print(Color.RED.value)
print(Color.BLUE.value)
print(Color.BLUE | Color.RED)   # 输出: ColorFlag.BLUE|RED
print((Color.BLUE & Color.RED).value)   # 输出: 0
```

标记类型和枚举类型貌似没有多大的区别，不过标记类型可以支持逻辑运算（暂时没看到更多的使用场景）。

### 2.4 其他一些特别的类型


```python
from typing import Iterator, NoReturn

# 函数返回生成器时，应该定义明确的返回值类型（生成器类型）：
def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a+b

print(next(fib(5)))

# 当函数没有明确的返回时，明确定义
def black_hole() -> NoReturn:
    raise Exception("There is no going back ...")
```

### 2.5 自定义类型

使用自定义类型能让代码可读性增强，毕竟int，str等都只是没有过多实际意义的词，而自定义的类型就不一样了，能定义明确的含义。

```python
from typing import NewType

# 定义：用户ID类型
UserID = NewType('UserID', int)
# 自定义一个类型
a: UserID = UserID(210)
# 下面这个语法上不会报错，
# 但是这是不规范的
b: UserID = UserID('test')
```

对于有些状态值或者类型之类的变量，如果都定义成枚举类型，也是挺麻烦的，使用自定义类型也能让代码可读性增强。

### 2.6 静态类型检查器

可以使用`mypy`这个工具，这个工具已经集成进`fastapi-start`脚手架里了:

```sh
fas check mypy /path/to/filename.py
```

不过测试使用下来，这个工具不是太智能，未必都应该修复。

## 3. 关于doctest测试

使用doctest进行函数测试及模块测试，使用如：

```python
"""
# 模块测试
>>> test(10)
21
"""

def test(i: int) -> int:
    """函数测试
    >>> test(10)
    20
    """
    return i * 2

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

- 函数应该写一些简单的单元测试，有一定的优势，这样会变成文档的一部分，带有example的作用。
- 在模块上使用doctest并没有太多的优势，还不如写在`if __name__ == "__main__"`。
- 不过doctest没法实现复杂的测试，那还是得用专用的单元测试工具。而且doctest并不只是校验返回值，如果在函数了加了一个print，就会导致测试不通过，不太友好。

所以，**doctest仅作为example是不错的，单元测试还是应该使用更加专业的工具**。

## 4. 单元测试

对于单元测试，我们的总的原则是：单元测试要写，但是又不能将单元测试搞得太复杂，花太多的精力在这上面。

单元测试工具选用`pytest`（这个工具和`go test`有点类似），简单的使用：

```python
# 文件: example.py
def func(i: int) -> int:
    return i * 2

# 文件: example_test.py
from .example import func
def test_func():
    assert func(10) == 20
    assert func(20) == 30
```

在相同的目录下执行命令`pytest`，该命令会自动找到`*_test.py`的文件（注意：当前目录需要文件__init__.py）执行测试用例。显然这个单元测试是不通过的，报错信息如下：

```python
    def test_func():
        assert func(10) == 20
>       assert func(20) == 30
E       assert 40 == 30
E        +  where 40 = func(20)

doctest_example_test.py:7: AssertionError
```

`pytest`可以递归自动发现测试文件，在使用过程中，也支持执行指定用例：

- 指定测试文件路径 `pytest /path/to/test/file.py`
- 指定测试类 `pytest /path/to/test/file.py:TestCase`
- 指定测试方法 `pytest another.test::TestClass::test_method`
- 指定测试函数 `pytest /path/to/test/file.py:test_function`
- 指定测试函数（输出print日志信息） `pytest -s /path/to/test/file.py:test_function`

关于单元测试，我们定义几个**使用规范**：

1. 我们写的函数或者类等，要时刻保持可测试的状态（或者说叫可观测状态）。
2. 测试用例文件名要对应，例如文件名为`filename.py`，则对应的测试用例文件名为`filename_test.py`。
3. 测试函数名要对应，例如业务函数名为`func_name`，则对应的测试函数名为`test_func_name`。
4. 测试类名要对应，例如原类名为`ClassName`，则对应测试类名为`TestClassName`。
5. 建议测试用例文件和功能文件放在相同目录下，方便查找，通常不需要一个单独的测试目录。
6. 优先考虑使用参数化测试：

```python
# 前面那个测试用例其实应该优化成这样：
import pytest

# 这里数据的部分完全可以定义成一个变量
# 这样就不必重复写很多个assert语句了
@pytest.mark.parametrize("params, expected", [([10], 20), ([20], 30)])
def test_func2(params, expected):
    assert func(*params) == expected
```

同样，执行之后，测试也是不通过的：

```python
    @pytest.mark.parametrize("params, expected", [([10], 20), ([20], 30)])
    def test_func2(params, expected):
>       assert func(*params) == expected
E       assert 40 == 30
E        +  where 40 = func(*[20])

doctest_example_test.py:18: AssertionError
```

如果把这个`parametrize`函数进行封装的话，应该可以做到更加简单，例如单元测试只要描述输入输出即可：

```python
test_data = [
    (func, [10], {}, 20),
    (func, [20], {}, 30)
]

@pytest.mark.parametrize("action, args, kwargs, expected", test_data)
def test_all_func(action, args, kwargs, expected):
    assert action(*args, **kwargs) == expected
```

这样，只要专注写好测试用例即可。

## 5. 数据库迁移

工具：Alembic

## 6. 异常重试

工具：tenacity

## 7
