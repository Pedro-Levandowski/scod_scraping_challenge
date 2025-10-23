from pathlib import Path
import json, requests

from src.scraper import Scraper
from src.downloader import Downloader
from src.extractor import Extractor

if __name__ == '__main__':
    BASE_URL = 'https://arth-inacio.github.io/scod_scraping_challenge/'

    with requests.Session() as s:
        scraper = Scraper(BASE_URL, timeout=10, session=s)
        downloader = Downloader(timeout=15, max_tentativas=2, session=s)
        extractor = Extractor()

        html = scraper.fetch_html()
        linhas = scraper.analisar_linhas_tabela(html)
        assert linhas, "Nenhuma linha encontrada na tabela."

        total_linhas = len(linhas)
        ok = 0
        falhas = 0

        for linha in linhas:
            try:
                codigo_linha = linha['codigo_linha']
                nome_arquivo = f'{codigo_linha}.pdf'
                destino = Path('boletos') / nome_arquivo

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