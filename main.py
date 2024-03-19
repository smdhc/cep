import csv
import requests
import time

def consultar_api_cep(cep: str) -> dict | bool:
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    data = response.json()
    if 'erro' in data:
        return False
    return data

def obter_arquivo_cep_entrada() -> list:
    with open('input/ceps.csv', 'r') as file:
        lista_cep_processamento = file.read().splitlines()
    lista_cep_processamento = [cep.strip().zfill(8) for cep in lista_cep_processamento]
    if len(lista_cep_processamento) < 1:
        raise Exception('Lista de CEPs vazia!')
    return lista_cep_processamento

def obter_ceps_processados() -> list:
    with open('output/base_ceps_processados.csv', 'r') as file:
        ceps_processados = file.read().splitlines()
    return ceps_processados

def filtrar_ceps_nao_processados(ceps_entrada: list, ceps_processados: list) -> list:
    ceps_nao_processados = [cep for cep in ceps_entrada if cep not in ceps_processados]
    return ceps_nao_processados

def gravar_cep_invalido(cep: str):
    with open('output/base_ceps_invalidos.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cep])

def gravar_cep_processado(cep: str):
    with open('output/base_ceps_processados.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([cep])

def gravar_cep_valido(cep: str, data: dict):
    with open('output/base_ceps_validos.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            cep, 
            data['cep'], 
            data['logradouro'], 
            data['complemento'], 
            data['bairro'], 
            data['localidade'], 
            data['uf'], 
            data['ibge'], 
            data['gia'], 
            data['ddd'], 
            data['siafi']])

DELAY_REQUISICAO_API_SEGUNDOS = 1

ceps_entrada = obter_arquivo_cep_entrada()
print(f"Total de CEPs de entrada: {len(ceps_entrada)}")
ceps_processados = obter_ceps_processados()
ceps_nao_processados = filtrar_ceps_nao_processados(ceps_entrada, ceps_processados)
print(f"Total de CEPs não processados: {len(ceps_nao_processados)}")

for ix, cep in enumerate(ceps_nao_processados):
    percentual_processamento = (ix+1)/len(ceps_nao_processados)*100
    print(f"Processando CEP {cep} ({ix+1}/{len(ceps_nao_processados)}) ({percentual_processamento:.2f}%)...")
    dados_cep_api = consultar_api_cep(cep)
    if dados_cep_api is False:
        print('- CEP inválido!')
        gravar_cep_invalido(cep)
    else:
        print('- CEP válido!')
        gravar_cep_valido(cep, dados_cep_api)
    gravar_cep_processado(cep)
    time.sleep(DELAY_REQUISICAO_API_SEGUNDOS)
print('Script finalizado!')