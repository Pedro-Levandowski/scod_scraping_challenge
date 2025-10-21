from typing import Optional
from pathlib import Path
import os, time
import requests

class Downloader:
    def __init__(self, timeout:int = 15, max_tentativas:int = 2, session:Optional[requests.Session] = None):
        self.timeout = timeout
        self.max_tentativas = max_tentativas
        self.session = session
    
    def download_pdf(self, url:str, caminho_destino:str, overwrite:bool = False, verificar_pdf:bool = True) -> str:
        if not overwrite and Path(caminho_destino).exists():
            return caminho_destino

        Path(caminho_destino).parent.mkdir(parents=True, exist_ok=True)
            
        
        if self.session is None:
            session = requests.Session()
        else:
            session = self.session

        criado = session is not self.session

        tmp_path = None 

        try:
            for tentativa in range(self.max_tentativas + 1):
                try:
                    # FECHA AUTOMATICAMENTE ao sair do bloco
                    with session.get(url, timeout=self.timeout, stream=True) as response:
                        status_code = response.status_code

                        if status_code != 200:
                            # retry só para 5xx
                            if status_code in {500, 502, 503, 504} and tentativa < self.max_tentativas:
                                time.sleep(1 * (tentativa + 1))
                                continue
                            raise ValueError(f'HTTP ({status_code}) ao tentar baixar a URL: {url}')

                        # --- salvar com segurança em .tmp ---
                        tmp_path = f"{caminho_destino}.tmp"
                        salvou_algo = False

                        with open(tmp_path, "wb") as arquivo:
                            for chunk in response.iter_content(chunk_size=65536):
                                if not chunk:
                                    continue

                                arquivo.write(chunk)
                                salvou_algo = True

                        if not salvou_algo:
                            raise ValueError("Download vazio (0 bytes)")

                        os.replace(tmp_path, caminho_destino)
                        return caminho_destino

                except requests.RequestException as erro:
                    if tentativa < self.max_tentativas:
                        time.sleep(1 * (tentativa + 1))   # 1s, 2s, 3s...
                        continue
                    raise ValueError(f'Erro de rede ao baixar {url}: {erro.__class__.__name__}') from erro
            raise ValueError(f"Falha ao baixar {url} após {self.max_tentativas + 1} tentativas")
        
        except Exception:
            try:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception:
                pass
            raise

                   
        finally:
            if criado: session.close()
            