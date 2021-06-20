from typing import NewType

# 定义：用户ID类型
UserID = NewType('UserID', int)
# 自定义一个类型
a: UserID = UserID(210)
# 下面这个语法上不会报错，
# 但是这是不规范的
b: UserID = UserID('test')
