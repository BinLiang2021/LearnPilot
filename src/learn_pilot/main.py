""" 
@file_name: main.py
@author: Bin Liang
@date: 2025-06-27
@updated: 2025-06-28 - 添加AI-Paper-Tutor功能

LearnPilot AI-Paper-Tutor 主入口
"""

import os
import sys
import argparse
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.learn_pilot.core.config.config import USER_DATA_PATH
from src.learn_pilot.services.pipeline_orchestrator import PipelineOrchestrator

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/learnpilot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_directories():
    """设置必要的目录结构"""
    directories = [
        USER_DATA_PATH,
        f"{USER_DATA_PATH}/papers",
        f"{USER_DATA_PATH}/outputs", 
        f"{USER_DATA_PATH}/temp",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"确保目录存在: {directory}")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="LearnPilot AI-Paper-Tutor - 智能论文学习助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 完整流水线处理
  python -m src.learn_pilot.main --input_dir=./user_data/papers --output_dir=./user_data/outputs
  
  # 只运行特定步骤
  python -m src.learn_pilot.main --step=analysis --input_dir=./user_data/papers
  
  # 设置用户偏好
  python -m src.learn_pilot.main --input_dir=./user_data/papers --user_level=beginner --daily_hours=2
        """
    )
    
    # 基本参数
    parser.add_argument(
        '--input_dir', 
        type=str, 
        default='./user_data/papers',
        help='输入论文目录 (Markdown格式)'
    )
    
    parser.add_argument(
        '--output_dir', 
        type=str, 
        default='./user_data/outputs',
        help='输出结果目录'
    )
    
    # 流水线控制
    parser.add_argument(
        '--step', 
        type=str, 
        choices=['analysis', 'extraction', 'full'],
        default='full',
        help='执行特定步骤或完整流水线'
    )
    
    # 用户偏好设置
    parser.add_argument(
        '--user_level', 
        type=str, 
        choices=['beginner', 'intermediate', 'advanced'],
        default='intermediate',
        help='用户学习水平'
    )
    
    parser.add_argument(
        '--daily_hours', 
        type=float, 
        default=2.0,
        help='每日可用学习时长（小时）'
    )
    
    parser.add_argument(
        '--total_days', 
        type=int, 
        default=7,
        help='总学习天数'
    )
    
    parser.add_argument(
        '--learning_goals', 
        type=str, 
        default='深入理解论文核心概念和方法',
        help='学习目标描述'
    )
    
    # 高级选项
    parser.add_argument(
        '--config_file', 
        type=str, 
        help='配置文件路径 (JSON格式)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='详细输出模式'
    )
    
    parser.add_argument(
        '--dry_run', 
        action='store_true',
        help='试运行模式（不执行实际操作）'
    )
    
    return parser.parse_args()

def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        "model_settings": {
            "temperature": 0.7,
            "max_tokens": 2000,
            "model_name": "gpt-4"
        },
        "processing_settings": {
            "chunk_size": 1000,
            "overlap": 200,
            "language": "zh-cn"
        },
        "output_settings": {
            "format": "markdown",
            "include_code": True,
            "include_graphs": True
        }
    }
    
    if config_file and os.path.exists(config_file):
        import json
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"已加载配置文件: {config_file}")
        except Exception as e:
            logger.warning(f"配置文件加载失败: {e}, 使用默认配置")
    
    return default_config

def create_user_preferences(args) -> Dict[str, Any]:
    """创建用户偏好设置"""
    return {
        "user_level": args.user_level,
        "daily_hours": args.daily_hours,
        "total_days": args.total_days,
        "learning_goals": args.learning_goals,
        "preferred_domains": [],  # 可以从历史数据推断
        "language": "zh-cn"
    }

def validate_inputs(args) -> bool:
    """验证输入参数"""
    # 检查输入目录
    if not os.path.exists(args.input_dir):
        logger.error(f"输入目录不存在: {args.input_dir}")
        return False
    
    # 检查是否有markdown文件
    input_path = Path(args.input_dir)
    md_files = list(input_path.glob("*.md"))
    if not md_files:
        logger.error(f"输入目录中没有找到Markdown文件: {args.input_dir}")
        return False
    
    logger.info(f"找到 {len(md_files)} 个论文文件")
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    return True

async def async_main():
    """异步主函数"""
    # 设置目录
    setup_directories()
    
    # 解析参数
    args = parse_arguments()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 启动 LearnPilot AI-Paper-Tutor")
    logger.info(f"📁 输入目录: {args.input_dir}")
    logger.info(f"📁 输出目录: {args.output_dir}")
    logger.info(f"🎯 执行步骤: {args.step}")
    logger.info(f"👤 用户水平: {args.user_level}")
    
    # 试运行模式
    if args.dry_run:
        logger.info("🧪 试运行模式 - 不执行实际操作")
        logger.info("配置验证完成，实际运行时将执行完整流水线")
        return
    
    # 验证输入
    if not validate_inputs(args):
        logger.error("❌ 输入验证失败")
        sys.exit(1)
    
    try:
        # 加载配置
        config = load_config(args.config_file)
        logger.info("✅ 配置加载完成")
        
        # 创建用户偏好
        user_preferences = create_user_preferences(args)
        logger.info("✅ 用户偏好设置完成")
        
        # 初始化流水线编排器
        orchestrator = PipelineOrchestrator(config=config)
        logger.info("✅ 流水线编排器初始化完成")
        
        # 执行流水线
        if args.step == 'full':
            logger.info("🔄 开始执行完整AI-Paper-Tutor流水线...")
            results = await orchestrator.run_full_pipeline(
                input_dir=args.input_dir,
                output_dir=args.output_dir,
                user_preferences=user_preferences
            )
        else:
            logger.info(f"🔄 执行单个步骤: {args.step}")
            results = await orchestrator.run_single_step(
                step_name=args.step,
                input_dir=args.input_dir,
                output_dir=args.output_dir,
                user_preferences=user_preferences
            )
        
        logger.info("✅ 流水线执行完成!")
        logger.info(f"📊 结果已保存到: {args.output_dir}")
        
        # 输出简要统计
        if results:
            logger.info("📈 执行统计:")
            for key, value in results.items():
                if isinstance(value, (list, dict)):
                    logger.info(f"  - {key}: {len(value)} 项")
                else:
                    logger.info(f"  - {key}: {value}")
        
    except KeyboardInterrupt:
        logger.info("⏸️  用户中断执行")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ 执行失败: {e}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)

def main():
    """主函数入口"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
    