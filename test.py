import os
import pickle
import unittest
from pathlib import Path
from itertools import combinations
from pickle_test_base import YieldTestBase


class TestPickleFilesEquality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output_dir = ("linux")  # 修改为你的输出目录
        cls.log_path = os.path.join(cls.output_dir, "pickle_test_log.txt")
        cls.file_names = set()
        cls.python_versions = [d for d in os.listdir(cls.output_dir) if os.path.isdir(os.path.join(cls.output_dir, d))]

        # 创建日志文件
        with open(cls.log_path, "w", encoding="utf-8") as f:
            f.write("Pickle 跨版本测试结果记录\n")
            f.write("=" * 60 + "\n\n")

        # 收集所有需要比较的.pkl文件名
        for version in cls.python_versions:
            version_dir = os.path.join(cls.output_dir, version)
            cls.file_names.update([f.name for f in Path(version_dir).glob('*.pkl')])

    def test_pickle_files_equality(self):
        """测试不同Python版本生成的.pkl文件是否在字节流上相等"""

        for file_name in self.file_names:
            base_name = os.path.splitext(file_name)[0]
            with self.subTest(file_name=file_name):
                contents = {}
                inputs = {}

                for version in self.python_versions:
                    version_dir = os.path.join(self.output_dir, version)
                    pkl_file_path = os.path.join(version_dir, file_name)
                    json_file_path = os.path.join(version_dir, f"{base_name}.json")

                    if os.path.exists(pkl_file_path):
                        with open(pkl_file_path, 'rb') as f:
                            contents[version] = f.read()
                        with open(pkl_file_path, 'rb') as f:
                            if YieldTestBase.check_integrity(pkl_file_path, json_file_path):
                                try:
                                    inputs[version] = pickle.load(f)
                                except Exception as e:
                                    inputs[version] = f"反序列化失败: {str(e)}"
                            else:
                                inputs[version] = "完整性校验失败"

                mismatches = []
                version_pairs = combinations(contents.keys(), 2)

                for v1, v2 in version_pairs:
                    c1, c2 = contents[v1], contents[v2]
                    i1, i2 = inputs.get(v1, "无输入"), inputs.get(v2, "无输入")
                    is_equal = (c1 == c2)

                    detail = (
                        f"测试文件: {file_name}\n"
                        f"测试类型: {base_name}\n"
                        f"比较版本: {v1} vs {v2}\n"
                        f"  - 输入数据 {v1}: {repr(i1)}\n"
                        f"  - 输入数据 {v2}: {repr(i2)}\n"
                        f"  - 长度对比: {len(c1)} vs {len(c2)}\n"
                        f"  - 前50字节(hex):\n"
                        f"      {v1}: {c1[:50].hex()}\n"
                        f"      {v2}: {c2[:50].hex()}\n"
                        f"  - 匹配结果: {'一致' if is_equal else '不一致'}\n"
                        + "-" * 60 + "\n"
                    )

                    with open(self.log_path, "a", encoding="utf-8") as log_file:
                        log_file.write(detail)

                    if not is_equal:
                        mismatches.append((v1, v2, file_name, c1, c2, i1, i2))

                if mismatches:
                    mismatch_details = []
                    for v1, v2, fn, c1, c2, i1, i2 in mismatches:
                        detail = (
                            f"\nMismatch between {v1} and {v2} in file '{fn}':\n"
                            f"  Input data from {v1}: {i1}\n"
                            f"  Input data from {v2}: {i2}\n"
                            f"  Length: {len(c1)} (from {v1}) vs {len(c2)} (from {v2})\n"
                            f"  First 50 bytes (hex):\n"
                            f"    From {v1}: {c1[:50].hex()}\n"
                            f"    From {v2}: {c2[:50].hex()}"
                        )
                        mismatch_details.append(detail)

                    full_message = "\n".join(mismatch_details)
                    print(full_message)
                    self.fail("Pickle files do not match across versions. See details above.")


if __name__ == "__main__":
    unittest.main()
