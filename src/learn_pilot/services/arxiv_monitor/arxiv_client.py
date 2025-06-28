"""
@file_name: arxiv_client.py
@author: bin.liang
@date: 2025-06-28
@description: ArXiv API客户端 - 负责从arXiv检索论文数据
"""

import requests
import feedparser
from typing import List, Dict, Any
from src.learn_pilot.core.logging.logger import logger


class ArxivClient:
    """ArXiv API客户端"""
    
    def __init__(self, base_url: str = 'http://export.arxiv.org/api/query'):
        self.base_url = base_url
    
    async def fetch_papers(
        self, 
        category: str, 
        search_term: str = '', 
        max_results: int = 2000
    ) -> List[Dict[str, Any]]:
        """
        从arXiv检索论文
        
        Args:
            category: arXiv类别代码 (如 'cs.AI')
            search_term: 额外搜索词
            max_results: 最大结果数
            
        Returns:
            论文数据列表
        """
        try:
            # 构建查询
            query = f'cat:{category}'
            if search_term:
                query += f'+AND+all:{search_term}'
            
            params = {
                'search_query': query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            logger.info(f"🔍 检索arXiv论文: category={category}, search_term={search_term}")
            
            # 发送请求
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # 解析RSS Feed
            feed = feedparser.parse(response.text)
            
            # 转换为标准格式
            papers = []
            for entry in feed.entries:
                paper = {
                    'title': entry.title,
                    'summary': entry.summary,
                    'url': entry.id,
                    'authors': [author.name for author in getattr(entry, 'authors', [])],
                    'arxiv_id': entry.id.split('/')[-1],
                    'published': getattr(entry, 'published', ''),
                    'links': [{'href': link.href, 'type': getattr(link, 'type', '')} for link in getattr(entry, 'links', [])]
                }
                papers.append(paper)
            
            logger.info(f"📚 成功检索到 {len(papers)} 篇论文")
            return papers
            
        except Exception as e:
            logger.error(f"❌ arXiv检索失败: {str(e)}")
            return [] 