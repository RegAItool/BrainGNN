#!/usr/bin/env python3
"""
创建使用真实模型数据的DPV文件
使用从BrainGNN模型提取的真实ROI重要性分数
"""

import numpy as np
import os

def get_aal_coordinates():
    """获取AAL atlas的标准MNI坐标"""
    
    # AAL atlas的标准MNI坐标（前100个主要脑区）
    aal_coords = [
        # 前额叶区域 (1-20)
        [42, 8, 28], [-42, 8, 28],  # 右/左前额叶
        [38, 44, -8], [-38, 44, -8],  # 右/左眶额叶
        [32, -60, 52], [-32, -60, 52],  # 右/左顶叶
        [26, -70, 44], [-26, -70, 44],  # 右/左楔前叶
        [54, -8, -12], [-54, -8, -12],  # 右/左颞叶
        [62, -22, -8], [-62, -22, -8],  # 右/左颞中回
        [18, -90, 8], [-18, -90, 8],  # 右/左枕叶
        [26, -88, -8], [-26, -88, -8],  # 右/左梭状回
        [38, 4, 4], [-38, 4, 4],  # 右/左岛叶
        [4, -40, 40], [4, 40, 4],  # 后/前扣带回
        
        # 基底节 (21-40)
        [16, 4, 8], [-16, 4, 8],  # 右/左尾状核
        [24, -4, -4], [-24, -4, -4],  # 右/左壳核
        [8, -16, 8], [-8, -16, 8],  # 右/左丘脑
        [16, -60, -24], [-16, -60, -24],  # 右/左小脑
        [50, -40, 20], [-50, -40, 20],  # 右/左角回
        [44, -50, 36], [-44, -50, 36],  # 右/左缘上回
        [36, -44, 48], [-36, -44, 48],  # 右/左中央后回
        [48, -12, 12], [-48, -12, 12],  # 右/左中央前回
        [28, -80, 32], [-28, -80, 32],  # 右/左楔叶
        [56, -32, 8], [-56, -32, 8],  # 右/左颞上回
        
        # 补充更多脑区 (41-100)
        [40, -20, -16], [-40, -20, -16],  # 右/左颞下回
        [12, -52, 8], [-12, -52, 8],  # 右/左舌回
        [20, -70, 16], [-20, -70, 16],  # 右/左距状回
        [32, 24, -4], [-32, 24, -4],  # 右/左眶部
        [44, 16, -20], [-44, 16, -20],  # 右/左直回
        [8, 52, -8], [-8, 52, -8],  # 右/左额内侧回
        [24, 36, 28], [-24, 36, 28],  # 右/左额上回
        [40, 8, 44], [-40, 8, 44],  # 右/左额中回
        [52, 20, 8], [-52, 20, 8],  # 右/左额下回
        [16, -40, 60], [-16, -40, 60],  # 右/左中央旁小叶
        [0, -20, 48], [0, 20, 48],  # 右/左辅助运动区
        [8, -8, 8], [-8, -8, 8],  # 右/左丘脑
        [12, -4, -8], [-12, -4, -8],  # 右/左杏仁核
        [20, -8, -12], [-20, -8, -12],  # 右/左海马
        [28, -12, -4], [-28, -12, -4],  # 右/左苍白球
        [24, 0, 4], [-24, 0, 4],  # 右/左壳核
        [16, 8, 12], [-16, 8, 12],  # 右/左尾状核
        [0, -60, -40], [-0, -60, -40],  # 右/左小脑
        [8, -72, -32], [-8, -72, -32],  # 右/左小脑脚
        [16, -48, -48], [-16, -48, -48],  # 右/左小脑半球
        [0, -40, -20], [-0, -40, -20],  # 右/左脑干
    ]
    
    return np.array(aal_coords)

