""" 
@file_name: paper_daily.py
@author: bin.liang
@date: 2025-06-28
@description: 论文监控日常任务入口点 - 使用新的PaperService架构
"""

import asyncio
from src.learn_pilot.core.logging.logger import logger
from src.learn_pilot.core.config.config import DATA_DIR
from src.learn_pilot.services.arxiv_monitor.paper_service import PaperService


async def fetch_cat_http(cat_code, search_term='', max_results=2000, download_selected=True, save_dir=f"{DATA_DIR}/ai_files"):
    """
    按类别获取论文的简化入口函数（向后兼容）
    
    Args:
        cat_code: arXiv类别代码
        search_term: 搜索词
        max_results: 最大结果数
        download_selected: 是否下载选中的论文
        save_dir: 保存目录
        
    Returns:
        处理结果统计
    """
    logger.info(f"🚀 开始论文监控任务: {cat_code}")
    
    # 使用新的PaperService
    service = PaperService(save_dir=save_dir)
    
    try:
        stats = await service.process_papers_by_category(
            category=cat_code,
            search_term=search_term,
            max_results=max_results
        )
        
        logger.info(f"📊 任务完成统计: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"❌ 论文监控任务失败: {str(e)}")
        return {
            'total_papers': 0,
            'selected_papers': 0,
            'downloaded_papers': 0,
            'error_count': 1,
            'success_rate': '0%'
        }


if __name__ == "__main__":
    # 运行示例
    stats = asyncio.run(fetch_cat_http('cs.AI', download_selected=True, save_dir=f"{DATA_DIR}/ai_recommend"))
    print(f"\n📊 论文处理完成:")
    print(f"   • 总计: {stats['total_papers']} 篇")
    print(f"   • 选中: {stats['selected_papers']} 篇")
    print(f"   • 下载: {stats['downloaded_papers']} 篇")
    print(f"   • 成功率: {stats['success_rate']}")