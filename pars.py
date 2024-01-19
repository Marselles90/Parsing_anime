# └── Создания Парсера
#     ├── get_html()
#     ├── processing()
#     └── run_parser()

import requests, json, csv
from bs4 import BeautifulSoup


def get_html(url, header):
    """
        get_html(url, header)


        url: Адрес сайта которую вы хотите спарсить
        hearder: Заголовок в сети

        Возвращает html страницу которую мы хотим спарсить 
        Если не сможет получить html возвращает ошибку
        Если все хорошо возвращает html страницу которую мы хотим спарсить 

        Используется для получения html страницы которую мы хотим спарсить
    """

    responce = requests.get(url, headers=header)

    if responce.status_code == 200:
        return responce.text
    
    else:
        raise Exception(f"Произошла ошибка при получении страницы: {responce.status_code}")
    

def processing(html):
    """
        processing(html)


        html: html страница которую мы хотим спарсить

        Возвращает данные которые мы хотим отобразить в таблице
        Если не сможет получить данные возвращает ошибку
        Если все хорошо возвращает данные которые мы хотим отобразить в таблице

        Используется для обработки html страницы которую мы хотим спарсить
    """

    soup = BeautifulSoup(html, 'lxml').find("div", {"id": "dle-content"})
    soup = soup.find_all("div", {"class": "shortstory"})

    info = []

    for shortstory in soup:
        temp_main_cont = shortstory.find('div', class_='shortstoryContent')
        temp_a = shortstory.find("div", {"class": "shortstoryHead"}).find("a")
        temp_p = temp_main_cont.find_all("p")
        temp_div = temp_main_cont.find_all("div")
        
        image_url = "https://v2.vost.pw" + temp_div[0].find("img").get("src")
        
        try:
            raiting = temp_div[1].find("li", class_='current-rating').text+'%'
            vote = temp_div[1].find("span").find('span').text
        except Exception as ex:
            vote = None
            raiting = None
        
        title = temp_a.text
        url = temp_a.get("href")
        year = temp_p[0].text
        genre = temp_p[1].text
        types = temp_p[2].text
        episodes = temp_p[3].text
        
        if len(temp_p[4].text.split()) <= 5:
            director = temp_p[4].text.split(': ')[1]
        else:
            director = None

        info.append({
            "title": title.split(" /")[0],
            "url": url,
            "year": year.split(": ")[1] + "г",
            "genre": genre.split(": ")[1].title(),
            "types": types.split(": ")[1],
            "episodes": episodes.split( ": " )[1],
            'vote': vote,
            "raiting": raiting,
            "director": director,
            'image_url': image_url,
        })
    
    return info


def run_parser():
    url = "https://v2.vost.pw/"
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
    big_date = []
    for page in range(1, 5):
        html = get_html(url + f'page/{page}/', header)
        data = processing(html)
        
        big_date.extend(data)
        print(f'Отработано страниц {page}')


    with open("v2.vost.json", "w") as file:
        json.dump(big_date, file, indent=4, ensure_ascii=False)

    return "Парсинг окончен"


print(run_parser())
