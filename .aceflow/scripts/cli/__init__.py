import argparse
# 替换相对导入为绝对导入
from core.workflow_navigator import WorkflowNavigator
from core.state_engine import PATEOASStateEngine
from core.memory_pool import GlobalMemoryPool

def main():
    parser = argparse.ArgumentParser(description='AceFlow-PATEOAS 工作流引擎')
    subparsers = parser.add_subparsers(dest='command')
    
    # 初始化命令
    init_parser = subparsers.add_parser('init', help='初始化项目')
    init_parser.set_defaults(func=init_project)
    
    # 更新状态命令
    status_parser = subparsers.add_parser('update-status', help='更新阶段状态')
    status_parser.add_argument('stage_id', help='阶段ID (如S1)')
    status_parser.add_argument('progress', type=int, help='进度百分比')
    status_parser.set_defaults(func=update_status)
    
    # 获取导航建议命令
    suggest_parser = subparsers.add_parser('get-suggestions', help='获取导航建议')
    suggest_parser.set_defaults(func=get_suggestions)
    
    # 记录异常命令
    abn_parser = subparsers.add_parser('record-abnormality', help='记录异常状态')
    abn_parser.add_argument('stage_id', help='阶段ID')
    abn_parser.add_argument('description', help='异常描述')
    abn_parser.add_argument('--severity', default='medium', help='严重程度 (high/medium/low)')
    abn_parser.set_defaults(func=record_abnormality)
    
    # 解决异常命令
    resolve_parser = subparsers.add_parser('resolve-abnormality', help='解决异常状态')
    resolve_parser.add_argument('abnormality_id', help='异常ID')
    resolve_parser.set_defaults(func=resolve_abnormality)
    
    # 确定流程分支命令
    workflow_parser = subparsers.add_parser('determine-workflow', help='确定流程分支')
    workflow_parser.add_argument('task_description', help='任务描述')
    workflow_parser.set_defaults(func=determine_workflow)
    
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

def init_project(args):
    """初始化项目结构"""
    state_engine = PATEOASStateEngine()
    memory_pool = GlobalMemoryPool()
    print("项目初始化完成，状态文件和记忆池已创建")

def update_status(args):
    """更新阶段状态"""
    state_engine = PATEOASStateEngine()
    state_engine.update_stage_progress(args.stage_id, args.progress)
    print(f"已更新 {args.stage_id} 进度至 {args.progress}%")

def get_suggestions(args):
    """获取导航建议"""
    state_engine = PATEOASStateEngine()
    suggestions = state_engine.get_navigation_suggestion()
    
    if suggestions:
        print("导航建议:")
        for s in suggestions:
            print(f"- [{s['priority']}] {s['message']}")
    else:
        print("当前无特殊导航建议，按计划进行下一阶段")

def record_abnormality(args):
    """记录异常状态"""
    state_engine = PATEOASStateEngine()
    abn = state_engine.record_abnormality(args.stage_id, args.description, args.severity)
    print(f"已记录异常: {abn['id']}")
    print(f"描述: {abn['description']}")

def resolve_abnormality(args):
    """解决异常状态"""
    state_engine = PATEOASStateEngine()
    success = state_engine.resolve_abnormality(args.abnormality_id)
    if success:
        print(f"异常 {args.abnormality_id} 已标记为已解决")
    else:
        print(f"未找到异常 {args.abnormality_id} 或已解决")

def determine_workflow(args):
    """确定流程分支"""
    navigator = WorkflowNavigator()
    workflow_type = navigator.determine_workflow(args.task_description)
    workflow_path = navigator.get_workflow_path(workflow_type)
    
    print(f"推荐流程分支: {workflow_type}")
    print(f"阶段路径: {' → '.join(workflow_path)}")
    
    # 更新状态中的流程类型
    state_engine = PATEOASStateEngine()
    state = state_engine.get_current_state()
    state['workflow_type'] = workflow_type
    state_engine.save_state(state)