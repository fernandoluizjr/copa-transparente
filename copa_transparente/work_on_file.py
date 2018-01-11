# coding: utf-8

from decimal import Decimal
from decimal import FloatOperation, getcontext
from datetime import datetime, timedelta

c = getcontext()

# garante q Decimal soh seja operado com Decimal e nao com float
c.traps[FloatOperation] = True

totais_agrupados_por_ano = {2010:0, 2011:0, 2012:0, 2013:0, 2014:0, 2015:0}

total = Decimal('0')
total_por_data = Decimal('0')
total_por_vigencia = Decimal('0')
start_date = datetime(2009, 1, 1)
end_date = datetime(2010, 1, 1)

all_companies = set() # garante q nao temos empresas duplicadas
intervals = [(Decimal('1000000000'), set()), # Agrupa as empresas por valor recebido
                (Decimal('500000000'), set()),
                (Decimal('100000000'), set()),
                (Decimal('10000000'), set()),
                (Decimal('1000000'), set()),
                (Decimal('100000'), set()),
                (Decimal('10000'), set()),
                (Decimal('1000'), set())]

def value_por_range_datas(_info):
    try:
        signature_date = datetime.strptime(info[7], '%d/%m/%Y')
        if signature_date > start_date and signature_date < end_date:
            return Decimal(info[5])
    except Exception as e:
        print(e)
        pass
    return Decimal('0')


def value_por_tempo_vigencia(info):
    try:
        start_date = datetime.strptime(info[8], '%d/%m/%Y')
        end_date = datetime.strptime(info[9], '%d/%m/%Y')
        date_diff = end_date - start_date # retorna timedelta q contem a diferenca das datas
        if date_diff.days < 10:
            return Decimal(info[5])
    except Exception as e:
        print(info)
        pass
    return Decimal('0')


def conta_contratos_por_range(info,year_start_date,year_end_date):
    try:
        start_date = datetime.strptime(info[8],'%d/%m/%Y')
        end_date = datetime.strptime(info[9], '%d/%m/%Y')
        if start_date > year_start_date and start_date < year_end_date:
            return 1
    except Exception as e:
        pass
    return 0

def dec(element, index):
    try:
        return Decimal(element[index])
    except:
        return Decimal('0')

with open('data/data/ExecucaoFinanceira.csv', 'r') as data:
    info = [line.strip().split(';') for line in data] # monta uma lista de registros. cada um eh uma lista de campos splitados
    total = sum([dec(element, 5) for element in info]) # monta outra lista soh com o campo 5 e passa pro sum()
# end with: at this point on the file will be closed.

with open('data/data/ExecucaoFinanceira.csv', 'r') as data:
    for line in data:
        try:
            info = line.strip().split(';')
            total_por_data += value_por_range_datas(info)
            total_por_vigencia += value_por_tempo_vigencia(info)
        except Exception as e:
            print('error {}'.format(line))
# end with: at this point on the file will be closed.

for year in totais_agrupados_por_ano.keys():
    start_date = datetime(year, 1, 1)
    end_date = start_date + timedelta(days=365)
    with open('data/data/ExecucaoFinanceira.csv', 'r') as data:
        for line in data:
            info = line.strip().split(';')
            totais_agrupados_por_ano[year] += conta_contratos_por_range(info, start_date, end_date)
    # end with: at this point on the file will be closed.


def get_id_and_value(info, lower):
    value = Decimal(info[5])
    if value > lower:
        return info[2], value
    return None, Decimal(0)

for lower, companies in intervals: # varre as empresas e joga nos sets especificos
    data = open('data/data/ExecucaoFinanceira.csv', 'r')
    for line in data:
        company_id, contract_value = get_id_and_value(line.strip().split(';'), lower)
        if company_id and not company_id in all_companies:
            companies.add(company_id)
        all_companies.add(company_id)
    data.close()


print("Total gasto: {}".format(total))
print("Total gasto com assinaturas entre {} e {} : {}".format(start_date, end_date, total_por_data))
print("Total gasto com contrados de menos de 11 dias {}".format(total_por_vigencia))

for year, signed in totais_agrupados_por_ano.items():
    print("{} execuções assinadas em {}".format(signed, year))

for lower, companies in intervals:
    print("{} empresas receberam mais de {}".format(len(companies), lower))
print("{} empresas no total".format(len(all_companies)))
