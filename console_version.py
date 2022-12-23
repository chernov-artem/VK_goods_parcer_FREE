""" Парсит товары из группы ВК сохраняет их в текстовый файл вида: Название;цена;url   """

import vk_api
import time
import datetime

#токен из файла
with open("token.txt", "r") as file:
    my_token = file.read()

# блок VK-api
session = vk_api.VkApi(token=my_token)
vk = session.get_api()

# переменные

def normal_price(s) -> int:
    """Получает цену из VK Api и возвращает её"""
    if len(s) <= 5:
        return int(s[:-2])
    else:
        price0 = s.split()
        price = int(price0[0] + price0[1][:-2])
        return price


def market_get_goods_dict(group_id):
    '''парсим товары группы и добавляем их все в словарь {id_товара : ['Название_товара', цена товара]}'''

    ''' Если число товаров < 200 используется 1 запрос. Если >200 используются запросы по 200 и 1 запрос на оставшуюся часть'''
    goods_dict = {}
    goods_00 = session.method('market.get', {'owner_id': group_id, 'count': 5})
    count_of_goods = goods_00["count"]
    n = count_of_goods // 200
    np = count_of_goods % 200
    time.sleep(0.5)

    if count_of_goods <= 200:

        goods0 = session.method('market.get', {'owner_id': group_id, 'count': count_of_goods})

        for i in range(count_of_goods):
            price = normal_price(goods0['items'][i]['price']['text'])
            goods_dict[goods0['items'][i]['id']] = [goods0['items'][i]['title'], price]
    else:
        for i in range(n):
            shift = i * 200
            time.sleep(1)
            goods0 = session.method('market.get', {'owner_id': group_id, 'count': 200, 'offset': shift})
            for j in range(200):
                price = normal_price(goods0['items'][j]['price']['text'])
                goods_dict[goods0['items'][j]['id']] = [goods0['items'][j]['title'],
                                                        price]  # key словаря = id товара; value = [название товара, цена товара]

        shift = n * 200
        time.sleep(1)
        goods0 = session.method('market.get', {'owner_id': group_id, 'count': np, 'offset': shift})
        for i in range(np):
            price = normal_price(goods0['items'][i]['price']['text'])
            goods_dict[goods0['items'][i]['id']] = [goods0['items'][i]['title'],
                                                    price]

    return goods_dict









if __name__ == '__main__':

