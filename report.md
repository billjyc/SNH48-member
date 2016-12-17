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
<td>165.64</td>
</tr>
<tr>
<td>Team NII</td>
<td>163.85</td>
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
果然，team SII的身高排名毫无悬念地排名第一，这跟大家口中“人高马大”的前辈的印象较符合；而N队和XII队身高较矮。
* 各团的身高极值<br>
  * 各团最高
  <table>
<tr>
<th>Team</th>
<th>姓名</th>
<th>身高(cm)</th>
</tr>
<tr>
<td>Team SII</td>
<td>吴哲晗</td>
<td>173</td>
</tr>
<tr>
<td>Team NII</td>
<td>江真仪</td>
<td>170</td>
</tr>
<tr>
<td>Team HII</td>
<td>刘佩鑫</td>
<td>170</td>
</tr>
<tr>
<td>Team X</td>
<td>汪佳翎</td>
<td>172</td>
</tr>
<tr>
<td>Team XII</td>
<td>陈韫灵</td>
<td>173</td>
</tr>
</table>

S队最高的居然是五折吴哲晗？但是从最近的公演来看，徐子轩的身高已经明显超过了五折，可以推断出官网上登记的身高应该是入团时候的身高。。。SB需要经常对成员资料进行更新啊

  * 各团最矮
    <table>
<tr>
<th>Team</th>
<th>姓名</th>
<th>身高(cm)</th>
</tr>
<tr>
<td>Team SII</td>
<td>袁雨桢</td>
<td>160</td>
</tr>
<tr>
<td>Team NII</td>
<td>罗兰</td>
<td>152</td>
</tr>
<tr>
<td>Team HII</td>
<td>杨惠婷，王露皎</td>
<td>160</td>
</tr>
<tr>
<td>Team X</td>
<td>杨韫玉</td>
<td>158</td>
</tr>
<tr>
<td>Team XII</td>
<td>刘增艳</td>
<td>157</td>
</tr>
</table>

余震居然是S队里最矮的，真的没看出来……
* 平均年龄
<table>
<tr>
<th>Team</th>
<th>平均年龄</th>
</tr>
<tr>
<td>Team SII</td>
<td>21.0</td>
</tr>
<tr>
<td>Team NII</td>
<td>21.3</td>
</tr>
<tr>
<td>Team HII</td>
<td>19.9</td>
</tr>
<tr>
<td>Team X</td>
<td>19.0</td>
</tr>
<tr>
<td>Team XII</td>
<td>17.8</td>
</tr>
</table>
S队虽然有一期生在里面，但是也有2-7期生在里面，所以平均年龄不是最大的；但是N队依然是以二期生为主的队伍，尤其是队中几位top成员年龄已经偏大，队伍老化问题有些严重，希望队中的年轻队员可以早日扛起大旗。

 * 各团最老
 <table>
<tr>
<th>Team</th>
<th>姓名</th>
<th>年龄</th>
</tr>
<tr>
<td>Team SII</td>
<td>徐晨辰</td>
<td>26</td>
</tr>
<tr>
<td>Team NII</td>
<td>曾艳芬</td>
<td>25</td>
</tr>
<tr>
<td>Team HII</td>
<td>徐晗</td>
<td>23</td>
</tr>
<tr>
<td>Team X</td>
<td>王晓佳</td>
<td>23</td>
</tr>
<tr>
<td>Team XII</td>
<td>张怡</td>
<td>22</td>
</tr>
</table>
 * 各团最年轻
  <table>
<tr>
<th>Team</th>
<th>姓名</th>
<th>年龄</th>
</tr>
<tr>
<td>Team SII</td>
<td>赵韩倩</td>
<td>16</td>
</tr>
<tr>
<td>Team NII</td>
<td>徐真</td>
<td>15</td>
</tr>
<tr>
<td>Team HII</td>
<td>孙珍妮</td>
<td>16</td>
</tr>
<tr>
<td>Team X</td>
<td>杨冰怡</td>
<td>16</td>
</tr>
<tr>
<td>Team XII</td>
<td>蒋舒婷</td>
<td>14</td>
</tr>
</table>
