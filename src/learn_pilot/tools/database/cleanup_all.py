"""
@file_name: cleanup_all.py
@author: bin.liang
@date: 2025-06-28
@description: 完全清空数据库和相关下载文件的脚本
⚠️  警告：此脚本会永久删除所有数据，请谨慎使用！
"""

import os
import sqlite3
import shutil
import asyncio
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

from src.learn_pilot.core.logging.logger import logger
from src.learn_pilot.core.config.config import DATA_DIR


class DatabaseCleaner:
    """数据库和文件完全清理工具"""
    
    def __init__(self, db_path: Optional[str] = None, data_dir: Optional[str] = None):
        self.db_path = db_path or f"{DATA_DIR}/papers.db"
        self.data_dir = Path(data_dir or DATA_DIR)
        self.ai_recommend_dir = self.data_dir / "ai_recommend"
        
    def get_current_status(self) -> dict:
        """获取当前数据库和文件状态"""
        status = {
            'db_exists': Path(self.db_path).exists(),
            'db_size': 0,
            'paper_count': 0,
            'download_dir_exists': self.ai_recommend_dir.exists(),
            'download_files_count': 0,
            'total_files_size': 0
        }
        
        # 检查数据库状态
        if status['db_exists']:
            db_path = Path(self.db_path)
            status['db_size'] = db_path.stat().st_size
            
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute("SELECT COUNT(*) FROM papers")
                    status['paper_count'] = cursor.fetchone()[0]
            except Exception as e:
                logger.warning(f"无法读取数据库记录数: {e}")
        
        # 检查下载文件状态
        if status['download_dir_exists']:
            try:
                for root, dirs, files in os.walk(self.ai_recommend_dir):
                    for file in files:
                        file_path = Path(root) / file
                        if file_path.exists():
                            status['download_files_count'] += 1
                            status['total_files_size'] += file_path.stat().st_size
            except Exception as e:
                logger.warning(f"无法扫描下载文件: {e}")
        
        return status
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    def display_status(self, status: dict):
        """显示当前状态"""
        print("\n" + "=" * 70)
        print("📊 当前数据状态")
        print("=" * 70)
        
        # 数据库信息
        if status['db_exists']:
            print(f"🗄️  数据库文件: {self.db_path}")
            print(f"📄 论文记录数: {status['paper_count']:,}")
            print(f"💾 数据库大小: {self.format_size(status['db_size'])}")
        else:
            print("🗄️  数据库文件: 不存在")
        
        print()
        
        # 下载文件信息
        if status['download_dir_exists']:
            print(f"📁 下载文件目录: {self.ai_recommend_dir}")
            print(f"📄 下载文件数: {status['download_files_count']:,}")
            print(f"💾 文件总大小: {self.format_size(status['total_files_size'])}")
        else:
            print("📁 下载文件目录: 不存在")
        
        print("=" * 70)
    
    def clear_database(self) -> Tuple[bool, str]:
        """清空数据库"""
        try:
            if not Path(self.db_path).exists():
                return True, "数据库文件不存在，无需清理"
            
            # 获取清理前的记录数
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM papers")
                before_count = cursor.fetchone()[0]
            
            # 清空表和重置自增ID（在事务中）
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM papers")
                conn.execute("DELETE FROM sqlite_sequence WHERE name='papers'")
                conn.commit()
            
            # VACUUM 必须在事务外执行
            conn = sqlite3.connect(self.db_path)
            try:
                conn.execute("VACUUM")
            finally:
                conn.close()
                
            logger.info(f"🗑️  已清空数据库，删除了 {before_count} 条记录")
            return True, f"成功清空数据库，删除了 {before_count} 条记录"
                
        except Exception as e:
            error_msg = f"清空数据库失败: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return False, error_msg
    
    def clear_download_files(self) -> Tuple[bool, str]:
        """清空下载文件"""
        try:
            if not self.ai_recommend_dir.exists():
                return True, "下载目录不存在，无需清理"
            
            # 统计文件信息
            file_count = 0
            total_size = 0
            
            for root, dirs, files in os.walk(self.ai_recommend_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        file_count += 1
                        total_size += file_path.stat().st_size
            
            # 删除整个目录
            shutil.rmtree(self.ai_recommend_dir)
            
            # 重新创建空目录
            self.ai_recommend_dir.mkdir(parents=True, exist_ok=True)
            
            size_str = self.format_size(total_size)
            result_msg = f"成功删除 {file_count} 个文件，释放空间 {size_str}"
            logger.info(f"🗑️  {result_msg}")
            return True, result_msg
            
        except Exception as e:
            error_msg = f"清空下载文件失败: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return False, error_msg
    
    def confirm_operation(self, status: dict) -> bool:
        """确认操作"""
        if status['paper_count'] == 0 and status['download_files_count'] == 0:
            print("✅ 数据库和文件目录已经是空的，无需清理")
            return False
        
        print("\n" + "⚠️ " * 25)
        print("🚨 危险操作警告 🚨")
        print("⚠️ " * 25)
        print("此操作将会 永久删除 以下数据：")
        
        if status['paper_count'] > 0:
            print(f"  • {status['paper_count']:,} 条论文记录")
            print(f"  • 数据库文件 ({self.format_size(status['db_size'])})")
        
        if status['download_files_count'] > 0:
            print(f"  • {status['download_files_count']:,} 个下载文件")
            print(f"  • 总计 {self.format_size(status['total_files_size'])} 数据")
        
        print("\n❌ 此操作 无法撤销！所有数据将永久丢失！")
        print("⚠️ " * 25)
        
        # 三重确认机制
        print("\n请输入以下确认信息：")
        
        # 第一次确认
        confirm1 = input("1️⃣ 输入 'YES' 确认要删除所有数据: ").strip()
        if confirm1 != 'YES':
            print("❌ 操作已取消")
            return False
        
        # 第二次确认
        confirm2 = input("2️⃣ 输入 'DELETE' 确认理解数据无法恢复: ").strip()
        if confirm2 != 'DELETE':
            print("❌ 操作已取消")
            return False
        
        # 第三次确认 - 时间戳验证
        current_time = datetime.now().strftime("%H%M")
        confirm3 = input(f"3️⃣ 输入当前时间 '{current_time}' 进行最终确认: ").strip()
        if confirm3 != current_time:
            print("❌ 时间验证失败，操作已取消")
            return False
        
        return True
    
    async def cleanup_all(self, force: bool = False) -> bool:
        """执行完全清理"""
        print("\n🧹 论文数据库完全清理工具")
        print("=" * 50)
        
        # 获取当前状态
        status = self.get_current_status()
        self.display_status(status)
        
        # 确认操作
        if not force and not self.confirm_operation(status):
            return False
        
        print("\n🚀 开始清理操作...")
        
        success_count = 0
        
        # 清空数据库
        if status['db_exists'] and status['paper_count'] > 0:
            print("\n1️⃣ 正在清空数据库...")
            db_success, db_msg = self.clear_database()
            print(f"   {'✅' if db_success else '❌'} {db_msg}")
            if db_success:
                success_count += 1
        else:
            print("\n1️⃣ 数据库无需清理")
            success_count += 1
        
        # 清空下载文件
        if status['download_dir_exists'] and status['download_files_count'] > 0:
            print("\n2️⃣ 正在清空下载文件...")
            files_success, files_msg = self.clear_download_files()
            print(f"   {'✅' if files_success else '❌'} {files_msg}")
            if files_success:
                success_count += 1
        else:
            print("\n2️⃣ 下载文件无需清理")
            success_count += 1
        
        # 显示结果
        print("\n" + "=" * 50)
        if success_count == 2:
            print("🎉 清理操作完成！所有数据已成功删除")
            print("💡 提示：现在可以重新开始收集论文数据")
        else:
            print("⚠️  清理操作部分失败，请检查错误信息")
        print("=" * 50)
        
        return success_count == 2


async def main():
    """主函数 - 命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="论文数据库完全清理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
警告：此工具会永久删除所有论文数据和下载文件！

使用示例：
  python cleanup_all.py                    # 交互式清理
  python cleanup_all.py --force            # 强制清理（跳过确认）
  python cleanup_all.py --db /path/to/custom.db  # 使用自定义数据库

⚠️ 强烈建议在清理前备份重要数据！
        """
    )
    
    parser.add_argument(
        '--db', '--database',
        type=str,
        help='指定数据库文件路径（可选）'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        help='指定数据目录路径（可选）'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制执行清理，跳过确认步骤（危险！）'
    )
    
    parser.add_argument(
        '--status-only',
        action='store_true',
        help='仅显示当前状态，不执行清理'
    )
    
    args = parser.parse_args()
    
    # 创建清理器
    cleaner = DatabaseCleaner(
        db_path=args.db,
        data_dir=args.data_dir
    )
    
    if args.status_only:
        # 仅显示状态
        status = cleaner.get_current_status()
        cleaner.display_status(status)
        return
    
    # 执行清理
    success = await cleaner.cleanup_all(force=args.force)
    
    if success:
        print("\n✨ 清理完成！系统已重置为初始状态")
    else:
        print("\n❌ 清理操作失败或被取消")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 