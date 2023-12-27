# ConvertibleBondAlerts 可转债提醒

这是一个Python脚本，专门用于提醒用户今日可申购的可转债信息。它通过访问特定API实时获取最新的可转债数据，并使用bark进行实时消息提醒。

## 功能

- 实时提醒今日可申购的可转债
- 通过bark发送消息提醒

## 快速开始

1. 克隆仓库到本地。
2. 安装所需依赖: `pip install -r requirements.txt`。
3. 设置环境变量`BARK_TOKEN`为您的bark token。
4. 运行脚本: `python main.py`。

## 配置

### 环境变量

- `BARK_TOKEN`: 您的bark应用token，用于发送消息提醒。请确保在运行脚本之前设置此环境变量。

## 贡献

如果您有任何功能请求或发现了bug，请随时提交issue或pull request。

## 许可

[MIT](LICENSE)
