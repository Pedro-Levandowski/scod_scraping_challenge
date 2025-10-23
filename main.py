from pathlib import Path
import json, requests

from src.scraper import Scraper
from src.downloader import Downloader

if __name__ == '__main__':
    BASE_URL = 'https://arth-inacio.github.io/scod_scraping_challenge/'

    with requests.Session() as s:
        scraper = Scraper(BASE_URL, timeout=10, session=s)
        downloader = Downloader(timeout=15, max_tentativas=2, session=s)

        html = scraper.fetch_html()
        rows = scraper.analisar_linhas_tabela(html)
        assert rows, "Nenhuma linha encontrada na tabela."

        # MICRO-TESTE: só 1 boleto
        rows = rows[:1]
        item = rows[0]
        assert "codigo_linha" in item, "Faltou incluir 'codigo_linha' no dict!"

        dest = Path("boletos") / f"{item['codigo_linha']}.pdf"
        print(f"[TESTE] Baixando {item['boleto_url']} -> {dest}")
        downloader.download_pdf(item["boleto_url"], str(dest), overwrite=False, verificar_pdf=True)

        # Ajusta para caminho local e remove o PK do JSON final (se quiser manter, comente a linha abaixo)
        item["boleto_url"] = dest.as_posix()
        item.pop("codigo_linha", None)

        Path("data").mkdir(exist_ok=True)
        Path("data/dados.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # Sanity checks
        assert dest.exists(), "PDF não foi criado."
        size = dest.stat().st_size
        print(f"[TESTE] Tamanho do PDF: {size} bytes")
        assert size > 0, "Download vazio (0 bytes)."
        with dest.open("rb") as f:
            head = f.read(5)
        print(f"[TESTE] Assinatura: {head!r}")
        assert head.startswith(b"%PDF-"), "Arquivo não começa com %PDF-."

        print("[TESTE] OK — PDF salvo e JSON gerado.")
    