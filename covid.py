import pandas as pd
import collections
from datetime import datetime
pd.set_option('display.max_rows', 100)

# UTILS
def confirmados(file):
    mask_conf = file["Classificacao"] == "Confirmados"
    casos_confirmados = file[mask_conf]
    return casos_confirmados

def entre_datas(casos_confirmados):
    # d1 = input("Entre com a primeira data: ")
    # d2 = input("Entre com a segunda data: ")
    d1 = '2019-06-20'
    d2 = '2021-07-10'
    
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    
    mask_data = (casos_confirmados["DataCadastro"] > d1) & (casos_confirmados["DataCadastro"] < d2)  
    return casos_confirmados[mask_data]


# LISTAR EM ORDEM ALFABÉTICA OS MUNICIPIOS COM MAIS DE N CASOS CONFIRMADOS    
def conf_municipios(file):
    casos_confirmados = confirmados(file)
    muni = casos_confirmados.groupby(by="Municipio")
    
    N = int(input("Entre com um número N: "))
    print("Municípios com mais de {} casos:" .format(N))
    
    df = muni.size().to_frame() 
    df = df.set_axis(['Casos'], axis=1)
    df = df.reset_index(level=0)
    
    for i in range(78):
        if df["Casos"][i] < N:
            df.drop([i], axis=0, inplace=True)
    print(df)

    
# CASOS DE COVID DIAGNOSTICADOS ENTRE DATAS
def casos_entre_datas(file):     
    casos_confirmados = confirmados(file) 
    casos_entre_datas = entre_datas(casos_confirmados)
    
    print("Casos confirmados entre as datas: {}" .format(len(casos_entre_datas)))

    
# RANKING DE CASOS POR CIDADE ENTRE DUAS DATAS
def top_N_cidades(file):
    casos_confirmados = confirmados(file)
    casos_entre_datas = entre_datas(casos_confirmados)

    top_N = (casos_entre_datas["Municipio"].value_counts().sort_values(ascending=False))
    print(top_N)

# % DE INTERNAÇÕES, MORTES E INTERNADOS QUE MORRERAM POR CIDADE OU GERAL
def porc_por_municipio(file):    
    cidade = input("Entre com a cidade desejada ('all' para todas): ")
    
    if cidade == 'all':
        casos_confirmados = confirmados(file)
        num_confirmados = len(casos_confirmados)
    else:
        casos_confirmados = confirmados(file)
        mask_cidade = casos_confirmados['Municipio'] == cidade
        casos_confirmados = casos_confirmados[mask_cidade]
        num_confirmados = len(casos_confirmados)

    mask_internado = casos_confirmados['FicouInternado'] == "Sim"    
    internacoes = casos_confirmados[mask_internado]
    num_internacoes = len(casos_confirmados[mask_internado])
    
    mask_mortes = casos_confirmados['DataObito'] != "0000-00-00"
    mortes = len(casos_confirmados[mask_mortes])
    
    mask_mortes_internados = internacoes['DataObito'] != "0000-00-00"
    mortes_internados = len(internacoes[mask_mortes_internados])
    
    
    print("Casos confirmados que resultaram em internações: {:.2f}%" .format(num_internacoes/num_confirmados*100))
    print("Casos confirmados que resultaram em óbito: {:.2f}%" .format(mortes/num_confirmados*100))
    print("Internações que resultaram em óbito: {:.2f}%" .format(mortes_internados/num_internacoes*100))
    

# MEDIA E DESVIO PADRAO DA IDADE DAS PESSOAS QUE MORRERAM E PORCENTAGEM DAS PESSOAS QUE MORRERAM SEM TER NENHUMA COMORBIDADE ENTRE DUAS DATAS
def media_desvio(file):
    casos_entre_datas = entre_datas(file)
    mask_mortes = casos_entre_datas['DataObito'] != "0000-00-00"
    mortes = casos_entre_datas[mask_mortes]
    mortes['IdadeNaDataNotificacao'] = (mortes['IdadeNaDataNotificacao'].str.split(' ').str.get(0))
    
    print("\nMédia de idade das pessoas que morreram: {:.2f} anos" .format(mortes['IdadeNaDataNotificacao'].astype(float).mean()))
    print("Desvio padrão da idade das pessoas que morreram: {:.2f} anos" .format(mortes['IdadeNaDataNotificacao'].astype(float).std()))
    
    # COMORBIDADE
    mask_pulmao = mortes['ComorbidadePulmao'] == "Não"
    sem_comorbidade = mortes[mask_pulmao]
    mask_cardio = mortes['ComorbidadeCardio'] == "Não"
    sem_comorbidade = sem_comorbidade[mask_cardio]
    mask_renal = mortes['ComorbidadeRenal'] == "Não"
    sem_comorbidade = sem_comorbidade[mask_renal]
    mask_diabetes = mortes['ComorbidadeDiabetes'] == "Não"
    sem_comorbidade = sem_comorbidade[mask_diabetes]
    mask_tabagismo = mortes['ComorbidadeTabagismo'] == "Não"
    sem_comorbidade = sem_comorbidade[mask_tabagismo]
    mask_obesidade = mortes['ComorbidadeObesidade'] == "Não"
    sem_comorbidade = sem_comorbidade[mask_obesidade]
    
    mortes_sem_comorbidade = len(sem_comorbidade)
    num_mortes = len(mortes)

    print("Porcentagem de pessoas que morreram sem possuir nenhuma comorbidade: {:.2f}%" .format(mortes_sem_comorbidade/num_mortes*100))
    
file = pd.read_csv('covid19ES.csv',parse_dates=["DataCadastro", "DataObito"])
conf_municipios(file)
casos_entre_datas(file)
top_N_cidades(file)
porc_por_municipio(file)
media_desvio(file)