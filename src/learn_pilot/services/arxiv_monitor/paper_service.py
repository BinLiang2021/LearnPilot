"""
@file_name: paper_service.py
@author: bin.liang
@date: 2025-06-28
@description: 论文服务类 - 实现论文检索、筛选、下载、存储的完整流程
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio

from src.learn_pilot.core.logging.logger import logger
from src.learn_pilot.tools.file_system.paper_repository import PaperRepository
from .arxiv_client import ArxivClient
from .filter_agent import FilterAgent
from .pdf_downloader import PdfDownloader


@dataclass
class PaperResult:
    """论文处理结果"""
    title: str
    research_problem: str
    key_contribution: list[str]
    key_concepts_and_techniques: list[str]
    summary: str
    url: str
    pdf_path: Optional[str]
    research_fields: List[str]
    is_selected: bool
    error: Optional[str] = None


class PaperService:
    """论文服务 - 协调各个组件完成论文处理流程"""
    
    def __init__(self, save_dir: str):
        self.arxiv_client = ArxivClient()
        self.filter_agent = FilterAgent()
        self.pdf_downloader = PdfDownloader()
        self.repository = PaperRepository()
        self.save_dir = save_dir
        
    async def process_papers_by_category(
        self, 
        category: str, 
        search_term: str = '', 
        max_results: int = 2000
    ) -> Dict[str, Any]:
        """
        按类别处理论文的完整流程
        
        Returns:
            处理结果统计
        """
        logger.info(f"🚀 开始处理类别: {category}, 搜索词: {search_term}")
        
        # 1. 检索论文
        papers = await self.arxiv_client.fetch_papers(
            category=category,
            search_term=search_term,
            max_results=max_results
        )
        
        logger.info(f"📚 检索到 {len(papers)} 篇论文")
        
        # 2. 并行处理论文
        results = await self._process_papers_batch(papers)
        
        # 3. 统计结果
        stats = self._calculate_stats(results)
        
        logger.info(f"✅ 处理完成: {stats}")
        return stats
        
    async def _process_papers_batch(self, papers: List[Dict]) -> List[PaperResult]:
        """批量处理论文"""
        semaphore = asyncio.Semaphore(5)  # 限制并发数
        tasks = [
            self._process_single_paper(paper, semaphore) 
            for paper in papers
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
        
    async def _process_single_paper(
        self, 
        paper: Dict, 
        semaphore: asyncio.Semaphore
    ) -> PaperResult:
        """处理单篇论文"""
        async with semaphore:
            try:
                # 1. 筛选论文
                filter_result = await self.filter_agent.filter_arxiv_paper(
                    paper['title'], 
                    paper['summary']
                )
                
                result = PaperResult(
                    title=paper['title'],
                    research_problem=filter_result['research_problem'],
                    key_contribution=filter_result['key_contribution'],
                    key_concepts_and_techniques=filter_result['key_concepts_and_techniques'],
                    summary=paper['summary'],
                    url=paper['url'],
                    pdf_path=None,
                    research_fields=[
                        field if isinstance(field, str) else field.value 
                        for field in filter_result['field']
                    ],
                    is_selected=filter_result['is_match'],
                    )
                
                # 2. 如果选中，下载PDF并存储
                if filter_result['is_match']:
                    pdf_path = await self.pdf_downloader.download_paper(
                        paper, 
                        f"{self.save_dir}/{result.research_fields[0]}"
                    )
                    result.pdf_path = pdf_path
                    
                    # 3. 保存到数据库
                    paper_data = {
                        'title': result.title,
                        'research_problem': result.research_problem,
                        'key_contribution': result.key_contribution,
                        'key_concepts_and_techniques': result.key_concepts_and_techniques,
                        'summary': result.summary,
                        'url': result.url,
                        'pdf_path': result.pdf_path,
                        'research_fields': result.research_fields,
                        'store_type': 'arxiv_recommend'
                    }
                    await self.repository.save_paper(paper_data)
                    
                    logger.info(f"🎯 选中并处理论文: {paper['title']}, 花费 {filter_result['usage']['estimated_cost_usd']} 美元")
                    
                return result
                
            except Exception as e:
                logger.error(f"❌ 处理论文失败 {paper['title']}: {str(e)}")
                return PaperResult(
                    title=paper['title'],
                    research_problem=paper['summary'],
                    key_contribution=paper['summary'],
                    key_concepts_and_techniques=paper['summary'],
                    summary=paper['summary'],
                    url=paper.get('url', ''),
                    pdf_path=None,
                    research_fields=[],
                    is_selected=False,
                    error=str(e)
                )
                
    def _calculate_stats(self, results: List[PaperResult]) -> Dict[str, Any]:
        """计算处理统计信息"""
        total = len(results)
        selected = sum(1 for r in results if r.is_selected)
        downloaded = sum(1 for r in results if r.pdf_path)
        errors = sum(1 for r in results if r.error)
        
        return {
            'total_papers': total,
            'selected_papers': selected,
            'downloaded_papers': downloaded,
            'error_count': errors,
            'success_rate': f"{(selected/total*100):.1f}%" if total > 0 else "0%"
        } 