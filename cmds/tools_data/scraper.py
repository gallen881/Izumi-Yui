import requests
import function

def scrap_eq(eq):
    function.print_time('Start scraping on cwb')
    r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-2B9F8C22-56A8-4E07-B771-3CBB03A94616')
    jdata = r.json()
    eqs = jdata['records']['earthquake']    # 轉換成 json 格式

    eq -= 1

    loc = eqs[eq]['earthquakeInfo']['epiCenter']['location']
    val = eqs[eq]['earthquakeInfo']['magnitude']['magnitudeValue']
    dep = eqs[eq]['earthquakeInfo']['depth']['value']
    eq_time = eqs[eq]['earthquakeInfo']['originTime']
    img = eqs[eq]['reportImageURI']

    function.print_time('Finish scraping')

    return loc, val, dep, eq_time, img