from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Inicializar o WebDriver com a forma mais simplificada
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

def login(driver, email, password):
    try:
        # Navegar até a página de login do Glassdoor
        driver.get("https://www.glassdoor.com.br/index.htm")

        # Clicar no botão 'Entrar'
        login_button = driver.find_element(By.XPATH, '/html/body/header/div[1]/div/div[2]/div/button')
        login_button.click()

        # Esperar o campo de email ser carregado e inserir o email
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='modalUserEmail']")))
        email_input = driver.find_element(By.XPATH, "//*[@id='modalUserEmail']")
        email_input.send_keys(email)

        # Clicar no botão 'Login com e-mail'
        login_with_email_button = driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[2]/button")
        login_with_email_button.click()

        # Esperar o campo de senha ser carregado e inserir a senha
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='modalUserPassword']")))
        password_input = driver.find_element(By.XPATH, "//*[@id='modalUserPassword']")
        password_input.send_keys(password)

        # Clicar no botão 'Entrar'
        login_button = driver.find_element(By.XPATH, "/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div/div/div/div/div/form/div[2]/button")
        login_button.click()
        
        # Esperar até que a página logada esteja carregada
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ContentNav']/li[2]/a")))

        time.sleep(1)

    except Exception as e:
        print(f"An error occurred during login: {e}")

def busca_empresa(driver, company_name):
    try:
        # Clicar em empresas
        empresas_button = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ContentNav"]/li[2]'))
        )
        empresas_button.click()

        # Esperar o campo de busca ser carregado e inserir o nome da empresa
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='companyAutocomplete-companyDiscover-employerSearch']"))
        )
        search_input.send_keys(company_name)

        # Clicar no botão de buscar empresa
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='Explore']/div[2]/div/div/div[2]/button/span/span"))
        )
        search_button.click()

        # Esperar a página de resultados carregar e clicar em avaliações
        reviews_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='EmpLinksWrapper']/div[2]/div/div[1]/a[2]"))
        )
        reviews_button.click()

        # Clicar em apagar filtros
        reviews_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[1]/div[1]/div[2]/div[1]/a'))
        )
        reviews_button.click()

    except Exception as e:
        print(f"An error occurred during company search: {e}")


