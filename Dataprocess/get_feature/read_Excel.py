import xlrd


def readExcel(filepath, sheet):
    Ptm_Mutations = xlrd.open_workbook(filepath)  # filepath:PTM_mutation.xlsx
    sheet = Ptm_Mutations.sheet_by_name(sheet)  # Sheet1
    rows = sheet.nrows
    cols = sheet.ncols

    return sheet, rows, cols


