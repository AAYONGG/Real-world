# test_boundary.py
from pickle_test_base import YieldTestBase


# 自定义类示例


class InheritedInt(int):
    pass


class SlotClass:
    __slots__ = ['a', 'b']

    def __init__(self):
        self.a = 1
        self.b = 2


def deep_list(depth):
    if depth == 0:
        return 0
    return [deep_list(depth - 1)]


class Collide:
    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, Collide)


def nested(depth):
    if depth == 0:
        return 0
    return [nested(depth - 1)]


class TestBoundaryValues(YieldTestBase):
    def generate_data(self):
        """考虑pickle序列化边界影响的数据"""

        # 原始测试数据
        long_str_255 = "a" * 255  # SHORT_BINUNICODE
        long_str_256 = "a" * 256  # BINUNICODE
        long_list_255 = list(range(255))
        long_list_256 = list(range(256))

        long_dict_255 = {str(i): i for i in range(255)}
        long_dict_256 = {str(i): i for i in range(256)}

        big_int = 2 ** 63  # long int 编码变化
        small_int = -2 ** 63

        float_nan = float('nan')
        float_inf = float('inf')
        float_neg_inf = float('-inf')

        bytes_edge = bytes(range(256))
        bytearray_edge = bytearray(range(256))

        # 新增边界样例
        float_subnormal = 5e-324  # IEEE 754 subnormal number (double)
        float_large_hex = float.fromhex('0x1.fffffffffffffp+1023')  # 最大正规数
        float_nan_payload = float.fromhex('nan')  # nan payload

        # 递归结构
        recursive_list = []
        recursive_list.append(recursive_list)
        recursive_dict = {}
        recursive_dict['self'] = recursive_dict

        deep_nested_1000 = nested(300)  # 极深嵌套列表

        # 超大集合和hash冲突集合
        collide_set = {Collide() for _ in range(1000)}

        # 多重引用示例
        shared_obj = [1, 2, 3]
        multi_ref_list = [shared_obj, shared_obj, shared_obj]

        # Unicode 边界字符串
        unicode_surrogate = "\ud800\udfff"  # 非常规代理对（低位高位）


        # 返回所有数据
        return [
            # 之前你测试过的数据
            long_str_255,
            long_str_256,
            long_list_255,
            long_list_256,
            long_dict_255,
            long_dict_256,
            big_int,
            small_int,
            float_nan,
            float_inf,
            float_neg_inf,
            bytes_edge,
            bytearray_edge,
            0, 1, 127, 128, 255, 256,
            2 ** 31 - 1, -2 ** 31, 2 ** 63 - 1, -2 ** 63,
            0.0, -0.0, 1.0, -1.0, 1e-300, 1e300,
            float('inf'), float('-inf'), float('nan'),
            "",
            "a" * 31,
            "a" * 32,
            "a" * 255,
            "a" * 256,
            "a" * 65535,
            "a" * 65536,
            b"",
            b"a" * 31,
            b"a" * 32,
            b"a" * 255,
            b"a" * 256,
            [],
            [1],
            list(range(255)),
            list(range(256)),
            list(range(257)),
            {},
            {"a": 1},
            {i: i for i in range(255)},
            {i: i for i in range(256)},
            set(),
            {1},
            {i for i in range(255)},
            {i for i in range(256)},
            None,
            True,
            False,
            [None, True, False],
            {"x": None, "y": True, "z": False},
            deep_list(10),
            deep_list(100),

            # 新拓展的边界数据
            float_subnormal,
            float_large_hex,
            float_nan_payload,
            recursive_list,
            recursive_dict,
            deep_nested_1000,
            collide_set,
            SlotClass(),
            InheritedInt(42),
            multi_ref_list,
            unicode_surrogate,
        ]
