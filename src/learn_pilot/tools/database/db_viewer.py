"""
@file_name: db_viewer.py
@author: bin.liang
@date: 2025-06-28
@description: 论文数据库查看器 - 提供数据查询、统计、导出等功能
"""

import asyncio
import json
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

from src.learn_pilot.tools.file_system.paper_repository import PaperRepository
from src.learn_pilot.core.logging.logger import logger


class PaperDBViewer:
    """论文数据库查看器"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.repository = PaperRepository(db_path)
        
    async def show_stats(self) -> Dict[str, Any]:
        """显示数据库统计信息"""
        stats = await self.repository.get_stats()
        
        print("=" * 60)
        print("📊 数据库统计信息")
        print("=" * 60)
        print(f"📚 论文总数: {stats['total_papers']}")
        print(f"✅ 已处理论文: {stats['processed_papers']}")
        print(f"🔍 研究领域数: {stats['unique_fields']}")
        print(f"📅 最近添加: {stats['latest_added'] or '无'}")
        
        if stats['total_papers'] > 0:
            success_rate = (stats['processed_papers'] / stats['total_papers']) * 100
            print(f"📈 处理成功率: {success_rate:.1f}%")
        
        print("=" * 60)
        return stats
    
    async def list_papers(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """列出论文列表"""
        papers = await asyncio.get_event_loop().run_in_executor(
            None, self._get_papers_with_pagination, limit, offset
        )
        
        if not papers:
            print("📭 暂无论文数据")
            return []
        
        # 格式化显示
        table_data = []
        for paper in papers:
            # 解析研究领域
            try:
                fields = json.loads(paper['research_fields']) if paper['research_fields'] else []
                fields_str = ', '.join(fields[:2])  # 只显示前两个领域
                if len(fields) > 2:
                    fields_str += f" (+{len(fields)-2})"
            except:
                fields_str = paper['research_fields'] or 'N/A'
            
            # 处理可能是字符串的字段，不要当作列表处理
            key_contribution = paper.get('key_contribution', '') or ''
            key_concepts_and_techniques = paper.get('key_concepts_and_techniques', '') or ''
            
            # 如果是字符串，直接使用；如果是列表，则连接
            if isinstance(key_contribution, list):
                key_contribution = ', '.join(key_contribution)
            if isinstance(key_concepts_and_techniques, list):
                key_concepts_and_techniques = ', '.join(key_concepts_and_techniques)
            
            table_data.append([
                paper['id'],
                paper['title'][:50] + ('...' if len(paper['title']) > 50 else ''),
                fields_str,
                paper.get('research_problem', '')[:50] + ('...' if len(paper.get('research_problem', '')) > 50 else ''),
                key_contribution[:50] + ('...' if len(key_contribution) > 50 else ''),
                key_concepts_and_techniques[:50] + ('...' if len(key_concepts_and_techniques) > 50 else ''),
                '✅' if paper['is_processed'] else '⏳',
                paper['add_date'] or 'N/A'
            ])
        
        headers = ['ID', 'Title', 'Fields', 'Problem', 'Contribution', 'Techniques', 'Status', 'Date']
        print(f"\n📋 论文列表 (显示 {offset+1}-{offset+len(papers)} 条)")
        print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=[4, 40, 20, 30, 30, 30, 8, 12]))
        
        return papers
    
    async def search_papers(self, keyword: str) -> List[Dict]:
        """搜索论文"""
        papers = await asyncio.get_event_loop().run_in_executor(
            None, self._search_papers_sync, keyword
        )
        
        if not papers:
            print(f"🔍 未找到包含 '{keyword}' 的论文")
            return []
        
        print(f"\n🔍 搜索结果: 找到 {len(papers)} 篇论文")
        await self._display_paper_list(papers)
        return papers
    
    async def show_papers_by_field(self, field: str) -> List[Dict]:
        """按研究领域显示论文"""
        papers = await self.repository.get_papers_by_field(field)
        
        if not papers:
            print(f"📭 未找到 '{field}' 领域的论文")
            return []
        
        print(f"\n🏷️ '{field}' 领域论文 ({len(papers)} 篇)")
        await self._display_paper_list(papers)
        return papers
    
    async def show_paper_detail(self, paper_id: int):
        """显示论文详情"""
        paper = await asyncio.get_event_loop().run_in_executor(
            None, self._get_paper_by_id, paper_id
        )
        
        if not paper:
            print(f"❌ 未找到ID为 {paper_id} 的论文")
            return
        
        print("\n" + "=" * 80)
        print("📄 论文详情")
        print("=" * 80)
        print(f"🆔 ID: {paper['id']}")
        print(f"📝 标题: {paper['title']}")
        print(f"📅 添加日期: {paper['add_date']}")
        print(f"🏷️ 存储类型: {paper.get('store_type', 'unknown')}")
        print(f"✅ 处理状态: {'已处理' if paper['is_processed'] else '未处理'}")
        
        # 研究领域
        try:
            fields = json.loads(paper['research_fields']) if paper['research_fields'] else []
            print(f"🔬 研究领域: {', '.join(fields) if fields else 'N/A'}")
        except:
            print(f"🔬 研究领域: {paper['research_fields'] or 'N/A'}")
        
        print(f"🔗 URL: {paper.get('url', 'N/A')}")
        print(f"📁 PDF路径: {paper.get('pdf_path') or '未下载'}")
        print(f"📄 Markdown路径: {paper.get('markdown_path') or '无'}")
        
        # 研究问题
        if paper.get('research_problem'):
            print(f"\n🎯 研究问题:")
            print(f"   {paper['research_problem']}")
        
        # 关键贡献
        if paper.get('key_contribution'):
            print(f"\n💡 关键贡献:")
            print(f"   {paper['key_contribution']}")
        
        # 关键概念和技术
        if paper.get('key_concepts_and_techniques'):
            print(f"\n🔧 关键概念和技术:")
            print(f"   {paper['key_concepts_and_techniques']}")
        
        # 摘要
        if paper.get('summary'):
            print(f"\n📋 摘要:")
            # 格式化摘要显示
            summary_lines = [paper['summary'][i:i+80] for i in range(0, len(paper['summary']), 80)]
            for line in summary_lines:
                print(f"   {line}")
        
        print("=" * 80)
    
    async def list_fields(self) -> List[str]:
        """列出所有研究领域"""
        fields = await asyncio.get_event_loop().run_in_executor(
            None, self._get_all_fields
        )
        
        print("\n🏷️ 所有研究领域:")
        for i, (field, count) in enumerate(fields, 1):
            print(f"   {i:2d}. {field:<20} ({count} 篇)")
        
        return [field for field, _ in fields]
    
    async def export_data(self, output_file: str = None) -> str:
        """导出数据"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"papers_export_{timestamp}.json"
        
        backup_path = await self.repository.backup_to_json(output_file)
        print(f"📁 数据已导出到: {backup_path}")
        return backup_path
    
    async def cleanup_database(self):
        """清理数据库（删除未处理的论文）"""
        count = await asyncio.get_event_loop().run_in_executor(
            None, self._cleanup_unprocessed
        )
        print(f"🧹 已清理 {count} 条未处理的论文记录")
    
    # 同步辅助方法
    def _get_papers_with_pagination(self, limit: int, offset: int) -> List[Dict]:
        """分页获取论文"""
        with sqlite3.connect(self.repository.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM papers 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            return [dict(row) for row in cursor.fetchall()]
    
    def _search_papers_sync(self, keyword: str) -> List[Dict]:
        """同步搜索论文"""
        with sqlite3.connect(self.repository.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM papers 
                WHERE title LIKE ? OR summary LIKE ?
                ORDER BY created_at DESC
            """, (f'%{keyword}%', f'%{keyword}%'))
            return [dict(row) for row in cursor.fetchall()]
    
    def _get_paper_by_id(self, paper_id: int) -> Optional[Dict]:
        """根据ID获取论文"""
        with sqlite3.connect(self.repository.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def _get_all_fields(self) -> List[tuple]:
        """获取所有研究领域及论文数量"""
        with sqlite3.connect(self.repository.db_path) as conn:
            cursor = conn.execute("""
                SELECT research_fields, COUNT(*) as count
                FROM papers 
                WHERE research_fields IS NOT NULL 
                GROUP BY research_fields
                ORDER BY count DESC
            """)
            
            # 解析JSON字段并统计
            field_counts = {}
            for row in cursor.fetchall():
                try:
                    fields = json.loads(row[0]) if row[0] else []
                    for field in fields:
                        field_counts[field] = field_counts.get(field, 0) + row[1]
                except:
                    continue
            
            return sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
    
    def _cleanup_unprocessed(self) -> int:
        """清理未处理的论文"""
        with sqlite3.connect(self.repository.db_path) as conn:
            cursor = conn.execute("DELETE FROM papers WHERE is_processed = 0")
            return cursor.rowcount
    
    async def _display_paper_list(self, papers: List[Dict], max_display: int = 10):
        """显示论文列表"""
        display_papers = papers[:max_display]
        
        table_data = []
        for paper in display_papers:
            try:
                fields = json.loads(paper['research_fields']) if paper['research_fields'] else []
                fields_str = ', '.join(fields[:2])
                if len(fields) > 2:
                    fields_str += f" (+{len(fields)-2})"
            except:
                fields_str = 'N/A'
            
            table_data.append([
                paper['id'],
                paper['title'][:50] + ('...' if len(paper['title']) > 50 else ''),
                paper['research_problem'][:50] + ('...' if len(paper['research_problem']) > 50 else ''),
                paper['key_contribution'][:50] + ('...' if len(paper['key_contribution']) > 50 else ''),
                paper['key_concepts_and_techniques'][:50] + ('...' if len(paper['key_concepts_and_techniques']) > 50 else ''),
                fields_str[:25] + ('...' if len(fields_str) > 25 else ''),
                '✅' if paper['is_processed'] else '⏳',
                paper['add_date'] or 'N/A'
            ])
        
        headers = ['ID', 'Title', 'Fields', 'Problem', 'Contribution', 'Techniques', 'Status', 'Date']
        print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=[4, 50, 25, 25, 25, 25, 8, 12]))
        
        if len(papers) > max_display:
            print(f"\n... 还有 {len(papers) - max_display} 篇论文未显示") 