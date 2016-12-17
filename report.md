最近莫名其妙的迷上了SNH 48，刚好最近放假无事可做，于是打算用爬虫在SNH 48的官网上爬取数据（总觉得有些羞耻）<br>

###工具选择
大二的时候在统计课上用java的jsoup爬过Amazon上的商品数据，不过时隔3年多已经忘得差不多了，加上现在大家都在说python多么方便之类的，于是这次我打算尝试使用python来进行这次爬取.<br>
一开始打算使用python原生库`urllib2`来进行爬取，但是一上来就倒在了正则表达式的丛林之中，之后我开始寻找方便进行网页内容抓取的框架，然后就找到了一款不错的框架[scrapy](http://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html)。Scrapy使用了一种基于 XPath 和 CSS 表达式机制: Scrapy Selectors 。 <br>

###爬取过程
首先在命令行中输入
```Bash
scrapy startproject tutorial
```
创建一个名叫“tutorial”的项目
####选择网站
所有成员的基本信息都列在http://www.snh48.com/member_list.php 中，点击每个成员的图片可以进入到该成员的详细资料页面。
####定义数据
`Item` 对象是自定义的python字典。 您可以使用标准的字典语法来获取到其每个字段的值。(字段即是我们之前用Field赋值的属性):
我们需要每个成员的信息如下：
* id
* 姓名
* 昵称 
* 身高
* 血型
* 所属队伍（目前SNH48本部一共有5支队伍，分别为Team SII, Team NII, Team HII, Team X, Team XII）
* 批次（SNH48目前共有七期团员）
* 生日（这个官网上只给出了月和日（毕竟女生的年龄是隐私……），所以这个只能手动扒了）
* 入团时间
* 个人详细信息页面链接
* 公式照链接
* 爱好
* 简介

Item的代码在[这里](https://github.com/billjyc/SNH48-member/blob/master/tutorial/items.py)
####编写抓取数据的spider
[spider代码](https://github.com/billjyc/SNH48-member/blob/master/tutorial/spiders/dmoz_spider.py)
####与MySQL的交互
pipeline的代码在[这里](https://github.com/billjyc/SNH48-member/blob/master/tutorial/pipelines.py)
####执行
在命令行中输入
```Bash
scrapy crawl snh48
```
即可得到结果


###结果分析
* 经过爬取，数据库中共有109条记录，说明SNH 48本部共有109位成员（包含被标记为“暂休”的几位成员）
* 各队的平均身高如下：
<table>
<tr>
<th>Team</th>
<th>平均身高(cm)</th>
</tr>
<tr>
<td>Team SII</td>
<td>163.85</td>
</tr>
<tr>
<td>Team NII</td>
<td>165.64</td>
</tr>
<tr>
<td>Team HII</td>
<td>165.33</td>
</tr>
<tr>
<td>Team X</td>
<td>165.56</td>
</tr>
<tr>
<td>Team XII</td>
<td>163.00</td>
</tr>
</table>
<br>
果然，team SII的身高排名毫无悬念地排名第一，这跟大家口中“人高马大”的前辈的印象较符合；而N队和XII队身高较矮。
