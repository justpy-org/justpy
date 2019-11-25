import justpy as jp


chart_def = """
 {
  chart: {
    type: 'bubble',
    zoomType: 'xy'
  },
  title: {
    text: 'Productivity vs Hours Worked vs GDP in 2014'
  },
  subtitle: {
    useHTML: true,
    text: 'Source: <a href="http://www.rug.nl/ggdc/productivity/pwt/">University of Groningen</a>'
  },
  yAxis: {
    title: {
      text: 'Annual working hours per worker'
    },
    labels:{
    format:'{value}h'
    }
  },
  xAxis: {
    title: {
      text: 'Productivity (Output in PPP-adjusted $ per hour worked)'
    },
        labels:{
    format:'{value}$'
    }
  },
  tooltip: {
    useHTML: true,
    headerFormat: null,
    pointFormat: '<b>Country</b>: {point.name}<br><b>Productivity</b>: {point.x}$<br/><b>Annual working hours</b>: {point.y}h <br/><b>GDP per capita</b>: {point.z}$  ',
 },
  legend: {
    enabled: false
  },
    plotOptions: {
        bubble: {
            dataLabels: {
                enabled: true,
                format:'{point.iso3}'
            },
        }
    },
  series: [{
    data: [
 {x:59.06,y:1501.71,z:93829.97,name:'Luxembourg',color:'#c5e1a5',iso3:'LUX'},
{x:47.56,y:2262.53,z:80305.45,name:'Singapore',color:'#c5e1a5',iso3:'SGP'},
{x:102.79,y:1426.87,z:63286.69,name:'Norway',color:'#c5e1a5',iso3:'NOR'},
{x:65.42,y:1568,z:56680.44,name:'Switzerland',color:'#c5e1a5',iso3:'CHE'},
{x:63.36,y:1764.6,z:51830.99,name:'United States',color:'#c5e1a5',iso3:'USA'},
{x:71.98,y:1821.26,z:48885.62,name:'Ireland',color:'#c5e1a5',iso3:'IRL'},
{x:65.48,y:1419.59,z:45668.44,name:'Netherlands',color:'#c5e1a5',iso3:'NLD'},
{x:62.14,y:1438.4,z:45082.15,name:'Denmark',color:'#c5e1a5',iso3:'DNK'},
{x:54.09,y:1608.52,z:44167.63,name:'Sweden',color:'#c5e1a5',iso3:'SWE'},
{x:54.04,y:1629.37,z:44122.65,name:'Austria',color:'#c5e1a5',iso3:'AUT'},
{x:64.43,y:1371.1,z:43417.73,name:'Germany',color:'#c5e1a5',iso3:'DEU'},
{x:48.44,y:1803.06,z:43395.57,name:'Australia',color:'#c5e1a5',iso3:'AUS'},
{x:48.57,y:1687.78,z:42946.36,name:'Canada',color:'#c5e1a5',iso3:'CAN'},
{x:38.02,y:1864,z:41424.44,name:'Iceland',color:'#c5e1a5',iso3:'ISL'},
{x:58.11,y:1575.28,z:41355.16,name:'Belgium',color:'#c5e1a5',iso3:'BEL'},
{x:49.23,y:1642.51,z:39017.54,name:'Finland',color:'#fff59d',iso3:'FIN'},
{x:48.07,y:1675.11,z:37983.13,name:'United Kingdom',color:'#fff59d',iso3:'GBR'},
{x:63.51,y:1473.46,z:37531.43,name:'France',color:'#fff59d',iso3:'FRA'},
{x:40.14,y:1729,z:37322.85,name:'Japan',color:'#fff59d',iso3:'JPN'},
{x:36.75,y:1762,z:34468.77,name:'New Zealand',color:'#fff59d',iso3:'NZL'},
{x:51.65,y:1733.92,z:33945.84,name:'Italy',color:'#fff59d',iso3:'ITA'},
{x:31.53,y:2124,z:33425.69,name:'South Korea',color:'#fff59d',iso3:'KOR'},
{x:26.93,y:1961.68,z:32340.93,name:'Malta',color:'#fff59d',iso3:'MLT'},
{x:33.98,y:1880.28,z:31812.63,name:'Israel',color:'#fff59d',iso3:'ISR'},
{x:39.12,y:1583.31,z:31595.56,name:'Trinidad and Tobago',color:'#fff59d',iso3:'TTO'},
{x:51.1,y:1688.79,z:31193.33,name:'Spain',color:'#fff59d',iso3:'ESP'},
{x:41.59,y:1826.8,z:29711.13,name:'Cyprus',color:'#ffcc80',iso3:'CYP'},
{x:34.29,y:1770.69,z:29119.62,name:'Czech Republic',color:'#ffcc80',iso3:'CZE'},
{x:38.12,y:1560.65,z:28459.91,name:'Slovenia',color:'#ffcc80',iso3:'SVN'},
{x:35.05,y:1763.21,z:27237.62,name:'Slovakia',color:'#ffcc80',iso3:'SVK'},
{x:29.09,y:1859.43,z:26957.24,name:'Estonia',color:'#ffcc80',iso3:'EST'},
{x:36.94,y:1833.53,z:26251.37,name:'Lithuania',color:'#ffcc80',iso3:'LTU'},
{x:34.9,y:1856.9,z:26023.67,name:'Portugal',color:'#ffcc80',iso3:'PRT'},
{x:24.18,y:1985,z:24880.08,name:'Russia',color:'#ffcc80',iso3:'RUS'},
{x:29.24,y:2039.28,z:24346.21,name:'Poland',color:'#ffcc80',iso3:'POL'},
{x:20.73,y:2267.6,z:24195.9,name:'Malaysia',color:'#ffcc80',iso3:'MYS'},
{x:29.09,y:1859.83,z:24016.3,name:'Hungary',color:'#ffcc80',iso3:'HUN'},
{x:33.35,y:2041.67,z:23989.14,name:'Greece',color:'#ffcc80',iso3:'GRC'},
{x:33.78,y:1832,z:22401.88,name:'Turkey',color:'#ffcc80',iso3:'TUR'},
{x:28.69,y:1938.48,z:22265.46,name:'Latvia',color:'#ffcc80',iso3:'LVA'},
{x:24.42,y:1990,z:22226.45,name:'Chile',color:'#ffcc80',iso3:'CHL'},
{x:25.63,y:1592.57,z:19827.56,name:'Uruguay',color:'#ef9a9a',iso3:'URY'},
{x:27.93,y:1816.5,z:19666.95,name:'Romania',color:'#ef9a9a',iso3:'ROU'},
{x:26.84,y:1776.66,z:18797.55,name:'Argentina',color:'#ef9a9a',iso3:'ARG'},
{x:17.71,y:2136.77,z:16459.06,name:'Mexico',color:'#ef9a9a',iso3:'MEX'},
{x:20.78,y:1644.06,z:16302.22,name:'Bulgaria',color:'#ef9a9a',iso3:'BGR'},
{x:16.84,y:1711.28,z:15371,name:'Brazil',color:'#ef9a9a',iso3:'BRA'},
{x:14.02,y:1672.28,z:15297.58,name:'Barbados',color:'#ef9a9a',iso3:'BRB'},
{x:10.46,y:2284.38,z:14853.46,name:'Thailand',color:'#ef9a9a',iso3:'THA'},
{x:12.37,y:2216,z:14392.04,name:'Costa Rica',color:'#ef9a9a',iso3:'CRI'},
{x:39.17,y:2234.5,z:12758.65,name:'China',color:'#ef9a9a',iso3:'CHN'},
{x:14.12,y:1771.65,z:12715.97,name:'Colombia',color:'#ef9a9a',iso3:'COL'},
{x:16.1,y:2215.2,z:12462.03,name:'South Africa',color:'#ef9a9a',iso3:'ZAF'},
{x:12.84,y:1790.29,z:11545.39,name:'Peru',color:'#ef9a9a',iso3:'PER'},
{x:13.8,y:2085.71,z:10922.83,name:'Ecuador',color:'#ef9a9a',iso3:'ECU'},
{x:15.44,y:2075.5,z:10650.39,name:'Sri Lanka',color:'#ef9a9a',iso3:'LKA'},
{x:12.98,y:1878.48,z:10522.37,name:'Saint Lucia',color:'#ef9a9a',iso3:'LCA'},
{x:10.88,y:2026.5,z:10003.09,name:'Indonesia',color:'#ef9a9a',iso3:'IDN'},
{x:10.13,y:1867.89,z:8053.05,name:'Jamaica',color:'#ef9a9a',iso3:'JAM'},
{x:12.45,y:1842,z:7971.12,name:'Armenia',color:'#ef9a9a',iso3:'ARM'},
{x:8.9,y:2115.29,z:6585.9,name:'Philippines',color:'#ef9a9a',iso3:'PHL'},
{x:6.4,y:2162.3,z:5389.9,name:'India',color:'#ef9a9a',iso3:'IND'},
{x:4.15,y:2339.95,z:5370.21,name:'Vietnam',color:'#ef9a9a',iso3:'VNM'},
{x:7.02,y:2282.6,z:4576.23,name:'Pakistan',color:'#ef9a9a',iso3:'PAK'},
{x:2.05,y:2510.41,z:3124.32,name:'Cambodia',color:'#ef9a9a',iso3:'KHM'},
{x:3.31,y:2371.81,z:2973.04,name:'Bangladesh',color:'#ef9a9a',iso3:'BGD'},
    ]
  }]
}
"""


def chart_test():
    wp = jp.WebPage()
    chart = jp.HighCharts(options=chart_def, a=wp, style='min-width: 310px; height: 500px; margin: 0 auto')
    return wp

jp.justpy(chart_test)
