## Pandas, Charts and Grids Examples

JustPy comes with a [pandas](https://pandas.pydata.org/) [extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) that makes it simple to create charts and grids from pandas data frames.

The charts are created using [Higcharts](https://www.highcharts.com/products/highcharts/) or [Highstock](https://www.highcharts.com/products/highstock/)

#@@ World Happiness Index
JustPy comes with a [pandas](https://pandas.pydata.org/) [extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) that makes it simple to create charts and grids using pandas data frames.

You can try the following program at http://justpy.ogr/happiness or try running it yourself ([getting started](tutorial/getting_started)).

In under 50 lines of code...
```python
import justpy as jp
import pandas as pd

# https://worldhappiness.report/ed/2019/
df = pd.read_csv('http://elimintz.github.io/happiness_report_2019.csv').round(3)


def grid_change(self, msg):
    # Called when grid changes due to sorting or filtering. Chart is updated based on changes
    msg.page.df = jp.read_csv_from_string(msg.data)
    c = msg.page.df.jp.plot('Country', msg.page.cols_to_plot, kind='column', title='World Happiness Ranking',
                    subtitle='Click and drag in the plot area to zoom in. Shift + drag to pan', temp=True)
    c.options.plotOptions.series.stacking = msg.page.stacking
    msg.page.c.options = c.options


def stack_change(self, msg):
    # Called when stacking option is changed.
    msg.page.c.options.plotOptions.series.stacking = self.value
    msg.page.stacking = self.value


def happiness_plot():
    # The request handler, creates a page with the graph and the gird
    wp = jp.QuasarPage()
    wp.stacking = ''
    wp.cols_to_plot = ['Unexplained', 'GDP', 'Social_support', 'Health', 'Freedom', 'Generosity', 'Corruption']
    wp.df = df
    d = jp.Div(classes='q-ma-lg', a=wp)
    bg = jp.QBtnToggle(push=True, glossy=True, toggle_color='primary', value='', a=d, input=stack_change)
    bg.options = [
          {'label': 'No Stacking', 'value': ''},
          {'label': 'Normal', 'value': 'normal'},
          {'label': 'percent', 'value': 'percent'}
        ]
    # Create chart
    c = df.jp.plot('Country', wp.cols_to_plot, kind='column', a=wp, title='World Happiness Ranking',
                   subtitle='Click and drag in the plot area to zoom in. Shift + drag to pan',
                   stacking='', classes='border m-2 p-2 q-ma-lg p-ma-lg')
    # Create grid
    g = df.jp.ag_grid(a=wp)
    for event_name in ['sortChanged', 'filterChanged']:
        g.on(event_name, grid_change)
    wp.c = c
    return wp


jp.justpy(happiness_plot)
```

### Stock Chart

See program run in 

```python
import justpy as jp
import pandas as pd
import datetime


grouping_units = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]

chart_dict = {
    'rangeSelector': {'selected': 1},
    'yAxis': [
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'OHLC'}, 'height': '60%', 'lineWidth': 2, 'resize': {'enabled': True}},
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'Volume'}, 'top': '65%', 'height': '35%', 'offset': 0, 'lineWidth': 2}
    ],
    'tooltip': {'split': True},
    'series': [
        {'type': 'candlestick', 'tooltip': {'valueDecimals': 2}, 'dataGrouping': {'units': grouping_units}},
        {'type': 'column', 'name': 'Volume', 'yAxis': 1, 'dataGrouping': {'units': grouping_units}}
    ]
}

epoch = datetime.datetime(1970, 1, 1)

def convert_date(date_string):
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def stock_test(request):
    wp = jp.WebPage()
    ticker= 'MSFT'
    data = pd.read_csv(f'https://elimintz.github.io/stocks/{ticker}.csv').round(2)
    chart = jp.HighStock(a=wp, options=chart_dict, style='height: 500px; margin: 0.25rem; padding: 0.5rem; border-width: 1px; border-style: solid; width: 80%;')
    chart.options.title.text = f'{ticker} Historical Prices'
    x = list(data['Date'].map(convert_date))
    chart.options.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
    chart.options.series[0].name = ticker
    chart.options.series[1].data = list(zip(x, data['Volume']))
    data.jp.ag_grid(a=wp, style='height: 500px; width: 80%; margin: 0.25rem; ')
    return wp


jp.justpy(stock_test)
```



# adfad

# HELLO
![](https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

**目录 (Table of Contents)**

[TOCM]

[TOC]

# Heading 1
## Heading 2               
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
# Heading 1 link [Heading link](https://github.com/pandao/editor.md "Heading link")
## Heading 2 link [Heading link](https://github.com/pandao/editor.md "Heading link")
### Heading 3 link [Heading link](https://github.com/pandao/editor.md "Heading link")
#### Heading 4 link [Heading link](https://github.com/pandao/editor.md "Heading link") Heading link [Heading link](https://github.com/pandao/editor.md "Heading link")
##### Heading 5 link [Heading link](https://github.com/pandao/editor.md "Heading link")
###### Heading 6 link [Heading link](https://github.com/pandao/editor.md "Heading link")

#### 标题（用底线的形式）Heading (underline)

This is an H1
=============

This is an H2
-------------

### 字符效果和横线等
                
----

~~删除线~~ <s>删除线（开启识别HTML标签时）</s>
*斜体字*      _斜体字_
**粗体**  __粗体__
***粗斜体*** ___粗斜体___

上标：X<sub>2</sub>，下标：O<sup>2</sup>

**缩写(同HTML的abbr标签)**

> 即更长的单词或短语的缩写形式，前提是开启识别HTML标签时，已默认开启

The <abbr title="Hyper Text Markup Language">HTML</abbr> specification is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.

### 引用 Blockquotes

> 引用文本 Blockquotes

引用的行内混合 Blockquotes
                    
> 引用：如果想要插入空白换行`即<br />标签`，在插入处先键入两个以上的空格然后回车即可，[普通链接](http://localhost/)。

### 锚点与链接 Links

[普通链接](http://localhost/)

[普通链接带标题](http://localhost/ "普通链接带标题")

直接链接：<https://github.com>

[锚点链接][anchor-id] 

[anchor-id]: http://www.this-anchor-link.com/

[mailto:test.test@gmail.com](mailto:test.test@gmail.com)

GFM a-tail link @pandao  邮箱地址自动链接 test.test@gmail.com  www@vip.qq.com

> @pandao

### 多语言代码高亮 Codes

#### 行内代码 Inline code

执行命令：`npm install marked`

#### 缩进风格

即缩进四个空格，也做为实现类似 `<pre>` 预格式化文本 ( Preformatted Text ) 的功能。

    <?php
        echo "Hello world!";
    ?>
    
预格式化文本：

    | First Header  | Second Header |
    | ------------- | ------------- |
    | Content Cell  | Content Cell  |
    | Content Cell  | Content Cell  |

#### JS代码　

```javascript
function test() {
	console.log("Hello world!");
}
 
(function(){
    var box = function() {
        return box.fn.init();
    };

    box.prototype = box.fn = {
        init : function(){
            console.log('box.init()');

			return this;
        },

		add : function(str) {
			alert("add", str);

			return this;
		},

		remove : function(str) {
			alert("remove", str);

			return this;
		}
    };
    
    box.fn.init.prototype = box.fn;
    
    window.box =box;
})();

var testBox = box();
testBox.add("jQuery").remove("jQuery");
```

#### HTML 代码 HTML codes

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charest="utf-8" />
        <meta name="keywords" content="Editor.md, Markdown, Editor" />
        <title>Hello world!</title>
        <style type="text/css">
            body{font-size:14px;color:#444;font-family: "Microsoft Yahei", Tahoma, "Hiragino Sans GB", Arial;background:#fff;}
            ul{list-style: none;}
            img{border:none;vertical-align: middle;}
        </style>
    </head>
    <body>
        <h1 class="text-xxl">Hello world!</h1>
        <p class="text-green">Plain text</p>
    </body>
</html>
```

### 图片 Images

Image:

![](https://pandao.github.io/editor.md/examples/images/4.jpg)

> Follow your heart.

![](https://pandao.github.io/editor.md/examples/images/8.jpg)

> 图为：厦门白城沙滩

图片加链接 (Image + Link)：

[![](https://pandao.github.io/editor.md/examples/images/7.jpg)](https://pandao.github.io/editor.md/images/7.jpg "李健首张专辑《似水流年》封面")

> 图为：李健首张专辑《似水流年》封面
                
----

### 列表 Lists

#### 无序列表（减号）Unordered Lists (-)
                
- 列表一
- 列表二
- 列表三
     
#### 无序列表（星号）Unordered Lists (*)

* 列表一
* 列表二
* 列表三

#### 无序列表（加号和嵌套）Unordered Lists (+)
                
+ 列表一
+ 列表二
    + 列表二-1
    + 列表二-2
    + 列表二-3
+ 列表三
    * 列表一
    * 列表二
    * 列表三

#### 有序列表 Ordered Lists (-)
                
1. 第一行
2. 第二行
3. 第三行

#### GFM task list

- [x] GFM task list 1
- [x] GFM task list 2
- [ ] GFM task list 3
    - [ ] GFM task list 3-1
    - [ ] GFM task list 3-2
    - [ ] GFM task list 3-3
- [ ] GFM task list 4
    - [ ] GFM task list 4-1
    - [ ] GFM task list 4-2
                
----
                    
### 绘制表格 Tables

| 项目        | 价格   |  数量  |
| --------   | -----:  | :----:  |
| 计算机      | $1600   |   5     |
| 手机        |   $12   |   12   |
| 管线        |    $1    |  234  |
                    
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell 

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |

| Item      | Value |
| --------- | -----:|
| Computer  | $1600 |
| Phone     |   $12 |
| Pipe      |    $1 |
                
----

#### 特殊符号 HTML Entities Codes

&copy; &  &uml; &trade; &iexcl; &pound;
&amp; &lt; &gt; &yen; &euro; &reg; &plusmn; &para; &sect; &brvbar; &macr; &laquo; &middot; 

X&sup2; Y&sup3; &frac34; &frac14;  &times;  &divide;   &raquo;

18&ordm;C  &quot;  &apos;

[========]

### Emoji表情 :smiley:

> Blockquotes :star:

#### GFM task lists & Emoji & fontAwesome icon emoji & editormd logo emoji :editormd-logo-5x:

- [x] :smiley: @mentions, :smiley: #refs, [links](), **formatting**, and <del>tags</del> supported :editormd-logo:;
- [x] list syntax required (any unordered or ordered list supported) :editormd-logo-3x:;
- [x] [ ] :smiley: this is a complete item :smiley:;
- [ ] []this is an incomplete item [test link](#) :fa-star: @pandao; 
- [ ] [ ]this is an incomplete item :fa-star: :fa-gear:;
    - [ ] :smiley: this is an incomplete item [test link](#) :fa-star: :fa-gear:;
    - [ ] :smiley: this is  :fa-star: :fa-gear: an incomplete item [test link](#);
 
#### 反斜杠 Escape

\*literal asterisks\*

[========]
            
### 科学公式 TeX(KaTeX)

$$E=mc^2$$

行内的公式$$E=mc^2$$行内的公式，行内的$$E=mc^2$$公式。

$$x > y$$

$$\(\sqrt{3x-1}+(1+x)^2\)$$
                    
$$\sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$

多行公式：

```math
\displaystyle
\left( \sum\_{k=1}^n a\_k b\_k \right)^2
\leq
\left( \sum\_{k=1}^n a\_k^2 \right)
\left( \sum\_{k=1}^n b\_k^2 \right)
```

```katex
\displaystyle 
    \frac{1}{
        \Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{
        \frac25 \pi}} = 1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {
        1+\frac{e^{-6\pi}}
        {1+\frac{e^{-8\pi}}
         {1+\cdots} }
        } 
    }
```

```latex
f(x) = \int_{-\infty}^\infty
    \hat f(\xi)\,e^{2 \pi i \xi x}
    \,d\xi
```
### 分页符 Page break

> Print Test: Ctrl + P

[========]

### 绘制流程图 Flowchart

```flow
st=>start: 用户登陆
op=>operation: 登陆操作
cond=>condition: 登陆成功 Yes or No?
e=>end: 进入后台

st->op->cond
cond(yes)->e
cond(no)->op
```

[========]
                    
### 绘制序列图 Sequence Diagram
                    
```seq
Andrew->China: Says Hello 
Note right of China: China thinks\nabout it 
China-->Andrew: How are you? 
Andrew->>China: I am good thanks!
```

### End