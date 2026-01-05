#!/bin/bash
# sync_and_translate.sh - 同步上游更新并翻译新文件

set -e

echo "🔄 开始同步上游仓库..."

# 获取上游更新
git fetch upstream
echo "✅ 获取上游更新完成"

# 切换到主分支
git checkout main

# 合并上游更新
echo "🔀 合并上游更新..."
git merge upstream/main -m "Merge upstream updates"

# 检查是否有新文件需要翻译
echo "📝 检查需要翻译的文件..."
poetry run python translate.py . --dry-run > translation_needed.txt 2>&1

# 从状态行提取需要翻译的文件数
files_to_translate=$(grep "Status:" translation_needed.txt | grep -o "[0-9]* need translation" | grep -o "[0-9]*")

# 如果没有找到状态行，尝试旧的方法
if [ -z "$files_to_translate" ]; then
    files_to_translate=$(grep "needs translation" translation_needed.txt | wc -l | tr -d ' ')
fi

if [ $files_to_translate -gt 0 ]; then
    echo "📚 发现 $files_to_translate 个文件需要翻译"

    # 询问是否开始翻译
    read -p "是否开始翻译？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 选择模型
        echo "请选择翻译模型："
        echo "1) openai/gpt-5.2-chat (推荐)"
        echo "2) gpt-3.5-turbo (快速，成本低)"
        echo "3) gpt-4o-mini (质量较好)"
        read -p "选择 (1-3): " model_choice

        case $model_choice in
            1) MODEL="openai/gpt-5.2-chat";;
            2) MODEL="gpt-3.5-turbo";;
            3) MODEL="gpt-4o-mini";;
            *) MODEL="openai/gpt-5.2-chat";;
        esac

        echo "🚀 使用 $MODEL 开始翻译..."
        poetry run python translate.py . -m $MODEL

        # 提交翻译结果
        echo "💾 提交翻译文件..."
        git add *_zh.md *_zh.txt
        git commit -m "Add Chinese translations for new files

        Translated using $MODEL
        Files translated: $files_to_translate"

        echo "✅ 翻译完成并已提交！"
    else
        echo "⏭️ 跳过翻译"
    fi
else
    echo "✨ 没有新文件需要翻译"
fi

# 清理临时文件
rm -f translation_needed.txt

# 询问是否推送
read -p "是否推送到你的 Fork？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main
    echo "✅ 已推送到你的 Fork"
else
    echo "⏸️ 未推送，稍后可运行: git push origin main"
fi

echo "🎉 同步完成！"