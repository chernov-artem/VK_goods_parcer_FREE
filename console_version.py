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

def save_foto_from_ID(group_id,item_id):
    res = session.method("market.getById", {"item_ids": f"-{group_id}_{item_id}", "extended": 1})
    list = []
    for i in res['items'][0]['photos']:
        list.append(i['sizes'][-1]['url'])
        print(i['sizes'][-1]['url'])
    return list





if __name__ == '__main__':
    # group_id = -107686276
    # res = market_get_goods_dict(group_id)
    # file_name = f"goods_id{str(group_id)[1:]}_{str(datetime.datetime.now())[:-7].replace(' ', '_').replace(':', '-')}.txt"
    # with open(str(file_name), "a+") as file:
    #     file.write("Muffin программы для бизнеса https://vk.com/muffin_programs_for_business\n\n")
    #     file.write("Содержание строчек:\n")
    #     file.write("Название товара;цена;ссылка на товар\n\n")
    #     for key, value in res.items():
    #         try:
    #             file.write(f"{value[0]};{value[1]};https://vk.com/market-{group_id}?w=product-{group_id}_{key}\n")
    #         except:
    #             file.write(f"{value[0][:-2]};{value[1]};https://vk.com/market-{group_id}?w=product-{group_id}_{key}\n")
    #
    # file_id_name = f"ids_{len(res.items())}_товаров.txt"
    #
    # with open(str(file_id_name), "a+") as file:
    #     for key in res.keys():
    #         file.write(f"{key}\n")

    dict_foto = {}

    with open("ids_2123_товаров.txt", "r") as file:
        for i in range(2123):
            time.sleep(0.3)
            id = int(file.readline())
            res = save_foto_from_ID(107686276, id)
            dict_foto[id] = res
            print(i, res)

    print('словарь:')
    with open("dict_foto.txt", "a") as file:
        file.write(str(dict_foto))
    print('\33[31mРабота программы окончена\33[0m')



