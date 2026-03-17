# pdf-parse-reader/main.py
import PyPDF2
import re
from typing import Optional, List

class PDFQuickReader:
    """PDF解析与速读工具：提取文本、关键信息（标题/关键词/摘要）、生成速读摘要"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_text = ""  # 存储解析后的原始文本

    def parse_pdf(self) -> Optional[str]:
        """解析PDF文本（处理常见PDF加密/读取异常）"""
        try:
            with open(self.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                # 检查PDF是否加密
                if pdf_reader.is_encrypted:
                    try:
                        pdf_reader.decrypt("")  # 尝试解密无密码的加密PDF
                    except:
                        print("PDF已加密，无法解析")
                        return None
                
                # 提取所有页面文本
                for page in pdf_reader.pages:
                    self.raw_text += page.extract_text() or ""
            return self.raw_text
        except FileNotFoundError:
            print(f"错误：未找到PDF文件 {self.pdf_path}")
            return None
        except Exception as e:
            print(f"解析PDF失败：{str(e)}")
            return None

    def extract_key_info(self) -> dict:
        """提取速读关键信息（标题/关键词/摘要，适配科研论文PDF）"""
        if not self.raw_text:
            return {"error": "未解析到PDF文本"}
        
        # 提取标题（匹配首行/大写/长文本，简单规则）
        title_match = re.search(r'^.{10,80}$', self.raw_text.strip(), re.MULTILINE)
        title = title_match.group() if title_match else "未识别标题"
        
        # 提取关键词（匹配Keywords/关键词：后的内容）
        keyword_pattern = re.compile(r'(Keywords|关键词)[：:]?\s*([^.\n]+)', re.IGNORECASE)
        keyword_match = keyword_pattern.search(self.raw_text)
        keywords = keyword_match.group(2).strip() if keyword_match else "未识别关键词"
        
        # 提取摘要（匹配Abstract/摘要：后的内容）
        abstract_pattern = re.compile(r'(Abstract|摘要)[：:]?\s*([^.\n]{50,500})', re.IGNORECASE)
        abstract_match = abstract_pattern.search(self.raw_text)
        abstract = abstract_match.group(2).strip() if abstract_match else "未识别摘要"
        
        return {
            "title": title,
            "keywords": keywords,
            "abstract": abstract,
            "quick_read_summary": f"【速读摘要】标题：{title}\n核心关键词：{keywords}\n摘要：{abstract}"
        }

# 示例使用
if __name__ == "__main__":
    # 替换为你的PDF文件路径
    pdf_reader = PDFQuickReader("research_paper.pdf")
    pdf_reader.parse_pdf()
    key_info = pdf_reader.extract_key_info()
    print(key_info["quick_read_summary"])