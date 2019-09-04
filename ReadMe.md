# Spider 高效爬虫实践



## 操作演示

- 爬取豆瓣 Top250 电影榜单并将爬虫数据可视化输出
  ![douban_top250](pictures/douban_top250.gif)

- 模拟浏览器行为爬取知乎动态页面
  ![zhihu_bybrowser](pictures/zhihu_bybrowser.gif)

- 数据输出一：电影评分分布图
  ![movies_of_the_same_rating](pictures/movies_of_the_same_rating.png)

- 数据输出二：榜单中电影数量前十大国家统计
  ![top10_country](pictures/top10_country.png)
  

## 功能

- 创建 Model 类，用于存放爬虫数据, 方便后续代码高效利用

- 自动爬取多页面
- 自动下载页面，提升效率及可靠性
- 浏览器翻页、下拉行为模拟，爬取动态页面
- 利用真实 cookie 通过身份验证, 爬取保护内容
- 利用 pyecharts 对爬虫数据进行可视化处理

 

## 使用方法

 

- 豆瓣 Top 250 Movies: 
  - 执行 douban.py
  - 运行结束后自动生成 douban.html; douban_bars.html; douban_radius.html 可在浏览器中查看
- 知乎浏览器行为模拟爬虫: 
  - 创建 serect.py 于根目录, 在浏览器中复制个人知乎账号的cookie，存放入 serect.py
    - 格式为: cookie = 'k=v;k=v;...'
    - cookie 需要去掉 _xsrf _zap tgw_l7_route 这三项
  - 执行 zhihu_bycookie.py 或zhihu_bybrowser.py
  - 无头浏览器模式可将 **# o.add_argument("--headless")** 取消注释再执行