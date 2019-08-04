# PhotoCrawlerWeb
基于Django微博照片爬取和识别的网站

本项目基于Requests框架，
开发一个对社交网站的照片爬取与识别的软件，
面向的是有想在社交网站查看特定照片需求的用户群体，
目的是让用户获取某一社交用户的所有照片，
并通过已知照片人像进行识别。

本照片爬取及识别的软件采用Requests库作为网络爬虫库来获取数据源，
采用selenium模拟登录微博，采用re库进行正则识别，
使用threading库进行多线程开发，
采用Django框架架构开发应用，
前端采用Bootstrap的开源工具库作为前端框架，
后端开发采用Python，数据存储在SQLite数据库中，
并通过ORM将数据表映射成对象操作数据库。

环境：
- python3.7
- 与浏览器版本的匹配的selenium driver
- requests库
- Django2.0
