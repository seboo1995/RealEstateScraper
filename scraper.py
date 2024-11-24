import traceback
import pandas as pd
import requests
from bs4 import BeautifulSoup
from databaseHandler import DBHandler

class Pazar3Scraper():
    def __init__(self):
       self.sBaseUrl = "https://www.pazar3.mk/oglasi/zivealista/prodazba?Page="
       self.iNumOfPagesScraped = 10
       self.dSelectors = {
           'adSelector':".row-listing",
           'titleSelector':'h2',
           'priceSelector': '.list-price',
           'metaInfoSelector': '.left-side > div',
           'linkSelector': '.Link_vis',
           'locationSelector':'.link-html'
       }
    def dfScrapePage(self):
        for i in range(1,self.iNumOfPagesScraped):
            sUrl = self.sBaseUrl+str(i)
            response = requests.get(sUrl)
            if response.status_code == 200:
                lAllAds = self.lGetAllAdsFromPage(response)
                dfRawData  = self.dfGetRawData(lAllAds)
                self.writeToDB(dfRawData)
                return dfRawData
            else:
                print("Log file writing")
    def lGetAllAdsFromPage(self,response:requests.Response):
        soup = BeautifulSoup(response.text)
        lAllAds = soup.select(self.dSelectors['adSelector'])
        return lAllAds

    def dfGetRawData(self,lAllAds):
        lResults = []
        for ad in lAllAds:
            try:
                title = ad.select_one(self.dSelectors['titleSelector']).text
            except Exception as e:
                print(f'Could not get title because of {e}')
                print(traceback.format_exc())
                title = ''

            try:
                price = ad.select_one(self.dSelectors['priceSelector']).text
            except Exception as e:
                print(f'Could not get price because of {e}')
                print(traceback.format_exc())
                price = ''

            try:
                metaInfo = ad.select_one(self.dSelectors['metaInfoSelector']).text
            except Exception as e:
                print(f'Could not get metainfo because of {e}')
                print(traceback.format_exc())
                metaInfo = ''

            try:
                link = ad.select_one(self.dSelectors['linkSelector'])['href']
                link = 'https://www.pazar3.mk'+link
            except Exception as e:
                print(f'Could not get link because of {e}')
                print(traceback.format_exc())
                link = ''


            try:
                locations = ad.select(self.dSelectors['locationSelector'])
                locations = [str(i.text) for i in locations]
                location = ','.join(locations)
            except Exception as e:
                print(f'Could not get location because of {e}')
                print(traceback.format_exc())
                location = ''
            dRes = {
                'title':title,
                'price':price,
                'metaInfo':metaInfo,
                'link':link,
                'location':location
            }
            lResults.append(dRes)

        return pd.DataFrame(lResults)

    def writeToDB(self,dfRawData):
        handler = DBHandler()
        handler.vAddRowsPazar3(dfRawData)

class Pazar3IndividualScraper():
    def __init__(self):
        pass



if __name__ == '__main__':
    scraper = Pazar3Scraper()
    scraper.dfScrapePage()









