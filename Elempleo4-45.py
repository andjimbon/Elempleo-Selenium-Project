
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from unidecode import unidecode
import re

# Gettin' the Page

driver = webdriver.Chrome()
driver.get("https://www.elempleo.com/co/ofertas-empleo/bogota/4-45-millones")

soup = BeautifulSoup(driver.page_source, 'html.parser')

puestos, cia, rango_salario, publicacion, links =[], [], [], [], []

# Iterating over pages

while True:

    # Job name
    jobs = []
    for i in soup.select('.text-ellipsis'):
        jobs.append(i.text)
    items = [item.strip() for item in jobs if str(item)]

    # Company
    company = []
    for i in soup.select('.info-company-name'):
        company.append(i.text)
    empresa = [item.strip() for item in company if str(item)]

    # Salary
    salary = []
    for i in soup.select('.info-salary'):
        salary.append(i.text)
    rango_sal = [item.strip() for item in salary if str(item)]

    # Item
    publish = []
    for i in soup.find_all("span", class_='info-publish-date pull-right'):
        publish.append(i.text)
    publi = [item.strip() for item in publish if str(item)]

    # Link
    url = []
    for i in soup.select('.text-ellipsis'):
        url.append(i.get('href'))

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "js-btn-next")))

        driver.find_element_by_xpath(("//li[@class='']/a[@class='js-btn-next']")).send_keys(Keys.ENTER)
        time.sleep(1.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        puestos.append(items)
        cia.append(empresa)
        rango_salario.append(rango_sal)
        publicacion.append(publi)
        links.append(url)

    except Exception: break

# Last Page

driver.find_element_by_xpath(("//li[@class=' disabled ']/a[@class='js-btn-next']")).send_keys(Keys.ENTER)
time.sleep(1.5)

# Job Name
jobs = []
for i in soup.select('.text-ellipsis'):
    jobs.append(i.text)
puesto_last_page = [item.strip() for item in jobs if str(item)]

# Company
company = []
for i in soup.select('.info-company-name'):
    company.append(i.text)
empresa_last_page = [item.strip() for item in company if str(item)]

# Salary
salary = []
for i in soup.select('.info-salary'):
    salary.append(i.text)
rango_sal_last_page = [item.strip() for item in salary if str(item)]

# item
publish = []
for i in soup.find_all("span", class_='info-publish-date pull-right'):
    publish.append(i.text)
publi_last_page = [item.strip() for item in publish if str(item)]

# Link
url_last_page = []
for i in soup.select('.text-ellipsis'):
    url_last_page.append(i.get('href'))

driver.quit()

# Nested list

ofertas_nested = puestos + puesto_last_page
companias_nested = cia + empresa_last_page
salario_nested = rango_salario + rango_sal_last_page
publi_nested =  publicacion + publi_last_page
links_nested = links + url_last_page

# Converting Nested list into a Flat List

ofertas = []
def flatlist(l):
    for i in l:
        if type(i) == list:
            flatlist(i)
        else:
            ofertas.append(str(unidecode(i)))

flatlist(ofertas_nested)

companias = []
def flatlist_cia(l):
    for i in l:
        if type(i) == list:
            flatlist_cia(i)
        else:
            companias.append(str(unidecode(i)))

flatlist_cia(companias_nested)

salario = []
def flatlist_sal(l):
    for i in l:
        if type(i) == list:
            flatlist_sal(i)
        else:
            salario.append(i)

flatlist_sal(salario_nested)

publicado = []
def flatlist_pub(l):
    for i in l:
        if type(i) == list:
            flatlist_pub(i)
        else:
            publicado.append(i)

flatlist_pub(publi_nested)

link_oferta = []
def flatlist_url(l):
    for i in l:
        if type(i) == list:
            flatlist_url(i)
        else:
            link_oferta.append(i)

flatlist_url(links_nested)


# Adding "http:" to link_oferta

link_oferta_concat = []

for i in link_oferta:
    if not re.findall(r'https:.*',i):
        link_oferta_concat.append(str('https://www.elempleo.com')+i)
    else:
        link_oferta_concat.append(i)

# Validation

print(len(ofertas))
print(len(companias))
print(len(salario))
print(len(publicado))
print(len(link_oferta_concat))


# Converting to Pandas

import pandas as pd

df = pd.DataFrame({'ofertas':ofertas,'Empresa':companias,'Rango_Salario':salario,'Publicado':publicado,'Link':link_oferta_concat})

# Removing 'Publicado'

df.Publicado = df.Publicado.str.replace(r'Publicado ', '')

# Exporting

df.to_csv(r'C:\your_path\4-45.csv', index=False)
