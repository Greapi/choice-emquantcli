# EMQ CLI 用户手册

本文档详细介绍 `emq` 命令行工具的使用方法，包括全局选项和各命令域的详细说明。

---

## 目录

- [概述](#概述)
- [全局选项](#全局选项)
- [认证命令 (auth)](#认证命令-auth)
- [市场数据命令 (market)](#市场数据命令-market)
- [组合命令 (portfolio)](#组合命令-portfolio)
- [额度命令 (quota)](#额度命令-quota)
- [原始命令 (raw)](#原始命令-raw)
- [输出格式](#输出格式)
- [环境变量](#环境变量)
- [使用示例](#使用示例)

---

## 概述

`emq` 是一个面向 EmQuantAPI 的领域驱动命令行工具，内置了运行时库，无需额外安装 SDK。

### 主要特性

- 领域化命令设计（auth、market、portfolio、quota、raw）
- 统一的输出格式（JSON/Table/CSV）
- 自动登录和凭证持久化
- 支持环境变量配置

---

## 全局选项

以下选项可在任何命令之前使用，作用于全局：

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--output` | `json` | 输出格式：`json`、`table` 或 `csv` |
| `--log-level` | `INFO` | 日志级别：`DEBUG`、`INFO`、`WARNING`、`ERROR` |
| `--log-file` | - | 可选的日志文件路径 |
| `--no-auto-login` | - | 禁用自动登录 |

### 使用方式

全局选项可放在子命令之前：

```bash
emq --output table market snapshot 000001.SZ CLOSE
```

或在叶子命令末尾使用 `--output` 进行覆盖：

```bash
emq market snapshot 000001.SZ CLOSE --output csv
```

如果两者都提供，叶子命令的 `--output` 优先级更高。

---

## 认证命令 (auth)

用于管理登录状态和凭证。

### auth login

登录到 EmQuant 服务，并可选保存凭证到本地。

**用法：**

```bash
emq auth login [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--user` | 否 | 用户名，也可通过 `EMQ_USER` 环境变量提供 |
| `--password` | 否 | 密码，也可通过 `EMQ_PASS` 环境变量提供 |
| `--force-login` | 否 | 强制登录（默认：`--force-login`） |
| `--no-force-login` | 否 | 不强制登录 |
| `--save` | 否 | 保存凭证到本地状态文件（默认：`--save`） |
| `--no-save` | 否 | 不保存凭证 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
# 使用环境变量登录
export EMQ_USER='your_username'
export EMQ_PASS='your_password'
emq auth login

# 直接指定用户名密码
emq auth login --user your_username --password your_password

# 登录但不保存凭证
emq auth login --user your_username --password your_password --no-save
```

### auth logout

登出并清除本地保存的凭证状态。

**用法：**

```bash
emq auth logout [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq auth logout
```

### auth status

查看当前认证状态，可选择探测远程 API 状态。

**用法：**

```bash
emq auth status [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--check` | 否 | 探测远程 API 状态 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
# 查看本地状态
emq auth status

# 探测远程 API 状态
emq auth status --check
```

---

## 市场数据命令 (market)

用于查询市场数据，提供高层封装的便捷查询方式。

### market snapshot

获取证券快照数据（截面数据）。

**用法：**

```bash
emq market snapshot <codes> <indicators> [选项]
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `codes` | 是 | 证券代码，多个用逗号分隔，如 `000001.SZ,000002.SZ` |
| `indicators` | 是 | 指标名称，多个用逗号分隔，如 `CLOSE,VOLUME` |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
# 查询单只股票收盘价
emq market snapshot 000001.SZ CLOSE

# 查询多只股票多个指标
emq market snapshot 000001.SZ,000002.SZ CLOSE,VOLUME,OPEN --output table
```

### market series

获取证券序列数据（时间序列数据）。

**用法：**

```bash
emq market series <codes> <indicators> --start <date> --end <date> [选项]
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `codes` | 是 | 证券代码，多个用逗号分隔 |
| `indicators` | 是 | 指标名称，多个用逗号分隔 |
| `--start` | 是 | 开始日期，格式 `YYYY-MM-DD` |
| `--end` | 是 | 结束日期，格式 `YYYY-MM-DD` |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
# 查询历史收盘价
emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31

# 查询多只股票历史数据
emq market series 000001.SZ,000002.SZ CLOSE,VOLUME --start 2025-01-01 --end 2025-01-31 --output table
```

---

## 组合命令 (portfolio)

用于管理投资组合和下单操作。

### portfolio create

创建一个新的投资组合。

**用法：**

```bash
emq portfolio create --code <code> --name <name> --initial-fund <amount> [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--name` | 是 | 组合名称 |
| `--initial-fund` | 是 | 初始资金金额 |
| `--remark` | 否 | 备注信息 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq portfolio create --code my_portfolio --name "我的组合" --initial-fund 100000 --remark "测试组合"
```

### portfolio list

列示所有投资组合。

**用法：**

```bash
emq portfolio list [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq portfolio list --output table
```

### portfolio hold

查询指定组合的持仓明细（对应 SDK 的 `preport` 方法，`indicator=hold`）。

**用法：**

```bash
emq portfolio hold --code <code> [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq portfolio hold --code my_portfolio --output table
```

### portfolio delete

删除指定投资组合（对应 SDK 的 `pdelete` 方法）。

为避免误删，必须显式传入 `--yes` 才会执行删除。

**用法：**

```bash
emq portfolio delete --code <code> --yes [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--yes` | 是 | 删除确认开关，不提供则拒绝执行 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq portfolio delete --code my_portfolio --yes
```

### portfolio order

通过文件方式对组合进行批量下单。

**用法：**

```bash
emq portfolio order --code <code> --orders-file <path> [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--orders-file` | 是 | 订单 JSON 文件路径 |
| `--remark` | 否 | 备注信息 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**订单文件格式：**

`--orders-file` 指定一个 JSON 文件路径，文件内容为一个字典，包含以下字段：

```json
{
  "code": "300059.SZ",
  "volume": 100,
  "price": 10.5,
  "date": "20250115",
  "time": "093000",
  "optype": 1,
  "cost": 0,
  "rate": 0
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `code` | 是 | 东财代码，格式如 `300059.SZ` |
| `volume` / `destvolume` / `weight` | 是 | 交易数量/目标数量/目标权重（取决于 OrderMode） |
| `price` | 是 | 交易价格 |
| `date` | 是 | 交易日期，格式 `YYYYMMDD`、`YYYY/MM/DD` 或 `YYYY-MM-DD` |
| `time` | 否 | 交易时间，格式 `HHMMSS` 或 `HH:MM:SS`（仅影响当日交易） |
| `optype` | 否 | 操作类型：1=买入，2=卖出，3=申购，4=赎回（股票对应1、2，场外基金对应3、4） |
| `cost` | 否 | 费用（元），与费率二选一，适用于场外基金、股票 |
| `rate` | 否 | 费率（%），与费用二选一，适用于场外基金 |

**OrderMode 说明（通过 `--options` 指定）：**
- `OrderMode=0`（默认）：`volume` 表示交易数量（正数买入，负数卖出）
- `OrderMode=1`：`destvolume` 表示目标持仓数量（调仓至目标数量）
- `OrderMode=2`：`weight` 表示目标权重（调仓至目标权重，总权重不超过1）

**示例：**

```bash
emq portfolio order --code my_portfolio --orders-file ./order.json
```

### portfolio qorder

快速下单，通过命令行参数直接下单，无需准备文件。

**用法：**

```bash
emq portfolio qorder --code <code> --stock <stock> --volume <volume> --price <price> --date <date> [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--stock` | 是 | 证券代码，如 `300059.SZ` |
| `--volume` | 是 | 交易数量（正数=买入，负数=卖出） |
| `--price` | 是 | 交易价格 |
| `--date` | 是 | 交易日期，格式 `YYYY-MM-DD` |
| `--time` | 否 | 交易时间，格式 `HHMMSS` 或 `HH:MM:SS` |
| `--type` | 否 | 操作类型：1=买入，2=卖出，3=申购，4=赎回（默认：0，自动判断） |
| `--remark` | 否 | 备注信息 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
# 买入 100 股
emq portfolio qorder --code my_portfolio --stock 300059.SZ --volume 100 --price 10.5 --date 2025-01-15

# 卖出 100 股
emq portfolio qorder --code my_portfolio --stock 300059.SZ --volume -100 --price 10.5 --date 2025-01-15

# 指定时间和操作类型
emq portfolio qorder --code my_portfolio --stock 300059.SZ --volume 100 --price 10.5 --date 2025-01-15 --time 09:30:00 --type 1
```

---

## 额度命令 (quota)

用于查询 API 使用额度和统计数据。

### quota usage

查询 API 使用额度情况。

**用法：**

```bash
emq quota usage [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--start` | 否 | 开始日期，格式 `YYYY-MM-DD`（默认：近 30 天） |
| `--end` | 否 | 结束日期，格式 `YYYY-MM-DD`（默认：今天） |
| `--func` | 否 | 函数名称过滤 |
| `--indicators` | 否 | 查询的指标字段（默认包含常用字段） |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**默认指标字段：**

`FUNCENAME,FUNCNAME,SECUTYPE,PERIOD,STARTDATE,ENDDATE,THRESHOLD,USEDDATA,USEDRATIO,AVAILABEDATA`

**示例：**

```bash
# 查询最近 30 天额度使用情况
emq quota usage

# 查询指定日期范围
emq quota usage --start 2025-01-01 --end 2025-01-31

# 指定输出格式
emq quota usage --output table
```

---

## 原始命令 (raw)

提供对 EmQuant SDK 原始命令的直接访问，适用于高级用户。

### raw css

原始快照查询（对应 SDK 的 `css` 方法）。

**用法：**

```bash
emq raw css <codes> <indicators> [选项]
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `codes` | 是 | 证券代码 |
| `indicators` | 是 | 指标名称 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq raw css 000001.SZ CLOSE --output table
```

### raw csd

原始序列查询（对应 SDK 的 `csd` 方法）。

**用法：**

```bash
emq raw csd <codes> <indicators> --start <date> --end <date> [选项]
```

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `codes` | 是 | 证券代码 |
| `indicators` | 是 | 指标名称 |
| `--start` | 是 | 开始日期 |
| `--end` | 是 | 结束日期 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq raw csd 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31
```

### raw pquery

原始组合查询（对应 SDK 的 `pquery` 方法）。

**用法：**

```bash
emq raw pquery [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq raw pquery
```

### raw porder

原始组合下单（对应 SDK 的 `porder` 方法）。

**用法：**

```bash
emq raw porder --code <code> --orders-file <path> [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--orders-file` | 是 | 订单 JSON 文件路径，格式详见 [portfolio order](#portfolio-order) 的订单文件格式说明 |
| `--remark` | 否 | 备注信息 |
| `--options` | 否 | 原始 EmQuant 选项字符串，支持 `OrderMode`、`autoAddCash` 等参数 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq raw porder --code my_portfolio --orders-file ./order.json

# 调仓至目标权重模式
emq raw porder --code my_portfolio --orders-file ./order.json --options "OrderMode=2"
```

### raw pdelete

原始组合删除（对应 SDK 的 `pdelete` 方法）。

为避免误删，必须显式传入 `--yes` 才会执行删除。

**用法：**

```bash
emq raw pdelete --code <code> --yes [选项]
```

**参数：**

| 选项 | 必填 | 说明 |
|------|------|------|
| `--code` | 是 | 组合代码 |
| `--yes` | 是 | 删除确认开关，不提供则拒绝执行 |
| `--options` | 否 | 原始 EmQuant 选项字符串 |
| `--output` | 否 | 输出格式覆盖 |

**示例：**

```bash
emq raw pdelete --code my_portfolio --yes
```

---

## 输出格式

所有命令支持三种输出格式：

### json（默认）

返回统一的 JSON 信封格式：

```json
{
  "success": true,
  "error": null,
  "meta": {
    "command": "market.snapshot",
    "row_count": 2
  },
  "data": [
    {"code": "000001.SZ", "CLOSE": 10.5}
  ]
}
```

### table

以 ASCII 表格形式展示，便于在终端阅读：

```
+-----------+-------+
| code      | CLOSE |
+-----------+-------+
| 000001.SZ | 10.5  |
+-----------+-------+
```

### csv

以 CSV 格式输出，便于导入到 Excel 或其他工具：

```csv
code,CLOSE
000001.SZ,10.5
```

---

## 环境变量

以下环境变量可用于配置工具行为：

| 变量名 | 说明 |
|--------|------|
| `EMQ_USER` | EmQuant 用户名 |
| `EMQ_PASS` | EmQuant 密码 |

**示例：**

```bash
export EMQ_USER='your_username'
export EMQ_PASS='your_password'
emq auth login
```

---

## 使用示例

### 完整工作流程示例

```bash
# 1. 设置环境变量并登录
export EMQ_USER='your_username'
export EMQ_PASS='your_password'
emq auth login

# 2. 查询市场数据
emq market snapshot 000001.SZ CLOSE --output table
emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31 --output table

# 3. 创建投资组合
emq portfolio create --code test_pf --name "测试组合" --initial-fund 100000

# 4. 查看组合列表
emq portfolio list --output table

# 5. 快速下单
emq portfolio qorder --code test_pf --stock 300059.SZ --volume 100 --price 10.5 --date 2025-01-15

# 6. 查询额度使用情况
emq quota usage --output table

# 7. 登出
emq auth logout
```

### 使用文件批量下单示例

创建订单文件 `orders.json`：

```json
{
  "code": "300059.SZ",
  "volume": 100,
  "price": 10.5,
  "date": "20250115",
  "time": "093000",
  "optype": 1
}
```

执行下单：

```bash
emq portfolio order --code my_portfolio --orders-file ./orders.json
```

---

## 注意事项

1. **凭证安全**：凭证保存在 `~/.emq/state.json` 文件中，注意保护好该文件
2. **自动登录**：业务命令会自动登录（如果已保存凭证），可使用 `--no-auto-login` 禁用
3. **日期格式**：所有日期参数使用 `YYYY-MM-DD` 格式
4. **错误处理**：命令失败时会返回包含错误信息的 JSON 信封，退出码非零
