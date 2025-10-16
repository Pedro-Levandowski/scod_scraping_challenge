import requests

class Scraper:
    def __init__(self, base_url: str, timeout: int = 10, session = None):
        self.base_url = base_url
        self.timeout = timeout
        self.session = session

    def fetch_html(self) -> str:
        if self.session == None:
            session = requests.Session()
        else:
            session = self.session
        
        criado = session is not self.session

        try:
            response = session.get(self.base_url, timeout=self.timeout)
        except requests.RequestException as erro:
            raise ValueError(f'Erro de rede ao baixar {self.base_url}') from erro
        status_code = response.status_code
        content_type = response.headers.get("Content-Type", "")

        try:
            if status_code != 200:
                raise ValueError(f'HTTP ({status_code}) ao tentar baixar a URL: {self.base_url} ')
            else:
                if content_type and "html" not in content_type.lower():
                    raise ValueError(f'A url ({self.base_url}) não contém "html"')
                else:
                    return response.text
        finally:
            if criado: session.close() 