import os
import random
import math
import pickle
import json
import hashlib
from pickle_test_base import YieldTestBase


def fuzzer_string(max_length=100, char_start=32, char_range=95):
    return ''.join(
        chr(random.randint(char_start, char_start + char_range - 1))
        for _ in range(random.randint(0, max_length))
    )


def fuzzer_number():
    choice = random.choice(["int", "float", "nan", "inf", "-inf"])
    if choice == "int":
        return random.randint(-1000000, 1000000)
    elif choice == "float":
        return random.uniform(-1e6, 1e6)
    elif choice == "nan":
        return float("nan")
    elif choice == "inf":
        return float("inf")
    elif choice == "-inf":
        return float("-inf")


def fuzzer_data(depth=0, max_depth=5):
    if depth >= max_depth:
        return random.choice([
            fuzzer_number(), fuzzer_string(), None,
            True, False, bytes(fuzzer_string(10), 'utf-8'),
            random.sample(range(100), k=random.randint(0, 5)),
        ])

    container_type = random.choice(["list", "dict", "set", "tuple", "base"])
    if container_type == "list":
        return [fuzzer_data(depth + 1, max_depth) for _ in range(random.randint(0, 5))]
    elif container_type == "dict":
        return {
            fuzzer_string(10): fuzzer_data(depth + 1, max_depth)
            for _ in range(random.randint(0, 5))
        }
    elif container_type == "set":
        return {
            str(fuzzer_data(depth + 1, max_depth))
            for _ in range(random.randint(0, 5))
        }
    elif container_type == "tuple":
        return tuple(fuzzer_data(depth + 1, max_depth) for _ in range(random.randint(0, 5)))
    else:
        return random.choice([fuzzer_number(), fuzzer_string(), None, True, False])


def is_pickleable(obj):
    try:
        pickle.dumps(obj, protocol=4)
        return True
    except Exception:
        return False


class TestFuzzing(YieldTestBase):
    def __init__(self, test_dir, fuzz_number=5, seed=None):
        self.fuzz_number = fuzz_number
        self.seed = seed or random.randint(0, 1 << 30)
        self.test_dir = test_dir
        self.meta_path = os.path.join("fuzz_metadata.json")
        self.data_path = os.path.join("fuzz_data.pkl")
        super().__init__(test_dir)

    def generate_data(self):
        if os.path.exists(self.data_path) and os.path.exists(self.meta_path):
            if self.check_integrity(self.data_path, self.meta_path):
                print("数据校验通过，未发现修改。")
                with open(self.data_path, "rb") as f:
                    print("[DEBUG] [DEBUG] [DEBUG] [DEBUG]")
                    print(pickle.load(f))
                with open(self.data_path, "rb") as f:
                    return pickle.load(f)

            else:
                print("数据完整性校验失败！数据被篡改或损坏。")

        print("Using random seed: {}".format(self.seed))
        random.seed(self.seed)

        data = []
        for _ in range(self.fuzz_number):
            entry = fuzzer_data(max_depth=random.randint(2, 5))
            if is_pickleable(entry):
                data.append(entry)
            else:
                print("跳过不可序列化数据：", repr(entry))

        # 保存并记录 SHA256
        data_bytes = pickle.dumps(data, protocol=4)
        sha256_hash = hashlib.sha256(data_bytes).hexdigest()

        metadata = {
            "seed": self.seed,
            "fuzz_number": self.fuzz_number,
            "sha256": sha256_hash
        }
        with open(self.meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        with open(self.data_path, "wb") as f:
            pickle.dump(data, f, protocol=4)

        print("已保存 FUZZ 数据文件和 metadata: {}, {}".format(self.data_path, self.meta_path))
        return data

    def __call__(self):

        for i, data in enumerate(self.data):
            file_path = os.path.join(self.test_dir, "{}_{}.pkl".format(self.__class__.__name__, i))
            self._serialize(data, file_path)

            json_path = os.path.join(self.test_dir, "{}_{}.json".format(self.__class__.__name__, i))
            self.save_data(data, json_path)
