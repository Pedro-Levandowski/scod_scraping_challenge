from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from src.utils import analisar_data, analisar_valor


class Scraper:
    def __init__(self, base_url: str, timeout: int = 10, session = None):
        self.base_url = base_url
        self.timeout = timeout
        self.session = session

    def fetch_html(self) -> str:
        """
            Baixa o HTML do self.url_base usando um timeout adequado
            Valida se o status retornado = 200 = OK
            Valida se o Content-Type possui 'html'
            Em caso de falhas retorna um ValueError claro
            Retorna o conteúdo HTML baixado 'response.text'
        """
        if self.session is None: #caso a classe Scraper ainda não possua uma Session em aberto será criado uma Session na variável session.
            session = requests.Session()
        else: #caso a classe Scraper já possua uma Session em aberto, a variável session irá receber a Session em aberto.
            session = self.session
        
        criado = session is not self.session #aqui a variável receberá True quando a session foi criada localmente e False quando a session já estava criada e não foi necessário criar uma nova. Isso irá ajudar no fim pois caso a session tenha sido aberta localmente a boa prática a ser seguida é fechá-la também localmente.

        try: #Tenta-se executar o código dentro desse bloco
            response = session.get(self.base_url, timeout=self.timeout) #utilizando a session (criada ou antes já existente) a variável response lança uma requisição GET para uma determinada URL base e armazena o retorno, utiliza um timeout pré-definido na própria classe. Esse timeout é importante para evitar carregamento infinito, limita a resposta a um certo tempo definido, no caso da classe Scraper esse timeout está definido como 10s.

            status_code = response.status_code # a variável status_code está armazenado o código que a requisição GET retornou, sendo 200 = OK.
            content_type = response.headers.get("Content-Type", "") # a variável content_type armazena o tipo de conteúdo presente no cabeçalho dessa requisição GET, no caso desse desafio estamos procurando o tipo HTML.

            if status_code != 200: # Esse if verifica se o código retornado pela requisição GET é diferente de 200 (como citado acima 200 = OK), caso seja, um erro é lançado.
                raise ValueError(f'HTTP ({status_code}) ao tentar baixar a URL: {self.base_url} ')
            elif content_type and "html" not in content_type.lower(): #Caso a condição acima seja falsa, será verificado se o tipo de conteudo retornado é HTML, caso não seja outro erro será lançado.
                raise ValueError(f'A url ({self.base_url}) não contém "html"')
            else: #Caso nenhuma das duas condições acima sejam verdadeiras, ou seja, está tudo certo com a requisição, será retornado o conteúdo da requisição GET, que é justamente a intenção da função fetch_html, "pegar" o código HTML.
                return response.text
                
        except requests.RequestException as erro: #Caso ocorra algum erro, ou o erro seja lançado dentro do bloco TRY, esse bloco será acionado para facilitar o entendimento do erro causado e não quebrar o script
            raise ValueError(f'Erro de rede ao baixar {self.base_url}: {erro.__class__.__name__}') from erro
        
        finally: #Ao final de tudo o código verifica se criado = True ou False, caso True, ele fecha a sessão criada, caso contrário, não há necessidade de fechar, pois se trata da Session da própria classe Scraper e não uma session criada localmente
            if criado: session.close()

    def analisar_linhas_tabela(self, html: str):
        """
            Transforma o HTML em uma árvore
            Seleciona as linhas da tabela
            Extrai os dados das linhas
            Retorna os dados de todas as linhas da tabela
        """
        try: #a função tentará executar o código abaixo
            soup = BeautifulSoup(html, "html.parser") #transforma o HTML baixado em fetch_html em uma árvore
            seletor = 'tr[data-cod_lancamento]' #define qual será o atributo CSS que irá diferenciar as linhas
            linhas = soup.select(seletor) #seleciona todas as linhas que tenham o seletor definido acima
            dados = [] #cria uma lista para armazenar os dados extraidos de cada linha
             
            if not linhas: #caso não possuam linhas a serem extraidas um ValueError será lançado especificando o que deu errado
                raise ValueError(f'A tabela está vazia ou então o seletor {seletor} está errado!')
            

            for idx, linha in enumerate(linhas, start=1): #cria um laço de repetição que pegará uma das linhas selecionadas acima por vez, baseado no index que irá ser incrementado 1 por 1 até percorrer todas as linhas da tabela
                colunas = linha.select("td") #seleciona todas as colunas da linha do index

                if not len(colunas) == 7: #se a linha do index não retornar exatamente 7 colunas será lançado um ValueError especificando o erro
                    raise ValueError(f'Linha #{idx}: Eram esperadas 7 colunas, foram encontradas {len(colunas)} colunas')
                
                descricao = colunas[0].get_text(strip=True) #atribui a primeira coluna à variável descricao
                exercicio = int(colunas[1].get_text(strip=True).replace("\xa0", " ")) #trata possíveis erros de formatações e atribui a segunda coluna à variável exercicio
                parcela = colunas[2].get_text(strip=True) #atribui a terceira coluna à variável parcela
                vencimento = analisar_data(colunas[3].get_text(strip=True)) #formata a data extraida da quarta ao formato (yyyy-mm-dd) utilizando a função analisar_data de src/utils.py e atribui à variável vencimento
                valor = analisar_valor(colunas[4].get_text(strip=True)) #formata o valor extraido da quinta coluna a float utilizando a função analisar_valor de src/utils.py e atribui à variável valor
                status = colunas[5].get_text(strip=True).replace("\xa0", " ") #trata possíveis erros de formatações e atribui a sexta coluna à variável status 

                if not status in {'Pago', 'Vencido', 'A vencer'}: #verifica se status é exatamente 'Pago', 'Vencido' ou 'A vencer', caso não seja lança um ValueError epecificando o erro
                    raise ValueError(f'Linha #{idx}: status inválido ({status})')
                
                link = colunas[6].select_one('a[href$=".pdf"]') #seleciona a tag a que contenha um link que termina com '.pdf' da coluna 7 e atribui à variável link

                if link is None: #verifica se algum link foi selecionado acima e caso não tenha sido lança um ValueError especificando o erro
                    raise ValueError(f'Linha #{idx}: link .pdf não foi encontrado!') 
                
                href = link.get("href", "").strip() #pega o atributo href da tag a atribuida a variável link e remove possíveis espaços tanto no início quanto no fim dessa string
                boleto_url = urljoin(self.base_url, href)   #transforma a URL relativa href na URL absoluta que leva ao link do boleto em questão usando a URL base do site, já definida na classe Scraper

                dado = { #cria os dados da linha e atribui as variáveis criadas acima a seu respectivo campo
                    "descricao": descricao,
                    "exercicio": exercicio,
                    "parcela": parcela,
                    "vencimento": vencimento,
                    "valor": valor,
                    "status": status,
                    "boleto_url": boleto_url
                }
                dados.append(dado) #adiciona os dados da linha à lista de dados

            return dados #retorna os dados de todas as linhas extraidas
        except ValueError as erro: #em caso de erro na tentativa de executar o bloco de código acima, um ValueError será lançado especificando o erro em questão
            raise ValueError(f'Erro ao extrair linhas da tabela. Detalhes: {erro}') from erro