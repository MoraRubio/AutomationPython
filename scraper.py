from selenium import webdriver
from datetime import date
from pandas import DataFrame, read_csv
import os

today = date.today().strftime("%d/%m/%y")

driver = webdriver.Firefox()

# Falabella
driver.get("https://www.falabella.com.co/falabella-co/category/cat1360967/Televisores?sortBy=derived.price.search%2Casc&f.product.attribute.Tama%C3%B1o_de_la_pantalla=65+pulgadas%3A%3A70+pulgadas&f.product.brandName=lg%3A%3Asamsung&facetSelected=true%2Ctrue%2Ctrue%2Ctrue")

results = driver.find_elements_by_class_name("search-results-list")

links = [result.find_elements_by_class_name("pod-link")[0].get_attribute("href") for result in results]

prices = [result.find_elements_by_class_name("price-0")[0].get_attribute("data-undefined-price") for result in results]

names = [result.find_elements_by_class_name("pod-subTitle")[0].get_attribute("textContent") for result in results]

# Alkosto
driver.get("https://www.alkosto.com/tv/televisores/ver/lg-samsung/60_y_mas_pulgadas/?dir=asc&order=price")

results = driver.find_elements_by_class_name("item")

links.extend([result.find_elements_by_class_name("product-name")[0].find_elements_by_xpath(".//*")[0].get_attribute("href") for result in results if result.find_elements_by_class_name("product-name")])

prices.extend([result.find_elements_by_class_name("price")[0].get_attribute("innerText") for result in results if result.find_elements_by_class_name("price")])

names.extend([result.find_elements_by_class_name("product-name")[0].find_elements_by_xpath(".//*")[0].get_attribute("title") for result in results if result.find_elements_by_class_name("product-name")])

data = DataFrame(data={"Link":links, f"{today}":prices}, index=names)

print(f"Datos encontrados: {data.shape[0]}")
if "PreciosTV.csv" in os.listdir(): 
	existing_data = read_csv("./PreciosTV.csv", sep=",")
	existing_data.merge(data, how="outer").to_csv("./PreciosTV.csv")
else:
	data.to_csv("./PreciosTV.csv")
