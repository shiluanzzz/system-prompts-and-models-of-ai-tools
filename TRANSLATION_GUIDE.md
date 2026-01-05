# 系统提示词中文翻译维护指南

## 初始设置

### 1. Fork 仓库
1. 访问 [原始仓库](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
2. 点击右上角 **Fork** 按钮
3. 选择你的账户创建 Fork

### 2. 克隆你的 Fork
```bash
git clone https://github.com/YOUR_USERNAME/system-prompts-and-models-of-ai-tools
cd system-prompts-and-models-of-ai-tools
```

### 3. 配置 Remotes
```bash
# 添加上游仓库
git remote add upstream https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools

# 验证配置
git remote -v
```

### 4. 安装依赖
```bash
# 安装 Poetry
pip install poetry

# 安装项目依赖
poetry install
```

### 5. 配置环境变量
创建 `.env` 文件：
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://your-api-base.com/v1  # 可选，如果使用代理
OPENAI_MODEL=gpt-3.5-turbo  # 默认模型
```

## 使用方法

### 手动同步和翻译
```bash
# 运行同步脚本
./sync_and_translate.sh
```

### 仅翻译（不同步）
```bash
# 查看需要翻译的文件
poetry run python translate.py . --dry-run

# 翻译所有文件
poetry run python translate.py . -m gpt-3.5-turbo

# 翻译特定目录
poetry run python translate.py "Cursor Prompts" -m gpt-3.5-turbo

# 翻译单个文件
poetry run python translate.py "path/to/file.txt" -m gpt-3.5-turbo
```

### 使用 GitHub Actions（自动化）

#### 设置 Secrets
在你的 Fork 仓库中，进入 Settings > Secrets and variables > Actions，添加：
- `OPENAI_API_KEY`：你的 OpenAI API 密钥
- `OPENAI_API_BASE`：（可选）API 代理地址

#### 手动触发
1. 进入 Actions 标签页
2. 选择 "Sync and Translate" 工作流
3. 点击 "Run workflow"
4. 选择翻译模型
5. 点击运行

#### 自动运行
工作流已配置为每周一自动运行，会：
1. 同步上游更新
2. 翻译新文件
3. 提交并推送到你的 Fork

## 翻译脚本选项

```bash
poetry run python translate.py --help
```

选项：
- `-m, --model`：指定模型（gpt-3.5-turbo, gpt-4o-mini, gpt-4o）
- `-f, --force`：强制重新翻译已存在的文件
- `--dry-run`：预览模式，不实际翻译
- `-e, --ext`：指定文件扩展名（默认 .md .txt）
- `--no-recursive`：不递归子目录

## 维护工作流

### 日常维护
1. 定期运行同步脚本获取上游更新
2. 翻译新增文件
3. 提交到你的 Fork
4. （可选）向原仓库提交 PR 贡献翻译

### 处理冲突
如果合并时有冲突：
```bash
# 手动解决冲突
git status  # 查看冲突文件
# 编辑冲突文件
git add .
git commit -m "Resolve merge conflicts"
```

### 贡献翻译
如果想贡献翻译给原仓库：
1. 创建新分支：`git checkout -b add-chinese-translations`
2. 提交翻译文件
3. 推送分支：`git push origin add-chinese-translations`
4. 在 GitHub 上创建 Pull Request

## 注意事项

1. **API 配额**：注意 OpenAI API 的使用配额和费用
2. **翻译质量**：建议使用 gpt-3.5-turbo 进行初次翻译，重要文件可用 gpt-4o 提升质量
3. **文件跳过**：已存在 `*_zh.md` 或 `*_zh.txt` 的文件会自动跳过
4. **批量翻译**：大量文件建议分批翻译，避免 API 限流

## 故障排除

### API 错误
- 检查 API key 是否正确
- 检查 API base URL（如果使用代理）
- 确认模型可用性

### Git 权限问题
- 确保已正确 Fork 仓库
- 检查 GitHub token 权限

### Poetry 问题
```bash
# 重新安装依赖
poetry install --no-cache

# 清理缓存
poetry cache clear pypi --all
```