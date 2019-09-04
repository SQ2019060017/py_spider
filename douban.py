import collections
import os
import requests
# from pandas.tests.groupby.test_value_counts import df
from pyquery import PyQuery as pq
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts

from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Scatter, Bar, Map, Pie

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
    m.name = e('.title').text()
    m.other = e('.other').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()

    director_lead, year_country_category = str(e('.bd').find('p').html()).split('<br/>')

    m.director = director_lead.split('导演: ')[1].split('主演')[0].split(' / ')[0]

    if '主演: ' in director_lead:

        m.lead = director_lead.split('主演: ')[1].split('...')[0].split('/')[0]

    raw_ycc = year_country_category.split('\xa0/\xa0')

    m.year = raw_ycc[0].split(' ')[-1]

    m.country = raw_ycc[1].split(' ')[0]

    m.category = raw_ycc[2].split('\n')[0]

    return m


def save_cover(movies):
    for m in movies:
        filename = '{}.jpg'.format(m.ranking)
        get(m.cover_url, filename)


def cached_page(url):
    filename = '{}.html'.format(url.split('=', 1)[-1])
    page = get(url, filename)
    return page


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    # https://movie.douban.com/top250?start=100
    page = cached_page(url)
    e = pq(page)
    items = e('.item')
    # 调用 movie_from_div 
    movies = [movie_from_div(i) for i in items]
    save_cover(movies)
    return movies


def table_base(Movies) -> Table:
    table = Table()
    headers = ['name', 'score', 'quote', 'cover_url', 'ranking', 'country']
    rows = []
    for movie in Movies:
        info = [movie.name, movie.score, movie.quote, movie.cover_url, movie.ranking, movie.country]
        rows.append(info)
        table.add(headers, rows).set_global_opts(
            title_opts=ComponentTitleOpts(title='多页爬虫', subtitle='利用URL自动爬取下一页')
        )
    table.render('douban.html')
    return table


def bar_base(Movies) -> Bar:
    scores = []
    score_class = []
    values = []
    for movie in Movies:
        scores.append(eval(movie.score))
        if eval(movie.score) not in score_class:
            score_class.append(eval(movie.score))

    dict = {}
    for key in scores:
        dict[key] = dict.get(key, 0) + 1

    print('score  class', score_class)
    print('dict', dict)
    for i in dict:
        values.append(dict[i])
    print(values)

    c = (
        Bar()
        .add_xaxis(sorted(score_class))

        .add_yaxis('', values)
        .set_global_opts(title_opts=opts.TitleOpts(title="Movie of the same rating"))

    )
    c.render('douban_bars.html')
    return c


def pie_radius(Movies) -> Pie:
    country_class = []
    countries = []
    top10_country = []
    top10_num = []
    for movie in Movies:
        countries.append(movie.country)
        if movie.country not in country_class:
            country_class.append(movie.country)

    dict = {}
    for key in countries:
        dict[key] = dict.get(key, 0) + 1

    dict_sorted = sorted(dict.items(), key=lambda item:item[1], reverse=True)
    print(dict_sorted)

    for i in range(10):
        top10_country.append(dict_sorted[i][0])
        top10_num.append(dict_sorted[i][1])

    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip(top10_country, top10_num)],
            radius=["40%", "75%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Top 10 Country"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            ),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    c.render('douban_radius.html')
    return c


def main():
    Movies = []
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_from_url(url)
        for movie in movies:
            Movies.append(movie)
        print('top250 movies', movies)

    table_base(Movies)
    bar_base(Movies)
    pie_radius(Movies)


if __name__ == '__main__':
    main()
