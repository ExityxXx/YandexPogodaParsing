import requests as rq
from bs4 import BeautifulSoup as BS



def parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36"
    }
    try:
        response = rq.get(url, headers=headers)
        response.raise_for_status()

        soup = BS(response.text, "html.parser")

        temperature_tag = soup.find_all("span", class_="temp__value temp__value_with-unit")
        city_name = soup.find("h1", class_="title title_level_1 header-title__title").text
        sky = soup.find("div", class_="link__condition day-anchor i-bem").text
        wind_speed = soup.find("span", class_="wind-speed")
        wind_direction_tag = soup.find("span", class_="fact__unit")
        wind_direction = wind_direction_tag.find("abbr").text
        humidity_level = soup.find("div", class_="term term_orient_v fact__humidity")
        humidity_level = humidity_level.find("span", class_="a11y-hidden").text
        information_about_the_landings = soup.find("p", class_="maps-widget-fact__title").text

        print("\t\t--==ПОГОДА==--")
        print(city_name)

        if len(temperature_tag) >= 2:
            actual_temperature = temperature_tag[0].text.strip()
            feels_like_temperature = temperature_tag[2].text.strip()

        print(f"{actual_temperature} Градусов цельсия\nОщущается как {feels_like_temperature} градусов цельсия")
        print(sky)
        print(f"Скорость ветра: {wind_speed.text} М/С, направление : {wind_direction}")
        print(humidity_level)
        print(information_about_the_landings)

        #with open("HTML's/parse.html", "w", encoding="utf-8") as parse_file:
            #parse_file.write(str(soup))
            # Можете сохранить в файл при желаний
    except rq.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
    except Exception as exp:
        print(f"Ошибка обработки: {exp}")
    finally:
        return response.status_code if response.status_code == 200 else None

parse_target = parse("https://yandex.ru/pogoda/28?utm_source=serp&utm_campaign=helper&utm_medium=desktop&utm_content=helper_desktop_main&utm_term=title")

if __name__ == "__main__":
    if parse_target == 200:
        print(parse_target)
    else:
        print("Ошибка")
