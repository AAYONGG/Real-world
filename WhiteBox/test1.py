import io
import unittest
import myPickle as pickle1


class BadPickler(pickle1.Pickler):
    def __init__(self):
        # 跳过父类初始化
        pass


class PersistentPickler(pickle1.Pickler):
    def persistent_id(self, obj):
        # 对某个自定义对象返回持久化ID
        if isinstance(obj, MyPersistentObject):
            return f"id:{obj.name}"
        return None

    def save_pers(self, pid):
        print(f"[持久化保存] ID = {pid}")
        super().save_pers(pid)  # 默认写入 BINGET 等操作码


class MyPersistentObject:
    def __init__(self, name):
        self.name = name


class MyObj:
    def __init__(self, name):
        self.name = name


class MyReducible:
    def __reduce__(self):
        return MyReducible, ()  # 返回一个构造该对象的元组


class Dummy:
    def __init__(self, value):
        self.value = value


class CustomPickler(pickle1.Pickler):
    def reducer_override(self, obj):
        if isinstance(obj, Dummy):
            return Dummy, (obj.value,)

        elif obj == "special_string":
            # 返回一个字符串触发 save_global
            return "custom.module.name"
        elif obj == "not_tuple":
            return 123  # 非法类型，测试异常
        elif obj == "short_tuple":
            return ("only_one_element",)  # 长度不够，测试异常
        return NotImplemented


class TestPickleWhiteBox(unittest.TestCase):
    # 构造Pickler对象不设置 _file_write 属性触发PicklingError路径
    def test_missing_file_write(self):
        p = BadPickler()
        with self.assertRaises(pickle1.PicklingError):
            p.dump("data")

    # 测试不同种类数据
    def test_basic_types(self):
        original = 123.23
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)
        original = 'hello'
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)
        original = [1, 2, 3, 'hello']
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)
        original = {'name': 'John', 'age': 25}
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)
        original = {1, 2, 3}
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)
        original = (1, "a", 3.14)
        self.assertEqual(pickle1.loads(pickle1.dumps(original)), original)

    # 使用持久化ID保存对象
    def test_persistent_id(self):
        obj = {
            "a": 1,
            "b": MyPersistentObject("example")
        }
        buf = io.BytesIO()
        pickler = PersistentPickler(buf)
        pickler.dump(obj)
        buf.getvalue()

    # 重复使用相同类
    def test_repetition_obj(self):
        shared_obj = MyObj("shared")
        data = {
            "first": shared_obj,
            "second": shared_obj  # 第二次引用，触发 memo 重用
        }
        pickle1.dumps(data)

    # 使用自定义的reducer_override方法，实现定制化序列化
    def test_custom_reducer_override(self):
        d = Dummy(123)
        buffer = io.BytesIO()
        pickler = CustomPickler(buffer, protocol=4)
        pickler.dump(d)
        buffer.seek(0)
        obj = pickle1.load(buffer)
        self.assertIsInstance(obj, Dummy)
        self.assertEqual(obj.value, 123)

    # 覆盖tuple错误抛出路径
    def test_non_tuple_return(self):
        buf = io.BytesIO()
        pickler = CustomPickler(buf)
        with self.assertRaises(pickle1.PicklingError):
            pickler.dump("not_tuple")

    def test_short_tuple(self):
        buf = io.BytesIO()
        pickler = CustomPickler(buf)
        with self.assertRaises(pickle1.PicklingError):
            pickler.dump("short_tuple")
