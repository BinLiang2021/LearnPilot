"""
@file_name: pdf_downloader.py
@author: bin.liang
@date: 2025-06-28
@description: PDF下载器 - 负责下载arXiv论文PDF文件
"""

import os
import asyncio
import aiohttp
import aiofiles
from typing import Dict, Any, Optional
from pathlib import Path
from src.learn_pilot.core.logging.logger import logger


class PdfDownloader:
    """PDF下载器 - 异步下载PDF文件"""
    
    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size
    
    async def download_paper(self, paper: Dict[str, Any], save_dir: str) -> Optional[str]:
        """
        下载论文PDF
        
        Args:
            paper: 论文数据字典
            save_dir: 保存目录
            
        Returns:
            下载成功时返回文件路径，失败时返回None
        """
        try:
            # 创建保存目录
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            
            # 获取PDF URL
            pdf_url = self._get_pdf_url(paper)
            if not pdf_url:
                logger.warning(f"⚠️ 未找到PDF链接: {paper['title']}")
                return None
            
            # 生成文件路径
            arxiv_id = paper.get('arxiv_id', paper['url'].split('/')[-1])
            filename = f"{arxiv_id}.pdf"
            filepath = os.path.join(save_dir, filename)
            
            # 如果文件已存在，跳过下载
            if os.path.exists(filepath):
                logger.info(f"📄 文件已存在，跳过下载: {filepath}")
                return filepath
            
            # 异步下载
            await self._download_file(pdf_url, filepath)
            
            logger.info(f"✅ 下载完成: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"❌ 下载失败 {paper.get('title', 'Unknown')}: {str(e)}")
            return None
    
    def _get_pdf_url(self, paper: Dict[str, Any]) -> Optional[str]:
        """获取PDF下载链接"""
        # 尝试从links中找到PDF链接
        for link in paper.get('links', []):
            if 'pdf' in link.get('type', '').lower() or link['href'].endswith('.pdf'):
                return link['href']
        
        # 如果没有直接的PDF链接，从arXiv ID构造
        arxiv_id = paper.get('arxiv_id')
        if not arxiv_id:
            arxiv_id = paper['url'].split('/')[-1]
        
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    async def _download_file(self, url: str, filepath: str):
        """异步下载文件"""
        temp_filepath = filepath + ".tmp"  # 使用临时文件
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    
                    # 获取预期文件大小
                    expected_size = response.headers.get('Content-Length')
                    if expected_size:
                        expected_size = int(expected_size)
                        logger.info(f"📏 预期文件大小: {expected_size / 1024 / 1024:.2f} MB")
                    
                    downloaded_size = 0
                    async with aiofiles.open(temp_filepath, 'wb') as f:
                        async for chunk in response.content.iter_chunked(self.chunk_size):
                            await f.write(chunk)
                            downloaded_size += len(chunk)
                    
                    # 验证文件大小
                    if expected_size and downloaded_size != expected_size:
                        raise ValueError(f"文件大小不匹配: 预期 {expected_size}, 实际 {downloaded_size}")
                    
                    # 基本PDF格式检查
                    await self._verify_pdf_format(temp_filepath)
                    
                    # 下载成功，移动到最终位置
                    os.rename(temp_filepath, filepath)
                    
        except Exception as e:
            # 清理临时文件
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            raise e
    
    async def _verify_pdf_format(self, filepath: str):
        """验证PDF文件格式"""
        async with aiofiles.open(filepath, 'rb') as f:
            header = await f.read(8)
            if not header.startswith(b'%PDF-'):
                raise ValueError("下载的文件不是有效的PDF格式") 
            