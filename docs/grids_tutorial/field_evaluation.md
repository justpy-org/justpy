# Evaluating Fields using JavaScript

Some advanced options in Ag-grid require providing a JavaScript function. The fields whose string representation should be evaluated as JavaScript need to be specified in the `evaluate` attribute.



In the example below, [tree data mode](https://www.ag-grid.com/javascript-grid-tree-data/) is implemented. It is only available in the enterprise edition of ag-grid. 

!!! warning
    Don't forget to set justpy.env to load the enterprise version of ag-grid

```python
import justpy as jp

grid_options = {
    'getDataPath': '''function(data) { return data.orgHierarchy; }''',
    'treeData': True,
    'defaultColDef': {
        'filter': True,
        'sortable': True,
        'resizable': True,
    },
    'columnDefs': [
        {'headerName': "job title", 'field': "jobTitle"},
        {'headerName': "employment type", 'field': "employmentType"},
    ],
    'rowData' : [
        {'orgHierarchy': ['Erica'], 'jobTitle': "CEO", 'employmentType': "Permanent"},
        {'orgHierarchy': ['Erica', 'Malcolm'], 'jobTitle': "VP", 'employmentType': "Permanent"},
        {'orgHierarchy': ['Erica', 'Bob'], 'jobTitle': "SVP", 'employmentType': "Permanent"},
        {'orgHierarchy': ['Erica', 'Bob', 'jo'], 'jobTitle': "eVP", 'employmentType': "Permanent"}
    ]
}

def grid_test9():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options)
    grid.evaluate = ['getDataPath']
    return wp

jp.justpy(grid_test9)
```