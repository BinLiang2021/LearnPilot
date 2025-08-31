#!/usr/bin/env python3
"""
简单的管理员用户审批工具
直接操作数据库，绕过API问题
"""

from src.learn_pilot.database import init_database, db_manager
from src.learn_pilot.database.models import User, Admin, UserStatus, UserApprovalRecord, ApprovalAction
from datetime import datetime
import sys


def list_pending_users():
    """列出待审批用户"""
    init_database()
    db = db_manager.get_session()
    
    try:
        pending_users = db.query(User).filter(User.status == UserStatus.PENDING).all()
        
        if not pending_users:
            print("📋 没有待审批的用户")
            return []
        
        print(f"\n📋 待审批用户列表 ({len(pending_users)} 个):")
        print("-" * 100)
        print(f"{'ID':<4} {'用户名':<15} {'邮箱':<25} {'姓名':<15} {'注册时间':<20} {'备注':<20}")
        print("-" * 100)
        
        for user in pending_users:
            created_at = user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'N/A'
            notes = (user.registration_notes[:17] + '...') if user.registration_notes and len(user.registration_notes) > 20 else user.registration_notes or 'N/A'
            print(f"{user.id:<4} {user.username:<15} {user.email or 'N/A':<25} "
                  f"{user.name:<15} {created_at:<20} {notes:<20}")
        
        print("-" * 100)
        return pending_users
        
    finally:
        db.close()


def approve_user(user_id, action='approve', reason='', notes=''):
    """审批用户"""
    init_database()
    db = db_manager.get_session()
    
    try:
        # 查找用户
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"❌ 用户ID {user_id} 不存在")
            return False
        
        if user.status != UserStatus.PENDING:
            print(f"❌ 用户 {user.username} 状态不是待审批 (当前状态: {user.status.value})")
            return False
        
        # 查找管理员 (使用默认admin)
        admin = db.query(Admin).filter(Admin.username == 'admin').first()
        if not admin:
            print("❌ 未找到管理员账户")
            return False
        
        # 更新用户状态
        previous_status = user.status.value
        
        if action == 'approve':
            user.status = UserStatus.APPROVED
            user.approved_at = datetime.now()
            user.approved_by = admin.id
            user.rejection_reason = None
            print(f"✅ 用户 {user.username} 已批准")
            
        elif action == 'reject':
            user.status = UserStatus.REJECTED
            user.rejection_reason = reason
            print(f"❌ 用户 {user.username} 已拒绝，原因: {reason}")
        
        # 创建审批记录
        approval_record = UserApprovalRecord(
            user_id=user.id,
            admin_id=admin.id,
            action=ApprovalAction.APPROVE if action == 'approve' else ApprovalAction.REJECT,
            reason=reason,
            notes=notes,
            previous_status=previous_status,
            new_status=user.status.value
        )
        
        db.add(approval_record)
        db.commit()
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ 审批失败: {e}")
        return False
    finally:
        db.close()


def interactive_approval():
    """交互式审批"""
    while True:
        users = list_pending_users()
        
        if not users:
            break
        
        print("\n🔧 用户审批操作:")
        print("输入用户ID进行审批，或输入 'q' 退出")
        
        try:
            user_input = input("\n请输入用户ID: ").strip()
            
            if user_input.lower() == 'q':
                break
            
            user_id = int(user_input)
            
            # 检查用户ID是否存在
            user = next((u for u in users if u.id == user_id), None)
            if not user:
                print("❌ 用户ID不存在")
                continue
            
            # 显示用户详情
            print(f"\n👤 用户详情:")
            print(f"   ID: {user.id}")
            print(f"   用户名: {user.username}")
            print(f"   姓名: {user.name}")
            print(f"   邮箱: {user.email or 'N/A'}")
            print(f"   等级: {user.level}")
            print(f"   兴趣: {', '.join(user.interests) if user.interests else 'N/A'}")
            print(f"   学习时间: {user.daily_hours}小时/天")
            print(f"   注册时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A'}")
            if user.registration_notes:
                print(f"   注册备注: {user.registration_notes}")
            
            print(f"\n选择操作:")
            print("1. 批准 (approve)")
            print("2. 拒绝 (reject)")
            print("3. 跳过")
            
            action_input = input("请选择 (1-3): ").strip()
            
            if action_input == '1':
                reason = input("批准原因 (可选): ").strip() or "管理员审批通过"
                notes = input("备注 (可选): ").strip()
                
                if approve_user(user_id, "approve", reason, notes):
                    print(f"✅ 用户 {user.username} 审批完成")
            
            elif action_input == '2':
                reason = input("拒绝原因 (必填): ").strip()
                if not reason:
                    print("❌ 拒绝原因不能为空")
                    continue
                
                notes = input("备注 (可选): ").strip()
                
                if approve_user(user_id, "reject", reason, notes):
                    print(f"❌ 用户 {user.username} 已拒绝")
            
            elif action_input == '3':
                print("⏭️  跳过该用户")
                continue
            
            else:
                print("❌ 无效选择")
        
        except ValueError:
            print("❌ 请输入有效的用户ID")
        except KeyboardInterrupt:
            print("\n👋 操作取消")
            break
        except Exception as e:
            print(f"❌ 操作错误: {e}")


def main():
    print("🚀 LearnPilot 简单管理员工具")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # 命令行模式
        if sys.argv[1] == 'list':
            list_pending_users()
        elif sys.argv[1] == 'approve' and len(sys.argv) >= 3:
            user_id = int(sys.argv[2])
            reason = sys.argv[3] if len(sys.argv) > 3 else "命令行批准"
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            approve_user(user_id, 'approve', reason, notes)
        elif sys.argv[1] == 'reject' and len(sys.argv) >= 4:
            user_id = int(sys.argv[2])
            reason = sys.argv[3]
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            approve_user(user_id, 'reject', reason, notes)
        else:
            print("用法:")
            print("  python3 simple_admin.py list                    # 列出待审批用户")
            print("  python3 simple_admin.py approve <用户ID> [原因] [备注]  # 批准用户")
            print("  python3 simple_admin.py reject <用户ID> <原因> [备注]   # 拒绝用户")
    else:
        # 交互模式
        print("📋 交互式用户审批")
        interactive_approval()
        print("👋 审批完成")


if __name__ == "__main__":
    main()