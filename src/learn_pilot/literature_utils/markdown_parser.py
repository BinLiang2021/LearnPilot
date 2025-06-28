"""
Markdown解析工具
用于解析论文Markdown文件，提取结构化信息
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import yaml

from src.learn_pilot.models.paper_models import Paper, Section, Author

logger = logging.getLogger(__name__)

class MarkdownParser:
    """Markdown论文解析器"""
    
    def __init__(self):
        self.logger = logger
        
        # 正则表达式模式
        self.patterns = {
            'yaml_frontmatter': r'^---\s*\n(.*?)\n---\s*\n',
            'title': r'^#\s+(.+?)(?:\n|$)',
            'section_h2': r'^##\s+(.+?)(?:\n|$)',
            'section_h3': r'^###\s+(.+?)(?:\n|$)',
            'section_h4': r'^####\s+(.+?)(?:\n|$)',
            'authors': r'(?:author[s]?|作者)[:\s]+(.+?)(?:\n|$)',
            'abstract': r'(?:abstract|摘要)[:\s]*\n(.*?)(?=\n#|\n##|\Z)',
            'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            'year': r'(?:year|年份|发表)[:\s]+(\d{4})',
            'venue': r'(?:venue|conference|journal|会议|期刊)[:\s]+(.+?)(?:\n|$)',
        }
    
    def parse_file(self, file_path: str) -> Paper:
        """
        解析Markdown文件
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            解析后的Paper对象
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.logger.info(f"开始解析文件: {file_path}")
            
            # 解析YAML前置信息
            metadata = self._parse_yaml_frontmatter(content)
            
            # 移除YAML前置信息
            content_without_yaml = self._remove_yaml_frontmatter(content)
            
            # 解析基本信息
            title = self._extract_title(content_without_yaml, metadata)
            authors = self._extract_authors(content_without_yaml, metadata)
            abstract = self._extract_abstract(content_without_yaml, metadata)
            
            # 解析章节结构
            sections = self._extract_sections(content_without_yaml)
            
            # 补充元信息
            year = self._extract_year(content_without_yaml, metadata)
            venue = self._extract_venue(content_without_yaml, metadata)
            
            # 创建Paper对象
            paper = Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                sections=sections,
                metadata=metadata,
                year=year,
                venue=venue
            )
            
            self.logger.info(f"解析完成: {title}, {len(sections)}个章节")
            return paper
            
        except Exception as e:
            self.logger.error(f"解析文件失败 {file_path}: {e}")
            raise
    
    def _parse_yaml_frontmatter(self, content: str) -> Dict[str, Any]:
        """解析YAML前置信息"""
        match = re.search(self.patterns['yaml_frontmatter'], content, re.DOTALL)
        if match:
            try:
                yaml_content = match.group(1)
                return yaml.safe_load(yaml_content) or {}
            except yaml.YAMLError as e:
                self.logger.warning(f"YAML解析失败: {e}")
                return {}
        return {}
    
    def _remove_yaml_frontmatter(self, content: str) -> str:
        """移除YAML前置信息"""
        return re.sub(self.patterns['yaml_frontmatter'], '', content, flags=re.DOTALL)
    
    def _extract_title(self, content: str, metadata: Dict[str, Any]) -> str:
        """提取标题"""
        # 优先使用metadata中的标题
        if 'title' in metadata:
            return str(metadata['title'])
        
        # 从内容中提取第一个一级标题
        match = re.search(self.patterns['title'], content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            # 清理标题中的常见前缀
            title = re.sub(r'^(?:Paper\s*Title\s*:?\s*|Title\s*:?\s*)', '', title, flags=re.IGNORECASE)
            return title
        
        return "Untitled Paper"
    
    def _extract_authors(self, content: str, metadata: Dict[str, Any]) -> List[Author]:
        """提取作者信息"""
        authors = []
        
        # 优先使用metadata中的作者信息
        if 'authors' in metadata:
            author_list = metadata['authors']
            if isinstance(author_list, list):
                for author_info in author_list:
                    if isinstance(author_info, str):
                        authors.append(Author(name=author_info))
                    elif isinstance(author_info, dict):
                        authors.append(Author(
                            name=author_info.get('name', ''),
                            affiliation=author_info.get('affiliation'),
                            email=author_info.get('email')
                        ))
                return authors
        
        # 从内容中提取作者信息
        match = re.search(self.patterns['authors'], content, re.IGNORECASE | re.MULTILINE)
        if match:
            authors_text = match.group(1).strip()
            # 分割作者名字
            author_names = re.split(r'[,;]|\sand\s', authors_text)
            for name in author_names:
                name = name.strip()
                if name:
                    # 提取邮箱
                    email_match = re.search(self.patterns['email'], name)
                    email = email_match.group(1) if email_match else None
                    # 清理姓名
                    clean_name = re.sub(self.patterns['email'], '', name).strip()
                    authors.append(Author(name=clean_name, email=email))
        
        return authors if authors else [Author(name="Unknown Author")]
    
    def _extract_abstract(self, content: str, metadata: Dict[str, Any]) -> str:
        """提取摘要"""
        # 优先使用metadata中的摘要
        if 'abstract' in metadata:
            return str(metadata['abstract'])
        
        # 从内容中提取摘要
        match = re.search(self.patterns['abstract'], content, re.IGNORECASE | re.DOTALL)
        if match:
            abstract = match.group(1).strip()
            return self._clean_text(abstract)
        
        return ""
    
    def _extract_sections(self, content: str) -> List[Section]:
        """提取章节结构"""
        sections = []
        
        # 按行分割内容
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # 检查是否是章节标题
            h2_match = re.match(self.patterns['section_h2'], line)
            h3_match = re.match(self.patterns['section_h3'], line)
            h4_match = re.match(self.patterns['section_h4'], line)
            
            if h2_match:
                # 保存前一个章节
                if current_section:
                    current_section.content = self._clean_text('\n'.join(current_content))
                    sections.append(current_section)
                
                # 创建新的二级章节
                current_section = Section(
                    title=h2_match.group(1).strip(),
                    content="",
                    level=2
                )
                current_content = []
                
            elif h3_match:
                # 保存前一个章节
                if current_section:
                    current_section.content = self._clean_text('\n'.join(current_content))
                    sections.append(current_section)
                
                # 创建新的三级章节
                current_section = Section(
                    title=h3_match.group(1).strip(),
                    content="",
                    level=3
                )
                current_content = []
                
            elif h4_match:
                # 保存前一个章节
                if current_section:
                    current_section.content = self._clean_text('\n'.join(current_content))
                    sections.append(current_section)
                
                # 创建新的四级章节
                current_section = Section(
                    title=h4_match.group(1).strip(),
                    content="",
                    level=4
                )
                current_content = []
                
            else:
                # 添加到当前章节内容
                if current_section is not None:
                    current_content.append(line)
        
        # 保存最后一个章节
        if current_section:
            current_section.content = self._clean_text('\n'.join(current_content))
            sections.append(current_section)
        
        return sections
    
    def _extract_year(self, content: str, metadata: Dict[str, Any]) -> Optional[int]:
        """提取发表年份"""
        if 'year' in metadata:
            try:
                return int(metadata['year'])
            except (ValueError, TypeError):
                pass
        
        match = re.search(self.patterns['year'], content, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
        
        return None
    
    def _extract_venue(self, content: str, metadata: Dict[str, Any]) -> Optional[str]:
        """提取发表场所"""
        if 'venue' in metadata:
            return str(metadata['venue'])
        
        match = re.search(self.patterns['venue'], content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """清理文本内容"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\n\s*\n', '\n\n', text)  # 多个连续空行变为两个
        text = re.sub(r'^\s+|\s+$', '', text)    # 移除开头结尾空白
        text = re.sub(r'\t', '    ', text)       # 制表符转空格
        
        return text
    
    def validate_paper(self, paper: Paper) -> List[str]:
        """验证解析结果"""
        issues = []
        
        if not paper.title or paper.title == "Untitled Paper":
            issues.append("缺少有效标题")
        
        if not paper.authors or paper.authors[0].name == "Unknown Author":
            issues.append("缺少作者信息")
        
        if not paper.abstract:
            issues.append("缺少摘要")
        
        if not paper.sections:
            issues.append("缺少章节内容")
        
        return issues

def parse_papers_from_directory(directory: str) -> List[Paper]:
    """
    从目录中解析所有Markdown论文文件
    
    Args:
        directory: 包含Markdown文件的目录路径
        
    Returns:
        解析后的Paper对象列表
    """
    parser = MarkdownParser()
    papers = []
    
    directory_path = Path(directory)
    if not directory_path.exists():
        logger.error(f"目录不存在: {directory}")
        return papers
    
    md_files = list(directory_path.glob("*.md"))
    logger.info(f"找到 {len(md_files)} 个Markdown文件")
    
    for md_file in md_files:
        try:
            paper = parser.parse_file(str(md_file))
            
            # 验证解析结果
            issues = parser.validate_paper(paper)
            if issues:
                logger.warning(f"文件 {md_file.name} 解析问题: {', '.join(issues)}")
            
            papers.append(paper)
            
        except Exception as e:
            logger.error(f"解析文件失败 {md_file}: {e}")
            continue
    
    logger.info(f"成功解析 {len(papers)} 篇论文")
    return papers

if __name__ == "__main__":
    # 测试代码
    parser = MarkdownParser()
    print("MarkdownParser 初始化完成")
