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

                print(f'[BAIXANDO] {codigo_linha} -> {destino}')
                downloader.download_pdf(linha['boleto_url'], str(destino), sobrescrever=False, verificar_pdf=True)

                linha_formatada, linha_compactada = extractor.extrair_linha_digitavel_do_pdf(destino)

                linha['boleto_url'] = destino.as_posix()
                linha['linha_digitavel'] = linha_formatada

                linha.pop('codigo_linha', None)

                with destino.open('rb') as arquivo:
                    assert arquivo.read(5).startswith(b'%PDF-'), f'Arquivo corrompido: {destino}'
                print(f'[SUCESSO] O arquivo {destino} foi baixado!')
                ok += 1

            except Exception as erro:
                falhas += 1
                print(f'[ERRO]: {linha.get('codigo_linha')} -> {erro}')
        
        print(f'[RESUMO]: sucesso: {ok} | falhas: {falhas} | total: {total_linhas}')

        Path('data').mkdir(exist_ok=True)
        Path('data/dados.json').write_text(
            json.dumps(linhas, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

        print("[DADOS]: [OK]: data/dados.json gerado.")