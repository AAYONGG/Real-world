import os
import pickle
import unittest
from pathlib import Path
from itertools import combinations
from pickle_test_base import YieldTestBase


class TestCrossPlatformPickleEquality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.systems = ['windows11', 'mac', 'linux']
        cls.root_dir = '.'
        cls.log_path = os.path.join(cls.root_dir, "cross_platform_pickle_test_log.txt")

        cls.python_versions = sorted([
            d.name for d in Path(cls.root_dir, 'windows11').iterdir()
            if d.is_dir()
        ])

        with open(cls.log_path, "w", encoding="utf-8") as f:
            f.write("Pickle 跨平台测试结果记录\n")
            f.write("=" * 60 + "\n\n")

        cls.file_names_by_version = {v: set() for v in cls.python_versions}
        for version in cls.python_versions:
            for system in cls.systems:
                version_dir = Path(cls.root_dir, system, version)
                if version_dir.exists():
                    cls.file_names_by_version[version].update([
                        f.name for f in version_dir.glob("*.pkl")
                    ])

    def test_cross_platform_pickle_files(self):
        for version in self.python_versions:
            file_names = self.file_names_by_version[version]
            for file_name in file_names:
                base_name = os.path.splitext(file_name)[0]

                with self.subTest(python_version=version, file_name=file_name):
                    contents = {}
                    inputs = {}

                    systems_with_file = [
                        system for system in self.systems
                        if Path(self.root_dir, system, version, file_name).exists()
                    ]

                    for system in systems_with_file:
                        file_path = Path(self.root_dir, system, version, file_name)
                        json_path = Path(self.root_dir, system, version, f"{base_name}.json")

                        with open(file_path, "rb") as f:
                            contents[system] = f.read()

                        with open(file_path, "rb") as f:
                            if YieldTestBase.check_integrity(str(file_path), str(json_path)):
                                try:
                                    inputs[system] = pickle.load(f)
                                except Exception as e:
                                    inputs[system] = f"反序列化失败: {str(e)}"
                            else:
                                inputs[system] = "完整性校验失败"

                    mismatches = []
                    for sys1, sys2 in combinations(systems_with_file, 2):
                        c1, c2 = contents[sys1], contents[sys2]
                        i1, i2 = inputs.get(sys1, "无输入"), inputs.get(sys2, "无输入")
                        is_equal = (c1 == c2)

                        detail = (
                            f"测试文件: {file_name}\n"
                            f"测试类型: {base_name}\n"
                            f"比较系统: {sys1} vs {sys2}（Python {version}）\n"
                            f"  - 输入数据 {sys1}: {repr(i1)}\n"
                            f"  - 输入数据 {sys2}: {repr(i2)}\n"
                            f"  - 长度对比: {len(c1)} vs {len(c2)}\n"
                            f"  - 前50字节(hex):\n"
                            f"      {sys1}: {c1[:50].hex()}\n"
                            f"      {sys2}: {c2[:50].hex()}\n"
                            f"  - 匹配结果: {'一致' if is_equal else '不一致'}\n"
                            + "-" * 60 + "\n"
                        )

                        with open(self.log_path, "a", encoding="utf-8") as log_file:
                            log_file.write(detail)

                        if not is_equal:
                            mismatches.append((sys1, sys2, file_name, c1, c2, i1, i2))

                    if mismatches:
                        mismatch_details = []
                        for sys1, sys2, fn, c1, c2, i1, i2 in mismatches:
                            detail = (
                                f"\nMismatch between {sys1} and {sys2} (Python {version}) in file '{fn}':\n"
                                f"  Input data from {sys1}: {i1}\n"
                                f"  Input data from {sys2}: {i2}\n"
                                f"  Length: {len(c1)} (from {sys1}) vs {len(c2)} (from {sys2})\n"
                                f"  First 50 bytes (hex):\n"
                                f"    From {sys1}: {c1[:50].hex()}\n"
                                f"    From {sys2}: {c2[:50].hex()}"
                            )
                            mismatch_details.append(detail)

                        full_message = "\n".join(mismatch_details)
                        print(full_message)
                        self.fail("Pickle files do not match across platforms. See details above.")


if __name__ == "__main__":
    unittest.main()
