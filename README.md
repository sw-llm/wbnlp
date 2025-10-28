基于Flask的微博舆情NLP分析系统

这是一个基于 Python Flask 框架的微博舆情分析与可视化平台。项目通过爬虫采集微博数据，使用 jieba 和 snownlp 进行自然语言处理，并最终通过 ECharts 在Web前端进行多维度的数据可视化。

✨ 主要功能

主页仪表盘：实时展示7日发帖趋势、帖子分类占比、热门评论用户词云等核心指标。

情感分析：对微博帖子、评论及热词进行情感倾向分析（正面、中性、负面）。

热词分析：展示热词排行榜、热词情感趋势，并可回溯相关评论。

IP地理分析：以地图形式展示发帖和评论用户的地域分布。

数据统计：多维度分析帖子的转评赞数据分布。

词云生成：动态生成微博文章、评论及热门用户的词云图。

用户认证：包含基本的用户登录与注册功能。

🚀 技术栈

后端：Flask, PyMySQL

数据处理：Pandas, Jieba (中文分词)

NLP分析：SnowNLP (情感分析)

可视化：ECharts, WordCloud

数据库：MySQL

🛠️ 如何运行

1. 环境准备

安装 Python 3.x

安装 MySQL 数据库

2. 克隆与安装依赖

# 1. 克隆项目
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd weiboNlpProject2

# 2. (推荐) 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖包
pip install -r requirements.txt


3. 配置数据库

在您的 MySQL 中创建一个新数据库，例如 weibo_nlp。

打开 util/dbUtil.py 文件。

修改 getCon() 函数中的数据库连接配置（host, user, password, db）。

（手动）根据项目需要创建表（例如 t_user, t_article, t_comment 等）。

4. 运行数据管线

警告: spider 目录下的爬虫（article_spider.py）依赖硬编码的个人Cookie，目前版本可能已失效，需要您自行更新Cookie才能运行。

# 1. (可选) 运行爬虫获取数据 (需要先配置Cookie)
# python spider/main.py  (或者单独运行 article_spider.py, comment_spider.py)

# 2. 运行NLP处理脚本，生成词频文件 (此步骤依赖爬虫生成的CSV)
python fenci/articleFenci.py
python fenci/commentFenci.py

# 3. (推荐) 将CSV数据导入数据库
# (您需要编写或运行一个导入脚本，例如上一轮我们讨论的 `hotwordDao.py`)


5. 启动Web应用

python app.py


应用将默认运行在 http://127.0.0.1:5000/。

📁 项目结构

weiboNlpProject2/
├── app.py             # Flask 应用主入口，包含蓝图注册和鉴权
├── requirements.txt   # 项目依赖
├── dao/               # 数据访问对象 (Data Access Object)，封装所有数据库操作
├── entity/            # 实体类 (数据模型)
├── fenci/             # NLP分词和词频统计脚本
│   ├── articleFenci.py
│   ├── commentFenci.py
│   └── stopWords.txt    # 停用词表
├── nlp/               # NLP 测试脚本 (如 snowNLPTest.py)
├── spider/            # 爬虫模块
│   ├── article_spider.py
│   └── comment_spider.py
├── static/            # 静态文件 (CSS, JS, Images)
│   ├── js/echarts.min.js
│   └── ...
├── templates/         # Flask 的 HTML 模板 (已废弃，被 view/page/templates 替代)
├── util/              # 工具类
│   ├── dbUtil.py      # 数据库连接工具
│   ├── wordcloudUtil.py # 词云生成工具
│   └── ...
├── view/              # 视图模块 (Flask 蓝图)
│   ├── page/            # 核心分析页面的后端逻辑和模板
│   │   ├── page.py      # 路由
│   │   └── templates/   # 页面HTML
│   └── user/            # 用户登录/注册的后端逻辑和模板
│       ├── user.py
│       └── templates/
└── wordcloud/         # 词云相关的字体、遮罩图片和测试脚本
