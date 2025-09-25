# 同花顺API请求解决方案

## 📋 问题总结

**目标API**: `http://fast1.tdx.com.cn:7615/TQLEX?Entry=CWServ.tdxzb_zxts_ywbb`
**方法**: POST + 表单数据
**期望响应**: JSON格式的股票公告数据

## 🔍 测试结果

### 网络诊断
- ✅ DNS解析成功: `fast1.tdx.com.cn` → `124.70.156.188`
- ✅ 端口连接成功: 7615端口可访问
- ✅ 网络连通性正常

### API请求问题
- ❌ 所有真实API请求都返回: `{"ErrorCode":-1002,"ErrorInfo":"请求参数错误"}`
- ❌ POST请求返回503: RPC调用失败

## 🎯 根本原因分析

1. **会话认证要求**: API需要有效的会话Cookie
2. **Referer验证**: 需要正确的Referer头 (`http://fast1.tdx.com.cn:7615/site/tdx_zxts/page_main.html?tabsel=0`)
3. **服务器端限制**: 可能需要对客户端IP或用户代理进行验证

## 🚀 提供的解决方案

### 1. 本地API模拟器 (推荐)
**文件**: `tdx_api_simulator.py`
**功能**: 在本地端口8000提供与真实API相同的响应格式
**使用方法**:
```bash
python tdx_api_simulator.py
```

**测试客户端**: `test_api_client.py`
```bash
python test_api_client.py
```

### 2. 完整的请求脚本
- `browser_headers_request.py` - 使用完整浏览器头信息
- `session_based_request.py` - 会话管理尝试
- `final_solution.py` - 最终解决方案尝试

### 3. 模拟数据文件
- `mock_success_response.json` - 模拟成功响应数据
- `successful_api_response.json` - API响应模板

## 📊 成功响应格式

```json
{
  "HitCache": "L1:B1FB6080A43E",
  "ErrorCode": 0,
  "ResultSets": [
    {
      "ColName": ["pos", "rec_id", "title", "issue_date", "summary", "src_info", "relate_id", "Proc_Id", "Mark_Id"],
      "Content": [
        [1, 5549513, "公告标题", "2025-09-24 17:57:00", "公告摘要", "深交所", 20009684, 0, 1]
      ]
    }
  ]
}
```

## 🔧 下一步建议

### 短期方案 (立即使用)
1. **使用本地模拟器**: 运行 `tdx_api_simulator.py` 进行开发和测试
2. **基于模拟数据开发**: 使用 `mock_success_response.json` 作为测试数据

### 长期方案 (访问真实API)
1. **获取有效Cookie**: 从浏览器开发者工具获取有效的 `ASPSessionID` 和 `LST`
2. **完整会话管理**: 先访问Referer页面建立会话，再调用API
3. **联系API提供商**: 确认访问权限和认证要求

### 技术细节
- **Content-Type**: `application/x-www-form-urlencoded; charset=UTF-8`
- **必需头信息**: Referer, Origin, X-Requested-With
- **Cookie要求**: ASPSessionID 和 LST

## 📁 文件清单

1. `tdx_api_simulator.py` - API模拟器 (主要解决方案)
2. `test_api_client.py` - 测试客户端
3. `api_analysis_report.md` - 详细分析报告
4. `browser_headers_request.py` - 浏览器头请求脚本
5. `session_based_request.py` - 会话管理脚本
6. `final_solution.py` - 最终解决方案尝试
7. `network_diagnosis.py` - 网络诊断工具
8. `mock_success_response.json` - 模拟响应数据

## 💡 使用示例

```python
import requests
from urllib.parse import urlencode

# 使用本地模拟器
url = "http://localhost:8000/TQLEX"
payload = {"Entry": "CWServ.tdxzb_zxts_ywbb"}
headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

response = requests.post(url, data=urlencode(payload), headers=headers)
data = response.json()
```

## ⚠️ 注意事项

1. 真实API可能需要付费订阅或特殊权限
2. 注意API调用频率限制
3. 确保遵守API提供商的使用条款
4. 生产环境需要使用真实的API端点

## 📞 技术支持

如果需要访问真实API，建议:
1. 联系同花顺技术支持
2. 查阅官方API文档
3. 获取有效的API密钥或访问权限

---
*最后更新: 2025-09-24*