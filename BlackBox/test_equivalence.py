# test_equivalence.py
import os
from collections import OrderedDict

from pickle_test_base import YieldTestBase
import math


class Dummy:
    def __init__(self, x):
        self.x = x

    def __eq__(self, other):
        return isinstance(other, Dummy) and self.x == other.x


class TestEquivalencePartitioning(YieldTestBase):
    def generate_data(self):
        recursive_list = []
        recursive_list.append(recursive_list)

        recursive_dict = {}
        recursive_dict["self"] = recursive_dict

        path = os.path.join("tests", "data")

        return [
            123,
            123.456,
            "hello",
            b"bytes",
            True,
            None,  # 基本类型（不可变类型）
            [1, 2, 3],
            (4, 5, 6),
            {7, 8, 9},
            {"a": 1, "b": 2},  # 容器类型（标准数据结构）
            [[1, 2], [3, [4, 5]]],
            {"outer": {"inner": {"key": "value"}}},
            (1, [2, {"three": 3}], "four"),  # 嵌套结构
            Dummy(10),
            Dummy("abc"),  # 自定义对象（不可预测内部结构的序列化）
            math.sqrt,
            len,
            type,  # 特殊内建对象或匿名函数
            {"c", "b", "a"},
            frozenset(["x", "y", "z"]),  # 顺序敏感容器
            recursive_list,
            recursive_dict,
            [  # 混合结构
                {"nums": [1, 2.0, 3], "bool": True},
                (None, Dummy("test"), {"bytes": b"\xff\xfe"}),
            ],
            {'int': 42, 'float': 3.14, 'str': 'hello', 'bool': True, 'none': None},
            path
        ]
