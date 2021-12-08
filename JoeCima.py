import requests
from bs4 import BeautifulSoup
import webbrowser
class colors:
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
while True:
    option = int(input("What do you want to do?(enter 1 or 2)\n1- Series\n2- Movie\n"))
    if option<=2 and option>=1:
        break
    else:
        print("please enter 1 or 2")

if option ==1:
    try:
        s2 = input("Enter series name: ")
        s = s2.replace(" ", "-")
        x=1
        html_page = requests.get("https://riko.egybest.asia/season/" + s + "-season-" + str(x))
        while html_page.status_code != 404:
            print(colors.GREEN+ "Season "+str(x)+" is available!"+colors.ENDC)
            x+=1
            html_page = requests.get("https://riko.egybest.asia/season/" + s + "-season-" + str(x))
        season = int(input("Enter Season number: "))
        ep1 = int(input("Enter episode number (from): "))
        ep2 = int(input("Enter episode number (to): "))
        counter_episodes = ep2
        while counter_episodes >= ep1:
            html_page = requests.get("https://riko.egybest.asia/episode/" + s + "-season-" + str(season) + "-ep-" + str(counter_episodes))
            src = html_page.content
            soup = BeautifulSoup(src, "lxml")
            link = soup.find("iframe", {"class": "auto-size"})
            f = link.get("src")
            result = requests.get("https://riko.egybest.asia" + f)
            webbrowser.open("https://riko.egybest.asia" + f)
            counter_episodes -= 1
    except:
        input("please re-check the information you entered!")
        exit()

else:
    s2= input("Enter movie name: ")
    s = s2.replace(" ", "%20")
    html_page = requests.get("https://riko.egybest.asia/explore/?q="+s)
    soup = BeautifulSoup(html_page.content, "lxml")
    l = soup.find_all("a",{"class":"movie"})
    m = soup.find_all("span",{"class":"title"})
    print("What movies do you want to watch?")
    counter =1
    for i in m:
        print(str(counter)+"- "+i.text)
        counter+=1
    desired = int(input("Please enter the number of the movie you want: "))
    ss = l[desired-1].get("href")
    html_page = requests.get(ss)
    soup = BeautifulSoup(html_page.content,"lxml")
    link = soup.find("iframe", {"class": "auto-size"})
    f = link.get("src")
    webbrowser.open("https://riko.egybest.asia" +f)

input("Enter any key to exit: ")