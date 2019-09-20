import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests

# UPDATE ROW IN GOOGLE SHEETS - PAGESPEED ANALYSIS

# CREDENTIALS TO CREATE A CLIENT TO INTERACT WITH GOOGLE DRIVE API

scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('sheetscredentials.json', scope)
client = gspread.authorize(creds)

# FIND SHEET WITH URLS TO TEST
testsheet = client.open('GOOGLE SHEETS NAME').worksheet('WORKSHEET WITH URLS TO TEST NAME')
URLs_to_test = testsheet.col_values(1), testsheet.row_values(2)

# FIND SHEET TO INPUT RESULTS
sheet = client.open('GOOGLE SHEETS NAME').worksheet('WORKSHEET FOR RESULTS TO BE INPUT')

# ESTABLISH INPUT COLUMNS - URLS TO TEST (A) AND DEVICE (G)
URLcol = testsheet.col_values(1)
devicecol = testsheet.col_values(7)

for i in URLcol:
    for p in devicecol:
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={i}&strategy={p}&prettyPrint=true'
        print(f'Requesting {x}...')
        response = requests.get(x)
        r = requests.get(x)
        final = r.json()

        dateTimeObj = datetime.now()
        Tdate = dateTimeObj.strftime("%d/%m/%y")
        TTime = timeStr = dateTimeObj.strftime("%H:%M:%S")

        psinsights = 'https://developers.google.com/speed/pagespeed/insights/?url=' + i + '&tab=' + p

    # THIS SECTION BREAKS DOWN THE SCORES IN TO TIMINGS AND PERFORMANCE SCORE

        try:
            urlid = final['id']
            split = urlid.split('?')
            urlid = split[0]
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            FCP = f'First Contentful Paint ~ {str(urlfcp)}'
            FCP2 = str(urlfcp)
            urlfi = final['lighthouseResult']['audits']['interactive']['displayValue']
            FI = f'First Interactive ~ {str(urlfi)}'
            FI2 = str(urlfi)
            urlle = final['lighthouseResult']['audits']['first-meaningful-paint']['displayValue']
            LE = f'First Meaningful Paint ~ {str(urlle)}'
            LE2 = str(urlle)
            urlscore = final['lighthouseResult']['categories']['performance']['score']
            ScorePerc = urlscore * 100
            Score = f'Performance Score ~ {str(ScorePerc)}'
            Score2 = str(ScorePerc)
            opportunity = final['lighthouseResult']['categories']['performance']['score']
            ListOpps = f'Performance Score ~ {str(opportunity)}'
            ListOpps2 = str(opportunity)



        except KeyError:
            print(f'<KeyError> One or more keys not found {i}.')


        try:
            # INPUTS RESULTS IN TO COLUMNS IN NAMED SHEET STARTING IN ROW 2
            row = [Tdate, TTime, ID2, ScorePerc, urlfcp, urlfi, urlle, p, psinsights]
            index = 2
            sheet.insert_row(row, index)
        except NameError:
            print(f'<NameError> Failing because of KeyError {i}.')

# TESTING
        try:
            print(ID)
            print(FCP)
            print(FI)
            print(LE)
            print(Score)
            print(Tdate)
            print(TTime)
            print(psinsights)

        except NameError:
            print(f'<NameError> Failing because of KeyError {i}.')
