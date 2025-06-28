"""
@file_name: __main__.py
@author: bin.liang
@date: 2025-06-28
@description: 论文数据库查看器模块主入口点
"""

import sys
import argparse
from .cli_app import run_cli


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="📚 论文数据库查看器 - 智能论文管理系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python -m common_tools.db_app                    # 使用默认数据库
  python -m common_tools.db_app --db custom.db     # 指定数据库文件
  
功能特点:
  • 📊 数据库统计信息
  • 🔍 智能搜索论文
  • 🏷️ 按领域分类浏览
  • 📄 详细论文信息
  • 📁 数据导出功能
  • 🧹 数据库清理工具
        """
    )
    
    parser.add_argument(
        "--db", 
        metavar="PATH",
        help="指定数据库文件路径 (默认: user_data/{USER_NAME}/papers.db)",
        default=None
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Paper DB Viewer v2.0"
    )
    
    args = parser.parse_args()
    
    # 显示启动信息
    print("=" * 70)
    print("📚 论文数据库查看器 v2.0")
    print("=" * 70)
    
    if args.db:
        print(f"🗄️ 使用数据库: {args.db}")
    else:
        print("🗄️ 使用默认数据库路径")
    
    try:
        run_cli(args.db)
    except KeyboardInterrupt:
        print("\n👋 程序被用户终止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序运行出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 