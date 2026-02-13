# 六十甲子象意百科查询系统（Phase 1）——系统架构设计任务书

## 1. 项目概述

构建一个面向六十甲子干支象意的结构化百科查询系统，提供干支基础信息、纳音五行、神煞、象意、喜忌、干支关系等知识的一站式检索与可视化。系统采用前后端分离架构，后端提供RESTful API，前端为响应式Web应用，数据库使用SQLite。本阶段仅实现核心查询功能与管理员数据管理，不涉及用户注册、收藏等个性化功能。

**核心目标**：建成国内首个专门针对六十甲子象意的结构化知识服务平台，数据准确、查询高效、易于扩展。

------

## 2. 技术栈建议（供架构师参考）

| 层次         | 推荐技术                     | 说明                                                         |
| :----------- | :--------------------------- | :----------------------------------------------------------- |
| **后端框架** | FastAPI（Python）            | 自动生成OpenAPI文档，高性能异步支持，与SQLAlchemy/Alembic集成良好 |
|              | 备选：Node.js + Express      | 也可，但需自行实现API文档                                    |
| **数据库**   | SQLite + SQLAlchemy ORM      | 文件数据库，无需额外服务，Alembic管理迁移                    |
| **API风格**  | RESTful JSON                 | 严格遵循REST语义                                             |
| **前端框架** | React 18 + Vite              | 轻量快速，组件化开发                                         |
|              | 备选：Vue 3 + Vite           | 同样优秀，团队熟悉优先                                       |
| **可视化库** | D3.js / ECharts              | 关系图谱、数据图表                                           |
| **UI组件库** | Ant Design / Element Plus    | 成熟、响应式                                                 |
| **部署**     | Docker + Docker Compose      | 单容器包含前后端（或分离容器）                               |
| **版本控制** | Git                          | GitHub / GitLab                                              |
| **项目管理** | 提供OpenAPI规范（yaml/json） | 前后端并行开发                                               |

**技术约束**：

- 数据库必须使用 **SQLite**，不得依赖外部数据库服务。
- 后端必须提供 **完整的OpenAPI规范**（Swagger UI）。
- 前端必须适配 **PC与移动端**（响应式设计，最小宽度320px）。
- 整个系统必须可 **Docker一键部署**。

------

## 3. 功能模块与对应API需求

### 模块A：干支基础查询

| 功能点       | API端点                                  | 方法 | 说明                                                         |
| :----------- | :--------------------------------------- | :--- | :----------------------------------------------------------- |
| 干支模糊搜索 | `/api/ganzhi/search?q={keyword}`         | GET  | 输入任意文字，返回匹配的干支列表（支持天干、地支、干支组合） |
| 单柱干支详情 | `/api/ganzhi/{ganzhi}`                   | GET  | 干支标准名称（如“甲子”），返回完整信息（纳音、象意、神煞、喜忌、关系等） |
| 多柱对比     | `/api/ganzhi/compare?list={gz1,gz2,...}` | GET  | 返回指定干支列表的对比数据（并排展示各字段）                 |

### 模块B：纳音专题

| 功能点        | API端点                          | 方法 | 说明                                                  |
| :------------ | :------------------------------- | :--- | :---------------------------------------------------- |
| 按干支查纳音  | `/api/nayin/by-ganzhi/{ganzhi}`  | GET  | 返回纳音名称、五行、状态、盛大/小弱等                 |
| 按纳音查干支  | `/api/nayin/{nayin_name}/ganzhi` | GET  | 返回属于该纳音的所有干支列表                          |
| 纳音状态列表  | `/api/nayin/status`              | GET  | 返回所有十二长生状态列表                              |
| 按状态查纳音  | `/api/nayin/status/{status}`     | GET  | 返回处于该状态的干支列表                              |
| 盛大/小弱分类 | `/api/nayin/category/{category}` | GET  | category = `shengda` 或 `xiaoruo`，返回对应纳音及干支 |
| 纳音推算演示  | `/api/nayin/calc/{ganzhi}`       | GET  | 返回该干支纳音的三种推算步骤（文本+数值）             |

### 模块C：神煞字典

| 功能点       | API端点                        | 方法 | 说明                                           |
| :----------- | :----------------------------- | :--- | :--------------------------------------------- |
| 神煞列表     | `/api/shensha`                 | GET  | 支持分页、按名称模糊搜索                       |
| 神煞详情     | `/api/shensha/{shensha_name}`  | GET  | 返回定义、查法、自带干支、吉凶、原文、现代解读 |
| 干支自带神煞 | `/api/ganzhi/{ganzhi}/shensha` | GET  | 返回该干支自带的所有神煞列表（含字形神煞）     |
| 字形神煞规则 | `/api/shensha/zixing`          | GET  | 返回字形与神煞的映射规则（前端可据此高亮）     |

### 模块D：干支关系图谱

