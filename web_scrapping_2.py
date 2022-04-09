from email import header
import time
import csv
from tracemalloc import start
from wsgiref import headers
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("./chromedriver")
browser.get(start_url)
time.sleep(10)
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyper_link","planet_type","orbital_radius","orbital_eccentricity"]
planet_data=[]
new_planet_data = []
def scrap():
    for i in range(1,501):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            current_page_num = int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif current_page_num > i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyper_link_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+hyper_link_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(f"{i}pagedone1")

def scrap_more_data(hyper_link):
    try:
        page = requests.get(hyper_link)
        soup = BeautifulSoup(page.contents,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyper_link)
scrap()
for index,data in enumerate(planet_data):
    scrap_more_data(data[5])
    print(f"{index+1}pagedone2")
final_planet_data = []
for index,data in enumerate(planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("/n","")]
    for elem in new_planet_data_element: final_planet_data.append(data+new_planet_data_element)
with open("final.csv","w") as f :
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            csv_writer.writerows(final_planet_data)
