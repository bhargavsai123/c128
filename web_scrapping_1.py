from email import header
import time
import csv
from tracemalloc import start
from wsgiref import headers
from selenium import webdriver
from bs4 import BeautifulSoup

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/bhargav/Downloads/c127/chromedriver")
browser.get(start_url)
time.sleep(10)

def scrap():
    headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date"]
    planet_data = []

    for i in range(0,501):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for i in range(0,501):
            for ul_tag in soup.find_all("ul",attrs=("class","exoplanet")):
                temp_list = []
                li_tags = ul_tag.find_all("li")
                for index,li_tag in enumerate(li_tags):
                    if index == 0:
                        temp_list.append(li_tag.find_all("a")[0].contents[0])
                    else:
                        try:
                            temp_list.append(li_tag.contents[0])
                        except:
                            temp_list.append(li_tag.contents[0])
                planet_data.append(temp_list)
            browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

        with open("scraper2.csv","w") as f :
            csv_writer = csv.writer(f)
            csv_writer.writerow(headers)
            csv_writer.writerows(planet_data)
    
scrap()
