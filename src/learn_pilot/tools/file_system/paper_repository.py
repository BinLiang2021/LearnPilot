"""
@file_name: paper_repository.py
@author: bin.liang
@date: 2025-06-28
@description: 论文数据仓库 - 提供安全的数据存储和查询功能
"""

import json
import sqlite3
import asyncio
from pathlib import Path
import traceback
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import asynccontextmanager

from src.learn_pilot.core.logging.logger import logger
from src.learn_pilot.core.config.config import DATA_DIR


class PaperRepository:
    """论文数据仓库 - 使用SQLite提供可靠的数据存储"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or f"{DATA_DIR}/papers.db"
        self._ensure_db_exists()
        
    def _ensure_db_exists(self):
        """确保数据库和表存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    research_problem TEXT,
                    key_contribution TEXT,
                    key_concepts_and_techniques TEXT,
                    summary TEXT,
                    url TEXT UNIQUE,
                    pdf_path TEXT,
                    markdown_path TEXT DEFAULT "",
                    research_fields TEXT,  -- JSON array
                    add_date TEXT,
                    store_type TEXT,
                    is_processed BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 为已存在的表添加新字段（如果不存在的话）
            try:
                conn.execute("ALTER TABLE papers ADD COLUMN markdown_path TEXT DEFAULT ''")
            except sqlite3.OperationalError:
                # 字段已存在，忽略错误
                pass
            
            # 创建索引提高查询性能
            conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON papers(url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fields ON papers(research_fields)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON papers(add_date)")
            
    def _convert_to_string(self, value: Any) -> str:
        """将值转换为字符串，特殊处理list类型"""
        if isinstance(value, list):
            return '\n'.join(str(item) for item in value) if value else ''
        elif value is None:
            return ''
        else:
            return str(value)
    
    async def save_paper(self, paper_data: Dict[str, Any]) -> bool:
        """
        保存论文数据，支持事务和重复检查
        
        Args:
            paper_data: 论文数据字典
            
        Returns:
            是否保存成功
        """
        try:
            # 转换数据格式，确保所有字段都是正确的类型
            processed_data = {
                'title': self._convert_to_string(paper_data.get('title', '')),
                'research_problem': self._convert_to_string(paper_data.get('research_problem', '')),
                'key_contribution': self._convert_to_string(paper_data.get('key_contribution', '')),
                'key_concepts_and_techniques': self._convert_to_string(paper_data.get('key_concepts_and_techniques', '')),
                'summary': self._convert_to_string(paper_data.get('summary', '')),
                'url': self._convert_to_string(paper_data.get('url', '')),
                'pdf_path': paper_data.get('pdf_path'),
                'markdown_path': self._convert_to_string(paper_data.get('markdown_path', '')),
                'research_fields': json.dumps(paper_data.get('research_fields', [])),
                'add_date': paper_data.get('add_date', datetime.now().strftime("%Y-%m-%d")),
                'store_type': paper_data.get('store_type', 'unknown'),
                'is_processed': 1 if paper_data.get('pdf_path') else 0
            }
            
            # 异步执行数据库操作
            await asyncio.get_event_loop().run_in_executor(
                None, self._save_to_db, processed_data
            )
            
            logger.info(f"💾 论文已保存: {processed_data['title'][:50]}...")
            return True
            
        except Exception as e:
            error_message = traceback.format_exc()
            logger.error(f"❌ 错误信息: {error_message}")
            return False
            
    def _save_to_db(self, data: Dict[str, Any]):
        """同步保存到数据库"""
        with sqlite3.connect(self.db_path) as conn:
            # 使用 INSERT OR REPLACE 避免重复
            conn.execute("""
                INSERT OR REPLACE INTO papers (
                    title, research_problem, key_contribution, key_concepts_and_techniques, 
                    summary, url, pdf_path, markdown_path, research_fields,
                    add_date, store_type, is_processed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['title'], data['research_problem'], data['key_contribution'], 
                data['key_concepts_and_techniques'], data['summary'], data['url'], 
                data['pdf_path'], data['markdown_path'], data['research_fields'],
                data['add_date'], 
                data['store_type'], data['is_processed']
            ))
            
    async def get_papers_by_field(self, field: str) -> List[Dict[str, Any]]:
        """根据研究领域查询论文"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self._query_by_field, field
        )
        
    def _query_by_field(self, field: str) -> List[Dict[str, Any]]:
        """同步查询指定领域的论文"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM papers WHERE research_fields LIKE ? ORDER BY created_at DESC",
                (f'%{field}%',)
            )
            return [dict(row) for row in cursor.fetchall()]
            
    async def get_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self._get_stats
        )
        
    def _get_stats(self) -> Dict[str, Any]:
        """同步获取统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(is_processed) as processed,
                    COUNT(DISTINCT research_fields) as unique_fields,
                    MAX(created_at) as latest_added
                FROM papers
            """)
            row = cursor.fetchone()
            
            return {
                'total_papers': row[0],
                'processed_papers': row[1],
                'unique_fields': row[2],
                'latest_added': row[3]
            }
            
    async def backup_to_json(self, backup_path: Optional[str] = None) -> str:
        """备份数据到JSON文件"""
        backup_path = backup_path or f"{DATA_DIR}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        papers = await asyncio.get_event_loop().run_in_executor(
            None, self._get_all_papers
        )
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
            
        logger.info(f"📁 数据已备份到: {backup_path}")
        return backup_path
        
    def _get_all_papers(self) -> List[Dict[str, Any]]:
        """获取所有论文数据"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM papers ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()] 
        