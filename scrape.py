import requests
import csv
from bs4 import BeautifulSoup


def filter_b(budget, peopleCount):
    b = list(map(lambda x: x*1000, list(map(int, budget.split('-')))))
    all_tours = gettour()
    ret = []
    if all_tours != None:
        for tour in all_tours:
            if len(tour) == 5:
                price = int(tour['price'].replace(',', ''))
                if b[0] < price < b[1]:
                    tour['sumPrice'] = '{:0,.0f}'.format(
                        price*int(peopleCount))
                    ret.append(tour)

        return ret

    else:
        return None
    pass


def gettour():
    try:
        url = 'http://alborzeman.ir/%D8%AA%D9%88%D8%B1%D9%87%D8%A7%DB%8C-%D8%A7%D9%84%D8%A8%D8%B1%D8%B2%D9%85%D9%86.html?order=category&dir=asc#tlb'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, features="html.parser")
        mother_table = soup.find("div", id='djcatalog')
        tables = mother_table.find_all(
            'div', class_='djc_item_in djc_clearfix')

        ret = []
        for i, table in enumerate(tables):
            tour = {}
            try:
                tour['image'] = table.find(
                    'img', class_='img-polaroid').get('src')
                tour['price'] = table.find(
                    'div', class_='djc_price').text.split(' ')[13]
                tour['tourname'] = table.find('div', class_='djc_title').find(
                    'a').text.replace('تور', '').strip()
                tour['date'] = table.find(
                    'td', class_='djc_value').text.strip().split('-')
                tour['link'] = 'http://www.alborzeman.ir' + \
                    table.find('a').get('href')
            except AttributeError:
                pass
            finally:
                ret.append(tour)
            pass
        return ret
    except:
        return None


if __name__ == "__main__":
    filter_b('0-100', '4')
    pass
