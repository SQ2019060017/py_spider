import os
import requests
from pyquery import PyQuery as pq

"""
存图
"""


class Model():
    """
    基类, 用来显示类的信息
    """

    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """

    def __init__(self):
        self.name = ''
        self.other = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def get(url, filename):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    # 电影名称
    m.name = e('.img_box').attr('alt')
    # 电影评分
    m.other = e('.c_fff').text()
    if m.other == '':
        m.other = e('.c_blue').text()
    m.score = e('.total').text() + e('.total2').text()
    # 电影简介
    m.quote = e('.mt3').text()
    # 电影海报
    m.cover_url = e('.img_box').attr('src')
    # 电影排名
    m.ranking = e('.number').text()
    return m


def save_cover(movies):
    for m in movies:
        filename = '{}.jpg'.format(m.ranking)
        get(m.cover_url, filename)


def cached_page(url):
    link = url.split('-', 1)
    if len(link) == 1:
        filename = '1.html'
    else:
        filename = '{}'.format(url.split('-', 1)[-1])
    page = get(url, filename)
    return page


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    # https://movie.douban.com/top250?start=100
    page = cached_page(url)
    e = pq(page)
    items = e('.top_list li')
    # 调用 movie_from_div 
    movies = [movie_from_div(i) for i in items]
    save_cover(movies)
    return movies


def main():
    for i in range(0, 10):
        if i == 0:
            url = 'http://www.mtime.com/top/movie/top100/'
        else:
            url = 'http://www.mtime.com/top/movie/top100/index-{}.html'.format(i + 1)

        movies = movies_from_url(url)
        print('top100 movies, {}'.format(i), movies)


if __name__ == '__main__':
    main()