| 功能点       | API端点                       | 方法 | 说明                                                         |
| :----------- | :---------------------------- | :--- | :----------------------------------------------------------- |
| 全部关系数据 | `/api/guanxi/all`             | GET  | 返回所有干支节点及关系边，供图谱渲染                         |
| 单干支关系   | `/api/ganzhi/{ganzhi}/guanxi` | GET  | 返回与该干支有合、冲、刑、害等关系的所有干支及关系类型       |
| 关系类型列表 | `/api/guanxi/types`           | GET  | 返回所有关系类型枚举（六合、三合、半合、六冲、六害、三刑、自刑、同位、隔八生子） |

### 模块E：管理员后台

| 功能点     | API端点              | 方法                | 说明                                   |
| :--------- | :------------------- | :------------------ | :------------------------------------- |
| 管理员登录 | `/api/admin/login`   | POST                | 简单JWT认证（Phase 1可简化，预设账户） |
| 干支管理   | `/api/admin/ganzhi`  | GET/POST/PUT/DELETE | 增删改查干支基础信息                   |
| 纳音管理   | `/api/admin/nayin`   | GET/POST/PUT/DELETE | 增删改查纳音信息                       |
| 象意管理   | `/api/admin/xiangyi` | GET/POST/PUT/DELETE | 增删改查象意条目（支持批量导入）       |
| 神煞管理   | `/api/admin/shensha` | GET/POST/PUT/DELETE | 增删改查神煞                           |
| 喜忌管理   | `/api/admin/xiji`    | GET/POST/PUT/DELETE | 增删改查喜忌                           |
| 关系管理   | `/api/admin/guanxi`  | GET/POST/PUT/DELETE | 增删改查干支关系                       |
| 数据导入   | `/api/admin/import`  | POST                | 接收JSON/CSV文件，批量导入初始数据     |
| 数据导出   | `/api/admin/export`  | GET                 | 导出全库数据为JSON备份                 |

------

## 4. 数据库模型详细设计（SQLAlchemy ORM）

### 4.1 干支表 (ganzhi)

| 字段                | 类型      | 约束             | 说明                                                   |
| :------------------ | :-------- | :--------------- | :----------------------------------------------------- |
| id                  | Integer   | PK               |                                                        |
| tiangan             | String(2) | Not Null         | 天干（甲、乙、丙、丁、戊、己、庚、辛、壬、癸）         |
| dizhi               | String(2) | Not Null         | 地支（子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥） |
| ganzhi              | String(4) | Unique, Not Null | 完整干支名（如“甲子”）                                 |
| tiangan_wuxing      | String(2) |                  | 天干五行                                               |
| dizhi_wuxing        | String(2) |                  | 地支五行                                               |
| yinyang             | String(2) |                  | 阴阳（阳/阴）                                          |
| fangwei             | String(4) |                  | 方位（东、南、西、北、中、东南、西南等）               |
| jijie               | String(4) |                  | 季节（春、夏、秋、冬、长夏）                           |
| tiangan_yuanshiming | String(8) |                  | 天干原始名（阏逢、旃蒙等）                             |
| dizhi_yuanshiming   | String(8) |                  | 地支原始名（困敦、赤奋若等）                           |
| special_desc        | Text      |                  | 特殊性质描述（如“宝物”“顽矿”）                         |

### 4.2 纳音表 (nayin)

| 字段            | 类型       | 约束          | 说明                                                         |
| :-------------- | :--------- | :------------ | :----------------------------------------------------------- |
| id              | Integer    | PK            |                                                              |
| ganzhi_id       | Integer    | FK(ganzhi.id) | 关联干支                                                     |
| nayin_name      | String(20) |               | 纳音名称（如“海中金”）                                       |
| nayin_wuxing    | String(2)  |               | 纳音五行                                                     |
| zhuangtai       | String(4)  |               | 十二长生状态（长生、沐浴、冠带、临官、帝旺、衰、病、死、墓、绝、胎、养） |
| shengda_xiaoruo | String(4)  |               | 盛大/小弱分类（盛大/小弱）                                   |
| zhuangtai_desc  | Text       |               | 状态描述（原文+现代解读）                                    |

### 4.3 象意表 (xiangyi)

| 字段        | 类型        | 约束          | 说明                                                         |
| :---------- | :---------- | :------------ | :----------------------------------------------------------- |
| id          | Integer     | PK            |                                                              |
| ganzhi_id   | Integer     | FK(ganzhi.id) | 关联干支                                                     |
| type        | String(10)  |               | 象意类型：核心、细分、组合                                   |
| category    | String(20)  |               | 细分类别：天文气象、地理建筑、人物伦常、性情、身体、事物、植物、器物（细分象意专用） |
| content     | String(100) |               | 象意文本（如“长子”）                                         |
| description | Text        |               | 简短解释                                                     |
| source      | String(10)  |               | 来源：原文/推理                                              |
| confidence  | Float       |               | 置信度（0-1），仅推理象意                                    |

