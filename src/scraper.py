import requests

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