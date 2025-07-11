#!/usr/bin/env python3
# .aceflow/scripts/analyze.py
"""
AceFlow 执行分析器
生成迭代分析报告。
"""

import json
from datetime import datetime
from pathlib import Path
import argparse
import re

class IterationAnalyzer:
    """分析指定迭代的所有产出物"""
    def __init__(self, iteration_id: str):
        self.iteration_id = iteration_id
        self.base_path = Path("aceflow_result") / iteration_id
        self.state_file = Path(".aceflow/state.json")
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """加载状态文件"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        return {}

    def analyze_completeness(self) -> dict:
        """分析各阶段完成情况"""
        stage_dirs = [d.name for d in self.base_path.iterdir() if d.is_dir()]
        return {
            "completed_stages": self.state.get("completed_stages", []),
            "total_stages": len(stage_dirs),
            "completion_rate": len(self.state.get("completed_stages", [])) / len(stage_dirs) * 100 if stage_dirs else 0
        }

    def analyze_test_results(self) -> dict:
        """分析S5测试报告"""
        test_dir = self.base_path / "S5_test_report"
        stats = {"total_files": 0, "pass_rate_avg": 0, "coverage_avg": 0, "failed_count": 0}
        rates, coverages = [], []

        if not test_dir.exists(): return stats
        
        files = list(test_dir.glob("s5_test_*.md"))
        stats["total_files"] = len(files)
        
        for file in files:
            content = file.read_text(encoding='utf-8')
            pass_rate_match = re.search(r"通过率:\s*([\d\.]+)%", content)
            coverage_match = re.search(r"覆盖率:\s*([\d\.]+)%", content)
            stats["failed_count"] += content.count("❌")
            if pass_rate_match: rates.append(float(pass_rate_match.group(1)))
            if coverage_match: coverages.append(float(coverage_match.group(1)))

        if rates: stats["pass_rate_avg"] = sum(rates) / len(rates)
        if coverages: stats["coverage_avg"] = sum(coverages) / len(coverages)
        return stats

    def analyze_code_review(self) -> dict:
        """分析S6代码评审报告"""
        review_file = self.base_path / "S6_codereview" / "s6_codereview.md"
        stats = {"critical": 0, "major": 0, "minor": 0}
        if not review_file.exists(): return stats
        
        content = review_file.read_text(encoding='utf-8')
        stats["critical"] = content.count("🔴")
        stats["major"] = content.count("🟡")
        stats["minor"] = content.count("🔵")
        return stats

    def generate_report(self) -> str:
        """生成Markdown格式的分析报告"""
        completeness = self.analyze_completeness()
        test_stats = self.analyze_test_results()
        review_stats = self.analyze_code_review()
        metrics = self.state.get("metrics", {})

        report = f"""
# AceFlow 迭代分析报告: {self.iteration_id}
**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 整体进度
- **完成度**: {completeness['completion_rate']:.1f}% ({len(completeness['completed_stages'])}/{completeness['total_stages']} 阶段)
- **已完成阶段**: {', '.join(completeness['completed_stages'])}
- **总任务数**: {metrics.get('total_tasks', 'N/A')}
- **已完成任务**: {metrics.get('completed_tasks', 'N/A')}

## 2. 质量分析
### 测试概览
- **平均通过率**: {test_stats['pass_rate_avg']:.1f}%
- **平均覆盖率**: {test_stats['coverage_avg']:.1f}%
- **总失败用例数**: {test_stats['failed_count']}

### 代码评审问题
- **🔴 严重问题**: {review_stats['critical']}
- **🟡 一般问题**: {review_stats['major']}
- **🔵 优化建议**: {review_stats['minor']}

## 3. 智能建议
"""
        suggestions = []
        if completeness['completion_rate'] < 100: suggestions.append("- ⚠️ 流程未完成，请检查卡点阶段。")
        if test_stats['pass_rate_avg'] < 90: suggestions.append("- 📉 测试通过率偏低，建议加强单元测试和代码审查。")
        if review_stats['critical'] > 0: suggestions.append("- 🚨 存在严重代码问题，需要优先修复。")
        if not suggestions: suggestions.append("- ✅ 整体表现良好，可总结经验并归档。")
        
        report += "\n".join(suggestions)
        return report.strip()

    def save_report(self, report: str):
        """保存报告到S8目录"""
        report_path = self.base_path / "S8_summary" / "analysis_report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding='utf-8')
        print(f"✅ 分析报告已保存至: {report_path}")

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='AceFlow 迭代分析器')
    parser.add_argument('--iteration', '-i', required=True, help='要分析的迭代ID')
    parser.add_argument('--save', '-s', action='store_true', help='保存报告到文件')
    
    args = parser.parse_args()
    
    analyzer = IterationAnalyzer(args.iteration)
    report = analyzer.generate_report()
    
    print(report)
    
    if args.save:
        analyzer.save_report(report)

if __name__ == "__main__":
    main()