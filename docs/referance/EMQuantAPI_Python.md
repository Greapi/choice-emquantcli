# EMQuantAPI Python Reference

> **Source URL**: [https://quantapi.eastmoney.com/Upload/EMQuantAPI_Python.html](https://quantapi.eastmoney.com/Upload/EMQuantAPI_Python.html)
>
> 本文档是东方财富 EMQuantAPI Python 接口的官方文档，包含完整的 API 说明、函数使用方法和参数详解。

---

## 升级公告

| **版本号** | 版本变动信息 | 发布时间 |
| --- | --- | --- |
| 2.6.1.0 | V2.6.0.0 -> V2.6.1.0 | 2025-10-30 |

1. 更新CFN资讯函数，新增市场舆情（对应终端资讯栏目）；
2. 新增一批A、港股一级市场相关专题；
3. 其他bug修复。

---

## 目录

- [接口配置](#接口配置)
- [登录函数](#登录函数)
- [退出函数](#退出函数)
- [数据函数](#数据函数)
  - [截面函数](#截面函数)
  - [序列函数](#序列函数)
  - [专题报表](#专题报表)
  - [宏观数据](#宏观数据)
- [资讯函数](#资讯函数)
- [资讯订阅](#资讯订阅)
- [板块截面函数](#板块截面函数)
- [功能函数](#功能函数)
  - [条件选股](#条件选股)
  - [宏观指标查询](#宏观指标查询)
  - [资讯板块查询](#资讯板块查询)
  - [取消资讯订阅](#取消资讯订阅)
  - [板块函数](#板块函数)
  - [交易日历](#交易日历)
  - [交易日偏移](#交易日偏移)
  - [区间交易日数](#区间交易日数)
  - [设置代理函数](#设置代理函数)
  - [人工激活函数](#人工激活函数)
  - [指标校验函数](#指标校验函数)
  - [代码校验函数](#代码校验函数)
  - [日期宏](#日期宏)
  - [流量查询函数](#流量查询函数)
- [组合函数](#组合函数)
  - [新建组合](#新建组合)
  - [组合资金调配](#组合资金调配)
  - [组合查询](#组合查询)
  - [批量下单](#批量下单)
  - [组合报表查询](#组合报表查询)
  - [删除组合](#删除组合)
- [错误类型](#错误类型)
- [常见问题](#常见问题)

---

## 接口配置

### 文件存放位置

在量化接口官网（ https://quantapi.eastmoney.com/）下载压缩包EmQuantAPI_Python.zip，下载完成后解压。其中：

- EmQuantAPISetup.exe安装应用程序（仅Windows系统使用）；
- installEmQuantAPI.py用于注册python接口；
- libs含接口的库文件，以及接口登录激活工具文件，通过手机号获取验证码，自动生成令牌用以登录；
- demo.py为示例脚本文件
- **注意**：保持接口文件相对路径，不要随意修改文件结构

### EMQuantAPI Python接口配置的系统环境要求与方法

**系统环境要求**

- Windows 系统，支持32位和64位系统，以及Microsoft Visual C++ 2010 可再发行组件包（可在电脑"程序和功能"中查看是否安装，下载链接如下）
  - 下载链接： http://choiceclub.eastmoney.com/#/articleDetail/8769
- Centos, Ubuntu，支持32位和64位系统；
- Mac OS 系统，支持64位系统，以及gtk+3.0环境（激活工具使用）
- Python版本： 2.6.x, 2.7.x, 3.x

**配置方法**

- **方法一**：在Windows系统中，在 **Python进程关闭** 的条件下，可右键以 **管理员身份** 运行EmQuantAPISetup.exe，选择已有的Python环境路径进行安装。
- **方式二**：在Windows/Linux/Mac系统中，在命令行运行 installEmQuantAPI.py 注册，若使用Anaconda编译器，请在编译器中运行installEmQuantAPI.py注册。
- **绑定手机号**
  - 登录Choice量化接口网站主页（ https://quantapi.eastmoney.com），点击右上角账户名-个人资料绑定手机号；或者登录Choice金融终端，进入用户中心-资料管理绑定手机号。

### 登录激活（四种方式）

**方式一**：在start函数中直接输入账号密码进行登录（该方式不生成userinfo登录令牌）

**方式二**：使用激活工具（适用于有图形界面）

根据所用系统环境，运行接口激活工具LoginActivator.exe（Windows）、loginactivator_mac（Mac）、loginactivator（Linux）/loginactivator_ubuntu（Ubuntu)，输入绑定手机号获取验证码，激活成功后生成令牌文件userInfo，用户使用时无需输入用户名和密码，默认从令牌中获取登录权限。一个账号最多支持在十台设备上激活。

**方式三**：上行短信登录验证（适用于无、有图形界面）

1. 手机号绑定API接口账号
2. 主动发送短信内容 "SXDL" 到 9535711 （三网合一，不区分运营商）
3. 完成上行短信发送后，调用登录函数start("LoginMode=SXDL,PhoneNumber=xxxxxxxx")，xxxxxx替换为发送短信的手机号
4. 最后登录成功，并且生成userinfo登录令牌
5. userinfo生成之后，下次登录无需重复进行短信验证登录

> **注意**： 
> 1) 发送短信会有通讯费用产生；
> 2) 不需要userInfo文件 登录成功后会生成一个userInfo文件；
> 3) 发送短信之后没有回执；
> 4) 短信失效时间10分钟

**方式四**：人工激活（适用于无、有图形界面）

1. 接口注册成功后，使用manualactive函数，修改并运行如下代码：
```python
# 人工激活代码示例
```
2. 联系客户经理或者客服验证并从邮箱中获取登录令牌userInfo。

---

## 登录函数

```python
start(options, logcallback, mainCallBack)
```

初始化登录函数，登录验证通过以后，即可正常使用接口函数获取数据

### 参数

| 参数名 | 简称 | 定义 | 输入/输出 | 描述 |
| --- | --- | --- | --- | --- |
| options | 可选参数 | 字符串 | 输入 | 附加参数，可填附加字段。见 **附注1** |
| logcallback | 可选参数 | c_LogCallback | 输入 | 日志回调函数 |
| mainCallBack | 可选参数 | c_DataCallback | 输入 | 主回调函数 |

### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

### 范例(Python2.x)

```python
# Python 2.x 示例
```

### 范例(Python3.x)

```python
# Python 3.x 示例
```

### 附注1 登录函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 用户名 | UserName | 字符串 | V2.5.4.6版本开始支持账密登录。若传入此参数且账号密码均不为空则使用账密登录模式。若要使用userinfo登录令牌模式，此参数不传 |
| 密码 | PassWord | 字符串 | 同上 |
| 服务器测速 | TestLatency | 0,1<br>缺省值 0 | 取值0，不测速，连接默认服务器 ；<br>取值1，登录前服务器测速，并保存为默认 |
| 强制登录 | ForceLogin | 0,1<br>缺省值 0 | 取值0，当线上已存在该账户时，不强制登录 ；<br>取值1，当线上已存在该账户时，强制登录，将前一位在线用户踢下线 ； |
| 记录登录信息标记 | RecordLoginInfo | 0,1<br>缺省值 1 | 取值0，不记录；<br>取值1，追加记录登录信息到logininfo.log文件，文件位于serverlist.json.e所在目录下 |
| 上行短信登录 | LoginMode | 取值范围：SXDL | 取值SXDL，进行上行短信登录验证，务必配合PhoneNumber参数一起使用。**使用方法**：用户先使用API绑定的手机号发送内容"SXDL"到9535711完成发送后，然后设置LoginMode和PhoneNumber参数，并调用start函数。成功后，自动生成userinfo。 |
| 手机号码 | PhoneNumber | 取值范围：中国境内11位有效手机号，且有API接口权限 | 同上 |
| HTTP超时时间设置 | HTTPTimeout | 缺省值：15 | 设置HTTP超时时间，单位秒 |
| HTTP三网地址设置 | USEHTTP | 1,2,3 | 取值1，电信；<br>取值2，移动；<br>取值3，联通<br>注意：不能跟参数UseProxy、UseInnerNet一起使用 |
| 内置代理设置 | UseProxy | -1,0,1,2,3 <br>默认值-1 | 使用前需要开通IP白名单，<br>取值-1，不做任何操作；<br>取值0，不使用代理，则不传；<br>取值1，使用内置代理1；<br>取值2，使用内置代理2；<br>取值3，使用内置代理3 |
| 是否使用外网 | UseInnerNet | -1,0，1<br>默认值-1 | 取值 0和-1 都表示使用外网， 其余值使用内网例如1。注意：UseProxy 与 UseInnerNet 同时使用时，UseInnerNet设置参数失效 |

---

## 退出函数

```python
stop()
```

退出登录

### 无参数

### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

## 数据函数

### 截面函数

```python
css(codes, indicators, options, *arga, **argb)
```

获取股票，指数，基金，期货等各个证券品种或组合的基本资料，财务，估值等截面数据

| 参数名 | 简称 | 定义 | | 描述 |
| --- | --- | --- | --- | --- |
| codes | 证券代码 | 字符串或者序列 | 输入 | 东财代码，支持多代码输入，以半角逗号分隔， **不支持跨品种证券输入** |
| indicators | 指标简称 | 字符串或者序列 | 输入 | 指标名称，支持多指标输入，以半角逗号分隔， **最多不超过64个**，详细指标列表见指标手册 |
| options | 可选参数 | 字符串 | 输入 | 附加参数，可填附加字段，见 **附注2** |
| arga | 可选参数 | 可变参数 | 预留 | |
| argb | 可选参数 | 可变参数 | 预留 | |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() # **本地日期**<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注2 截面函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 是否输出pandas格式 | Ispandas | 0，1<br>缺省值：0 | 非pandas格式--0<br>pandas格式--1<br>需要安装pandas包 |
| pandas索引 | RowIndex | 1，2<br>缺省值：1 | 证券代码--1<br>日期--2； |
| 空值替换 | ShowBlank | 整数 | 对返回数据中的空值的进行特殊处理<br>例如：ShowBlank=0，所有的空值都替换成0 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

> **（注：截面函数每分钟请求次数不能超过700次）**

---

### 序列函数

```python
csd(codes, indicators, startdate, EndDate, options, *arga, **argb)
```

获取股票，指数，基金，期货等各个证券品种或组合的序列数据

#### 参数

| 参数名 | 参数简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| codes | 证券代码 | 字符串或者序列 | 东财代码，支持多代码输入，以半角逗号分隔 |
| indicators | 指标简称 | 字符串或者序列 | 指标名称，支持多指标输入，以半角逗号分隔， **最多不超过64个**，详细指标列表见指标手册 |
| startdate | 起始日期 | 字符串或者datetime | 支持格式： YYYYMMDD，YYYY/MM/DD，YYYY/M/D，YYYY-MM-DD，YYYY-M-D |
| EndDate | 截止日期 | 字符串或者datetime | 支持格式： YYYYMMDD，YYYY/MM/DD，YYYY/M/D，YYYY-MM-DD，YYYY-M-D |
| options | 可选参数 | 字符串 | 附加参数，可填附加字段，见 **附注3** |
| arga | 可选参数 | 可变参数 | 预留 |
| argb | 可选参数 | 可变参数 | 预留 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注3 序列函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 是否输出pandas格式 | Ispandas | 0--1<br>缺省值：0 | 非pandas格式--0;<br>pandas格式--1;<br>需要安装pandas包; |
| pandas索引 | RowIndex | 1--2<br>缺省值：1 | 证券代码--1；<br>日期--2； |
| 日期周期 | Period | 1--4<br>缺省值：1 | 日期周期：日，周，月，年 <br>分别对应：１，２，３，４ |
| 复权方式 | AdjustFlag | 1--3<br>缺省值：1 | 不复权--1<br>后复权--2<br>前复权--3 |
| 币种 | CurType | 1--4<br>缺省值：1 | 原始币种--1<br>人民币--2<br>美元--3<br>港币--4<br>(仅适用于港美股指标) |
| 按日期排序 | Order | 1--2<br>缺省值：1 | 升序--1<br>降序--2 |
| 市场类型 | Market | 见说明<br>缺省值："CNSESH" | CNSESH 上海证券交易所 <br>CNSESZ 深圳证券交易所 <br>HKSE00 香港证券交易所 <br>USSE00 美国证券交易所 <br>USSEND 美国纳斯达克市场 <br>USSENY 纽约证券交易所 <br>CNFEBC 渤海商品交易所 <br>CNFEDC 大连商品交易所 <br>CNFESF 上海期货交易所 <br>CNFEZC 郑州商品交易所 <br>INE000 上海国际能源交易中心<br>CNGCSH 上海黄金交易所<br>HKME00 香港商品交易所<br>0 自然日 <br>1 全部交易日 <br>CNSH00 沪股通交易日 <br>CNSHHK 沪港股通交易日 <br>CNSZ00 深股通交易日 <br>CNSZHK 深港股通交易日 <br>NYMEX0 纽约商业期货交易所 <br>USFENY 纽约商品交易所 <br>CME000 芝加哥商业交易所 <br>LDMETL 伦敦金属交易所 <br>LDEXCH 伦敦证券交易所 <br>SGSE00 新加坡交易所 |
| 空值替换 | ShowBlank | 整数 | 对返回数据中的空值的进行特殊处理，例如：ShowBlank=0，所有的空值都替换成0 |
| 沿用之前数据 | filldata | 0,1<br>缺省值：0 | 不沿用--0；<br>沿用--1 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

> **（注：序列函数每分钟请求次数不能超过700次）**

---

### 专题报表

```python
ctr(ctrName, indicators, options)
```

提供专题报表数据

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| ctrName | 报表名称 | 字符串 | 东财报表名称，详细枚举见指标手册 |
| indicators | 报表字段简称 | 字符串或者序列 | 报表字段简称，支持多字段输入，以半角逗号分隔，传空或匹配不到时展示报表全部字段，字段枚举详见指标手册 |
| options | 报表参数 | 字符串 | 报表参数明细，详见指标手册，其他可选参数见 **附注4** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注4 专题报表函数可选参数列表

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 是否输出pandas格式 | Ispandas | 取值范围：0，1 <br>缺省值：0 | 非pandas格式--0；<br>pandas格式--1；<br>需要安装pandas包 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |
| 编码类型 | ENCODE | UTF-8;<br>GBK;<br>GB2312<br>默认值为空（代表自动判断） | 部分文字无法准确判断编码，需要指定编码 |

---

### 宏观数据

```python
edb(edbids, options)
```

获取宏观指标数据

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| edbids | 宏观指标id | 字符串 | 宏观指标id，支持多代码输入，最多不超过100个，以半角逗号分隔，宏观指标列表见量化接口官网-命令生成-宏观数据 |
| options | 可选参数 | 字符串 | 附加参数，可填""，可填附加字段，见 **附注7** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注7 宏观数据函数可选参数列表

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 是否输出pandas格式 | Ispandas | 取值范围：0，1 <br>缺省值：0 | 非pandas格式--0；<br>pandas格式--1；<br>需要安装pandas包 |
| pandas索引 | RowIndex | 取值范围：1，2 <br>缺省值：0 | 宏观指标ID--1；<br>日期--2； |
| 起始日期 | StartDate | 支持格式： YYYYMMDD， YYYY/MM/DD， YYYY/M/D ，<br>YYYY-MM-DD ，YYYY-M-D | 若StartDate不传，从第一条数据开始返回；<br>若EndDate不传，返回至最新一条数据；<br>若都不传则输出全部数据. |
| 截止日期 | EndDate | 同上 | 同上 |
| 最新一条数据 | IsLatest | 取值范围：0，1 <br>缺省值：0 | 取值0，选定日期范围内数据<br>取值1，最新一条数据 |
| 请求指标真实发布日期 | IsPublishDate | 取值范围：0，1 <br>缺省值：0 | 取值0，不请求publishdate<br>取值1，请求publishdate<br>备注：只有部分EDB指标有发布日期 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |
| 调整返回日期 | FixDate | 取值范围：0,1<br> 缺省值：0 | 取值0，按原始日期返回，不进行调整;<br>取值1，调整返回的日期为每个周期对应的最后一个自然日，如年频指标则返回每年的12月31日 |

---

## 资讯函数

```python
cfn(codes, content, mode, options)
```

提供多个证券品种的公告、新闻等历史资讯和多个板块的历史资讯查询

### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| codes | 证券代码或板块代码 | 字符串、列表、元组 | 东财代码，支持多代码，以半角逗号分开。证券代码和板块代码不能混用。板块代码需先调用资讯板块查询函数获取。 |
| content | 请求内容类型 | 字符串 | companynews-公司资讯 <br>industrynews-行业资讯<br>report-公告<br>regularreport-定期公告<br>tradeinfo-重大事项（交易信息）<br>**content为前面几个的时候codes必须为证券代码**<br>sectornews-板块资讯<br>**content为sectornews时codes必须为板块代码**<br>content支持前面五个混合，以半角逗号分隔。sectornews和其他不能混合请求 |
| mode | 请求模式 | 枚举int | eCfnMode_StartToEnd = 1 # starttime和endtime中间的所有资讯 eCfnMode_EndCount = 2 # 提取endtime的近count条数据 |
| options | 可选参数 | 字符串 | 附加参数，可填""，可填附加字段，详见下表 |

### options可选参数

| **中文名称** | **英文名称** | 说明 |
| --- | --- | --- |
| 开始时间 | starttime | 模式一必传，模式二无意义。YYYYMMDDHHMMSS或者YYYYMMDD |
| 结束时间 | endtime | YYYYMMDDHHMMSS或者YYYYMMDD。为空则为当前时间 |
| 资讯条数 | count | 模式二必传，模式一无意义，在模式二返回以endtime为基准的近count条资讯 |

### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

### EmQuantData.Data中指标字段说明

| 输出字段 | 字段中文 |
| --- | --- |
| datetime | 展示时间（公告只展示日期，部分盘后公告展示日期是下一个交易日） |
| eitime | 生产时间（公告只提供2017/01/01之后的数据并且只含日期） |
| code | 证券代码或板块代码 |
| content | 请求类型 |
| title | 资讯标题 |
| infoCode | 资讯编码 |
| medianname | 来源 |
| url | 链接 |
| type | 舆情正负面类型<br>备注：①仅对舆情类资讯生效，其他类型资讯传出空值；②对于未打标的舆情类资讯，也会传出空值；③对于已打标的舆情标签，每个标签均有对应一种正负面类型，可能为"正面、负面、未判断" |
| label | 舆情标签<br>备注：①仅对舆情类资讯生效，其他类型资讯传出空值；②一个资讯可能会有0个或多个舆情标签 |

---

## 资讯订阅

```python
cnq(codes, content, options, fncallback)
```

订阅多个证券品种的公告、新闻等资讯和多个板块的资讯

### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| codes | 证券代码或板块代码 | 字符串、列表、元组 | 东财代码，支持多代码，以半角逗号分开。证券代码和板块代码不能混用。板块代码需先调用资讯板块查询函数获取。 |
| content | 请求内容类型 | 字符串 | companynews-公司资讯 <br>industrynews-行业资讯<br>report-公告<br>regularreport-定期公告<br>tradeinfo-重大事项（交易信息）<br>**content为前面几个的时候codes必须为证券代码**<br>sectornews-板块资讯<br>**content为sectornews时codes必须为板块代码**<br>content支持前面五个混合，以半角逗号分隔。sectornews和其他不能混合请求 |
| options | 可选参数 | 字符串 | ""，预留，暂无可选参数 |
| fncallback | 回调函数 | | 资讯订阅回调，可以使用该函数对返回的数据进行处理 |

### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

---

## 板块截面函数

```python
cses(blockcodes, indicators, options, *arga, **argb)
```

获取沪深京股票板块的基本资料、财务等截面数据

| 参数名 | 简称 | 定义 | | 描述 |
| --- | --- | --- | --- | --- |
| blockcodes | 板块代码 | 字符串或者序列 | 输入 | 东财板块代码，以B_开头，如 "B_018005001001"，支持多代码输入，以半角逗号分隔， **最多不超过6** |
| indicators | 指标简称 | 字符串或者序列 | 输入 | 指标名称，支持多指标输入，以半角逗号分隔， **最多不超过15个**，详细指标列表见指标手册 |
| options | 可选参数 | 字符串 | 输入 | 附加参数，可填附加字段，见 **附注8** |
| arga | 可选参数 | 可变参数 | 预留 | |
| argb | 可选参数 | 可变参数 | 预留 | |

### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() # **本地日期**<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

### 附注8 截面函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 是否取最新板块成分 | isHistory | 0,1 | **必传参数**<br>0，取最新板块成分<br>1，取历史板块成分 |
| 是否输出pandas格式 | Ispandas | 0，1<br>缺省值：0 | 非pandas格式--0<br>pandas格式--1<br>需要安装pandas包 |
| pandas索引 | RowIndex | 1，2<br>缺省值：1 | 证券代码--1<br>日期--2； |
| 空值替换 | ShowBlank | 整数 | 对返回数据中的空值的进行特殊处理<br>例如：ShowBlank=0，所有的空值都替换成0 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

> **（注：板块截面函数不支持多线程）**

---

## 功能函数

### 条件选股

```python
cps(cpsCodes, cpsIndicators, cpsConditions, cpsOptions)
```

条件选股函数

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| cpsCodes | 板块代码或证券代码 | 字符串、列表、元组 | 控制选股范围，CPS函数只能选取沪深京的板块和证券代码，取值格式有两种：<br>1. 板块代码，以B_开头，如 "B_001004"，常见板块代码见 **附注9**;<br> 2. 东财代码，多个代码间用半角逗号隔开，如"000001.SZ,000002.SZ,600000.SH" |
| cpsIndicators | 条件参数 | 字符串 | 定义条件表达式使用的参数，多个参数之间用英文分号隔开,内部各参数用半角逗号隔开，具体指标和英文简称见接口官网命令生成-功能函数-条件选股，如： s1,LISTDATE;s2,TOTALSHARE,2021-06-18 |
| cpsConditions | 条件表达式 | 字符串 | 条件表达式，各表达式用 and 连接，表达式支持的操作符：ANY，CONTAINALL，ISNULL，ISNOTNULL，比较运算符, 算术运算符，逻辑运算符(必须小写)如and、or、not 等，具体操作符释义详见 **附注10**；条件参数引用格式： [参数名1]，例如： [s1] >10 and [s2] > [s1] and not CONTAINANY ([s3],重工,银行)；若选择的条件是日期，需加d( )，例如：[s4]>d(2017/7/21)，若选日期区间，需用多项日期表达式，用and连接，例如：[s4]>d(2013-09-30) and [s4]<d(2014-07-10) |
| cpsOptions | 附加参数 | 字符串 | 其他附加条件，如排序、取前N条选股结果等，具体使用规则见 **附注11** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = list() #数据结果 |

#### 附注9 常见板块代码

| **板块名称** | **板块代码** |
| --- | --- |
| 全部A股 | 001004 |
| 上证A股 | 001005 |
| 深证A股 | 001006 |
| 深证B股 | 001013 |
| 上证B股 | 001012 |
| 全部B股 | 001011 |
| 创业板 | 001010 |
| 中小板 | 001009 |
| 深证主板 | 001008 |
| 深证主板A股 | 001007 |
| 风险警示股票 | 001023 |
| 风险警示股票（深交所） | 001025 |
| 风险警示股票（上交所） | 001024 |
| 已发行待上市股票 | 001020 |
| 正在发行的股票 | 001019 |
| *ST | 001018 |
| ST | 001017 |
| 全部A股(非金融石油石化) | 001044 |
| 可转债标的 | 001046 |
| 融资融券标的 | 001045 |
| 深股通 | 001041 |
| 沪深股通 | 001047 |
| 深证主板B股 | 001033 |
| 中小板(含ST,ST*) | 001032 |
| 深证主板A股(含ST,ST*) | 001031 |
| 沪股通 | 001038 |
| 中证500成份 | 009006062 |
| 中证1000成份 | 009007552 |
| 上证50指数成份 | 009007063 |
| 上证180指数成份 | 009007060 |
| 创业板综成份 | 009007145 |
| 创业板指成份 | 009007144 |
| 中小板综成份 | 009007125 |
| 中小板指成份 | 009007124 |
| 上证综合指数成份 | 009007104 |
| 沪深300成份 | 009006195 |
| 深证综合指数成份 | 009007251 |
| MSCI中国（概念类） | 007230 |
| 预盈预增 | 007054 |
| 预亏预减 | 007053 |

#### 附注10 操作符列表

| **分类** | **操作符** | **描述** | **详细** | **举例** |
| --- | --- | --- | --- | --- |
| 算术运算符 | + - \\* / | 加 减 乘 除 | | |
| 比较运算符 | > = < >= <= <> | 大于 等于 小于 大于或等于 小于或等于 不等于 | | |
| 逻辑运算符 | and or not | 与 或 非 | | |
| | ANY CONTAINANY | 包含任意一个 | | ANY( s[1] , 中国 , 美国 ) 表示当变量s1中包含"中国"或"美国"则成立 |
| | CONTAINALL | 包含所有值 | | CONTAINALL ( s[1] , 中国 , 美国 ) 表示当变量s1中包含"中国"且包含"美国"则成立 |
| | MAX | 取最大的N个值 | 用在Top表达式中，对选股结果取TOP | top=max([s1],100) |
| | MIN | 取最小的N个值 | 用在在Top表达式中，对选股结果取最小的N行 | top=min([s2],100) |
| | ISNULL ISNOTNULL | 等于空值 不等于空值 | 条件选股取空值或不取空值，多项输入用and连接 | isnull([s1])and isnotnull([s2]) |

#### 附注11 排序表达式和Top表达式使用规则

| **字段说明** | **取值格式** | **取值示例** |
| --- | --- | --- |
| 排序表达式：对返回的结果进行排序 | 格式：orderby=[rd\|ra]，（rd为降序，ra为升序） 支持变量引用，引用格式为方括号+变量名 多个排序字段间，以=> 符号分隔 支持的操作符：rd,ra,算术运算符，"=>"分隔符 | orderby=rd([s1]*2) => ra([s2]) |
| Top表达式：对返回结果按指定排序提取前N行 | 格式：top=max(排序字段表达式,行数)或top=min(排序字段表达式,行数) 支持变量引用，引用格式为方括号+变量名 支持的操作符and,or,算术运算符 | top = max([s1],100) and min([s2],100) |
| 板块成分日期：选择的板块成分的日期 | 格式：sectordate=板块历史成分的日期，若sectordate不传则默认取最新的一天。 | sectordate=2018-07-18 |
| 超时时间设置 | 格式：RECVtimeout=正整数，单位秒，如 设置60代表60秒 | RECVtimeout=60 |

---

### 宏观指标查询

```python
edbquery(edbids, indicators, options)
```

获取宏观指标id详情信息

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| edbids | 宏观指标id | 字符串 | 宏观指标id，支持多代码输入，最多不超过100个，以半角逗号分隔 |
| indicators | 详情字段简称 | 字符串 | 详情字段简称，支持多字段输入，以半角逗号分隔，传空或匹配不到时则输出全部字段，详细字段列表见 **附注12** |
| options | 可选参数 | 字符串 | 附加参数，可填NULL，可填附加字段 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注12 宏观指标信息查询函数支持字段列表

| **字段简称** | **中文简称** | **备注** |
| --- | --- | --- |
| ID | 指标ID | |
| Name | 指标名称 | |
| Unit | 单位 | |
| Source | 来源 | |
| Region | 国家/地区 | |
| Frequency | 日期频率 | 1 日 2 周 3 旬 4 半月 5 月 6 季 7 半年 8 年 9 不定期 |
| Startdate | 起始日期 | |
| Enddate | 截止日期 | |
| Updatetime | 更新时间 | |

---

### 资讯板块查询

```python
cfnquery()
```

获取资讯函数和资讯订阅函数支持的板块信息

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

EmQuantData.Data字段说明

| 输出字段 | 字段中文 |
| --- | --- |
| seccode | 板块代码 |
| secname | 板块名称 |
| psecname | 母板块中文名称 |

---

### 取消资讯订阅

```python
cnqc(serialID)
```

取消特定或所有的资讯订阅

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| serialID | 流水号 | 数字 | 传入特定流水号，取消对应的资讯订阅； 传入0，取消所有的资讯订阅 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

### 板块函数

```python
sector(pukeycode, enddate, options, *arga, **argb)
```

获取Choice金融终端指定系统板块证券代码成分列表， **目前只支持沪深股票、上交所期权的历史成分查询，其他板块只能获取最新成分**

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| pukeycode | 板块代码 | 字符串 | 通过 Choice 量化接口网站命令生成（ https://quantapi.eastmoney.com/Cmd/Sector?from=web）获取 |
| enddate | 截止日期 | 字符串或者datetime | 支持格式： YYYYMMDD，YYYY/MM/DD，YYYY/M/D，<br>YYYY-MM-DD，YYYY-M-D |
| options | 可选参数 | 字符串 | 附加参数，可填NULL，可填附加字段，见 **附注13** |
| arga | 可选参数 | 可变参数 | 预留 |
| argb | 可选参数 | 可变参数 | 预留 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = list() #数据结果 |

#### 附注13 板块函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 自选股板块查询 | selfblock | 1 | 1-自选股板块，获取本账号最新的全部自选股板块代码和名称，例sector("","","selfblock=1")，板块代码和日期传空。 |
| 是否输出pandas格式 | Ispandas | 0,1<br>缺省值：0 | 非pandas格式--0;<br>pandas格式--1;<br>需要安装pandas包; |
| pandas索引 | RowIndex | 1,2<br>缺省值：1 | 证券代码--1；<br>日期--2； |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

---

### 交易日历

```python
tradedates(startdate, enddate, options, *arga, **argb)
```

获取指定交易市场，指定时间区间的日期序列

#### 输入

| 参数名 | 简称 | 定义 | | 描述 |
| --- | --- | --- | --- | --- |
| startdate | 起始日期 | 字符串或者datetime | 支持格式： YYYYMMDD， YYYY/MM/DD YYYY/M/D ，YYYY-MM-DD ，YYYY-M-D | |
| enddate | 截止日期 | 字符串或者datetime | 支持格式： YYYYMMDD， YYYY/MM/DD ，YYYY/M/D，YYYY-MM-DD，YYYY-M-D | 不建议使用未来交易日 |
| options | 可选参数 | 字符串 | In | 附加参数，可填NULL，可填附加字段，见 **附注14** |
| arga | 可选参数 | 可变参数 | | 预留 |
| argb | 可选参数 | 可变参数 | | 预留 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = list() #数据结果 |

#### 附注14 交易日函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 日期周期 | Period | 1--5，缺省值：1 | 日期周期：日，周，月，年，季<br>分别对应：１，２，３，４，5 |
| 按日期排序 | Order | 1--2，缺省值：1 | 升序--1； 降序--2 |
| 市场类型 | Market | 见说明，缺省值："CNSESH" | CNSESH 上海证券交易所<br>CNSESZ 深圳证券交易所<br>HKSE00 香港证券交易所<br>USSE00 美国证券交易所 <br>USSEND 美国纳斯达克市场<br>USSENY 纽约证券交易所 <br>CNFEBC 渤海商品交易所 <br>CNFEDC 大连商品交易所 <br>CNFESF 上海期货交易所 <br>CNFEZC 郑州商品交易所<br>INE000 上海国际能源交易中心<br>CNGCSH 上海黄金交易所<br>HKME00 香港商品交易所<br>CNSH00 沪股通交易日<br>CNSHHK 沪港股通交易日 <br>CNSZ00 深股通交易日 <br>CNSZHK 深港股通交易日 <br>NYMEX0 纽约商业期货交易所 <br>USFENY 纽约商品交易所 <br>CME000 芝加哥商业交易所 <br>LDMETL 伦敦金属交易所 <br>LDEXCH 伦敦证券交易所 <br>SGSE00 新加坡交易所 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

---

### 交易日偏移

```python
getdate(tradedate, offday, options, *arga, **argb)
```

获取指定市场交易日历推算第N天交易日

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| tradedate | 交易日期 | 字符串或者datetime | 支持格式： YYYYMMDD，YYYY/MM/DD，YYYY/M/D，YYYY-MM-DD ，YYYY-M-D |
| offday | 偏移天数 | 数字 | N=0时，返回交易日当天； N>0时，交易日往后取最近第N个交易日的日期，若交易日期为最新交易日并N>0,则返回最新交易日； N<0,时，交易日往前取最近第N个交易日的日期。 |
| options | 可选参数 | 字符串 | 附加参数，可填附加字段，见附 **注15** |
| arga | 可选参数 | 可变参数 | 预留 |
| argb | 可选参数 | 可变参数 | 预留 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = list() #数据结果 |

#### 附注15 偏移N天函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 市场类型 | Market | 见说明，缺省值："CNSESH" | CNSESH 上海证券交易所<br>CNSESZ 深圳证券交易所 <br>HKSE00 香港证券交易所 <br>USSE00 美国证券交易所 <br>USSEND 美国纳斯达克市场 <br>USSENY 纽约证券交易所 <br>CNFEBC 渤海商品交易所 <br>CNFEDC 大连商品交易所 <br>CNFESF 上海期货交易所 <br>CNFEZC 郑州商品交易所 <br>INE000 上海国际能源交易中心<br>CNGCSH 上海黄金交易所<br>HKME00 香港商品交易所<br>CNSH00 沪股通交易日 <br>CNSHHK 沪港股通交易日 <br>CNSZ00 深股通交易日 <br>CNSZHK 深港股通交易日 <br>NYMEX0 纽约商业期货交易所 <br>USFENY 纽约商品交易所 <br>CME000 芝加哥商业交易所 <br>LDMETL 伦敦金属交易所 <br>LDEXCH 伦敦证券交易所 <br>SGSE00 新加坡交易所 |
| 超时时间设置 | RECVtimeout | 正整数 | 单位秒，如 设置60代表60秒 |

---

### 区间交易日数

```python
tradeCal(startdate, enddate, options)
```

获取指定交易市场，指定时间区间的交易日个数

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| startdate | 起始日期 | 字符串或者datetime | 支持格式： YYYYMMDD， YYYY/MM/DD YYYY/M/D ，YYYY-MM-DD ，YYYY-M-D |
| enddate | 截止日期 | 字符串或者datetime | 支持格式： YYYYMMDD， YYYY/MM/DD YYYY/M/D ，YYYY-MM-DD ，YYYY-M-D |
| options | 可选参数 | 字符串 | 附加参数，可填附加字段，见 **附注15** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

### 设置代理函数

```python
setproxy(type, proxyip, port, verify, usr, pwd)
```

设置代理

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| type | 代理类型 | 数字（整数） | ePT_NONE：不使用代理 <br>ePT_HTTP：HTTP代理 <br>ePT_HTTPS：HTTPS代理 <br>ePT_SOCK4：SOCK4代理 <br>ePT_SOCK5:SOCK5代理 |
| proxyip | 代理服务器地址 | 字符串 | 代理服务器IP |
| port | 代理服务器端口 | 数字（整数） | 代理服务器Port |
| verify | 是否验证账户名和密码 | 布尔值 | True：验证代理服务器账户名和密码 <br>False：不验证 |
| usr | 账户名 | 字符串 | 代理服务器账户名 |
| pwd | 密码 | 字符串 | 代理服务器密码 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

### 人工激活函数

```python
manualactive(uname, password, options, logcallback)
```

人工激活登录。本函数可独立使用，无需调用start。本函数适用于无界面运行环境（如远程linux）或无法运行LoginActivator程序的情况，激活成功后将通过邮件获得的激活文件"userInfo"放到"ServerList.json.e"同级目录，再调用start登录

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| uname | 用户名 | 字符串 | 输入用户名 |
| password | 密码 | 字符串 | 输入密码 |
| options | 附加参数 | 字符串 | 邮箱地址必传，格式"email= xx@xx.com" |
| logcallback | 附加参数 | 字符串 | 日志回调函数，也可传None |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

### 指标校验函数

```python
cfc(codes, indicators, options)
```

支持校验css/csd/cses函数的代码+指标模式

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| codes | 证券代码 | 字符串 | 东财代码或组合代码或板块代码，支持多代码输入，以半角逗号分隔 |
| indicators | 字段简称 | 字符串或者序列 | 指标字段简称，支持多字段输入，以半角逗号分隔 |
| options | 参数 | 字符串 | 参数明细，见 **16** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注16 指标校验函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 函数种类 | funtype | css、csd、cses | css-截面函数<br>csd-序列函数<br>cses-板块截面函数<br>**注**：单个传入，不支持多个拼接 |

---

### 代码校验函数

```python
cec(codes, options)
```

支持判断东财代码是否有效，同时提供补齐后缀的功能

#### 输入

| 参数 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| codes | 证券代码 | 字符串 | 东财代码，支持多代码输入，以半角逗号分隔 |
| options | 参数 | 字符串 | 参数明细，见 **附注17** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注17 代码校验函数可选参数列表

| 中文名称 | 英文名称 | 取值范围 | 说明 |
| --- | --- | --- | --- |
| 数据返回类型 | Returntype | 0,1 | 0-检测模式，结果查看T/F字段；<br>1-补全模式，结果查看FULLCODES字段，有可能为空或者None，也有可能有多种后缀 |
| 证券品种 | SecuType | 1-8 | **适配Returntype=1使用**，默认值为1,<br>1-股票，<br>2-债券，<br>3-基金理财，<br>4-利率，<br>5-指数，<br>6-期货现货，<br>7-期权，8-外汇 |
| 证券市场 | SecuMarket | 0-5 | **适配Returntype=1使用**，默认值为1,<br>当SecuType=1时，0-全部，1-沪深，2-三板，3-港股，4-美股，5-伦股；<br>当SecuType=2时，0-全部，1-交易所，2-银行间，3-其他；<br>当SecuType=3时，0-全部，1-交易所，2-场外，3-理财；<br>当SecuType=4时，0-全部，1-交易所，2-银行间，3-其他；<br>当SecuType=5时，0-全部，1-东财优先，2-申万优先；<br>当SecuType=6时，0-全部；<br>当SecuType=7时，0-全部；<br>当SecuType=8时，0-全部，1-人民币中间价，2-银行间，3-国际外汇 |

---

### 日期宏

在日期参数中可直接使用字母替代或者加减法运算获取对应的日期，分为相对日期和绝对日期。

#### 相对日期

可用于日期相对计算。

| 相对日期 | 参数英文 | 描述 |
| --- | --- | --- |
| 交易日 | TD | 搭配market参数 可按照指定市场交易日历返回，默认CNSESH上交所，市场列表参考 **附注14 交易日历函数参数列表** |
| 日历日 | D | |
| 日历周 | W | |
| 日历月 | M | |
| 日历季 | Q | |
| 日历半年 | HY | |
| 日历年 | Y | |
| 开始日期 | SD | 引用标识，如 当StartDate="20221020"时，则可设置EndDate="SD+5D" 代表取2022年10月20日到这之后的5天的日期区间 |
| 截止日期 | ED | 引用标识，如 当EndDate="20221020"时，则可设置StartDate="ED-5D" 代表取截止日期的前五天到截止日的日期区间 |

#### 绝对日期

特殊,可返回指定字母对应的具体日期。

| 绝对日期 | 参数英文 | 描述 |
| --- | --- | --- |
| 上市首日 | S | 仅支持css/csd |
| 最新 | N | |
| 最新报告期 | MRQ | 仅支持css |
| 去年一季 | LQ1 | |
| 去年中报 | LQ2 | |
| 去年三季 | LQ3 | |
| 去年年报 | LQ4 | |
| 今年一季 | RQ1 | |
| 今年中报 | RQ2 | |
| 今年三季 | RQ3 | |
| 今年年报 | RQ4 | |
| 本年初 | RYF | |
| 本周一 | RWF | |
| 本月初 | RMF | |
| 上周末 | LWE | |
| 上月末 | LME | |
| 上半年末 | LHYE | |
| 下半年初 | RHYF | |
| 上年末 | LYE | |
| 本季初 | RQF | |
| 本季末 | RQE | |
| 上季末 | LQE | |

#### 说明

1. 支持加减法运算，比如 'ED-10D' 代表 从截止日前推 10 天；'SD+5TD' 代表从开始日往后推5个交易日。
2. 运算中，数字代表 N 个周期，只支持整数。
3. 负号'-'代表前推，没有负号或用加号代表后推。
4. 不带SD/ED标识，则默认从最新开始推，比如 '-5D' 从最新往前推5天。

#### 举例

1. 起始日期为1个周前，截至日期为最新 StartDate= -1W , EndDate= N
2. 报告期为最新 ReportDate = MRQ

---

### 流量查询函数

```python
getfunctionused(funcname, indicators, options)
```

查询函数使用量情况

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| funcname | 函数名称 | 字符串 | 量化接口函数名称，仅支持单个函数查询，传空值返回全部函数，具体可查询函数见 **附注18**，例如：EM_CSS。 |
| indicators | 查询字段 | 字符串 | 查询字段，支持传多个字段，使用逗号分隔，传空值则返回全部字段，具体参数见 **附注19**，例如：FUNCENAME。 |
| options | 参数 | 字符串 | 日期参数，见 **附注20**。 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

#### 附注18 函数列表

| **函数名称** | 参数值 |
| --- | --- |
| 截面函数 | EM_CSS |
| 序列函数 | EM_CSD |
| 专题报表函数 | EM_CTR |
| 宏观数据函数 | EM_EDB |
| 资讯函数 | EM_CFN |
| 资讯订阅函数 | EM_CNQ |
| 板块截面函数 | EM_CSES |
| 条件选股函数 | EM_CPS |
| 自选股查询接口 | EM_SECTOR |
| 宏观查询函数 | EM_EDBQUERY |
| 新建组合函数 | pcreate |
| 组合资金调配函数 | pctransfer |
| 组合下单函数 | porder |
| 组合报表函数 | preport |
| 组合查询函数 | pquery |
| 删除组合函数 | pdelete |
| 函数校验接口 | EM_CFC |
| 代码校验接口 | EM_CEC |

#### 附注19 查询字段参数列表

| **查询字段名称** | 参数值 |
| --- | --- |
| 函数简称 | FUNCENAME |
| 函数名称 | FUNCNAME |
| 证券品种 | SECUTYPE |
| 流量计算周期 | PERIOD |
| 起始日期 | STARTDATE |
| 截止日期 | ENDDATE |
| 流量阈值 | THRESHOLD |
| 使用量 | USEDDATA |
| 使用量占比 | USEDRATIO |
| 剩余流量 | AVAILABEDATA |
| 套餐名称 | PACKAGENAME |
| 套餐有效期 | EFFECTIVEDATE |

#### 附注20 日期参数

| 参数名称 | 参数值 |
| --- | --- |
| 起始日期 | StartDate，传具体日期，日期格式：YYYY-MM-DD |
| 截止日期 | EndDate，传具体日期，日期格式：YYYY-MM-DD |

---

## 组合函数

### 新建组合

```python
pcreate(combinCode, combinName, initialFound, remark, options)
```

新建组合

#### 输入

| 参数名 | 参数简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| combinCode | 组合代码 | 字符串 | 组合代码，英文和数字， **最大10位，单个账户最多支持30个** |
| combinName | 组合名称 | 字符串 | 组合名称 |
| initialFound | 初始资金 | 数字 | 初始资金，上限99999999999 |
| remark | 组合说明 | 字符串 | 组合说明 |
| options | 附加参数 | 字符串 | 附加参数，可填空字串，可填附加字段，见 **附注21** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = list() #数据结果 |

#### 附注21 新建组合函数可选参数列表

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 组合类型 | combintype | 1-4<br>默认值 1 | 1 成长型<br>2 指数型<br>3 平衡型 <br>4 稳健型 |
| 创建公司 | createcompany | 字符串 | 默认留空 |
| 业绩基准 | criteria | 1-16 默认3 | 1 上证指数<br>2 深证成指<br>3 沪深300指数<br>4 上证A股指数<br>5 上证180指数 <br>6 上证50指数<br>7 深证100指数 <br>8 中小板指<br>9 中小板综<br>10 创业板指 <br>11 深证综指<br>12 三板做市指数 <br>13 基金指数<br>14 中证500指数<br>15 中证100指数<br>16 中证1000指数 |

---

### 组合资金调配

```python
pctransfer(combinCode, transferdirect, date, opCash, remark, options)
```

提供组合出入金调配

#### 参数

| 参数名 | 参数简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| combinCode | 组合代码 | 字符串 | 组合代码，英文和数字，最大10位，单个账户最多支持30个 |
| transferdirect | 资金调配方向 | 字符串 | in：增加资金 out：减少资金 |
| date | 调配日期 | 字符串或者datetime | 交易日期格式：YYYYMMDD,YYYY/MM/DD,YYYY/M/D,YYYY-MM-DD,YYYY-M-D |
| opCash | 调配资金量 | 数字 | 增加或减少的资金量，上限100000000000 |
| remark | 说明 | 字符串 | 说明 |
| options | 附加参数 | 字符串 | 附加参数，可填空字串，可填附加字段，见 **附注22** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data =dict() #数据结果 |

#### 附注22 组合资金调配函数可选参数列表

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 调配方式 | transfertype | 1-2 | 1、单个组合增加或减少 2、组合间调配 |
| 组合2 ID | combincode2 | 字符串 | 若transfertype为2 则必传 |
| 调配时间 | time | 24小时 | 格式：HHMMSS，仅在当天有效 |

---

### 组合查询

```python
pquery(options)
```

提供组合账户信息相关数据

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| options | 附加参数 | 字符串 | 附加参数，详见 **附注23** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果，详见 **附注24** |

#### 附注23 组合查询函数附加参数明细

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 组合类型 | combinetype | 0-我管理的组合<br>1-我关注的组合 | 默认值：0 |

#### 附注24 返回数据具体参数明细

| **参数名** | **简称** | **备注** |
| --- | --- | --- |
| COMBINCODE | 组合代码 | |
| GROUPNAME | 组合名称 | |
| STARTCAST | 初始资金 | |
| RESTFOUND | 剩余资金 | |
| CREATEDATE | 创建日期 | |
| MODIFYDATE | 最近调整日期 | |
| GROUPTYPE | 组合类型 | 1：成长型 2：指数型 3：平衡型 4：稳健型 |
| MONEYTYPE | 基准货币 | 1：人民币 2：美元 3：港币 |
| criteria | 组合业绩基准 | 1 上证指数<br>2 深证成指<br>3 沪深300指数<br>4 上证A股指数<br>5 上证180指数 <br>6 上证50指数<br>7 深证100指数 <br>8 中小板指<br>9 中小板综<br>10 创业板指 <br>11 深证综指<br>12 三板做市指数 <br>13 基金指数<br>14 中证500指数<br>15 中证100指数<br>16 中证1000指数 |
| CREATECOMPANY | 创建公司 | |
| REMARK | 组合说明 | |
| LEVEL | 组合等级 | 1：普通组合 2：POP组合 |
| FOLLOWEDID | 关注组合ID | 仅在请求关注组合数据时，返回对应ID |

---

### 批量下单

```python
porder(combincode, orderdict, remark, options)
```

组合批量下单

#### 输入

| 参数名 | 简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| combincode | 组合代码 | 字符串 | 组合代码 |
| orderdict | 下单参数 | 字典 | 具体下单信息，见 **附注25** |
| remark | 备注信息 | 字符串 | 备注信息 |
| options | 附加参数 | 字符串 | 附加参数，见 **附注26** |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

#### 附注25 orderdict参数定义列表

| 序号 | **参数名** | **简称** | **定义** | **是否必填参数** | **说明** |
| --- | --- | --- | --- | --- | --- |
| 1 | code | 代码 | 字符串 | 是 | 东财代码，格式为'300059.SZ' |
| 2 | volume /<br>destvolume /<br>weight | 数量或金额/<br>目标数量/<br>目标权重 | 数字 | 是 | 股票、场内基金数量（正负表示买入、卖出），<br>场外基金申购定投金额、赎回份额 option参数：<br>OrderMode=0时表示交易数量或金额<br>OrderMode=1时表示持仓目标数量<br>OrderMode=2时表示持仓目标权重 |
| 3 | price | 价格 | 数字 | 是 | 交易价格 |
| 4 | date | 日期 | 字符串 | 是 | 交易日期格式为"YYYYMMDD,YYYY/MM/DD,YYYY-MM-DD" |
| 5 | time | 时间 | 字符串 | 否 | 交易时间，格式为"hhmmss，hh:mm:ss" <br>（只影响当日交易，历史交易后台默认150000录入计算） |
| 6 | optype | 操作 | 数字 | 否 | 1买入，2卖出，3申购，4赎回<br>股票交易对应1、2，<br>场外基金交易对应3、4 |
| 7 | cost | 费用 | 数字 | 否 | 场外基金申购、赎回费用/费率，二选一填写，另一个位置填写0。<br>费用为0，则读取费率；<br>费率为0，则读取费用；<br>两者都为0，表示0费用、费率；<br>两者都不为0，默认读取第一个费用。<br>单位：费用 元；费率 %<br>**适用于对场外基金、股票品种** |
| 8 | rate | 费率 | 数字 | 否 | **仅适用于对场外基金品种** |

#### 附注26 组合交易附加参数options列表

| **中文名称** | **英文名称** | **取值范围** | **说明** |
| --- | --- | --- | --- |
| 补入现金方式 | autoAddCash | 0--2，缺省值：0 | 0：不补充<br>1：先扣除可用现金，不足再补充<br>2：全部外部补充本次批量买入操作所需现金 |
| 下单模式 | OrderMode | 0--2，缺省值：0 | 0：按数量交易 volume传入交易数量<br>1：调仓至目标数量，destvolume传目标数量<br>2：调仓至目标权重，weight传目标权重，总权重相加不能超过1<br>备注：1 和 2 不支持逆回购 |

---

### 组合报表查询

```python
preport(combinCode, indicator, options)
```

查询组合报表信息

#### 输入

| 参数名 | 参数简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| combinCode | 组合代码 | 字符串 | 组合代码，支持单次查询单个组合的单个报表 |
| indicator | 报表名称 | 字符串 | 报表名称，hold(持仓查询)， record(交易记录查询)，Contri（业绩贡献-已清仓股票），stagePerf（周期回报-阶段回报），profAna（盈亏分析-区间分析），RiskAna（风险分析），VarAna（VAR分析），GDaily（组合日报），TDaily（交易日报），ctransferrecord(组合资金调配报表) |
| options | 附加参数 | 字符串 | 附加参数，可填空字符串，可填附加字段，见指标手册 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息<br> self.Codes = list() #东财代码<br> self.Indicators = list() #指标简称<br> self.Dates = list() #日期序列<br> self.RequestID = 0 #请求ID <br> self.SerialID = 0 #返回的订阅号 <br> self.Data = dict() #数据结果 |

---

### 删除组合

```python
pdelete(combinCode, options)
```

删除组合

#### 输入

| 参数名 | 参数简称 | 定义 | 描述 |
| --- | --- | --- | --- |
| combinCode | 组合代码 | 字符串 | 组合代码 |
| options | 附加参数 | 字符串 | 附加参数，可不填 |

#### 返回

| 类型 | 描述 |
| --- | --- |
| EmQuantData结构体 | class EmQuantData:<br> def __init__(self):<br> self.ErrorCode = 0 #错误码<br> self.ErrorMsg = 'success' #错误信息 |

---

## 错误类型

| 错误标识 | 错误描述 | 错误代码 |
| --- | --- | --- |
| EQERR_SECUSS | 成功 | 0 |
| EQERR_NO_LOGIN | 用户未登陆 | 10001001 |
| EQERR_USERNAMEORPASSWORD_ERR | 用户名或密码错误 | 10001002 |
| EQERR_NO_ACCESS | 用户无API权限 | 10001003 |
| EQERR_ACCESS_EXPIRE | 用户API权限过期 | 10001004 |
| EQERR_GETUSERINFO_FAIL | 获取用户信息失败 | 10001005 |
| EQERR_DLLVESION_EXPIRE | DLL版本号过期 | 10001006 |
| EQERR_NO_LV2_ACCESS | 用户无API_LV2权限 | 10001007 |
| EQERR_LV2_ACCESS_EXPIRE | 用户API_LV2权限过期 | 10001008 |
| EQERR_LOGIN_COUNT_LIMIT | 账号登陆数达到上限 | 10001009 |
| EQERR_LOGIN_FAIL | 用户登陆失败 | 10001010 |
| EQERR_LOGIN_DISCONNECT | 用户登陆掉线 | 10001011 |
| EQERR_ACCESS_INSUFFICIENCE | 用户权限不足 | 10001012 |
| EQERR_IS_LOGIN | 用户正在登录 | 10001013 |
| EQERR_NEED_ACTIVATE | 需要登录激活 | 10001014 |
| EQERR_LOGIN_SERVICE_ERR | 登录服务异常 | 10001015 |
| EQERR_IS_MANUAL_ACTIVATE | 正在人工激活 | 10001016 |
| EQERR_NOTNEED_MANUAL_ACTIVATE | 无需人工激活 | 10001017 |
| EQERR_MANUAL_ACTIVATE_FAIL | 人工激活失败 | 10001018 |
| EQERR_DIFFRENT_DEVICE | 激活设备与登录设备不一致 | 10001019 |
| EQERR_USERINFO_EXPIRED | userInfo已失效需重新激活 | 10001020 |
| EQERR_INFOQUERY_LOGIN_FAIL | 资讯查询服务登录验证失败 | 10001023 |
| EQERR_INFOSUB_LOGIN_FAIL | 资讯订阅服务登录验证失败 | 10001024 |
| EQERR_INFO_FLOW_FAIL | 资讯服务流量验证失败 | 10001025 |
| EQERR_SMS_INVALIED | 无效的上行短信 | 10001026 |
| EQERR_CHQQUOTE_LOGIN_FAIL | 专项服务登录验证失败 | 10001027 |
| EQERR_CHQQUOTE_ACCESS_FAIL | 专项服务权限验证失败 | 10001028 |
| EQERR_GET_TRADE_FAIL | 获取交易日失败 | 10000001 |
| EQERR_INIT_OBTAIN_CLASS_FAIL | 初始化主类失败 | 10000002 |
| EQERR_NEW_MEM_FAIL | 申请内存失败 | 10000003 |
| EQERR_PARSE_DATA_ERR | 解析数据错误 | 10000004 |
| EQERR_UNGZIP_DATA_FAIL | gzip解压失败 | 10000005 |
| EQERR_UNKNOWN_ERR | 未知错误 | 10000006 |
| EQERR_FUNCTION_INTERNAL_ERR | 函数内部错误 | 10000007 |
| EQERR_OUTOF_BOUNDS | 数组越界 | 10000008 |
| EQERR_NO_DATA | 无数据 | 10000009 |
| EQERR_SYSTEM_ERROR | 系统级别错误 | 10000010 |
| EQERR_SERVERLIST_ERROR | 服务器列表错误 | 10000011 |
| EQERR_OPERATION_FAILURE | 操作失败 | 10000012 |
| EQERR_SERVICE_ERROR | 服务错误 | 10000013 |
| EQERR_GETSERVERLIST_FAIL | 获取服务器列表失败 | 10000014 |
| EQERR_SERVICE_TIMEOUT | 服务超时 | 10000015 |
| EQERR_FREQUENCY_OVER | 请求频次过高 | 10000016 |
| EQERR_OVERSEAS_IP_RESTRICTED | 海外IP受限 | 10000017 |
| EQERR_POP_GROUP_NOT_SUPPORT | POP组合不支持此操作 | 10000018 |
| EQERR_SOCKET_ERR | 网络错误 | 10002001 |
| EQERR_CONNECT_FAIL | 网络连接失败 | 10002002 |
| EQERR_CONNECT_TIMEOUT | 网络连接超时 | 10002003 |
| EQERR_RECVCONNECTION_CLOSED | 网络接收时连接断开 | 10002004 |
| EQERR_SENDSOCK_FAIL | 网络发送失败 | 10002005 |
| EQERR_SENDSOCK_TIMEOUT | 网络发送超时 | 10002006 |
| EQERR_RECVSOCK_FAIL | 网络接收错误 | 10002007 |
| EQERR_RECVSOCK_TIMEOUT | 网络接收超时 | 10002008 |
| EQERR_HTTP_FAIL | http访问失败 | 10002010 |
| EQERR_WAIT_NET_RES_TIMEOUT | 等待网络响应超时 | 10002011 |
| EQERR_INFO_RECONNECT | 资讯服务器重连 | 10002013 |
| EQERR_INFO_RECONNECT_FAIL | 资讯服务器连续重连失败 | 10002014 |
| EQERR_CHQQUOTE_RECONNECT | 专项服务器重连 | 10002015 |
| EQERR_CHQQUOTE_RECONNECT_FAIL | 专项服务器连续重连失败 | 10002016 |
| EQERR_INPARAM_EMPTY | 传入参数为空 | 10003001 |
| EQERR_OUTPARAM_EMPTY | 传出参数为空 | 10003002 |
| EQERR_PARAM_ERR | 参数错误 | 10003003 |
| EQERR_START_DATE_ERR | 起始日期格式不正确 | 10003004 |
| EQERR_END_DATE_ERR | 截止日期格式不正确 | 10003005 |
| EQERR_START_BIGTHAN_END | 起始日期大于截至日期 | 10003006 |
| EQERR_DATE_ERR | 日期格式不正确 | 10003007 |
| EQERR_CODE_INVALIED | 无效的证券代码 | 10003008 |
| EQERR_CODE_REPEAT | 证券代码重复 | 10003009 |
| EQERR_INDICATOR_INVALIED | 无效的指标 | 10003010 |
| EQERR_USERNAME_EMPTY | 用户名为空 | 10003011 |
| EQERR_PASSWORD_EMPTY | 密码为空 | 10003012 |
| EQERR_TO_UPPER_LIMIT | 订阅数或股票总数达到上限 | 10003013 |
| EQERR_MIXED_INDICATOR | 不支持的混合指标 | 10003014 |
| EQERR_INDICATOR_TO_UPPER_LIMIT | 单次订阅指标达到上限 | 10003015 |
| EQERR_BEYOND_DATE_SUPPORT | 超出日期支持范围 | 10003016 |
| EQERR_BASE_LESS_THAN_END | 复权基期小于截止日期 | 10003017 |
| EQERR_MIXED_CODES_MARKET | 不支持的混合证券品种 | 10003018 |
| EQERR_NO_SUPPORT_CODES_MARKET | 不支持的证券代码品种 | 10003019 |
| EQERR_ORDER_TO_UPPER_LIMIT | 交易条数超过上限 | 10003020 |
| EQERR_NO_SUPPORT_ORDERINFO | 不支持的交易信息 | 10003021 |
| EQERR_INDICATOR_REPEAT | 指标重复 | 10003022 |
| EQERR_INFOBKCODE_INVALIED | 资讯板块代码错误 | 10003023 |
| EQERR_INFOSIZE_TOOLARGE | 资讯数据量过大 | 10003024 |
| EQERR_INFO_SEARCH_NODATA | 资讯查询不到数据 | 10003025 |
| EQERR_INFOBKCODE_REPEAT | 资讯板块代码重复 | 10003026 |

---

## 常见问题

### 激活注册

**1. Mac下无法使用打开激活工具？**

- 打开桌面终端命令行，安装CommandLine Tools ：xcode-select –install
- 安装Homebrew：ruby -e "$(curl --insecure -fsSL https://cdn.jsdelivr.net/gh/ineo6/homebrew-install/install)"，直到看到Installation successful
- 安装GTK+3.0：brew install gtk+3

**2. 有图形界面的Linux点击激活工具无反应？**

- 在命令行使用./loginactivator_ubuntu(Ubuntu专用激活工具) 或./loginactivator（除Ubuntu之外的激活工具）
- 使用chmod命令获取执行权限

**3. 激活工具错误提示：获取图片验证码失败，稍后再试？**

- 确认是否有外网限制，如有网络限制，需要将Choice服务器添加至网络白名单，联系Choice相关工作人员（400-620-1818）获取白名单地址；
- 发送serverlist.json.e同级目录下的激活日志ActivatorLog.txt给Choice相关工作人员。

**4. 激活工具错误提示：发送激活码失败？**

- 重启激活工具再次尝试激活
- 仍然失败，查看serverlist.json.e同级目录下的激活日志ActivatorLog.txt错误提示，直接联系下Choice相关工作人员（400-620-1818）

**5. 无图形界面怎么激活？**

- 运行人工激活函数manualactive或者询问客服人员获取人工激活脚本

**6. 如何使人工激活函数进行激活？**

- 1）以C++语言64位为例。取消\\x64\\EmQuantAPITestExe文件夹中main.cpp中的注释，并将自己的账号密码邮箱填进语句中
- 2）在makefile文件夹中使用make命令编译生成新的emquantapitest文件。
- 3）运行bin目录下的emquantapitest

2）以Python语言为例。创建Manualactivate.py脚本，代码如下：

```python
# 人工激活脚本示例
```

这个文件放到installEmQuantAPI同级地方； 先运行installEmQuantAPI，返回installed success之后；填写脚本中用户信息，运行后观察如下日志，即可联系客户经理获取登录令牌。

**7. Linux或者mac报错Errno13 Permission denied**

- 运行注册文件权限不足，需要切换到root

**8. 报错丢失MSVCP100.dll或者WinError126或者WinError 193**

- 根据python安装的版本，对应安装 Microsoft Visual C++ 2010可再发行组件包
- 下载链接： http://choiceclub.eastmoney.com/#/articleDetail/8769

---

### 登录函数

**1. 如何使用上行短信登录**

- 手机号绑定API接口账号
- 主动发送短信内容 "SXDL" 到 9535711 （三网合一，不区分运营商）
- 完成上行短信发送后，调用登录函数start("LoginMode=SXDL,PhoneNumber=xxxxxxxx")，xxxxxx替换为发送短信的手机号
- 最后登录成功，并且生成userinfo登录令牌
- userinfo生成之后，下次登录无需重复进行短信验证登录

> **注意**: 
> 1) 发送短信会有通讯费用产生
> 2) 不需要userInfo文件 登录成功后会生成一个userInfo文件
> 3) 发送短信之后没有回执
> 4) 短信失效时间10分钟

**2. 报错login count up to limit**

- 确认下是否在多台电脑或者多进程使用，因为账号不能同时在多个IP地址上登录，并且当前账号不支持多进程。可以在start参数中加强制登录参数ForceLogin=1。正式账号可联系客户经理开通多点登录服务，支持多进程。

**3. 报错EQERR_USERINFO_EXPIRED**

- 一般是修改密码导致的，一旦修改密码，需要重新激活。

**4. 报错EQERR_DIFFRENT_DEVICE**

- 激活时设备和当前设备不一致。如果是由于设备更换，需要重新激活。确认设备号是否变化可通过查看userinfo同级目录下的登录日志文件logininfo.log中devicenumber最近的登录中是否变化。同一设备上只需要首次使用的时候激活。激活文件有效期一年。

**5. 报错userInfo不存在或不可用**

- 需要先运行激活程序生成userInfo文件

---

### 序列函数

**1. 报错The number of WaitHandles must be less than or equal to 64**

- 指标单次传入不能超过64个

**2. 报错em_csd无权限？**

- 登录接口官网 https://quantapi.eastmoney.com/Flow 点击流量查询或者找客户经理帮查询下，看下是否是csd对应品种流量已用完。

**3. 市场类型没有想要的市场怎么办？**

- 可以选择自然日 market=0，再自行过滤。

---

### 截面函数

**各个函数中的ReportDate要传什么？**

- ReportDate报告日期为每个季度的最后一个自然日，一季报(0331)，中报(0630)，三季报(0930)，年报(1231)，需要对应年度的可以在日期前加上年份，例如2017年三季报为20170930（ReportDate=20170930，支持YYYYMMDD,YYYY-MM-DD,YYYY/MM/DD），和实际的定期报告公告披露日无关。
