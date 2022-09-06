import justpy as jp
import pandas as pd

wm_df = pd.read_csv("https://elimintz.github.io/women_majors.csv").round(2)


async def select_all_rows(self, msg):
    await self.grid.run_api("selectAll()", msg.page)


async def deselect_rows(self, msg):
    await self.grid.run_api("deselectAll()", msg.page)


async def resetFilters(self, msg):
    await self.grid.run_api("setFilterModel()", msg.page)


async def restoreFilters(self, msg):
    # savedFilterValues = msg.page.filterValues
    await self.grid.run_api(
        "setFilterModel({year: {type: 'lessThan',filter: '1980'}})", msg.page
    )


def row_selected(self, msg):
    wp = msg.page
    if msg.selected:
        wp.selected_rows[msg.rowIndex] = msg.data
    else:
        wp.selected_rows.pop(msg.rowIndex)


def downloadRow(self, msg):
    wp = msg.page
    wp.resultSelect.text = wp.selected_rows.values()


def grid_test():
    wp = jp.QuasarPage(dark=False)

    wp.selected_rows = {}

    grid = wm_df.jp.ag_grid(a=wp)
    grid.options.pagination = True
    grid.options.paginationAutoPageSize = True
    grid.options.columnDefs[0].checkboxSelection = True
    grid.options.columnDefs[0].headerCheckboxSelection = True
    grid.options.columnDefs[0].headerCheckboxSelectionFilteredOnly = True
    grid.options.columnDefs[1].hide = True
    # grid.options.columnDefs[1].floatingFilter = True

    # grid.options.defaultColDef.filter = True
    grid.options.defaultColDef.floatingFilter = True
    grid.options.defaultColDef.enableValue = True
    grid.options.defaultColDef.editable = True

    grid.options.rowSelection = "multiple"
    grid.options.sideBar = True
    grid.on("rowSelected", row_selected)

    d = jp.Div(classes="q-pa-md q-gutter-sm", a=wp)
    jp.QButton(label="Download", color="primary", a=d, click=downloadRow)
    buttonResetFilter = jp.QButton(
        label="Reset filter", color="primary", a=d, click=resetFilters
    )
    buttonResetFilter.grid = grid
    restoreRestoreFilter = jp.QButton(
        label="Restore filter", color="primary", a=d, click=restoreFilters
    )
    restoreRestoreFilter.grid = grid
    wp.resultSelect = jp.Div(
        classes="q-pa-md q-gutter-sm", a=wp, text="The result will be displayed here"
    )

    return wp


from examples.basedemo import Demo

Demo("Stackoverflow question 73497028 test", grid_test)
