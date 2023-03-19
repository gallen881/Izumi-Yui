import requests
import urllib.parse
import json
import core.function as function

class Pinterest:
    urls_path = './data/urls.json'
    jdata = function.open_json(urls_path)
    search_keyword = 'anime girl'
    bookmark = ''
    url = "https://tr.pinterest.com/resource/BaseSearchResource/get/?"

    def __init__(self, amount):
        self.amount = amount

    def reset_bookmark(self):
        self.bookmark = ''

    def image_data(self):        
        if self.bookmark == "":
            return '''{"options":{"isPrefetch":false,"query":"''' + self.search_keyword + '''","scope":"pins","no_fetch_context_on_resource":false},"context":{}}'''
        else:
            return '''{"options":{"page_size":25,"query":"''' + self.search_keyword + '''","scope":"pins","bookmarks":["''' + self.bookmark + '''"],"field_set_key":"unauth_react","no_fetch_context_on_resource":false},"context":{}}'''.strip()

    def get_pinterest_urls(self):
        image_urls = []
        times = 0
        rtimes = 0
        function.print_detail(memo='INFO', obj='Start scraping on Pinterest')
        while True:
            r = requests.get(self.url, params={"source_url": f"/search/pins/?q={urllib.parse.quote(self.search_keyword)}", "data": self.image_data()})
            jsonData = json.loads(r.content)
            resource_response = jsonData["resource_response"]
            data = resource_response["data"]
            results = data["results"]

            for i in results:
                if i["images"]["orig"]["url"] not in image_urls and i["images"]["orig"]["url"] not in self.jdata["pinterest"] and i["images"]["orig"]["url"] not in Pinterest.jdata["nopinterest"]:
                    image_urls.append(i["images"]["orig"]["url"])
            
            times += 1

            if len(image_urls) > self.amount or times >= self.amount * 7 or rtimes == 2:
                function.print_detail(memo='INFO', obj=f'Add "{image_urls}"')
                function.print_detail(memo='INFO', obj=f'Add "{len(image_urls)}" pictures')
                self.jdata['pinterest'].extend(image_urls)
                function.write_json(self.urls_path, self.jdata)
                break
            else:
                try:
                    self.bookmark = resource_response["bookmark"]
                except:
                    self.reset_bookmark()
                    function.print_detail(memo='WARN', obj='No bookmark, reseting Pinterest bookmark')
                    rtimes += 1
                function.print_detail(memo='COMPLETENESS', obj=f'About {len(image_urls) / self.amount * 100}%')

        return len(image_urls)

class Pixiv:
    def get_pixiv_urls_pid(pid):
        function.print_detail(memo='INFO', obj=f'Start scraping for "illust({pid})" on Pixiv')
        r = json.loads(requests.get(f'https://www.pixiv.net/ajax/illust/{pid}').content)['body']
        try:
            formed_link = []
            for page in range(int(r['pageCount'])):
                formed_link.append(r['urls']['original'].replace('i.pximg.net/img-original', 'pixiv.ibaraki.workers.dev').replace('img', 'img-original/img').replace('p0', f'p{page}'))
                function.print_detail(memo='INFO', obj=f'Form {formed_link[page]}')
            return formed_link
        except:
            return ['Picture not found']

    def get_pixiv_urls_uid(uid):
        function.print_detail(memo='INFO', obj=f'Start scraping for "user({uid})" on Pixiv')
        r = json.loads(requests.get(f'https://www.pixiv.net/ajax/user/{uid}/profile/all').content)
        try:
            name = r['body']['pickup'][0]['userName']
        except:
            name = 'User name not found'
        return r['body']['illusts'].keys(), name

    
class Earthquake:
    def scrap_eq(eq):
        function.print_detail(memo='INFO', obj='Start scraping on cwb')
        r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-2B9F8C22-56A8-4E07-B771-3CBB03A94616')
        jdata = r.json()
        eqs = jdata['records']['earthquake']

        eq -= 1

        loc = eqs[eq]['earthquakeInfo']['epiCenter']['location']
        val = eqs[eq]['earthquakeInfo']['magnitude']['magnitudeValue']
        dep = eqs[eq]['earthquakeInfo']['depth']['value']
        eq_time = eqs[eq]['earthquakeInfo']['originTime']
        img = eqs[eq]['reportImageURI']

        function.print_detail(memo='INFO', obj='Finish scraping')

        return loc, val, dep, eq_time, img