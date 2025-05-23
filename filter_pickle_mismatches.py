def filter_mismatches(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result_blocks = []
    current_block = []
    for line in lines:
        if line.strip().startswith("-" * 20):
            # 到达一个段落的结尾
            block_text = ''.join(current_block)
            if "匹配结果: 一致" not in block_text:
                result_blocks.append(block_text)
            current_block = []
        else:
            current_block.append(line)

    # 处理最后一段（如果没有以分隔线结尾）
    if current_block:
        block_text = ''.join(current_block)
        if "匹配结果: 一致" not in block_text:
            result_blocks.append(block_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(result_blocks))

    print(f"✅ 已完成过滤。不一致测试结果已保存至: {output_file}")


if __name__ == "__main__":
    input_log_path = "cross_platform_pickle_test_log.txt"   # 修改为你的输入文件名
    output_log_path = "output_diffos.txt"     # 输出文件名
    filter_mismatches(input_log_path, output_log_path)
