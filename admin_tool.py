#!/usr/bin/env python3
"""
LearnPilot 管理员工具
用于用户审批和管理操作
"""

import requests
import json
from datetime import datetime
from typing import Optional, List, Dict, Any


class LearnPilotAdmin:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.admin_info = None
    
    def login(self, username: str = "admin", password: str = "admin123") -> bool:
        """管理员登录"""
        try:
            response = requests.post(f"{self.base_url}/api/admin/login", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]["access_token"]
                self.admin_info = data["admin"]
                print(f"✅ 管理员登录成功: {self.admin_info['name']} ({self.admin_info['role']})")
                return True
            else:
                print(f"❌ 登录失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 登录错误: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        if not self.token:
            raise Exception("请先登录")
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_pending_users(self) -> List[Dict[str, Any]]:
        """获取待审批用户列表"""
        try:
            response = requests.get(
                f"{self.base_url}/api/admin/users/pending", 
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("pending_users", [])
            else:
                print(f"❌ 获取待审批用户失败: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ 获取用户列表错误: {e}")
            return []
    
    def approve_user(self, user_id: int, action: str = "approve", reason: str = "", notes: str = "") -> bool:
        """审批用户
        
        Args:
            user_id: 用户ID
            action: 动作 (approve, reject, suspend, reactivate)
            reason: 原因
            notes: 备注
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/admin/users/approve",
                headers=self._get_headers(),
                json={
                    "user_id": user_id,
                    "action": action,
                    "reason": reason,
                    "notes": notes
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 用户审批成功: {data['status']}")
                return True
            else:
                print(f"❌ 用户审批失败: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 审批错误: {e}")
            return False
    
    def list_pending_users(self):
        """显示待审批用户列表"""
        users = self.get_pending_users()
        
        if not users:
            print("📋 没有待审批的用户")
            return
        
        print(f"\n📋 待审批用户列表 ({len(users)} 个):")
        print("-" * 80)
        print(f"{'ID':<4} {'用户名':<15} {'邮箱':<25} {'姓名':<15} {'注册时间':<20}")
        print("-" * 80)
        
        for user in users:
            created_at = user.get('created_at', '')[:16].replace('T', ' ')  # 简化时间格式
            print(f"{user['id']:<4} {user['username']:<15} {user.get('email', 'N/A'):<25} "
                  f"{user['name']:<15} {created_at:<20}")
        
        print("-" * 80)
    
    def interactive_approval(self):
        """交互式用户审批"""
        self.list_pending_users()
        users = self.get_pending_users()
        
        if not users:
            return
        
        print("\n🔧 用户审批操作:")
        print("1. 输入用户ID进行审批")
        print("2. 输入 'q' 退出")
        
        while True:
            try:
                user_input = input("\n请输入用户ID (或 'q' 退出): ").strip()
                
                if user_input.lower() == 'q':
                    break
                
                user_id = int(user_input)
                
                # 检查用户ID是否存在
                user = next((u for u in users if u['id'] == user_id), None)
                if not user:
                    print("❌ 用户ID不存在")
                    continue
                
                print(f"\n👤 用户详情:")
                print(f"   ID: {user['id']}")
                print(f"   用户名: {user['username']}")
                print(f"   姓名: {user['name']}")
                print(f"   邮箱: {user.get('email', 'N/A')}")
                print(f"   等级: {user.get('level', 'N/A')}")
                print(f"   兴趣: {', '.join(user.get('interests', []))}")
                print(f"   注册时间: {user.get('created_at', 'N/A')}")
                if user.get('registration_notes'):
                    print(f"   注册备注: {user['registration_notes']}")
                
                print(f"\n选择操作:")
                print("1. 批准 (approve)")
                print("2. 拒绝 (reject)")
                print("3. 跳过")
                
                action_input = input("请选择 (1-3): ").strip()
                
                if action_input == '1':
                    reason = input("批准原因 (可选): ").strip() or "管理员审批通过"
                    notes = input("备注 (可选): ").strip()
                    
                    if self.approve_user(user_id, "approve", reason, notes):
                        users = [u for u in users if u['id'] != user_id]  # 从列表中移除已处理的用户
                        if not users:
                            print("✅ 所有待审批用户已处理完成")
                            break
                
                elif action_input == '2':
                    reason = input("拒绝原因 (必填): ").strip()
                    if not reason:
                        print("❌ 拒绝原因不能为空")
                        continue
                    
                    notes = input("备注 (可选): ").strip()
                    
                    if self.approve_user(user_id, "reject", reason, notes):
                        users = [u for u in users if u['id'] != user_id]  # 从列表中移除已处理的用户
                        if not users:
                            print("✅ 所有待审批用户已处理完成")
                            break
                
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
    print("🚀 LearnPilot 管理员工具")
    print("=" * 40)
    
    admin = LearnPilotAdmin()
    
    # 尝试登录
    if not admin.login():
        print("❌ 无法登录，请检查:")
        print("   1. 后端是否在运行 (http://localhost:8000)")
        print("   2. 管理员账户密码是否正确")
        return
    
    # 显示菜单
    while True:
        print(f"\n📋 管理员面板 - {admin.admin_info['name']}")
        print("-" * 30)
        print("1. 查看待审批用户")
        print("2. 交互式用户审批")
        print("3. 退出")
        
        try:
            choice = input("请选择操作 (1-3): ").strip()
            
            if choice == '1':
                admin.list_pending_users()
            elif choice == '2':
                admin.interactive_approval()
            elif choice == '3':
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请输入 1-3")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 操作错误: {e}")


if __name__ == "__main__":
    main()