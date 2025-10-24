from pathlib import Path
import json, requests

from src.scraper import Scraper
from src.downloader import Downloader
from src.extractor import Extractor

if __name__ == '__main__':
    BASE_URL = 'https://arth-inacio.github.io/scod_scraping_challenge/' #define a URL base para a extração de dados

    with requests.Session() as s: #executa o código abaixo levando em consideração que a Session criada está na variável s
        scraper = Scraper(BASE_URL, timeout=10, session=s) #Instancia um Scraper utilizando URL base definida, seta um timeout de 10s e usa a session s
        downloader = Downloader(timeout=15, max_tentativas=2, session=s) #instancia um Downloader setando um timeout de 15s, maximo de tentativas = 2 e usa a session s
        extractor = Extractor() #instancia um Extractor

        html = scraper.fetch_html() #baixa o código HTML utilzando a função fetch_html() da classe Scraper e atribui à variável html
        linhas = scraper.analisar_linhas_tabela(html) #atribui os dados das linhas a variável linhas
        assert linhas, "Nenhuma linha encontrada na tabela." #garante que ao menos uma linha tenha sido encontrada

        total_linhas = len(linhas) #pega o total de linhas com dados retornadas e atribui à variável total_linhas
        ok = 0 #cria a variável ok que inicialmente será 0
        falhas = 0 #cria a variável falhas que inicialmente será 0

        for linha in linhas: #percorre um conjunto de dados das linhas por vez
            try: #tenta executar o bloco de código abaixo
                codigo_linha = linha['codigo_linha'] #pega o codigo_linha dos dados da linha extraida e atribui à variável codigo_linha
                nome_arquivo = f'{codigo_linha}.pdf'  #cria uma variável nome_arquivo e define como sendo o código da linha com a extensão .pdf
                destino = Path('boletos') / nome_arquivo #define que o destino do arquivo será a pasta boletos e o arquivo terá o nome definido acima

                print(f'[BAIXANDO] {codigo_linha} -> {destino}') #imprime na tela que o boleto da linha em questão está sendo baixado
                downloader.download_pdf(linha['boleto_url'], str(destino), sobrescrever=False, verificar_pdf=True) #utiliza a função download_pdf() da classe Downloader para baixar o pdf da linha em questão no destino predefinido, sem sobrescrever e verificando se o que está sendo baixado realmente é PDF

                linha_formatada, linha_compactada = extractor.extrair_linha_digitavel_do_pdf(destino) #utiliza a função extrair_linha_digitavel_do_pdf() da classe Extractor para extrair a linha digitável do PDF baixado acima buscando pelo destino onde ele está instalado, logo em seguida ele atribui a linha digitável à variável linha_formatada e apenas os digitos da linha digitável à variável linha_compactada

                linha['boleto_url'] = destino.as_posix() #define que o dado 'boleto_url' seja o caminho onde foi baixado o boleto
                linha['linha_digitavel'] = linha_formatada #cria um dado da linha que é a linha_digitável e atribui a variável linha_formatada a esse dado 

                linha.pop('codigo_linha', None) #tira o codigo_linha dos dados da linha, porque a intenção é que ele não apareça no JSON final, apesar de ter sido útil durante a execução do código

                with destino.open('rb') as arquivo: #o arquivo baixado no destino é aberto e atribuido a variavel arquivo e executa o código abaixo
                    assert arquivo.read(5).startswith(b'%PDF-'), f'Arquivo corrompido: {destino}' #Garante que o arquivo baixado realmente é um PDF
                print(f'[SUCESSO] O arquivo {destino} foi baixado!') #imprime uma mensagem de sucesso caso o arquivo em questão foi baixado corretamente e realmente é um PDF
                ok += 1 #Incrementa 1 à variável ok

            except Exception as erro: #em caso de falha na execução do bloco try, incrementa 1 e imprime na tela que deu erro no download da linha, também especifica qual erro foi
                falhas += 1
                print(f"[ERRO]: {linha.get('codigo_linha')} -> {erro}")
        
        print(f'[RESUMO]: sucesso: {ok} | falhas: {falhas} | total: {total_linhas}') #Ao sair do laço for, imprime um resumo informando quantos arquivos foram baixados corretamente, quantos falharam e o total de arquivos

        Path('data').mkdir(exist_ok=True) #Garante que a pasta data exista (Cria se necessário)
        Path('data/dados.json').write_text( #Garante que dados.json exista dentro da pasta data e escreve todos os dados extraidos dentro do documento dados.json
            json.dumps(linhas, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        print("[DADOS]: [OK]: data/dados.json gerado.") #Imprime que o dados.json foi gerado com sucesso