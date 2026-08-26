# Trade Review Assistant

一个使用 Python 编写的命令行交易复盘工具，可以记录、查询、删除交易，并生成交易统计报告。

## 当前版本

V0.2

## 功能

- 新增交易记录
- 校验股票名、买入价、卖出价和数量
- 查看全部历史交易
- 按编号删除交易
- 删除交易前要求确认
- 计算总盈亏
- 计算胜率
- 查找最高盈利交易
- 使用 JSON 保存历史数据
- 程序重启后自动恢复历史数据
- 处理文件不存在、空文件和损坏 JSON
- 使用 pytest 进行自动化测试

## 环境要求

- Python 3.12

## 安装与运行

克隆仓库：

```bash
git clone https://github.com/WanYe-autumn/AI-Agent-learning.git
cd AI-Agent-learning
```

创建并激活虚拟环境：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

进入项目并安装依赖：

```bash
cd 02-trade-review-assistant
python -m pip install -r requirements.txt
```

启动程序：

```bash
python main.py
```

## 使用方法

启动后按照菜单选择操作：

```text
1. 新增交易
2. 查看全部交易
3. 删除交易
0. 退出
```

新增交易的输入格式：

```text
股票名,买入价,卖出价,数量
```

示例：

```text
beone,250,256,100
```

程序会自动计算：

```text
profit = (sell_price - buy_price) * quantity
```

## 运行测试

```bash
python -m pytest -v
```

当前共有 25 个自动化测试，覆盖：

- 正常与错误输入解析
- 盈亏、胜率和最高盈利计算
- 按编号查询与删除
- JSON 正常保存和读取
- 文件不存在、空文件和损坏 JSON

## 项目结构

```text
02-trade-review-assistant/
├── main.py
├── models.py
├── services.py
├── io_utils.py
├── requirements.txt
├── README.md
└── tests/
    ├── test_demo.py
    ├── test_models.py
    ├── test_services.py
    └── test_io_utils.py
```

## 数据说明

交易历史保存在项目目录下的 `trade_report.json`。

该文件是运行数据，不会提交到 Git。程序首次运行时如果文件不存在，会自动从空交易列表开始。

## 已知限制

- 当前使用 JSON 文件存储数据
- 暂不支持编辑已有交易
- 暂无图形界面或 Web API