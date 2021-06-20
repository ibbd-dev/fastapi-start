# Python开发最佳实践

## 1. 基础规范

- [PEP8规范](https://pep8.org/)
- [PEP8中文版（版本略旧）](https://alvinzhu.xyz/2017/10/07/python-pep-8/)
- [遵循Google的开源项目风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)

补充：

- Python版本选择3.8或者以上；
- 在pep8中代码行的字符串限制为80个字符，这个在有点少，我们放宽到110个字符。

## 2. 类型提示

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

### 2.4 生成器类型

函数返回生成器时，应该定义明确的返回值类型：

```python
from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a+b

print(next(fib(5)))
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

可以使用`mypy`这个工具，这个工具已经集成进`fastapi-start`脚手架里了。

