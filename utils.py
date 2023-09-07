import gspread

def connect(credentials_file):
    return gspread.service_account(filename=credentials_file)

def open_worksheet(spreadsheet, spreadsheet_name, worksheet_name):
    return spreadsheet.open(spreadsheet_name).worksheet(worksheet_name)

def append_data(worksheet, data):
    worksheet.append_row(data)