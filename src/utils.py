from datetime import datetime
import re, unicodedata

def analisar_data(data_entrada: str) -> str:
    """
        -Converte datas (dd/mm/yyyy) para (yyyy-mm-dd);
        -Normaliza NBSP e espaços;
        -Trata possíveis erros e específica em caso de erro.
    """
    try: #tenta executar o bloco de código abaixo
        data_entrada = data_entrada.replace('\xa0', ' ').strip() #pega a data passada como parametro e troca os caracteres '\xa0' por espaços normais, depois remove possíveis espaços com o .strip()

        formato_entrada = "%d/%m/%Y" #define qual é o formato de data que será passado como parâmetro
        formato_saida = "%Y-%m-%d" #define qual é o formato de data que retornará

        data_validada = datetime.strptime(data_entrada, formato_entrada) #valida que a data de entrada está de acordo com o formato de entrada
        data_formatada = datetime.strftime(data_validada, formato_saida) #transforma a data validada no formato correto de saída

        return data_formatada #a função retorna a data convertida para o formato desejado
 
    except ValueError as erro: #caso ocorra erro na execução do bloco try, um ValueError será lançado especificando o erro
        raise ValueError(f'Data inválida: {data_entrada}') from erro
    
def analisar_valor(valor_entrada: str) -> float:
    """
        -Converte valores de string para float;
        -Transforma de (x.xxx,xx) para (xxxx.xx), por exemplo (1.250,00) para (1250.00);
        -Tira o 'R$' do valor, separando apenas o valor.
        -Lança erro em caso de valor negativo
    """
    try:
        valor_entrada = valor_entrada.replace('\xa0', ' ').strip() #pega o valor passado como parâmetro e troca os caracteres '\xa0' por espaços normais, depois remove possíveis espaços com o .strip()
        valor_sem_rs = valor_entrada.replace('R$', '').strip() #pega o valor de entrada e tira o 'R$' do valor
        valor_sem_ponto_milhar = valor_sem_rs.replace('.', '') #pega o valor ja sem o 'R$' e tira os pontos de milhar dele
        valor_com_ponto_no_lugar_de_virgula = valor_sem_ponto_milhar.replace(',', '.') #pensando no formato necessário para float, trocas as virgulas por pontos que irão diferenciar os decimais 
        valor_formatado = float(valor_com_ponto_no_lugar_de_virgula) #transforma esse valor que atualmente está em string para float de fato

        if valor_formatado < 0: #se o valor estiver negativo lançará um ValueError especificando o erro
            raise ValueError('Valor Negativo não é permitido')
        else: #caso contrário, está correto e o valor em float é retornado pela função
            return valor_formatado

    except ValueError as erro: #caso haja erro na execução do bloco try lançará um ValueError especificando o erro
        raise ValueError(f'Valor inválido: {valor_entrada}') from erro
    
def formatar_minuscula(string: str) -> str:
    """
        Deixa em minuscula e remove acentos
    """
    string = string.replace("\xa0", " ") #Trata NBSP
    string = unicodedata.normalize("NFD", string) #normaliza a string, trocando caracteres que possuem acento embutido pela base. ex: 'á' vira 'a' e 'ç' vira 'c'
    string = "".join(caractere for caractere in string if not unicodedata.combining(caractere)) #pega cada caracter da string e junta novamente somente os que não são combinantes (acentos e outros caracteres especiais)
    return string.lower() #a função retorna a string com todas as mudanças acima em minúsculo

def apenas_digitos(string: str) -> str:
    """
        Remove tudo que não for dígito
    """
    return re.sub(r"\D+", "", string) #substitui tudo que não é digito por "", ou seja, remove o que não é digito

def proxima_linha_nao_vazia(linhas: list[str], idx_inicio: int) -> str | None:
    """
        Retorna a próxima linha não vazia após o índice de início, ou None
    """
    for i in range(idx_inicio + 1, len(linhas)): #percorre desde a linha do index de início até a última linha
        linha_candidata = linhas[i].replace("\xa0", " ").strip() #trata NBSP e tira possíveis espaços na linha candidata a ser a próxima não vazia

        if linha_candidata: #caso a linha possua conteúdo, a função retornará essa linha, caso contrário, irá voltar ao for
            return linha_candidata
    return None #caso o for seja percorrido completamente sem que uma linha seja retornada, significa que não há linhas não vazias após a desejada, então retorna None
