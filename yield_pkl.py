# yield_pkl.py
import os
import sys

from BlackBox import test_equivalence, test_boundary

from BlackBox import test_fuzzing


def main(output_dir, test_way):
    os.makedirs(output_dir, exist_ok=True)
    if test_way == "boundary":
        test_boundary.TestBoundaryValues(output_dir)
    elif test_way == "equivalence":
        test_equivalence.TestEquivalencePartitioning(output_dir)
    elif test_way == "fuzzing":
        test_fuzzing.TestFuzzing(output_dir, 30)

    print("已使用 Python {} 生成文件: {} 相关序列对象".format(sys.version.split()[0], test_way))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate .pkl files using different Python versions.")
    parser.add_argument("--output-dir", required=True, help="Directory to save the generated .pkl and .json files.")
    args = parser.parse_args()

    main(args.output_dir, "boundary")
    main(args.output_dir, "equivalence")
    main(args.output_dir, "fuzzing")

