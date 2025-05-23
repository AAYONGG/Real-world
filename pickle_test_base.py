# pickle_test_base.py
import hashlib
import json

import os
import pickle
from typing import Any


class YieldTestBase:
    """基类：封装共用测试逻辑"""

    def __init__(self, test_dir):
        self.test_dir = test_dir
        os.makedirs(self.test_dir, exist_ok=True)
        self.data = self.generate_data()

        self()

    @staticmethod
    def check_integrity(data_path, meta_path):
        """验证数据完整性"""

        with open(data_path, "rb") as f:
            data_bytes = f.read()
        hash_now = hashlib.sha256(data_bytes).hexdigest()

        with open(meta_path, "r") as f:
            metadata = json.load(f)

        if metadata["sha256"] != hash_now:
            print("比较{}与{})失败！".format(os.path.basename(data_path), os.path.basename(meta_path)))
            return False
        else:
            return True

    @staticmethod
    def save_data(data, dill_filename):
        # Compute SHA256 hash
        data_bytes = pickle.dumps(data, protocol=4)
        sha256_hash = hashlib.sha256(data_bytes).hexdigest()

        # Save metadata
        metadata = {
            "sha256": sha256_hash
        }

        with open(dill_filename, "w") as f:
            json.dump(metadata, f, indent=2)

        print("已保存 metadata:{}".format(dill_filename))

    def generate_data(self) -> Any:
        """子类需实现：生成测试数据"""
        pass

    def _serialize(self, data: Any, output_path: str) -> None:
        with open(output_path, "wb") as f:
            pickle.dump(data, f, protocol=4)

    def __call__(self):
        for i, data in enumerate(self.data):
            filename = "{}_{}.pkl".format(self.__class__.__name__, i)
            file_path = os.path.join(self.test_dir, filename)
            self._serialize(data, file_path)

            data_path = os.path.join(self.test_dir, "{}_{}.json".format(self.__class__.__name__, i))
            self.save_data(data, data_path)