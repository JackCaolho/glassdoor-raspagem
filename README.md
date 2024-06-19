<h1>Glassdoor Review Scraper</h1>

<p>Este projeto utiliza Selenium para automatizar a coleta de avaliações de empresas no Glassdoor. As avaliações coletadas incluem nota, título, data, cargo, tempo de trabalho, prós e contras. Os dados são então armazenados em um arquivo Excel.</p>

<h2>Pré-requisitos</h2>
<ul>
    <li>Python 3.x</li>
    <li>Selenium</li>
    <li>ChromeDriver</li>
    <li>Pandas</li>
    <li>openpyxl</li>
</ul>

<h2>Instalação</h2>
<ol>
    <li>Instale o Selenium e o Pandas:
        <pre><code>pip install selenium pandas openpyxl</code></pre>
    </li>
    <li>Baixe o <a href="https://sites.google.com/a/chromium.org/chromedriver/downloads">ChromeDriver</a> e certifique-se de que ele está no seu PATH ou forneça o caminho correto ao inicializar o <code>Service</code>.
    </li>
</ol>

<h2>Estrutura do Código</h2>

<h3>Inicialização do WebDriver</h3>
<p>O WebDriver é inicializado com as opções necessárias para maximizar a janela do navegador.</p>
<pre><code>service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
</code></pre>

<h3>Função de Login</h3>
<p>A função <code>login</code> faz login na conta do Glassdoor com as credenciais fornecidas.</p>
<pre><code>def login(driver, email, password):
    # Código de login ...
</code></pre>

<h3>Função de Busca de Empresa</h3>
<p>A função <code>busca_empresa</code> procura por uma empresa específica no Glassdoor e navega até a página de avaliações.</p>
<pre><code>def busca_empresa(driver, company_name):
    # Código de busca ...
</code></pre>

<h3>Função para Navegar para a Próxima Página</h3>
<p>A função <code>ir_para_proxima_pagina</code> navega para a próxima página de avaliações.</p>
<pre><code>def ir_para_proxima_pagina(driver):
    # Código para ir para a próxima página ...
</code></pre>

<h3>Função para Raspar Avaliações</h3>
<p>A função <code>raspar_avaliacoes</code> coleta as avaliações de várias páginas e retorna os dados coletados.</p>
<pre><code>def raspar_avaliacoes(driver, num_paginas):
    # Código para raspar avaliações ...
</code></pre>

<h3>Exemplo de Uso</h3>
<p>Um exemplo de como usar as funções definidas para realizar a raspagem de dados e salvar os resultados em um arquivo Excel.</p>
<pre><code>try:
    driver = webdriver.Chrome()
    email = "seu_email@example.com"
    password = "sua_senha"
    company_name = "Nome da Empresa"

    login(driver, email, password)
    busca_empresa(driver, company_name)
    
    num_paginas = 10
    notas, titulos, datas, cargos, tempos, pros, contras = raspar_avaliacoes(driver, num_paginas)
    
    data = {
        'Nota': notas,
        'Título': titulos,
        'Data': datas,
        'Cargo': cargos,
        'Tempo do Funcionário': tempos,
        'Pros': pros,
        'Contras': contras
    }
    df = pd.DataFrame(data)
    df.to_excel('avaliacoes.xlsx', index=False)
    print(df)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    time.sleep(600)
    driver.quit()
</code></pre>

<h2>Conclusão</h2>
<p>Este projeto automatiza a coleta de avaliações de empresas no Glassdoor, permitindo a análise dos dados para obter insights sobre a percepção dos funcionários em relação à empresa. É um exemplo prático de como utilizar Selenium para web scraping e Pandas para manipulação de dados.</p>
