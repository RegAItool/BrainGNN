#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并详细版本论文
Compile Complete Detailed Paper
"""

import os

def compile_detailed_paper():
    """合并详细版本的论文文件"""
    
    print("📄 合并详细版本BrainGNN论文...")
    
    # 读取主要部分
    main_part = ""
    continuation_part = ""
    
    # 读取主文件 (到Results结束)
    with open('./paper/braingnn_detailed_version.tex', 'r', encoding='utf-8') as f:
        main_content = f.read()
        # 找到Results部分结束的位置
        main_part = main_content
    
    # 读取续部分 (Discussion及后续)
    with open('./paper/detailed_continuation.tex', 'r', encoding='utf-8') as f:
        continuation_content = f.read()
        # 移除文件头的注释部分
        lines = continuation_content.split('\n')
        start_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('\\section{Discussion}'):
                start_idx = i
                break
        continuation_part = '\n'.join(lines[start_idx:])
    
    # 合并完整论文
    # 找到主文件中需要插入续部分的位置
    main_lines = main_part.split('\n')
    
    # 找到插入点 (在## [Continue reading next part...]之前)
    insert_idx = len(main_lines)
    for i, line in enumerate(main_lines):
        if '## [Continue reading next part...]' in line:
            insert_idx = i
            break
    
    # 合并文件
    complete_paper = '\n'.join(main_lines[:insert_idx]) + '\n\n' + continuation_part
    
    # 保存完整版本
    output_file = './paper/braingnn_complete_detailed.tex'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(complete_paper)
    
    # 计算文件统计
    file_size = os.path.getsize(output_file) / 1024
    line_count = len(complete_paper.split('\n'))
    word_count = len(complete_paper.split())
    
    print(f"✅ 详细版本论文编译完成!")
    print(f"📁 输出文件: {output_file}")
    print(f"📊 文件大小: {file_size:.1f} KB")
    print(f"📝 行数: {line_count:,}")
    print(f"🔤 单词数: {word_count:,}")
    
    return output_file

def create_paper_statistics():
    """创建论文统计信息"""
    
    print("\n📊 创建论文版本对比...")
    
    papers = {
        'Standard Version': './paper/braingnn_pain_classification_with_citations.tex',
        'Detailed Version': './paper/braingnn_complete_detailed.tex'
    }
    
    stats = {}
    
    for name, filepath in papers.items():
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stats[name] = {
                'file_size_kb': os.path.getsize(filepath) / 1024,
                'lines': len(content.split('\n')),
                'words': len(content.split()),
                'sections': content.count('\\section{'),
                'subsections': content.count('\\subsection{'),
                'subsubsections': content.count('\\subsubsection{'),
                'equations': content.count('\\begin{equation}') + content.count('\\begin{align}'),
                'figures': content.count('\\includegraphics'),
                'tables': content.count('\\begin{table}'),
                'citations': content.count('\\cite{')
            }
    
    # 创建统计报告
    stats_content = """# 📊 BrainGNN论文版本统计对比

## 📁 文件版本信息

### 🎯 标准版本 (braingnn_pain_classification_with_citations.tex)
- **目标**: 期刊投稿标准版本
- **特点**: 符合IEEE格式要求，内容精炼
- **使用场景**: 直接投稿到期刊

### 📚 详细版本 (braingnn_complete_detailed.tex)
- **目标**: 完整技术细节版本
- **特点**: 包含所有实验细节、方法说明、深度分析
- **使用场景**: 技术审查、博士论文章节、完整归档

## 📈 内容统计对比

| 指标 | 标准版本 | 详细版本 | 增加量 |
|------|----------|----------|--------|"""
    
    if 'Standard Version' in stats and 'Detailed Version' in stats:
        std_stats = stats['Standard Version']
        det_stats = stats['Detailed Version']
        
        comparisons = [
            ('文件大小 (KB)', std_stats['file_size_kb'], det_stats['file_size_kb']),
            ('总行数', std_stats['lines'], det_stats['lines']),
            ('单词数', std_stats['words'], det_stats['words']),
            ('章节数', std_stats['sections'], det_stats['sections']),
            ('小节数', std_stats['subsections'], det_stats['subsections']),
            ('子小节数', std_stats['subsubsections'], det_stats['subsubsections']),
            ('公式数', std_stats['equations'], det_stats['equations']),
            ('图表数', std_stats['figures'], det_stats['figures']),
            ('表格数', std_stats['tables'], det_stats['tables']),
            ('引用数', std_stats['citations'], det_stats['citations'])
        ]
        
        for metric, std_val, det_val in comparisons:
            increase = det_val - std_val
            increase_pct = (increase / std_val * 100) if std_val > 0 else 0
            stats_content += f"\n| {metric} | {std_val:.1f} | {det_val:.1f} | +{increase:.1f} (+{increase_pct:.1f}%) |"
    
    stats_content += """

## 🎯 版本选择建议

### 📄 使用标准版本的情况:
- **期刊投稿**: 直接提交给IEEE Trans. Biomedical Engineering等期刊
- **会议论文**: 提交到MICCAI、IPMI等会议
- **快速审查**: 需要快速了解核心贡献
- **页面限制**: 有严格页面数量限制的场合

### 📚 使用详细版本的情况:
- **技术审查**: 深度技术细节审查
- **方法复现**: 完整复现实验流程
- **博士论文**: 作为论文章节的技术基础
- **内部文档**: 完整的技术归档和知识传递
- **专利申请**: 详细的技术说明支撑

## 🔧 详细版本的增强内容

### 🧠 神经科学深度分析:
- 脑区功能的详细解释
- 神经网络系统的完整描述
- 连接模式的深入分析
- 与已知疼痛理论的对比

### ⚙️ 技术实现细节:
- 完整的数学公式推导
- 详细的算法伪代码
- 超参数选择的理由
- 消融实验的完整结果

### 📊 实验分析扩展:
- 详细的统计分析
- 子群体分析结果
- 跨数据集验证
- 误差分析和敏感性测试

### 🏥 临床应用展望:
- 详细的临床转化路径
- 监管审批考虑
- 成本效益分析
- 实施挑战和解决方案

## 🎉 总结

两个版本互为补充，满足不同需求：
- **标准版本**: 精炼高效，适合发表和快速传播
- **详细版本**: 完整全面，适合深度研究和技术传承

建议根据具体使用场景选择合适的版本！

---
🧠 **BrainGNN: 从创新算法到临床应用的完整技术体系**
"""
    
    stats_file = './paper/PAPER_STATISTICS.md'
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(stats_content)
    
    print(f"✅ 统计报告创建: {stats_file}")
    
    return stats

def main():
    """主函数"""
    print("=" * 60)
    print("📄 BrainGNN详细版本论文编译")
    print("=" * 60)
    
    # 编译详细版本论文
    output_file = compile_detailed_paper()
    
    # 创建统计信息
    stats = create_paper_statistics()
    
    print("\n" + "=" * 60)
    print("✅ 详细版本论文编译完成!")
    print("\n📁 现在您有两个完整版本:")
    print("  📄 标准版本: braingnn_pain_classification_with_citations.tex")
    print("  📚 详细版本: braingnn_complete_detailed.tex")
    print("\n🎯 使用建议:")
    print("  • 期刊投稿 → 使用标准版本")
    print("  • 技术审查 → 使用详细版本")
    print("  • 方法复现 → 使用详细版本")
    print("  • 博士论文 → 使用详细版本")
    print("\n📊 详细对比: PAPER_STATISTICS.md")
    print("=" * 60)

if __name__ == "__main__":
    main()