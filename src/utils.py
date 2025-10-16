from datetime import datetime

def analisar_data(data_entrada: str) -> str:
    """
        -Converte datas (dd/mm/yyyy) para (yyyy-mm-dd);
        -Normaliza NBSP e espaços;
        -Trata possíveis erros e específica em caso de erro.
    """
    try:
        data_entrada = data_entrada.replace('\xa0', ' ').strip()

        formato_entrada = "%d/%m/%Y"
        formato_saida = "%Y-%m-%d"

        data_validada = datetime.strptime(data_entrada, formato_entrada)
        data_formatada = datetime.strftime(data_validada, formato_saida)

        return data_formatada
 
    except ValueError as erro:
        raise ValueError(f'Data inválida: {data_entrada}') from erro
    
def analisar_valor(valor_entrada: str) -> float:
    """
        -Converte valores de string para float;
        -Transforma de (x.xxx,xx) para (xxxx.xx), por exemplo (1.250,00) para (1250.00);
        -Tira o 'R$' do valor, separando apenas o valor.
        -Lança erro em caso de valor negativo
    """
    try:
        valor_entrada = valor_entrada.replace('\xa0', ' ').strip()
        valor_sem_rs = valor_entrada.replace('R$', '').strip()
        valor_sem_ponto_milhar = valor_sem_rs.replace('.', '')
        valor_com_ponto_no_lugar_de_virgula = valor_sem_ponto_milhar.replace(',', '.')
        valor_formatado = float(valor_com_ponto_no_lugar_de_virgula)

        if valor_formatado < 0:
            raise ValueError('Valor Negativo não é permitido')
        else:
            return valor_formatado

    except ValueError as erro:
        raise ValueError(f'Valor inválido: {valor_entrada}') from erro
