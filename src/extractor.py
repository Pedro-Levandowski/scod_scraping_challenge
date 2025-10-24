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
        caminho_pdf = Path(caminho_pdf) #Atribui o caminho do pdf que se deseja extrair o texto na variável caminho_pdf
        if not caminho_pdf.exists(): #Caso o caminho do pdf passado como parâmetro não exista, lança um ValueError especificando o erro
            raise ValueError(f'PDF não encontrado: {caminho_pdf}')
        
        textos = [] #Cria a lista textos, inicialmente vazia
        
        with pdfplumber.open(caminho_pdf) as pdf: #abre o pdf que está no caminho passado como parâmetro e salva na variável pdf
            for pagina in pdf.pages: #esse laço for percorre as páginas que existem no pdf em questão
                textos.append(pagina.extract_text() or "") #extrai o texto da página da vez na iteração e adiciona a lista textos
        return "\n".join(textos) #a função retorna uma string concatenando os conteúdos extraídos (páginas) com quebra de linhas
    
    def extrair_linha_digitavel_do_texto(self, raw_texto: str) -> tuple[str, str]:
        """
            Encontra a 'linha digitável' usando o rótulo no texto bruto.
            Retorna (linha_formatada, linha compacta)
            Se houver conteúdo após ':' na mesma linha do rótulo, utiliza esse conteúdo
            Senão, usa a próxima linha não vazia
        """
        linhas = [linha.rstrip() for linha in raw_texto.splitlines()] #pega o texto (de algum PDF) passado como parâmetro e usa o splitlines() separar ele linha por linha, cada linha passará por um rstrip() que irá tirar possíveis espaços a direita e depois, uma por uma será salva na lista linhas

        if not linhas: #caso nenhuma linha seja salva na lista linhas um ValueError será lançado especificando o erro
            raise ValueError("Texto vazio!")
        
        for i, linha in enumerate(linhas): #cria um for que vai de linha em linha e conta a linha que está na variável i
            rotulo = formatar_minuscula(linha) #utiliza a função formatar_minuscula criada em utils.py para tratar possíveis caracteres especiais e transformar a linha toda para minúscula
            if 'linha digitavel' in rotulo: #verifica se a linha atual possui 'linha digitavel'
                if ':' in linha: #caso a condição acima seja verdadeira, verifica se depois de 'linha digitavel' tem texto na frente, caso possua, essa será a linha digitável
                    apos = linha.split(':', 1)[1].strip()
                    if apos:
                        linha_formatada = ' '.join(apos.split())
                        return linha_formatada, apenas_digitos(linha_formatada) #a função retorna a linha formatada e compactada caso esteja ainda na mesma linha de 'linha digitavel'

                proxima = proxima_linha_nao_vazia(linhas, i) #pega a próxima linha não vazia após a linha que possui 'linha digitavel'
                
                if proxima: #caso ache uma proxima linha com conteudo, essa será a linha digitavel
                    linha_formatada = ' '.join(proxima.split())
                    return linha_formatada, apenas_digitos(linha_formatada) # a função retorna a linha formatada e compactada caso esteja na próxima linha com conteúdo
                
                raise ValueError("Rótulo encontrado, mas não há valor após ele!") #lança erro caso saia do if sem achar o conteudo que vem após 'linha digitavel'
        raise ValueError("Rótulo 'Linha digitável' não encontrado!") #lança erro caso saia do for sem achar o rotulo 'linha digitavel'
    
    def extrair_linha_digitavel_do_pdf(self, caminho_pdf: str | Path) -> tuple[str, str]:
        """
            Atalho que já extrai texto do caminho onde o pdf está e logo em seguida extrai a linha digitavel do texto do pdf utlizando as funções criadas acima
        """
        raw = self.extrair_texto(caminho_pdf) #define o texto extraido do pdf na variável raw
        return self.extrair_linha_digitavel_do_texto(raw) #a função retorna a linha digitável presente no texto extraido do PDF (boleto)