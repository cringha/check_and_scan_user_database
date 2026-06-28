

import jieba.posseg as pseg

def extract_names_jieba(text):
    """
    使用 jieba 库进行分词和词性标注，提取人名
    """
    names = []
    words = pseg.cut(text)

    for word, flag in words:
        names.append(f"{word}-{flag}")
        # if flag == 'nr':  # 'nr' 表示人名[reference:5]
        #     names.append(word)
    return list(set(names))  # 去重


# 打开文件
with open('../data/file-list.txt', 'r', encoding='gbk') as file:
    # 逐行读取并输出
    for line in file:
        names = extract_names_jieba(line)  # 使用end=''以避免在行尾自动添加换行符
        print(line, " " , names)

# 示例
# text = "马云和马化腾在杭州会面，讨论人工智能的未来。"
# print(extract_names_jieba(text))
# # 输出: ['马云', '马化腾']