from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

PATH = r'C:\Users\yuri_\PycharmProjects\Centroestudos\venv\codigos\ProjetoScraping\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://riovagas.com.br/")
search = driver.find_element_by_id("s")
search.send_keys("estágio")
search.send_keys(Keys.RETURN)

def busca():
    try:
        alvo = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-box-inside"))
        )
        artigos = alvo.find_elements_by_tag_name("article")
        for artigo in artigos:
            header = artigo.find_element_by_class_name("entry-title")
            print(header.text)
            link = header.find_elements_by_tag_name("a")
            for l in link:
                print(l.get_attribute('href'))


            tags = artigo.find_elements_by_class_name("entry-meta")
            lista_tags = []
            for tag in tags:
                t = tag.find_elements_by_tag_name("a")
                for index in t:
                    lista_tags.append(index.text)


                data_hora = tag.find_elements_by_class_name("updated")
                lista_date_time = []
                for dh in data_hora:
                    hora_exata = dh.find_elements_by_tag_name("time")
                    for index in hora_exata:
                        lista_date_time.append(index.text)
                print(lista_date_time)
            print(lista_tags)
            print('\n')

    except Exception as e:
        driver.quit()

def pularPagina():
    try:
        navegacao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-box-inside"))
        )
        pages = navegacao.find_elements_by_class_name("page-numbers")
        for index, page in enumerate(pages):
            if index == (len(pages) - 1):
                page.click()

    except Exception as e:
        driver.quit()

def main():
    for index in range(0,4):
        print(f"busca página {index + 1}")
        busca()
        pularPagina()
        print()
    driver.quit()


main()