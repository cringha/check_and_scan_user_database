# from pyhanlp import HanLP
#
#
# def extract_names_hanlp(text):
#     """
#     使用 HanLP 进行分词并开启人名识别
#     """
#     # 创建分词器并开启人名识别[reference:7]
#     segment = HanLP.newSegment().enableNameRecognize(True)
#     result = segment.seg(text)
#
#     names = [term.word for term in result if str(term.nature) == 'nr']
#     return list(set(names))
#
#
#
#
# # 打开文件
# with open('data/file-list.txt', 'r', encoding='gbk') as file:
#     # 逐行读取并输出
#     for line in file:
#         names = extract_names_hanlp(line)  # 使用end=''以避免在行尾自动添加换行符
#         print(line, " " , names)
#
# # 示例
# # text = "张艺谋导演的新电影由刘德华主演。"
# # print(extract_names_hanlp(text))
# # # 输出: ['张艺谋', '刘德华']

import hanlp
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH) # 世界最大中文语料库
HanLP(['2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。', '阿婆主来到北京立方庭参观自然语义科技公司。'])