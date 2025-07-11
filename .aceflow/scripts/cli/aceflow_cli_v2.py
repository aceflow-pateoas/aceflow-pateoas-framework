#!/usr/bin/env python3
"""
AceFlow CLI 增强版 v2.0
支持轻量级、标准、完整三种模式的命令行界面
"""

import argparse
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
import questionary
from datetime import datetime
import subprocess
import webbrowser

# 导入核心模块
sys.path.append(str(Path(__file__).parent.parent))
from core.multi_mode_state_engine import MultiModeStateEngine, FlowMode, StageStatus
from init_wizard import AceFlowInitWizard

class AceFlowCLI:
    """AceFlow命令行界面"""
    
    def __init__(self):
        self.engine = None
        self.project_root = Path.cwd()
        self.aceflow_dir = self.project_root / ".aceflow"
        
    def _ensure_initialized(self) -> bool:
        """确保项目已初始化"""
        if not self.aceflow_dir.exists():
            print("❌ 当前目录未初始化AceFlow项目")
            if questionary.confirm("是否现在初始化？").ask():
                wizard = AceFlowInitWizard()
                wizard.run()
                return self.aceflow_dir.exists()
            return False
        
        if not self.engine:
            self.engine = MultiModeStateEngine(self.project_root)
        return True
    
    def cmd_init(self, args):
        """初始化项目"""
        wizard = AceFlowInitWizard()
        
        if args.mode:
            # 非交互模式
            print(f"🚀 初始化AceFlow项目 (模式: {args.mode})")
            # TODO: 实现非交互式初始化
            print("非交互式初始化功能开发中...")
        else:
            # 交互模式
            wizard.run()
    
    def cmd_status(self, args):
        """显示项目状态"""
        if not self._ensure_initialized():
            return
        
        summary = self.engine.get_flow_summary()
        
        print("\\n" + "="*50)
        print("🏗️  AceFlow 项目状态")
        print("="*50)
        print(f"📊 流程模式: {summary['mode']}")
        print(f"🎯 当前阶段: {summary['current_stage']}")
        print(f"📈 整体进度: {summary['overall_progress']}%")
        print(f"✅ 完成阶段: {summary['completed_stages']}/{summary['total_stages']}")
        
        print("\\n🔄 阶段详情:")
        for stage in summary['stages']:
            status_icon = self._get_status_icon(stage['status'])
            assignee = f" ({stage['assignee']})" if stage['assignee'] else ""
            print(f"  {status_icon} {stage['id']} - {stage['name']} [{stage['progress']}%]{assignee}")
        
        if args.verbose:
            self._show_detailed_status()
    
    def cmd_next(self, args):
        """获取下一步建议"""
        if not self._ensure_initialized():
            return
        
        actions = self.engine.get_next_actions()
        
        if not actions:
            print("🎉 当前没有待办事项，项目进展顺利！")
            return
        
        print("\\n🎯 下一步行动建议:")
        for i, action in enumerate(actions, 1):
            priority_icon = "🔴" if action['priority'] == 'high' else "🟡" if action['priority'] == 'medium' else "🟢"
            print(f"  {i}. {priority_icon} {action['title']}")
            print(f"     {action['description']}")
        
        if args.auto:
            # 自动执行高优先级任务
            high_priority_actions = [a for a in actions if a['priority'] == 'high']
            if high_priority_actions:
                action = high_priority_actions[0]
                print(f"\\n🚀 自动执行: {action['title']}")
                self._execute_action(action)
    
    def cmd_progress(self, args):
        """更新进度"""
        if not self._ensure_initialized():
            return
        
        current_stage = self.engine.state.get('current_stage')
        if not current_stage:
            print("❌ 没有当前活动阶段")
            return
        
        if args.stage:
            stage_id = args.stage
        else:
            stage_id = current_stage
        
        if args.progress is not None:
            # 直接设置进度
            self.engine.update_stage_state(stage_id, progress=args.progress)
            print(f"✅ 已更新阶段 {stage_id} 进度为 {args.progress}%")
        else:
            # 交互式更新
            self._interactive_progress_update(stage_id)
    
    def cmd_start(self, args):
        """开始阶段"""
        if not self._ensure_initialized():
            return
        
        stage_id = args.stage or self.engine.state.get('current_stage')
        if not stage_id:
            print("❌ 请指定要开始的阶段")
            return
        
        assignee = args.assignee or questionary.text("负责人 (可选):").ask()
        
        success = self.engine.start_stage(stage_id, assignee if assignee else None)
        if success:
            print(f"🚀 已开始阶段: {stage_id}")
            
            # 显示阶段信息
            stage_info = self.engine._get_stage_info_by_id(stage_id)
            if stage_info:
                print(f"📋 阶段名称: {stage_info.display_name}")
                print(f"📝 阶段描述: {stage_info.description}")
                print(f"⏱️  预计时间: {stage_info.duration_estimate}")
                print(f"📦 交付物: {', '.join(stage_info.deliverables)}")
        else:
            print(f"❌ 开始阶段失败: {stage_id}")
    
    def cmd_complete(self, args):
        """完成阶段"""
        if not self._ensure_initialized():
            return
        
        stage_id = args.stage or self.engine.state.get('current_stage')
        if not stage_id:
            print("❌ 请指定要完成的阶段")
            return
        
        notes = []
        if args.notes:
            notes = [args.notes]
        elif not args.no_notes:
            note = questionary.text("完成备注 (可选):").ask()
            if note:
                notes = [note]
        
        success = self.engine.complete_stage(stage_id, notes)
        if success:
            print(f"✅ 已完成阶段: {stage_id}")
            
            # 显示下一阶段
            next_stage = self.engine.state.get('current_stage')
            if next_stage and next_stage != stage_id:
                next_stage_info = self.engine._get_stage_info_by_id(next_stage)
                if next_stage_info:
                    print(f"➡️  下一阶段: {next_stage_info.display_name}")
        else:
            print(f"❌ 完成阶段失败: {stage_id}")
    
    def cmd_mode(self, args):
        """切换流程模式"""
        if not self._ensure_initialized():
            return
        
        current_mode = self.engine.current_mode
        
        if args.mode:
            new_mode = FlowMode(args.mode)
            if new_mode == current_mode:
                print(f"✅ 已经是 {new_mode.value} 模式")
                return
            
            if not args.force:
                print(f"当前模式: {current_mode.value}")
                print(f"目标模式: {new_mode.value}")
                
                if not questionary.confirm(
                    f"确定要切换到 {new_mode.value} 模式吗？",
                    default=False
                ).ask():
                    print("取消切换")
                    return
            
            preserve_progress = not args.reset
            success = self.engine.switch_flow_mode(new_mode, preserve_progress)
            
            if success:
                print(f"✅ 已切换到 {new_mode.value} 模式")
                if preserve_progress:
                    print("✅ 进度数据已保留")
                else:
                    print("⚠️  进度数据已重置")
            else:
                print(f"❌ 切换模式失败")
        else:
            # 显示当前模式信息
            print(f"当前模式: {current_mode.value}")
            modes = [
                ("minimal", "轻量级模式 (P→D→R)"),
                ("standard", "标准模式 (P1→P2→D1→D2→R1)"),
                ("complete", "完整模式 (S1→S2→S3→S4→S5→S6→S7→S8)")
            ]
            
            print("\\n可用模式:")
            for mode_id, description in modes:
                current = " (当前)" if mode_id == current_mode.value else ""
                print(f"  - {mode_id}: {description}{current}")
    
    def cmd_deliverable(self, args):
        """管理交付物"""
        if not self._ensure_initialized():
            return
        
        stage_id = args.stage or self.engine.state.get('current_stage')
        if not stage_id:
            print("❌ 请指定阶段")
            return
        
        if args.list:
            # 列出交付物
            self._list_deliverables(stage_id)
        elif args.deliverable:
            # 更新交付物状态
            completed = not args.incomplete
            self.engine.update_deliverable_status(stage_id, args.deliverable, completed)
            status = "完成" if completed else "未完成"
            print(f"✅ 已标记交付物 '{args.deliverable}' 为{status}")
        else:
            # 交互式管理
            self._interactive_deliverable_management(stage_id)
    
    def cmd_memory(self, args):
        """记忆管理"""
        if not self._ensure_initialized():
            return
        
        if args.add:
            # 添加记忆
            self._add_memory_interactive()
        elif args.search:
            # 搜索记忆
            self._search_memory(args.search)
        elif args.list:
            # 列出记忆
            self._list_memories(args.type)
        else:
            print("请指定操作: --add, --search, --list")
    
    def cmd_web(self, args):
        """启动Web界面"""
        if not self._ensure_initialized():
            return
        
        web_file = self.aceflow_dir / "web" / "index.html"
        if not web_file.exists():
            print("❌ Web界面文件不存在")
            return
        
        port = args.port or 8080
        
        if args.serve:
            # 启动本地服务器
            try:
                import http.server
                import socketserver
                import threading
                
                class Handler(http.server.SimpleHTTPRequestHandler):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, directory=str(self.aceflow_dir / "web"), **kwargs)
                
                with socketserver.TCPServer(("", port), Handler) as httpd:
                    print(f"🌐 Web界面已启动: http://localhost:{port}")
                    if not args.no_browser:
                        webbrowser.open(f"http://localhost:{port}")
                    
                    try:
                        httpd.serve_forever()
                    except KeyboardInterrupt:
                        print("\\n👋 Web服务已停止")
                        
            except Exception as e:
                print(f"❌ 启动Web服务失败: {e}")
        else:
            # 直接在浏览器中打开文件
            webbrowser.open(f"file://{web_file.absolute()}")
            print(f"🌐 已在浏览器中打开Web界面")
    
    def cmd_config(self, args):
        """配置管理"""
        if not self._ensure_initialized():
            return
        
        if args.list:
            # 显示配置
            with open(self.aceflow_dir / "config.yaml", 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(yaml.dump(config, default_flow_style=False, allow_unicode=True))
        elif args.set:
            # 设置配置
            key, value = args.set.split('=', 1)
            self._set_config(key, value)
        elif args.get:
            # 获取配置
            value = self._get_config(args.get)
            print(f"{args.get} = {value}")
        else:
            # 交互式配置
            self._interactive_config()
    
    def cmd_help(self, args):
        """显示帮助"""
        help_text = """
🚀 AceFlow CLI v2.0 - AI驱动的敏捷开发工作流

基础命令:
  init           初始化项目
  status         显示项目状态
  next           获取下一步建议
  
流程管理:
  start          开始阶段
  complete       完成阶段
  progress       更新进度
  mode           切换流程模式
  
内容管理:
  deliverable    管理交付物
  memory         记忆管理
  
工具:
  web            启动Web界面
  config         配置管理
  help           显示帮助
  
使用 'aceflow <command> --help' 查看详细帮助
        """
        print(help_text)
    
    def _get_status_icon(self, status: str) -> str:
        """获取状态图标"""
        icons = {
            'completed': '✅',
            'in_progress': '🔄',
            'pending': '⏳',
            'blocked': '🚫',
            'skipped': '⏭️'
        }
        return icons.get(status, '❓')
    
    def _show_detailed_status(self):
        """显示详细状态"""
        current_stage_id = self.engine.state.get('current_stage')
        if not current_stage_id:
            return
        
        stage_info = self.engine._get_stage_info_by_id(current_stage_id)
        stage_state = self.engine.get_stage_state(current_stage_id)
        
        if not stage_info:
            return
        
        print("\\n📋 当前阶段详情:")
        print(f"  阶段ID: {stage_info.id}")
        print(f"  阶段名称: {stage_info.display_name}")
        print(f"  描述: {stage_info.description}")
        print(f"  预计时间: {stage_info.duration_estimate}")
        print(f"  负责人: {stage_state.assignee or '未指定'}")
        
        if stage_state.start_time:
            print(f"  开始时间: {stage_state.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if stage_info.deliverables:
            print("\\n📦 交付物状态:")
            for deliverable in stage_info.deliverables:
                completed = stage_state.deliverables_status.get(deliverable, False)
                icon = "✅" if completed else "⏳"
                print(f"    {icon} {deliverable}")
        
        if stage_state.notes:
            print("\\n📝 备注:")
            for note in stage_state.notes:
                print(f"    - {note}")
    
    def _interactive_progress_update(self, stage_id: str):
        """交互式进度更新"""
        stage_state = self.engine.get_stage_state(stage_id)
        current_progress = stage_state.progress
        
        print(f"当前进度: {current_progress}%")
        new_progress = questionary.text(
            "新进度 (0-100):",
            default=str(current_progress),
            validate=lambda x: x.isdigit() and 0 <= int(x) <= 100
        ).ask()
        
        if new_progress:
            self.engine.update_stage_state(stage_id, progress=int(new_progress))
            print(f"✅ 进度已更新为 {new_progress}%")
    
    def _execute_action(self, action: Dict):
        """执行建议的操作"""
        action_type = action['type']
        
        if action_type == 'start_stage':
            current_stage = self.engine.state.get('current_stage')
            if current_stage:
                self.engine.start_stage(current_stage)
                print(f"✅ 已开始阶段: {current_stage}")
        
        elif action_type == 'complete_stage':
            current_stage = self.engine.state.get('current_stage')
            if current_stage:
                self.engine.complete_stage(current_stage)
                print(f"✅ 已完成阶段: {current_stage}")
        
        # 可以添加更多操作类型
    
    def _list_deliverables(self, stage_id: str):
        """列出交付物"""
        stage_info = self.engine._get_stage_info_by_id(stage_id)
        stage_state = self.engine.get_stage_state(stage_id)
        
        if not stage_info or not stage_info.deliverables:
            print(f"阶段 {stage_id} 没有交付物")
            return
        
        print(f"\\n📦 阶段 {stage_id} 的交付物:")
        for deliverable in stage_info.deliverables:
            completed = stage_state.deliverables_status.get(deliverable, False)
            icon = "✅" if completed else "⏳"
            print(f"  {icon} {deliverable}")
    
    def _interactive_deliverable_management(self, stage_id: str):
        """交互式交付物管理"""
        stage_info = self.engine._get_stage_info_by_id(stage_id)
        if not stage_info or not stage_info.deliverables:
            print(f"阶段 {stage_id} 没有交付物")
            return
        
        while True:
            self._list_deliverables(stage_id)
            
            action = questionary.select(
                "选择操作:",
                choices=[
                    "标记完成",
                    "标记未完成",
                    "退出"
                ]
            ).ask()
            
            if action == "退出":
                break
            
            deliverable = questionary.select(
                "选择交付物:",
                choices=stage_info.deliverables
            ).ask()
            
            if deliverable:
                completed = action == "标记完成"
                self.engine.update_deliverable_status(stage_id, deliverable, completed)
                status = "完成" if completed else "未完成"
                print(f"✅ 已标记 '{deliverable}' 为{status}")
    
    def _add_memory_interactive(self):
        """交互式添加记忆"""
        # 这里需要实现记忆添加逻辑
        # 目前先显示占位符
        print("🧠 记忆添加功能开发中...")
    
    def _search_memory(self, query: str):
        """搜索记忆"""
        print(f"🔍 搜索记忆: {query}")
        print("记忆搜索功能开发中...")
    
    def _list_memories(self, memory_type: str = None):
        """列出记忆"""
        type_filter = f" (类型: {memory_type})" if memory_type else ""
        print(f"📝 记忆列表{type_filter}")
        print("记忆列表功能开发中...")
    
    def _set_config(self, key: str, value: str):
        """设置配置"""
        print(f"设置配置: {key} = {value}")
        print("配置设置功能开发中...")
    
    def _get_config(self, key: str) -> str:
        """获取配置"""
        print("配置获取功能开发中...")
        return "配置值"
    
    def _interactive_config(self):
        """交互式配置"""
        print("⚙️ 交互式配置功能开发中...")


def main():
    """主函数"""
    cli = AceFlowCLI()
    
    parser = argparse.ArgumentParser(
        description="AceFlow CLI v2.0 - AI驱动的敏捷开发工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    parser_init = subparsers.add_parser('init', help='初始化项目')
    parser_init.add_argument('--mode', choices=['minimal', 'standard', 'complete'], 
                           help='流程模式')
    parser_init.add_argument('--non-interactive', action='store_true', 
                           help='非交互模式')
    parser_init.set_defaults(func=cli.cmd_init)
    
    # status 命令
    parser_status = subparsers.add_parser('status', help='显示项目状态')
    parser_status.add_argument('-v', '--verbose', action='store_true', 
                              help='显示详细信息')
    parser_status.set_defaults(func=cli.cmd_status)
    
    # next 命令
    parser_next = subparsers.add_parser('next', help='获取下一步建议')
    parser_next.add_argument('--auto', action='store_true', 
                           help='自动执行高优先级任务')
    parser_next.set_defaults(func=cli.cmd_next)
    
    # progress 命令
    parser_progress = subparsers.add_parser('progress', help='更新进度')
    parser_progress.add_argument('--stage', help='阶段ID')
    parser_progress.add_argument('--progress', type=int, metavar='N',
                               help='进度百分比 (0-100)')
    parser_progress.set_defaults(func=cli.cmd_progress)
    
    # start 命令
    parser_start = subparsers.add_parser('start', help='开始阶段')
    parser_start.add_argument('stage', nargs='?', help='阶段ID')
    parser_start.add_argument('--assignee', help='负责人')
    parser_start.set_defaults(func=cli.cmd_start)
    
    # complete 命令
    parser_complete = subparsers.add_parser('complete', help='完成阶段')
    parser_complete.add_argument('stage', nargs='?', help='阶段ID')
    parser_complete.add_argument('--notes', help='完成备注')
    parser_complete.add_argument('--no-notes', action='store_true',
                               help='不添加备注')
    parser_complete.set_defaults(func=cli.cmd_complete)
    
    # mode 命令
    parser_mode = subparsers.add_parser('mode', help='切换流程模式')
    parser_mode.add_argument('mode', nargs='?', 
                           choices=['minimal', 'standard', 'complete'],
                           help='目标模式')
    parser_mode.add_argument('--force', action='store_true',
                           help='强制切换，不询问确认')
    parser_mode.add_argument('--reset', action='store_true',
                           help='重置进度数据')
    parser_mode.set_defaults(func=cli.cmd_mode)
    
    # deliverable 命令
    parser_deliverable = subparsers.add_parser('deliverable', help='管理交付物')
    parser_deliverable.add_argument('--stage', help='阶段ID')
    parser_deliverable.add_argument('--list', action='store_true',
                                  help='列出交付物')
    parser_deliverable.add_argument('--deliverable', help='交付物名称')
    parser_deliverable.add_argument('--incomplete', action='store_true',
                                  help='标记为未完成')
    parser_deliverable.set_defaults(func=cli.cmd_deliverable)
    
    # memory 命令
    parser_memory = subparsers.add_parser('memory', help='记忆管理')
    parser_memory.add_argument('--add', action='store_true', help='添加记忆')
    parser_memory.add_argument('--search', help='搜索记忆')
    parser_memory.add_argument('--list', action='store_true', help='列出记忆')
    parser_memory.add_argument('--type', help='记忆类型')
    parser_memory.set_defaults(func=cli.cmd_memory)
    
    # web 命令
    parser_web = subparsers.add_parser('web', help='启动Web界面')
    parser_web.add_argument('--serve', action='store_true',
                          help='启动本地服务器')
    parser_web.add_argument('--port', type=int, default=8080,
                          help='服务器端口')
    parser_web.add_argument('--no-browser', action='store_true',
                          help='不自动打开浏览器')
    parser_web.set_defaults(func=cli.cmd_web)
    
    # config 命令
    parser_config = subparsers.add_parser('config', help='配置管理')
    parser_config.add_argument('--list', action='store_true',
                             help='显示配置')
    parser_config.add_argument('--set', help='设置配置 (key=value)')
    parser_config.add_argument('--get', help='获取配置')
    parser_config.set_defaults(func=cli.cmd_config)
    
    # help 命令
    parser_help = subparsers.add_parser('help', help='显示帮助')
    parser_help.set_defaults(func=cli.cmd_help)
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # 执行命令
        args.func(args)
    except KeyboardInterrupt:
        print("\\n\\n👋 操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ 执行失败: {e}")
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()