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

# 这样是不符合规范的
data4: Dict[str, int] = {'age': 23.5}