### 4.4 神煞表 (shensha)

| 字段         | 类型       | 约束   | 说明                       |
| :----------- | :--------- | :----- | :------------------------- |
| id           | Integer    | PK     |                            |
| name         | String(30) | Unique | 神煞名称（如“进神”“悬针”） |
| type         | String(10) |        | 类型：字形神煞/组合神煞    |
| check_method | Text       |        | 查法描述                   |
| jixiong      | String(4)  |        | 吉凶属性（吉/凶/平）       |
| yuanwen      | Text       |        | 原文摘录                   |
| modern_desc  | Text       |        | 现代解读                   |
| remark       | Text       |        | 备注                       |

### 4.5 干支-神煞关联表 (ganzhi_shensha)

| 字段       | 类型    | 约束           | 说明                             |
| :--------- | :------ | :------------- | :------------------------------- |
| id         | Integer | PK             |                                  |
| ganzhi_id  | Integer | FK(ganzhi.id)  |                                  |
| shensha_id | Integer | FK(shensha.id) |                                  |
| is_zixing  | Boolean |                | 是否为字形自动生成（True/False） |

### 4.6 喜忌表 (xiji)

| 字段         | 类型       | 约束          | 说明                       |
| :----------- | :--------- | :------------ | :------------------------- |
| id           | Integer    | PK            |                            |
| ganzhi_id    | Integer    | FK(ganzhi.id) |                            |
| type         | String(4)  |               | 喜/忌                      |
| target_type  | String(10) |               | 对象类型：五行、季节、地支 |
| target_value | String(20) |               | 具体对象（如“木”“春”“寅”） |
| remark       | Text       |               | 备注                       |

### 4.7 干支关系表 (guanxi)

| 字段          | 类型       | 约束 | 说明                                                     |
| :------------ | :--------- | :--- | :------------------------------------------------------- |
| id            | Integer    | PK   |                                                          |
| ganzhi1       | String(4)  |      | 干支1（直接存字符串，简化查询）                          |
| ganzhi2       | String(4)  |      | 干支2                                                    |
| relation_type | String(20) |      | 六合、三合、半合、六冲、六害、三刑、自刑、同位、隔八生子 |
| remark        | Text       |      | 备注                                                     |

------

## 5. 前端页面与组件规划

| 路由路径                | 页面名称   | 主要组件                                                     | 说明                         |
| :---------------------- | :--------- | :----------------------------------------------------------- | :--------------------------- |
| `/`                     | 首页       | SearchBar, HotGanzhiCards, QuickEntry                        | 全局搜索、热门干支、快速入口 |
| `/ganzhi/:ganzhi`       | 干支详情页 | GanzhiHeader, NayinCard, XiangyiTabs, ShenshaList, XijiList, GuanxiTable, CompareButton | 核心页面                     |
| `/compare`              | 对比中心   | CompareSelector, CompareTable, ExportButton                  | 多柱对比                     |
| `/nayin`                | 纳音专题页 | NayinCategoryNav, NayinList, NayinDetail                     | 纳音分类与详情               |
| `/nayin/status/:status` | 纳音状态页 | NayinStatusList, StatusDescCard                              | 按状态查看干支               |
| `/shensha`              | 神煞字典   | ShenshaIndex, ShenshaSearch, ShenshaDetail                   | 神煞列表与详情               |
| `/guanxi`               | 关系图谱页 | GraphCanvas, FilterToolbar, SearchNode                       | 图谱可视化                   |
| `/admin`                | 管理后台   | LoginForm, Dashboard, DataTables                             | 管理员入口                   |

------

## 6. 部署架构

### 6.1 开发环境

- 后端：`uvicorn main:app --reload` 监听 `8000` 端口
- 前端：`vite` 开发服务器，监听 `5173` 端口，代理API到后端

### 6.2 生产环境（Docker）

**方案一：单容器一体化**

- 基于 `python:3.11-slim` 构建镜像，包含：
  - 编译好的前端静态文件（放在 `static` 目录）
  - FastAPI 后端应用
  - SQLite 数据库文件（挂载卷持久化）
- 启动命令：`uvicorn main:app --host 0.0.0.0 --port 80`
- 前端通过同域 `/api` 访问后端

**方案二：双容器（推荐）**

- **backend**：FastAPI应用 + SQLite（挂载卷）
- **frontend**：Nginx 容器，提供静态文件，反向代理 `/api` 到 backend
- 使用 `docker-compose` 编排

### 6.3 数据持久化

- SQLite 数据库文件应存放在**命名卷**或**绑定挂载目录**中，避免容器销毁后数据丢失。
- 初始数据可通过 `init_db.py` 脚本在首次启动时自动导入。