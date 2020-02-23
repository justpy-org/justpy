import re, json

chart_def1 = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas are nice', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""

chart_def = """
{
    chart: {
        type: 'spline'
    },
    title: {
        text: 'Monthly Average Temperature'
    },
    subtitle: {
        text: 'Source WorldClimate.com'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    yAxis: {
        title: {
            text: 'Temperature'
        }},
        
    tooltip: {
        crosshairs: true,
        shared: true
    },
    plotOptions: {
        spline: {
            marker: {
                radius: 4,
                lineColor: '#666666',
                lineWidth: 1
            }
        }
    },
    series: [{
        name: 'Tokyo',
        marker: {
            symbol: 'square'
        },
        data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, {
            y: 26.5,
            marker: {
                symbol: 'url(https//www.highcharts.com/samples/graphics/sun.png)'
            }
        }, 23.3, 18.3, 13.9, 9.6]

    }, {
        name: 'London',
        marker: {
            symbol: 'diamond'
        },
        data: [{
            y: 3.9,
            marker: {
                symbol: 'url(https//www.highcharts.com/samples/graphics/snow.png)'
            }
        }, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
    }]
}
"""

chart_def3 = """

"""
my_chart_def = """
{
    chart: {
        type: 'bar'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    legend: {
        layout: 'vertical',
        floating: true,
        backgroundColor: '#FFFFFF',
        align: 'right',
        verticalAlign: 'top',
        y: 60,
        x: -60
    },
    series: [{
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""


item = """
{

    chart: {
        type: 'item'
    },

    title: {
        text: 'Highcharts item chart'
    },

    subtitle: {
        text: 'Parliament visualization'
    },

    legend: {
        labelFormat: '{name} <span style="opacity: 0.4">{y}</span>'
    },

    series: [{
        name: 'Representatives',
        keys: ['name', 'y', 'color', 'label'],
        data: [
            ['The Left', 69, '#BE3075', 'DIE LINKE'],
            ['Social Democratic Party', 153, '#EB001F', 'SPD'],
            ['Alliance 90/The Greens', 67, '#64A12D', 'GRÜNE'],
            ['Free Democratic Party', 80, '#FFED00', 'FDP'],
            ['Christian Democratic Union', 200, '#000000', 'CDU'],
            ['Christian Social Union in Bavaria', 46, '#008AC5', 'CSU'],
            ['Alternative for Germany', 94, '#009EE0', 'AfD']
        ],
        dataLabels: {
            enabled: true,
            format: '{point.label}'
        },

        // Circular options
        center: ['50%', '88%'],
        size: '170%',
        startAngle: -100,
        endAngle: 100
    }]
}
"""
def strip_white_spaces(s):
    s_list = s.split("'")
    for i, item in enumerate(s_list):
        if not i % 2:
            s_list[i] = re.sub("\s+", "", item)
    return "'".join(s_list)


def create_dict_for_colons(s):
    d = {}
    handle_flag = True
    for i, c in enumerate(s):
        if c==':':
            d[i] = handle_flag
        elif c=='"':
            handle_flag = not handle_flag
    return d


def string_to_json(chart_def):
    s = strip_white_spaces(chart_def.replace('\n', ' ').encode("ascii", "ignore").decode('utf-8'))
    s = s.replace('"', '|||')
    s = s.replace("'", '"')
    d = create_dict_for_colons(s)
    ns = []
    print(s)
    pos = 0
    inserted_chars = 0
    for i, c in enumerate(s):
        ns.append(c)
        # if c==':' and s[i-1] not in ['"', "'"]:
        if c==':' and d[i]:
            pos = i
            # raise error if pos is 0
            while s[pos] not in [',', '{', '(', '[']:
                pos -= 1
            ns.insert(pos + 1 + inserted_chars, '"')
            inserted_chars += 1
            ns.insert(i + inserted_chars, '"')
            inserted_chars += 1
    print('The result:')
    print(ns)
    print(''.join(ns))
    result = ''.join(ns).replace('|||', "'")
    print(result)
    result = json.loads(result)
    print(result)
    return result


test_string = "{hello1: 'you', hello2: 'you', hello3: 'you'}"
test_string1 = "{hello1: 'yo {}{:u', hello2: '{:you', hello3: 'you:}'}"
string_to_json(test_string)
print('-----')
string_to_json(chart_def1)
print('-----')
string_to_json(chart_def)
print('-----')
string_to_json(my_chart_def)
print('-----')
string_to_json(test_string1)
print('-----')
string_to_json(item)

# print(create_dict_for_colons('{hello: "you:"}'))