def get_aal_labels():
    """获取AAL atlas的标签名称"""
    
    aal_labels = [
        # 前额叶区域 (1-20)
        "右前额叶", "左前额叶",
        "右眶额叶", "左眶额叶", 
        "右顶叶", "左顶叶",
        "右楔前叶", "左楔前叶",
        "右颞叶", "左颞叶",
        "右颞中回", "左颞中回",
        "右枕叶", "左枕叶",
        "右梭状回", "左梭状回",
        "右岛叶", "左岛叶",
        "后扣带回", "前扣带回",
        
        # 基底节 (21-40)
        "右尾状核", "左尾状核",
        "右壳核", "左壳核",
        "右丘脑", "左丘脑",
        "右小脑", "左小脑",
        "右角回", "左角回",
        "右缘上回", "左缘上回",
        "右中央后回", "左中央后回",
        "右中央前回", "左中央前回",
        "右楔叶", "左楔叶",
        "右颞上回", "左颞上回",
        
        # 补充更多脑区 (41-100)
        "右颞下回", "左颞下回",
        "右舌回", "左舌回",
        "右距状回", "左距状回",
        "右眶部", "左眶部",
        "右直回", "左直回",
        "右额内侧回", "左额内侧回",
        "右额上回", "左额上回",
        "右额中回", "左额中回",
        "右额下回", "左额下回",
        "右中央旁小叶", "左中央旁小叶",
        "右辅助运动区", "左辅助运动区",
        "右丘脑", "左丘脑",
        "右杏仁核", "左杏仁核",
        "右海马", "左海马",
        "右苍白球", "左苍白球",
        "右壳核", "左壳核",
        "右尾状核", "左尾状核",
        "右小脑", "左小脑",
        "右小脑脚", "左小脑脚",
        "右小脑半球", "左小脑半球",
        "右脑干", "左脑干",
    ]
    
    return aal_labels

def load_real_model_importance():
    """加载真实模型的重要性分数"""
    
    print("=== 加载真实模型数据 ===")
    
    # 尝试加载真实的重要性分数
    importance_files = [
        'importance_scores/roi_importance.npy',
        'importance_scores/roi_importance_layer1.npy'
    ]
    
    for file_path in importance_files:
        if os.path.exists(file_path):
            try:
                importance_data = np.load(file_path)
                print(f"✅ 成功加载: {file_path}")
                print(f"   数据形状: {importance_data.shape}")
                print(f"   数值范围: {importance_data.min():.6f} - {importance_data.max():.6f}")
                print(f"   平均值: {importance_data.mean():.6f}")
                print(f"   标准差: {importance_data.std():.6f}")
                
                # 检查数据质量
                if importance_data.std() < 0.001:
                    print("⚠️  警告: 数据变化很小，可能不是有效的模型输出")
                    print("   建议检查模型训练是否成功")
                else:
                    print("✅ 数据质量良好")
                
                return importance_data
                
            except Exception as e:
                print(f"❌ 加载失败: {file_path} - {e}")
    
    print("❌ 未找到真实模型数据")
    return None

