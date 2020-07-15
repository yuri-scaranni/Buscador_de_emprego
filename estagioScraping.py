from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time, datetime

#Caminho para exe do framework, voltado para chrome
PATH = r'C:\Users\yuri_\PycharmProjects\Centroestudos\venv\codigos\ProjetoScraping\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# Site que será visitado
driver.get("https://riovagas.com.br/")

# Encontrando elemento de 'busca' no html
search = driver.find_element_by_id("s")
# Passando palavra de pesquisa
search.send_keys('estágio')
search.send_keys(Keys.RETURN)

# função para dividir uma lista grande em listas pequenas com N itens.
def dividir_lista(lista, lista_fim):
    n = 5
    tamanho = len(lista)
    for x in range(n):
        inicio = int(x * tamanho / n)
        fim = int((x + 1) * tamanho / n)
        lista_fim.append(lista[inicio:fim])
    return lista_fim


# função que busca os dados e retorna uma lista[N-listas] com os dados
def busca():
    lista_vagas = []
    vagas = []
    try:
        # Acrescentando uma espera de 20s até a classe passada aparecer no browser.
        alvo = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-box-inside"))
        )
        # Atribuindo à váriavel as tags
        artigos = alvo.find_elements_by_tag_name("article")

        #LOOP nos artigos da página
        for artigo in artigos:
            # Pegando título da vaga do artigo
            header = artigo.find_element_by_class_name("entry-title")
            # Pegando hiperlink do artigo
            link = header.find_elements_by_tag_name("a")
            # Pegando hora e data da postagem de cada artigo
            hora_exata = artigo.find_elements_by_tag_name("time")

            #LOOP p/ pegar 'tags'/'palavras-chave' presentes em cada artigo
            tags = artigo.find_elements_by_class_name("entry-meta")
            lista_tags = []
            for tag in tags:
                t = tag.find_elements_by_tag_name("a")
                for index in t:
                    lista_tags.append(index.text)

            # Inserindo os dados retirados do artigo em uma lista com quebra de linha
            vagas.append(hora_exata[0].text)
            vagas.append(header.text)
            vagas.append(link[0].get_attribute('href'))
            vagas.append(lista_tags)
            vagas.append('\n')

        # Instanciando variavel que recebe função para 'splitar' os artigos da página
        # Fazendo de 1 lista, N listas, cada lista sendo uma postagem.
        listagem = (dividir_lista(vagas, lista_vagas))
        return listagem

    except Exception as e:
        print(e)
        driver.quit()


# Função para passar página
def pularPagina():
    try:
        # Acrescentando uma espera de 10s até a classe passada aparecer no browser.
        navegacao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-box-inside"))
        )
        # Atribuindo à váriavel a lista de html onde se encontra o botão para
        # troca de pages.
        pages = navegacao.find_elements_by_class_name("page-numbers")
        for index, page in enumerate(pages):
            if index == (len(pages) - 1):
                page.click()

    except Exception as e:
        driver.quit()

# Função para atribuir data ao titulo do arquivo txt
def titulo():
    return str(datetime.datetime.today())[:10] + '.txt'


def main():
    # Abrindo/criando arquivo de texto
    with open(f'{titulo()}', 'w+', encoding='utf8') as arq:
        # LOOP de páginas a serem navegadas
        for index in range(0, 2):
            texto = f'***VAGAS BUSCADAS HOJE, PÁGINA {index}***\n\n'
            print(f"busca página {index + 1}")
            arq.write(texto)
            # Instanciando a função de busca pelos dados
            # O retorno dessa função é uma matriz de dados
            vag = busca()
            #LOOPANDO a matriz como um todo
            for indice in vag:
                #LOOPANDO as listas(arrays) presentes na matriz
                for i in indice:
                    # Gravando no txt
                    arq.write(str(i))
                    arq.write('\n')
            pularPagina()
        driver.quit()

main()




