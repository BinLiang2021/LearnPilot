# Perplexity AI 查询工具

这个工具提供了与 Perplexity AI API 交互的功能，用于进行智能搜索和研究查询。

## 功能特性

- 🔍 **智能搜索**: 使用 Perplexity 的在线搜索模型进行实时信息查询
- 📚 **研究查询**: 专门针对学术研究优化的查询功能
- 🌊 **流式响应**: 支持实时流式输出，提升用户体验
- 🎯 **多模型支持**: 支持多种 Perplexity 模型选择
- 📖 **引用支持**: 自动获取和返回信息来源

## 安装依赖

确保你已经安装了以下依赖：

```bash
pip install openai python-dotenv
```

## 配置

1. 在项目根目录创建 `.env` 文件
2. 添加你的 Perplexity API Key：

```env
PERPLEXITY_API_KEY=your_api_key_here
```

获取 API Key 的步骤：
1. 访问 [Perplexity AI 官网](https://perplexity.ai)
2. 注册账户并设置付款信息
3. 在开发者界面生成 API Key

## 使用方法

### 基本查询

```python
from perpelxity_utils import search_perplexity

# 简单查询
result = search_perplexity("What are the latest trends in AI?")
print(result['content'])
```

### 高级查询

```python
from perpelxity_utils import PerplexityClient

# 创建客户端
client = PerplexityClient()

# 自定义查询
result = client.query(
    query="Explain quantum computing",
    model="sonar_large",  # 选择模型
    temperature=0.1,      # 控制创造性
    max_tokens=1000,      # 限制响应长度
    system_prompt="You are a technical expert.",  # 自定义系统提示
    return_sources=True   # 返回来源信息
)

print(result['content'])
print(f"Sources: {len(result['citations'])}")
```

### 研究查询

```python
from perpelxity_utils import research_topic

# 针对研究优化的查询
result = research_topic(
    topic="Recent advances in neural networks",
    focus_domains=["academic papers", "research publications"]
)

print(result['content'])
```

### 流式查询

```python
client = PerplexityClient()

# 实时流式输出
for chunk in client.stream_query("Explain machine learning"):
    print(chunk, end="", flush=True)
```

## 支持的模型

- `sonar_large`: `llama-3.1-sonar-large-128k-online` (默认)
- `sonar_huge`: `llama-3.1-sonar-huge-128k-online`  
- `sonar_small`: `llama-3.1-sonar-small-128k-online`
- `sonar_large_chat`: `llama-3.1-sonar-large-128k-chat`
- `sonar_small_chat`: `llama-3.1-sonar-small-128k-chat`

## API 响应格式

```python
{
    "content": "响应内容",
    "model": "使用的模型名称", 
    "usage": {
        "prompt_tokens": 输入token数,
        "completion_tokens": 输出token数,
        "total_tokens": 总token数
    },
    "citations": [引用来源列表]
}
```

## 错误处理

工具包含完整的错误处理机制：

```python
try:
    result = search_perplexity("your query")
except Exception as e:
    print(f"查询失败: {e}")
```

常见错误：
- `ValueError`: API Key 未设置
- `API Error`: API 请求失败（检查 API Key 和余额）

## 使用示例

运行 `example_usage.py` 查看完整的使用示例：

```bash
cd learn_pilot_src/src/literature_utils/knowledge_search/
python example_usage.py
```

## 注意事项

1. **API 计费**: Perplexity API 按使用量计费，请注意控制使用量
2. **速率限制**: API 可能有速率限制，建议合理控制请求频率
3. **模型选择**: 不同模型有不同的性能和成本，根据需要选择
4. **数据隐私**: API 提交的数据不会用于模型训练

## 技术支持

如有问题或建议，请联系开发团队或查看 [Perplexity API 文档](https://docs.perplexity.ai/)。 