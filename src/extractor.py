from pathlib import Path
import pdfplumber

from src.utils import formatar_minuscula, apenas_digitos, proxima_linha_nao_vazia

class Extractor:
    def __init__(self):
        pass

    def extrair_texto(self, caminho_pdf: str | Path) -> str:
        """
            Lê todo o texto do PDF e concatena o texto de todas as páginas com quebra de linhas
        """
        caminho_pdf = Path(caminho_pdf)
        if not caminho_pdf.exists():
            raise ValueError(f'PDF não encontrado: {caminho_pdf}')
        
        textos = []
        
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                textos.append(pagina.extract_text() or "")
        return "\n".join(textos)
    
    def extrair_linha_digitavel_do_texto(self, raw_texto: str) -> tuple[str, str]:
        """
            Encontra a 'linha digitável' usando o rótulo no texto bruto.
            Retorna (linha_formatada, linha compacta)
            Se houver conteúdo após ':' na mesma linha do rótulo, utiliza esse conteúdo
            Senão, usa a próxima linha não vazia
        """
        linhas = [linha.rstrip() for linha in raw_texto.splitlines()]

        if not linhas:
            raise ValueError("Texto vazio!")
        
        for i, linha in enumerate(linhas):
            rotulo = formatar_minuscula(linha)
            if 'linha digitavel' in rotulo:
                if ':' in linha:
                    apos = linha.split(':', 1)[1].strip()
                    if apos:
                        linha_formatada = ' '.join(apos.split())
                        return linha_formatada, apenas_digitos(linha_formatada)

                proxima = proxima_linha_nao_vazia(linhas, i)
                
                if proxima:
                    linha_formatada = ' '.join(proxima.split())
                    return linha_formatada, apenas_digitos(linha_formatada)
                
                raise ValueError("Rótulo encontrado, mas não há valor após ele!")
        raise ValueError("Rótulo 'Linha digitável' não encontrado!")
    
    def extrair_linha_digitavel_do_pdf(self, caminho_pdf: str | Path) -> tuple [str, str]:
        """
            Atalho que já extrai texto do caminho onde o pdf está e logo em seguida extrai a linha digitavel do texto do pdf utlizando as funções criadas acima
        """
        raw = self.extrair_texto(caminho_pdf) #define o texto extraido do pdf na variável raw
        return self.extrair_linha_digitavel_do_texto(raw) #a função retorna a linha digitável presente no texto extraido do PDF (boleto)