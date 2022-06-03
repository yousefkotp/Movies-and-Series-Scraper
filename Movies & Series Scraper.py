import requests
from bs4 import BeautifulSoup
import webbrowser

while True:
    option = int(input("What do you want to watch ?(enter 1 or 2 or 3)\n1- Series\n2- Movie\n3- Download a whole season\n"))
    if 3 >= option >= 1:
        break
    else:
        print("please enter 1 or 2 or 3")

if option == 1:                      # Watch a series
    series_name = input("Enter series name: ")
    series_name.rstrip(" ")
    series_name = series_name.replace(" ", "-")

    # Preparing our html page and soup
    html_page = requests.get("https://riko.egybest.asia/explore/?q=" + series_name)
    soup = BeautifulSoup(html_page.content, "lxml")

    # Scraping links and titles of series resulted from the query
    links_of_recommended_series = soup.find_all("a", {"class": "movie"})
    titles_of_recommended_series = soup.find_all("span", {"class": "title"})
    print("Which series do you want to watch?")

    counter_series = 1
    for i in titles_of_recommended_series:
        print(str(counter_series)+"- "+i.text)
        counter_series += 1
    series_number = int(input("Enter the number corresponding to your wanted series: "))

    # Preparing html page and soup for desired series
    html_page = requests.get(links_of_recommended_series[series_number-1].get("href"))
    soup = BeautifulSoup(html_page.content, "lxml")

    # Scraping links and titles of seasons of the desired series
    temp_list = soup.find("div", {"class": "contents movies_small"})
    seasons_links = temp_list.findAll("a")          # i.get("href")
    seasons_links.reverse()

    season = int(input("There are "+str(len(seasons_links))+" Seasons, Enter your desired season number: "))

    # Preparing html page and soup to be used to scrape episodes links
    html_page = requests.get(seasons_links[season-1].get("href"))
    soup = BeautifulSoup(html_page.content, "lxml")

    # Scraping episodes links and titles
    temp_list = soup.find("div", {"class": "movies_small"})
    episodes_links = temp_list.findAll("a")
    episodes_links.reverse()

    print("There are " + str(len(episodes_links)) + " episodes")
    ep1 = int(input("Enter episode number (from): "))
    ep2 = int(input("Enter episode number (to): "))

    counter_episodes = ep2
    while counter_episodes >= ep1:      # Iterating through desired episodes
        html_page = requests.get(episodes_links[counter_episodes-1].get("href"))
        soup = BeautifulSoup(html_page.content, "lxml")
        link = soup.find("iframe", {"class": "auto-size"})
        watching_link = link.get("src")
        result = requests.get("https://riko.egybest.asia" + watching_link)
        webbrowser.open("https://riko.egybest.asia" + watching_link)
        counter_episodes -= 1

elif option == 2:       # Watch a movie
    movie_name = input("Enter movie name: ")
    movie_name.rstrip(" ")
    movie_name = movie_name.replace(" ", "%20")

    html_page = requests.get("https://riko.egybest.asia/explore/?q="+movie_name)
    soup = BeautifulSoup(html_page.content, "lxml")

    movies_links = soup.find_all("a", {"class": "movie"})
    movies_titles = soup.find_all("span", {"class": "title"})
    print("What movies do you want to watch?")

    counter = 1
    for i in movies_titles:
        print(str(counter)+"- "+i.text)
        counter += 1

    movie_number = int(input("Please enter the number of the movie you want: "))
    movie_link = movies_links[movie_number-1].get("href")

    html_page = requests.get(movie_link)
    soup = BeautifulSoup(html_page.content, "lxml")

    link = soup.find("iframe", {"class": "auto-size"})
    watching_link = link.get("src")
    webbrowser.open("https://riko.egybest.asia" + watching_link)


else:       # Download a whole season
    series_name = input("Enter series name: ")
    series_name.rstrip(" ")
    series_name = series_name.replace(" ", "-")
    season = int(input("Enter Season number: "))

    html_page = requests.get("https://mycima.tube/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84-"+str(series_name)+"-%d9%85%d9%88%d8%b3%d9%85-"+str(season)+"-")
    if html_page.status_code == 404:
        html_page = requests.get("https://mycima.tube/series/%D9%85%D9%88%D8%B3%D9%85-"+str(season)+"-%D9%85%D8%B3%D9%84%D8%B3%D9%84-"+str(series_name))
    soup = BeautifulSoup(html_page.content, "lxml")
    x = soup.find('ul', {'class': "Season--Download--Mycima--Single"})
    if x is None:
        print("This feature is not available for "+str(series_name)+" season "+str(season)+"!")
        exit(1)

    temp = x.findAll("a")
    qualities = soup.find_all("resolution")
    links = []
    for i in temp:
        links.append(i.get("href"))

    counter_qualities = 1
    for i in qualities:
        print(str(counter_qualities)+"- " + i.text)
        counter_qualities += 1

    quality = int(input("Enter your desired quality: "))
    webbrowser.open(links[quality-1])


input("Enter any key to exit: ")