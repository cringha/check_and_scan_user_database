from typing import List

import fitz  # PyMuPDF

class LaborContractPageExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.page_count = self.doc.page_count

    def is_contract_first_page(self, page_text: str) -> bool:
        """判断是否为合同首页"""
        text = page_text.replace("\n", "").replace(" ", "")
        # 必须条件
        has_title = "劳动合同" in text
        has_company = "恒安嘉新(北京)科技股份公司" in text
        has_party_b = "乙方:" in text
        has_sign_date = "签订日期:" in text
        # 排除续订、变更页面
        exclude1 = "劳动合同续订书" in text
        exclude2 = "劳动合同变更书" in text

        if exclude1 or exclude2:
            return False
        return has_title and has_company and has_party_b and has_sign_date

    def is_term_page(self, page_text: str) -> bool:
        """判断是否为工作期限（合同期限）页"""
        text = page_text.replace("\n", "").replace(" ", "")
        has_section_title = "合同期限" in text
        has_type_word = ("无固定期限劳动合同" in text) or ("固定期限劳动合同" in text)
        has_probation = "试用期" in text
        exclude1 = "劳动合同续订书" in text
        exclude2 = "劳动合同变更书" in text
        if exclude1 or exclude2:
            return False
        return has_section_title and has_type_word and has_probation

    def is_sign_seal_page(self, page_text: str, page) -> bool:
        """判断是否盖章+人员签字页：文本+页面是否包含图片（印章）"""
        text = page_text.replace("\n", "").replace(" ", "")
        has_statement = "本人声明:" in text
        has_sign_label = "乙方签名:" in text
        has_attachment = "附件1:" in text
        # 页面是否存在图片（公章图片）
        image_list = page.get_images(full=True)
        has_seal_img = len(image_list) > 0

        exclude1 = "劳动合同续订书" in text
        exclude2 = "劳动合同变更书" in text
        if exclude1 or exclude2:
            return False
        # 满足文本条件，或者页面有印章图片+签名文字
        cond_text = has_statement and has_sign_label and has_attachment
        cond_img = has_seal_img and has_sign_label
        return cond_text or cond_img

    def run_extract(self):
        """遍历全部页面，匹配三类页面，返回页码（从0开始）"""
        result = {
            "contract_first_page": None,
            "contract_term_page": None,
            "seal_sign_page": None
        }
        for page_idx in range(self.page_count):
            page = self.doc[page_idx]
            page_text = page.get_text()
            if self.is_contract_first_page(page_text):
                result["contract_first_page"] = page_idx
            elif self.is_term_page(page_text):
                result["contract_term_page"] = page_idx
            elif self.is_sign_seal_page(page_text, page):
                result["seal_sign_page"] = page_idx
        return result

    def save_target_pages1(self, output_pdf_name: str, target_page_index_list):
        """把目标页码导出为新的PDF文件"""
        new_doc = fitz.new_document()
        for idx in target_page_index_list:
            new_doc.insert_pdf(self.doc, from_page=idx, to_page=idx)
        new_doc.save(output_pdf_name)
        new_doc.close()

    def save_target_pages(self, output_pdf_name: str, target_page_index_list: List[int]):
        """导出目标页面生成新PDF，修复点：fitz.open()创建空白文档"""
        new_doc = fitz.open()  # ✅替换旧的 fitz.new_document()
        for idx in target_page_index_list:
            new_doc.insert_pdf(self.doc, from_page=idx, to_page=idx)
        new_doc.save(output_pdf_name)
        new_doc.close()

    def close(self):
        self.doc.close()


if __name__ == "__main__":
    # ========= 使用示例 =========
    pdf_file = r"e:/崔渊博-恒安-脱敏--无固定期限合同1 (1).pdf"
    extractor = LaborContractPageExtractor(pdf_file)
    res = extractor.run_extract()
    print("识别结果，页码从0开始：", res)

    # 收集需要导出的页面
    target_pages = []
    for v in res.values():
        if v is not None:
            target_pages.append(v)
    print(f"待导出页面索引：{target_pages}")

    # 输出截取后的pdf
    extractor.save_target_pages("contract_extract_output.pdf", target_pages)
    extractor.close()