# Função para navegar para a próxima página
def ir_para_proxima_pagina(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//button[@data-test='next-page']")
        next_button.click()
        time.sleep(10)
    except Exception as e:
        print(f"An error occurred while navigating to the next page: {e}")


# Função para interpretar a recomendação
def interpretar_recomendacao(svg_element):
    try:
        # Verificar o tipo de elemento SVG
        svg_type = svg_element.tag_name

        # Se for um círculo, significa Sem resposta
        if svg_type == 'circle':
            return 'Sem resposta'
        elif svg_type == 'path':
            # Verificar o atributo 'd' para determinar o tipo de ícone
            path_data = svg_element.get_attribute('d')
            if "M18.299" in path_data:
                return 'Não'
            elif "M8.835" in path_data:
                return 'Sim'
        
        # Se não for nenhum dos casos acima, retornar Neutro
        return 'Neutro'
    except Exception as e:
        print(f"An error occurred while interpreting recommendation: {e}")
        return 'Neutro'
    

# Função para extrair os valores dos atributos "d" ou "x" dos elementos SVG
def extrair_valor_d_ou_x(svg_elements):
    valores = []
    for svg in svg_elements:
        path_elements = svg.find_elements(By.TAG_NAME, 'path')
        rect_elements = svg.find_elements(By.TAG_NAME, 'rect')
        if path_elements:
            primeiro_caminho_d = path_elements[0].get_attribute('d')
            valores.append(primeiro_caminho_d)
        elif rect_elements:
            primeiro_caminho_x = rect_elements[0].get_attribute('x')
            valores.append(primeiro_caminho_x)
        else:
            valores.append('Neutro')
    return valores

# Função para raspar avaliações em várias páginas
def raspar_avaliacoes(driver, num_paginas):
    todas_notas = []
    todos_titulos = []
    todas_datas = []
    todos_cargos = []
    todos_pros = []
    todos_contras = []
    todas_recomendacoes = []
    todas_visoes_mercado = []

    for _ in range(num_paginas):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'review-details_overallRating__Rxhdr')]"))
            )
            
            # Coletar todas as notas das avaliações
            notas_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'review-details_overallRating__Rxhdr')]")
            notas = [nota.text for nota in notas_elements]

            # Coletar todos os títulos das avaliações
            titulos_elements = driver.find_elements(By.XPATH, "//h2[@data-test='review-details-title']/a")
            titulos = [titulo.text for titulo in titulos_elements]

            # Coletar todas as datas das avaliações
            datas_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'timestamp_reviewDate__fBGY6')]")
            datas = [data.text for data in datas_elements]

            # Coletar todos os cargos dos avaliadores
            cargos_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'review-details_employee__MeSp3')]")
            cargos = [cargo.text for cargo in cargos_elements]

            # Coletar todos os pros das avaliações
            pros_elements = driver.find_elements(By.XPATH, "//span[@data-test='review-text-pros']")
            pros = [pro.text for pro in pros_elements]

            # Coletar todos os contras das avaliações
            contras_elements = driver.find_elements(By.XPATH, "//span[@data-test='review-text-cons']")
            contras = [contra.text for contra in contras_elements]

            # Coletar todos os elementos SVG de recomendação
            recomendacao_elements = driver.find_elements(By.XPATH, "//div[@class='review-details_iconContainer__xl07_']//span[contains(@class, 'review-details_ratingTitle__DaJ1N')][contains(text(),'Recomenda')]/parent::div/preceding-sibling::div/span/svg")
            recomendacoes = extrair_valor_d_ou_x(recomendacao_elements)

            # Coletar todos os elementos SVG de visão de mercado
            visao_mercado_elements = driver.find_elements(By.XPATH, "//div[@class='review-details_iconContainer__xl07_']//span[contains(@class, 'review-details_ratingTitle__DaJ1N')][contains(text(),'Visão de mercado da empresa')]/parent::div/preceding-sibling::div/span/svg")
            visoes_mercado = extrair_valor_d_ou_x(visao_mercado_elements)

            # Agregar os dados da página atual aos DataFrames intermediários
            todas_notas.extend(notas)
            todos_titulos.extend(titulos)
            todas_datas.extend(datas)
            todos_cargos.extend(cargos)
            todos_pros.extend(pros)
            todos_contras.extend(contras)
            todas_recomendacoes.extend(recomendacoes)
            todas_visoes_mercado.extend(visoes_mercado)

            # Navegar para a próxima página
            ir_para_proxima_pagina(driver)
        
        except Exception as e:
            print(f"An error occurred during review scraping: {e}")
            continue

    return todas_notas, todos_titulos, todas_datas, todos_cargos, todos_pros, todos_contras, todas_recomendacoes, todas_visoes_mercado

# Exemplo de uso das funções
try:
    email = "paraello01@hotmail.com"
    password = "BHpG.@hU@b9GWva"
    company_name = "Sinqia"

    login(driver, email, password)
    busca_empresa(driver, company_name)
    
    # Raspagem de avaliações em 10 páginas
    num_paginas = 2
    notas, titulos, datas, cargos, pros, contras, recomendacoes, visoes_mercado = raspar_avaliacoes(driver, num_paginas)
    
    # Imprimir a contagem de elementos e listas de valores
    print("Contagem de elementos para 'Recomenda':", len(recomendacoes))
    print("Contagem de elementos para 'Visao_de_Mercado':", len(visoes_mercado))

    print("\nValores encontrados para 'Recomenda':")
    print(recomendacoes)
    print("\nValores encontrados para 'Visao_de_Mercado':")
    print(visoes_mercado)

    # Criar um DataFrame com pandas
    data = {
        'Nota': notas,
        'Título': titulos,
        'Data': datas,
        'Cargo': cargos,
        'Pros': pros,
        'Contras': contras,
        'Recomenda': recomendacoes,
        'Visao_de_Mercado': visoes_mercado
    }
    df = pd.DataFrame(data)
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Aguarde um pouco para visualizar os resultados antes de fechar o navegador
    time.sleep(100)
    driver.quit()
