from src.scraper import Scraper

if __name__ == '__main__':
    site_teste = Scraper('https://arth-inacio.github.io/scod_scraping_challenge/', 10)

    html = site_teste.fetch_html()

    print("len:", len(html))
    print(html[:120].replace("\n", " "))
    