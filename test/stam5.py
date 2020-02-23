import justpy as jp
import pandas as pd

game_of_thrones = [{
        "season": 1,
        "episode": 1,
        "title": "Winter Is Coming",
        "rating": 9
    },
    {
        "season": 1,
        "episode": 2,
        "title": "The Kingsroad",
        "rating": 8.8
    },
    {
        "season": 1,
        "episode": 3,
        "title": "Lord Snow",
        "rating": 8.7
    },
    {
        "season": 1,
        "episode": 4,
        "title": "Cripples, Bastards, and Broken Things",
        "rating": 8.8
    },
    {
        "season": 1,
        "episode": 5,
        "title": "The Wolf and the Lion",
        "rating": 9.1
    },
    {
        "season": 1,
        "episode": 6,
        "title": "A Golden Crown",
        "rating": 9.2
    },
    {
        "season": 1,
        "episode": 7,
        "title": "You Win or You Die",
        "rating": 9.2
    },
    {
        "season": 1,
        "episode": 8,
        "title": "The Pointy End",
        "rating": 9
    },
    {
        "season": 1,
        "episode": 9,
        "title": "Baelor",
        "rating": 9.6
    },
    {
        "season": 1,
        "episode": 10,
        "title": "Fire and Blood",
        "rating": 9.5
    },
    {
        "season": 2,
        "episode": 1,
        "title": "The North Remembers",
        "rating": 8.8
    },
    {
        "season": 2,
        "episode": 2,
        "title": "The Night Lands",
        "rating": 8.5
    },
    {
        "season": 2,
        "episode": 3,
        "title": "What Is Dead May Never Die",
        "rating": 8.8
    },
    {
        "season": 2,
        "episode": 4,
        "title": "Garden of Bones",
        "rating": 8.8
    },
    {
        "season": 2,
        "episode": 5,
        "title": "The Ghost of Harrenhal",
        "rating": 8.8
    },
    {
        "season": 2,
        "episode": 6,
        "title": "The Old Gods and the New",
        "rating": 9.1
    },
    {
        "season": 2,
        "episode": 7,
        "title": "A Man Without Honor",
        "rating": 8.9
    },
    {
        "season": 2,
        "episode": 8,
        "title": "The Prince of Winterfell",
        "rating": 8.8
    },
    {
        "season": 2,
        "episode": 9,
        "title": "Blackwater",
        "rating": 9.7
    },
    {
        "season": 2,
        "episode": 10,
        "title": "Valar Morghulis",
        "rating": 9.4
    },
    {
        "season": 3,
        "episode": 1,
        "title": "Valar Dohaeris",
        "rating": 8.8
    },
    {
        "season": 3,
        "episode": 2,
        "title": "Dark Wings, Dark Words",
        "rating": 8.6
    },
    {
        "season": 3,
        "episode": 3,
        "title": "Walk of Punishment",
        "rating": 8.9
    },
    {
        "season": 3,
        "episode": 4,
        "title": "And Now His Watch Is Ended",
        "rating": 9.6
    },
    {
        "season": 3,
        "episode": 5,
        "title": "Kissed by Fire",
        "rating": 9
    },
    {
        "season": 3,
        "episode": 6,
        "title": "The Climb",
        "rating": 8.8
    },
    {
        "season": 3,
        "episode": 7,
        "title": "The Bear and the Maiden Fair",
        "rating": 8.7
    },
    {
        "season": 3,
        "episode": 8,
        "title": "Second Sons",
        "rating": 9
    },
    {
        "season": 3,
        "episode": 9,
        "title": "The Rains of Castamere",
        "rating": 9.9
    },
    {
        "season": 3,
        "episode": 10,
        "title": "Mhysa",
        "rating": 9.1
    },
    {
        "season": 4,
        "episode": 1,
        "title": "Two Swords",
        "rating": 9.1
    },
    {
        "season": 4,
        "episode": 2,
        "title": "The Lion and the Rose",
        "rating": 9.7
    },
    {
        "season": 4,
        "episode": 3,
        "title": "Breaker of Chains",
        "rating": 8.9
    },
    {
        "season": 4,
        "episode": 4,
        "title": "Oathkeeper",
        "rating": 8.8
    },
    {
        "season": 4,
        "episode": 5,
        "title": "First of His Name",
        "rating": 8.7
    },
    {
        "season": 4,
        "episode": 6,
        "title": "The Laws of Gods and Men",
        "rating": 9.7
    },
    {
        "season": 4,
        "episode": 7,
        "title": "Mockingbird",
        "rating": 9.1
    },
    {
        "season": 4,
        "episode": 8,
        "title": "The Mountain and the Viper",
        "rating": 9.7
    },
    {
        "season": 4,
        "episode": 9,
        "title": "The Watchers on the Wall",
        "rating": 9.6
    },
    {
        "season": 4,
        "episode": 10,
        "title": "The Children",
        "rating": 9.7
    },
    {
        "season": 5,
        "episode": 1,
        "title": "The Wars to Come",
        "rating": 8.5
    },
    {
        "season": 5,
        "episode": 2,
        "title": "The House of Black and White",
        "rating": 8.5
    },
    {
        "season": 5,
        "episode": 3,
        "title": "High Sparrow",
        "rating": 8.5
    },
    {
        "season": 5,
        "episode": 4,
        "title": "Sons of the Harpy",
        "rating": 8.7
    },
    {
        "season": 5,
        "episode": 5,
        "title": "Kill the Boy",
        "rating": 8.6
    },
    {
        "season": 5,
        "episode": 6,
        "title": "Unbowed, Unbent, Unbroken",
        "rating": 8
    },
    {
        "season": 5,
        "episode": 7,
        "title": "The Gift",
        "rating": 9
    },
    {
        "season": 5,
        "episode": 8,
        "title": "Hardhome",
        "rating": 9.9
    },
    {
        "season": 5,
        "episode": 9,
        "title": "The Dance of Dragons",
        "rating": 9.5
    },
    {
        "season": 5,
        "episode": 10,
        "title": "Mother's Mercy",
        "rating": 9.1
    },
    {
        "season": 6,
        "episode": 1,
        "title": "The Red Woman",
        "rating": 8.5
    },
    {
        "season": 6,
        "episode": 2,
        "title": "Home",
        "rating": 9.4
    },
    {
        "season": 6,
        "episode": 3,
        "title": "Oathbreaker",
        "rating": 8.7
    },
    {
        "season": 6,
        "episode": 4,
        "title": "Book of the Stranger",
        "rating": 9.1
    },
    {
        "season": 6,
        "episode": 5,
        "title": "The Door",
        "rating": 9.7
    },
    {
        "season": 6,
        "episode": 6,
        "title": "Blood of My Blood",
        "rating": 8.4
    },
    {
        "season": 6,
        "episode": 7,
        "title": "The Broken Man",
        "rating": 8.6
    },
    {
        "season": 6,
        "episode": 8,
        "title": "No One",
        "rating": 8.4
    },
    {
        "season": 6,
        "episode": 9,
        "title": "Battle of the Bastards",
        "rating": 9.9
    },
    {
        "season": 6,
        "episode": 10,
        "title": "The Winds of Winter",
        "rating": 9.9
    },
    {
        "season": 7,
        "episode": 1,
        "title": "Dragonstone",
        "rating": 8.6
    },
    {
        "season": 7,
        "episode": 2,
        "title": "Stormborn",
        "rating": 8.9
    },
    {
        "season": 7,
        "episode": 3,
        "title": "The Queen's Justice",
        "rating": 9.2
    },
    {
        "season": 7,
        "episode": 4,
        "title": "The Spoils of War",
        "rating": 9.8
    },
    {
        "season": 7,
        "episode": 5,
        "title": "Eastwatch",
        "rating": 8.8
    },
    {
        "season": 7,
        "episode": 6,
        "title": "Beyond the Wall",
        "rating": 9.1
    },
    {
        "season": 7,
        "episode": 7,
        "title": "The Dragon and the Wolf",
        "rating": 9.5
    },
    {
        "season": 8,
        "episode": 1,
        "title": "Winterfell",
        "rating": 7.6
    },
    {
        "season": 8,
        "episode": 2,
        "title": "A Knight of the Seven Kingdoms",
        "rating": 7.9
    },
    {
        "season": 8,
        "episode": 3,
        "title": "The Long Night",
        "rating": 7.5
    },
    {
        "season": 8,
        "episode": 4,
        "title": "The Last of the Starks",
        "rating": 5.5
    },
    {
        "season": 8,
        "episode": 5,
        "title": "The Bells",
        "rating": 6.1
    },
    {
        "season": 8,
        "episode": 6,
        "title": "The Iron Throne",
        "rating": 4.2
    }
]

# alcohol = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")
# bad_drivers = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/bad-drivers/bad-drivers.csv', encoding="ISO-8859-1")
# births = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_1994-2003_CDC_NCHS.csv', encoding="ISO-8859-1")
wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm.info()
wm.columns
print(wm.columns)
print(wm.index)

def grid_test():
    wp = jp.WebPage()
    c = jp.LinkedChartGrid(wm, 0, range(1,len(wm.columns)), kind='column', a=wp, classes='m-4 p-2 border',
                        stacking='', title='Alcohol Consumption per Country', subtitle='538 data')
    c.grid.options.enableCharts = True
    c.grid.options.enableRangeSelection = True
    # jp.LinkedChartGrid(bad_drivers, 0, [1,2,3,4,5,6,7], kind='column', a=wp, classes='m-4 p-2 border-4', title='Bad Drivers per US State', subtitle='538 data')
    # births.jp.ag_grid(a=wp)
    return wp

jp.justpy(grid_test)