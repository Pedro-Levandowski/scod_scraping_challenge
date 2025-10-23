from typing import Optional
from pathlib import Path
import os, time
import requests

class Downloader:
    def __init__(self, timeout:int = 15, max_tentativas:int = 2, session:Optional[requests.Session] = None): #metodo construtor da classe Downloader
        self.timeout = timeout
        self.max_tentativas = max_tentativas
        self.session = session
    
    def download_pdf(self, url:str, caminho_destino:str, sobrescrever:bool = False, verificar_pdf:bool = True) -> str: #Cria a função download_pdf que recebe alguns parametros
        """
            Baixa um PDF em streaming (chunk a chunk) com retries para erros 5xx/RequestException.
            Se verificar_pdf=True, valida o conteúdo: aceita Content-Type com 'pdf' OU assinatura '%PDF-' no 1º chunk.
            Grava primeiro em <dest>.tmp e depois move de forma atômica para caminho_destino.
            Idempotente: se o arquivo já existe e sobrescrever/overwrite=False, retorna imediatamente.
        """

        if not sobrescrever and Path(caminho_destino).exists(): #Caso não deseje sobreescrever e já exista o caminho do destino a função já retorna o caminho do destino existente
            return caminho_destino

        Path(caminho_destino).parent.mkdir(parents=True, exist_ok=True) #garante que o diretório pai existe (cria se necessário)
            
        
        if self.session is None: #caso a classe Downloader ainda não possua uma session, será atribuida uma nova session a variável session
            session = requests.Session()
        else: #caso contrário, a session já existente que será atribuida a variável session
            session = self.session

        criado = session is not self.session #caso a session tenha sido criada localmente, a variável criado será True, se já existia antes será False

        tmp_path = None #cria uma variável para definir um caminho temporário

        try: #tenta executar o bloco de código abaixo
            for tentativa in range(self.max_tentativas + 1): #verifica se a tentativa atual fere o máximo de tentativas
                try: #tenta executar o bloco de código abaixo

                    with session.get(url, timeout=self.timeout, stream=True) as response: #tenta fazer um get em um URL definido como parametro, timeout definido na classe e com stream que baixa gradualmente o conteudo do PDF (chunk a chunk) e salva na variável response
                        status_code = response.status_code #Pega o código de status da requisição get feita acima e salva na variável status_code

                        if status_code != 200: #Verifica se o código é diferente de 200 (200 = OK)
                           
                            if status_code in {500, 502, 503, 504} and tentativa < self.max_tentativas: #caso o código realmente seja diferente de 200, que é o único aceitável, realiza outra verificação, dessa vez, vai ver se o código de erro retornado é 500, 502, 503 ou 504 e se for algum desses e a tentativa atual for menor do que o máximo de tentativas irá tentar fazer a requisição GET novamente 
                                time.sleep(1 * (tentativa + 1))
                                continue
                            raise ValueError(f'HTTP ({status_code}) ao tentar baixar a URL: {url}') #Caso não se enquadre nos códigos 5xx acima ou tenha excedido o máximo de tentativas, um ValueError será lançado especificando o erro em questão

                        #caso o get seja bem sucedido, o código abaixo será executado

                        tmp_path = f"{caminho_destino}.tmp" #define o caminho temporário sendo o caminho de destino padrão com a extensão .tmp (que define que o arquivo é temporário) e atribui a variável tmp_path
                        salvou_algo = False #cria a variável salvou_algo e define inicialmente como False pois nada foi salvo ainda

                        content_type = response.headers.get("Content-Type", "").lower() #pega o Content-Type do cabeçalho da requisição GET feita, já deixa em letras minúsculas e salva na variável content_type

                        with open(tmp_path, "wb") as arquivo: #cria um arquivo no caminho temporário para escrita binária 'wb' usando a variável arquivo
                            primeiro_chunk = None #cria uma variável para armazenar o primeiro chunk (bloco de bytes) que chegar da resposta HTTP, inicialmente None, pois ainda não capturou nada

                            for chunk in response.iter_content(chunk_size=65536): #cria um laço que percorre os chunks em blocos de tamanho 65536 bytes e enquanto não percorrer tudo executa o bloco de código abaixo
                                if not chunk: #se não tiver chunk na iteração retorna ao laço for
                                    continue

                                if primeiro_chunk is None: #caso não tenha primeiro chunk ainda, vai salvar o chunk atual na variável primeiro_chunk
                                    primeiro_chunk = chunk

                                    if verificar_pdf: #verifica se no parâmetro da função foi passado que deve ser verificado se é PDF
                                        if 'pdf' not in content_type and not primeiro_chunk.startswith(b'%PDF-'): #verifica se é PDF e caso não seja lança um ValueError especificando o erro
                                            raise ValueError(f'O conteúdo não aparenta ser PDF (Content-Type = {content_type})')
                                        
                                    arquivo.write(primeiro_chunk) #salva o primeiro chunk no arquivo
                                    salvou_algo = True #altera o valor de salvou_algo para True, pois o primeiro chunk foi salvo no arquivo
                                    continue #retorna ao laço for

                                arquivo.write(chunk) #salva o chunk atual no arquivo
                                salvou_algo = True #define como True o valor de salvou_algo

                        if not salvou_algo: #após o laço for verifica se salvou algo e caso não tenha, lança um ValueError especificando o erro
                            raise ValueError("Download vazio (0 bytes)")

                        os.replace(tmp_path, caminho_destino) #depois de já ter salvo em um arquivo temporário, se chegou até esse ponto, significa que está ok o arquivo, então o .tmp é tirado do arquivo e ele fica pronto
                        return caminho_destino #a função retorna o caminho do arquivo

                except requests.RequestException as erro: #Em caso de erro na execução do try, verifica-se se a tentativa atual excedeu o limite de tentativas definido, caso ainda não tenha, tenta novamente, caso contrário lança um ValueError especificando o erro
                    if tentativa < self.max_tentativas:
                        time.sleep(1 * (tentativa + 1))  
                        continue
                    raise ValueError(f'Erro de rede ao baixar {url}: {erro.__class__.__name__}') from erro
            raise ValueError(f"Falha ao baixar {url} após {self.max_tentativas + 1} tentativas") #lança um erro geral avisando que depois de tantas tentativas não foi póssível baixar
        
        except Exception: #caso ocorra erro no bloco try relacionado a esse except, o sistema tentará remover o arquivo temporário criado. Caso esse arquivo nem tenha sido criado vai ignorar e lançar o erro necessário.
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            raise

                   
        finally: #Ao final de tudo, caso a sessão tenha sido criada localmente, irá fechar, pois é uma boa prática que quem abre uma sessão deve fechá-la
            if criado: session.close()
            