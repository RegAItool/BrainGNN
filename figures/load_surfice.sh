#!/bin/bash
# SurfIce加载脚本
# SurfIce Loading Script

echo "🧠 开始加载BrainGNN疼痛分类结果..."

# 设置文件路径
BASE_DIR="/Users/hanyu/Desktop/BrainGNN_Pytorch-main/figures"
BRAIN_TEMPLATE="$BASE_DIR/surfice_templates/brain_fixed.ply"
ACTIVATION_DATA="$BASE_DIR/surfice_visualization/braingnn_pain_activation.nii.gz"

echo "📁 检查文件..."
if [ ! -f "$BRAIN_TEMPLATE" ]; then
    echo "❌ 大脑模板不存在: $BRAIN_TEMPLATE"
    echo "🔄 尝试其他格式..."
    BRAIN_TEMPLATE="$BASE_DIR/surfice_templates/brain.obj"
fi

if [ ! -f "$ACTIVATION_DATA" ]; then
    echo "❌ 激活数据不存在: $ACTIVATION_DATA"
    exit 1
fi

echo "✅ 文件检查完成"
echo "🚀 在SurfIce中手动加载以下文件:"
echo "   1. 大脑模板: $BRAIN_TEMPLATE"
echo "   2. 激活数据: $ACTIVATION_DATA"
echo ""
echo "📖 加载步骤:"
echo "   1. 打开SurfIce"
echo "   2. File → Open → 选择大脑模板"
echo "   3. Overlay → Add → 选择激活数据"
echo "   4. 调整颜色和透明度"
echo ""
echo "🎯 期待看到98.7%准确率的疼痛分类结果!"
