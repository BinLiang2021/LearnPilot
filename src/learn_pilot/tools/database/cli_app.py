"""
@file_name: cli_app.py
@author: bin.liang
@date: 2025-06-28
@description: 论文数据库查看器CLI应用主程序
"""

import asyncio
import sys
from typing import Optional

from .db_viewer import PaperDBViewer
from src.learn_pilot.core.logging.logger import logger


class PaperDBCLI:
    """论文数据库CLI应用"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.viewer = PaperDBViewer(db_path)
        self.running = True
        
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 70)
        print("📚 论文数据库查看器 CLI v2.0")
        print("=" * 70)
        print("1️⃣  查看数据库统计")
        print("2️⃣  列出最近论文")
        print("3️⃣  搜索论文")
        print("4️⃣  按领域查看")
        print("5️⃣  查看论文详情")
        print("6️⃣  列出所有领域")
        print("7️⃣  导出数据")
        print("8️⃣  数据库清理")
        print("9️⃣  分页浏览")
        print("0️⃣  退出程序")
        print("-" * 70)
    
    async def run(self):
        """运行CLI应用"""
        print("🚀 启动论文数据库查看器...")
        
        try:
            # 显示初始统计
            await self.viewer.show_stats()
            
            while self.running:
                self.show_menu()
                choice = input("请选择操作 (0-9): ").strip()
                
                try:
                    await self.handle_choice(choice)
                except KeyboardInterrupt:
                    print("\n\n⚠️ 用户中断操作")
                    break
                except Exception as e:
                    print(f"\n❌ 操作失败: {str(e)}")
                    logger.error(f"CLI操作失败: {str(e)}")
                
                if choice != '0':
                    input("\n按 Enter 继续...")
                    
        except KeyboardInterrupt:
            print("\n👋 程序被用户终止")
        finally:
            print("👋 感谢使用论文数据库查看器!")
    
    async def handle_choice(self, choice: str):
        """处理用户选择"""
        if choice == '0':
            self.running = False
            return
        
        elif choice == '1':
            await self.viewer.show_stats()
            
        elif choice == '2':
            limit = self.get_int_input("显示论文数量", default=20, max_val=100)
            await self.viewer.list_papers(limit=limit)
            
        elif choice == '3':
            keyword = input("🔍 请输入搜索关键词: ").strip()
            if keyword:
                await self.viewer.search_papers(keyword)
            else:
                print("❌ 搜索关键词不能为空")
                
        elif choice == '4':
            fields = await self.viewer.list_fields()
            if fields:
                try:
                    index = self.get_int_input("选择领域编号", min_val=1, max_val=len(fields)) - 1
                    await self.viewer.show_papers_by_field(fields[index])
                except (ValueError, IndexError):
                    print("❌ 无效的领域编号")
            
        elif choice == '5':
            paper_id = self.get_int_input("论文ID", min_val=1)
            if paper_id:
                await self.viewer.show_paper_detail(paper_id)
                
        elif choice == '6':
            await self.viewer.list_fields()
            
        elif choice == '7':
            filename = input("📁 导出文件名 (留空使用默认): ").strip()
            await self.viewer.export_data(filename if filename else None)
            
        elif choice == '8':
            confirm = input("⚠️ 确认清理未处理的论文? (y/N): ").lower()
            if confirm == 'y':
                await self.viewer.cleanup_database()
            else:
                print("❌ 操作已取消")
                
        elif choice == '9':
            await self.paginated_browse()
            
        else:
            print("❌ 无效选择，请输入 0-9")
    
    async def paginated_browse(self):
        """分页浏览功能"""
        page = 0
        page_size = 10
        
        while True:
            papers = await self.viewer.list_papers(limit=page_size, offset=page * page_size)
            
            if not papers:
                if page == 0:
                    print("📭 暂无论文数据")
                else:
                    print("📄 已到达最后一页")
                break
            
            print(f"\n📄 第 {page + 1} 页 (每页 {page_size} 条)")
            print("操作: [n]下一页 [p]上一页 [d]查看详情 [q]退出")
            
            action = input("请选择操作: ").lower().strip()
            
            if action == 'n':
                page += 1
            elif action == 'p' and page > 0:
                page -= 1
            elif action == 'p' and page == 0:
                print("❌ 已经是第一页")
            elif action == 'd':
                try:
                    paper_id = int(input("请输入论文ID: "))
                    await self.viewer.show_paper_detail(paper_id)
                except ValueError:
                    print("❌ 请输入有效的论文ID")
            elif action == 'q':
                break
            else:
                print("❌ 无效操作")
    
    def get_int_input(self, prompt: str, default: int = None, min_val: int = None, max_val: int = None) -> Optional[int]:
        """获取整数输入"""
        while True:
            try:
                default_hint = f" (默认: {default})" if default is not None else ""
                range_hint = ""
                if min_val is not None and max_val is not None:
                    range_hint = f" ({min_val}-{max_val})"
                elif min_val is not None:
                    range_hint = f" (≥{min_val})"
                elif max_val is not None:
                    range_hint = f" (≤{max_val})"
                
                user_input = input(f"🔢 {prompt}{range_hint}{default_hint}: ").strip()
                
                if not user_input and default is not None:
                    return default
                
                if not user_input:
                    return None
                
                value = int(user_input)
                
                if min_val is not None and value < min_val:
                    print(f"❌ 值不能小于 {min_val}")
                    continue
                    
                if max_val is not None and value > max_val:
                    print(f"❌ 值不能大于 {max_val}")
                    continue
                    
                return value
                
            except ValueError:
                print("❌ 请输入有效的数字")
            except KeyboardInterrupt:
                return None


def run_cli(db_path: Optional[str] = None):
    """运行CLI应用入口点"""
    try:
        cli = PaperDBCLI(db_path)
        asyncio.run(cli.run())
    except Exception as e:
        print(f"❌ 应用启动失败: {str(e)}")
        logger.error(f"CLI应用启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="论文数据库查看器")
    parser.add_argument("--db", help="数据库文件路径", default=None)
    args = parser.parse_args()
    
    run_cli(args.db) 