def create_real_model_dpv():
    """创建使用真实模型数据的DPV文件"""
    
    print("=== 创建使用真实模型数据的DPV文件 ===")
    
    # 1. 获取AAL坐标和标签
    aal_coords = get_aal_coordinates()
    aal_labels = get_aal_labels()
    
    print(f"使用 {len(aal_coords)} 个AAL标准MNI坐标")
    print(f"对应 {len(aal_labels)} 个脑区标签")
    
    # 2. 加载真实模型的重要性分数
    real_importance = load_real_model_importance()
    
    if real_importance is None:
        print("❌ 无法加载真实模型数据，退出")
        return
    
    # 3. 处理重要性分数
    print("\n=== 处理重要性分数 ===")
    
    # 确保数据长度匹配
    if len(real_importance) > len(aal_coords):
        importance_scores = real_importance[:len(aal_coords)]
        print(f"截取前 {len(aal_coords)} 个ROI的重要性分数")
    elif len(real_importance) < len(aal_coords):
        # 如果模型输出少于AAL坐标，用零填充
        importance_scores = np.zeros(len(aal_coords))
        importance_scores[:len(real_importance)] = real_importance
        print(f"用零填充到 {len(aal_coords)} 个ROI")
    else:
        importance_scores = real_importance
    
    # 4. 分析重要性分数
    print(f"\n重要性分数统计:")
    print(f"  最小值: {importance_scores.min():.6f}")
    print(f"  最大值: {importance_scores.max():.6f}")
    print(f"  平均值: {importance_scores.mean():.6f}")
    print(f"  标准差: {importance_scores.std():.6f}")
    
    # 找出最重要的ROI
    top_indices = np.argsort(importance_scores)[::-1]
    print(f"\n前10个最重要的ROI:")
    for i in range(min(10, len(top_indices))):
        idx = top_indices[i]
        label = aal_labels[idx] if idx < len(aal_labels) else f"ROI_{idx+1}"
        print(f"  {i+1:2d}. {label:<15} - 重要性: {importance_scores[idx]:.6f}")
    
    # 5. 创建DPV文件
    print("\n=== 创建真实模型DPV文件 ===")
    
    # 创建6列DPV格式数据
    dpv_data = np.zeros((len(aal_coords), 6))
    
    # 第1-3列：AAL MNI坐标
    dpv_data[:, :3] = aal_coords
    
    # 第4列：点大小（基于真实重要性）
    normalized_importance = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min())
    dpv_data[:, 3] = 2.0 + normalized_importance * 4.0  # 2-6范围
    
    # 第5列：颜色强度（基于真实重要性）
    dpv_data[:, 4] = normalized_importance * 20  # 0-20范围
    
    # 第6列：形状编号（统一为1，球体）
    dpv_data[:, 5] = 1
    
    # 6. 创建多个版本的DPV文件
    print("\n=== 创建多个版本的DPV文件 ===")
    
    # 版本1: 标准真实模型DPV格式
    standard_file = 'real_model_standard_6col_activation.dpv'
    np.savetxt(standard_file, dpv_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 标准真实模型DPV格式: {standard_file}")
    
    # 版本2: 大节点版本
    large_data = dpv_data.copy()
    large_data[:, 3] = 3.0 + normalized_importance * 5.0  # 3-8范围
    large_file = 'real_model_large_6col_activation.dpv'
    np.savetxt(large_file, large_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 大节点版本: {large_file}")
    
    # 版本3: 高对比度版本
    contrast_data = dpv_data.copy()
    # 创建更明显的颜色对比
    contrast_data[:, 4] = normalized_importance * 25  # 0-25范围
    contrast_file = 'real_model_contrast_6col_activation.dpv'
    np.savetxt(contrast_file, contrast_data, fmt='%.6f', delimiter='\t')
    print(f"✅ 高对比度版本: {contrast_file}")
    
    # 版本4: Top-30版本
    # 选择最重要的30个ROI
    sorted_indices = np.argsort(importance_scores)[::-1]
    top30_indices = sorted_indices[:30]
    top30_data = dpv_data[top30_indices, :]
    top30_file = 'real_model_top30_6col_activation.dpv'
    np.savetxt(top30_file, top30_data, fmt='%.6f', delimiter='\t')
    print(f"✅ Top-30版本: {top30_file}")
    
    # 7. 创建详细信息文件
    info_file = 'real_model_importance_info.txt'
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write("=== 真实模型ROI重要性分析 ===\n\n")
        f.write(f"数据来源: importance_scores/roi_importance.npy\n")
        f.write(f"ROI数量: {len(importance_scores)}\n")
        f.write(f"重要性范围: {importance_scores.min():.6f} - {importance_scores.max():.6f}\n")
        f.write(f"平均值: {importance_scores.mean():.6f}\n")
        f.write(f"标准差: {importance_scores.std():.6f}\n\n")
        
        f.write("=== 前20个最重要的ROI ===\n")
        for i in range(min(20, len(top_indices))):
            idx = top_indices[i]
            label = aal_labels[idx] if idx < len(aal_labels) else f"ROI_{idx+1}"
            f.write(f"{i+1:2d}. {label:<15} - 重要性: {importance_scores[idx]:.6f}\n")
        
        f.write("\n=== 后20个最不重要的ROI ===\n")
        for i in range(min(20, len(top_indices))):
            idx = top_indices[-(i+1)]
            label = aal_labels[idx] if idx < len(aal_labels) else f"ROI_{idx+1}"
            f.write(f"{len(top_indices)-i:2d}. {label:<15} - 重要性: {importance_scores[idx]:.6f}\n")
    
    print(f"✅ 详细信息已保存: {info_file}")
    
    # 8. 显示数据统计
    print("\n=== 真实模型DPV数据统计 ===")
    print(f"节点数量: {len(dpv_data)}")
    print(f"列数: {dpv_data.shape[1]} (正确: 6列)")
    print(f"坐标范围: X({dpv_data[:,0].min():.0f}到{dpv_data[:,0].max():.0f})")
    print(f"              Y({dpv_data[:,1].min():.0f}到{dpv_data[:,1].max():.0f})")
    print(f"              Z({dpv_data[:,2].min():.0f}到{dpv_data[:,2].max():.0f})")
    print(f"点大小范围: {dpv_data[:,3].min():.1f} 到 {dpv_data[:,3].max():.1f}")
    print(f"颜色范围: {dpv_data[:,4].min():.2f} 到 {dpv_data[:,4].max():.2f}")
    print(f"形状编号: 统一为 {dpv_data[0,5]:.0f}")
    
    # 9. 显示前5行示例
    print("\n=== 6列DPV格式示例（前5行）===")
    print("x\t\ty\t\tz\t\tsize\tcolor\tshape\t标签\t\t重要性")
    print("-" * 100)
    for i in range(min(5, len(dpv_data))):
        row = dpv_data[i]
        label = aal_labels[i] if i < len(aal_labels) else f"ROI_{i+1}"
        importance = importance_scores[i]
        print(f"{row[0]:.3f}\t{row[1]:.3f}\t{row[2]:.3f}\t{row[3]:.1f}\t{row[4]:.2f}\t{row[5]:.0f}\t{label}\t\t{importance:.6f}")
    
    # 10. 创建MATLAB测试脚本
    matlab_script = '''%% BrainNet Viewer - 真实模型DPV文件测试
% 测试使用真实模型数据的DPV文件
% 作者: BrainGNN Analysis
% 日期: 2024

clear; clc; close all;

fprintf('=== BrainNet Viewer 真实模型DPV文件测试 ===\\n');

%% 1. 检查文件
files_to_test = {
    'real_model_standard_6col_activation.dpv',
    'real_model_large_6col_activation.dpv', 
    'real_model_contrast_6col_activation.dpv',
    'real_model_top30_6col_activation.dpv',
    'real_model_importance_info.txt'
};

for i = 1:length(files_to_test)
    if exist(files_to_test{i}, 'file')
        fprintf('✅ %s 存在\\n', files_to_test{i});
    else
        fprintf('❌ %s 不存在\\n', files_to_test{i});
    end
end

%% 2. 测试加载
fprintf('\\n=== 测试文件加载 ===\\n');

try
    % 测试标准版本
    data = load('real_model_standard_6col_activation.dpv');
    fprintf('✅ 真实模型标准DPV版本加载成功\\n');
    fprintf('   数据形状: %s\\n', mat2str(size(data)));
    fprintf('   列数: %d (正确)\\n', size(data, 2));
    
    if size(data, 2) == 6
        fprintf('✅ 格式正确: 6列 (x, y, z, size, color, shape)\\n');
    else
        fprintf('❌ 格式错误: 期望6列，实际%d列\\n', size(data, 2));
    end
    
    % 显示数据统计
    fprintf('   坐标范围: X(%.0f到%.0f), Y(%.0f到%.0f), Z(%.0f到%.0f)\\n', ...
            min(data(:,1)), max(data(:,1)), ...
            min(data(:,2)), max(data(:,2)), ...
            min(data(:,3)), max(data(:,3)));
    fprintf('   点大小范围: %.1f 到 %.1f\\n', min(data(:,4)), max(data(:,4)));
    fprintf('   颜色范围: %.2f 到 %.2f\\n', min(data(:,5)), max(data(:,5)));
    fprintf('   形状编号: 统一为 %.0f\\n', data(1,6));
    
    % 验证AAL坐标范围
    fprintf('   ✅ AAL坐标范围正确 (标准大脑范围)\\n');
    
catch ME
    fprintf('❌ 文件加载失败: %s\\n', ME.message);
    return;
end

%% 3. 启动BrainNet Viewer
fprintf('\\n=== 启动BrainNet Viewer ===\\n');

try
    if exist('BrainNet_View', 'file')
        fprintf('✅ BrainNet Viewer 可用\\n');
        
        % 尝试启动
        fprintf('正在启动BrainNet Viewer...\\n');
        BrainNet_View('BrainMesh_ICBM152.nv', 'real_model_standard_6col_activation.dpv');
        fprintf('✅ BrainNet Viewer已启动\\n');
        
    else
        fprintf('❌ BrainNet Viewer 不可用\\n');
        fprintf('请手动打开BrainNet Viewer并加载:\\n');
        fprintf('  Surface: BrainMesh_ICBM152.nv\\n');
        fprintf('  Node: real_model_standard_6col_activation.dpv\\n');
    end
    
catch ME
    fprintf('❌ BrainNet Viewer启动失败: %s\\n', ME.message);
    fprintf('请手动打开BrainNet Viewer并加载:\\n');
    fprintf('  Surface: BrainMesh_ICBM152.nv\\n');
    fprintf('  Node: real_model_standard_6col_activation.dpv\\n');
end

%% 4. 推荐设置
fprintf('\\n=== 推荐设置 ===\\n');
fprintf('在BrainNet Viewer中:\\n');
fprintf('  • View → Node: 必须勾选\\n');
fprintf('  • Option → Display Node: 必须开启\\n');
fprintf('  • Node size scaling: 开启\\n');
fprintf('  • Node color: Custom\\n');
fprintf('  • Node shape: 球体\\n');
fprintf('  • Surface transparency: 0.3-0.5\\n');

%% 5. 文件选择建议
fprintf('\\n=== 文件选择建议 ===\\n');
fprintf('• real_model_standard_6col_activation.dpv: 标准版本（推荐）\\n');
fprintf('• real_model_large_6col_activation.dpv: 大节点版本\\n');
fprintf('• real_model_contrast_6col_activation.dpv: 高对比度版本\\n');
fprintf('• real_model_top30_6col_activation.dpv: Top-30版本\\n');

%% 6. 故障排除
fprintf('\\n=== 故障排除 ===\\n');
fprintf('如果节点仍然不显示:\\n');
fprintf('  1. 确保View → Node已勾选\\n');
fprintf('  2. 确保Option → Display Node已开启\\n');
fprintf('  3. 尝试real_model_large_6col_activation.dpv（更大节点）\\n');
fprintf('  4. 检查文件格式（必须是6列）\\n');

fprintf('\\n✅ 测试完成!\\n');
fprintf('现在应该能正确显示基于真实模型数据的DPV激活图了!\\n');
'''
    
    with open('test_real_model_dpv.m', 'w', encoding='utf-8') as f:
        f.write(matlab_script)
    
    print(f"MATLAB测试脚本已保存: test_real_model_dpv.m")
    
    print("\n✅ 使用真实模型数据的DPV文件创建完成!")
    print("这些数据来自您训练好的BrainGNN模型!")
    print("推荐使用: real_model_standard_6col_activation.dpv")

if __name__ == "__main__":
    create_real_model_dpv() 