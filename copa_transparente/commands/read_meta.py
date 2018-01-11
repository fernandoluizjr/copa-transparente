# coding: utf-8

import os

def extract_file_extension(filename):
    return filename.split('.')[0]

def read_lines(filename):
    _file = open(os.path.join("data/meta-data", filename), "rt")
    data = _file.read().split("\n")
    _file.close()
    return data

def read_meta_data(filename):
    meta_data = []
    for line in read_lines(filename):
        if line: # linha nao vazia
            meta_data.append(tuple(line.split('\t')[:3]))
    return meta_data

def prompt():
    print("\nO que deseja ver?")
    print("(l) Listar entidades")
    print("(d) Exibir atributos de uma entidade")
    print("(r) Exibir referências de uma entidade")
    print("(s) Sair do programa")
    return input('')

def main():
    meta = {} # dicionário nome entidade -> atributos

    keys = {} # dicionário identificador -> nome entidade

    relationships = {} # dicionário de relacionamentos

    for meta_data_file in os.listdir("data/meta-data"):
        table_name = extract_file_extension(meta_data_file)
        atributos = read_meta_data(meta_data_file)
        identificador = atributos[0][0]

        meta[table_name] = atributos
        keys[identificador] = table_name

    for k, v in meta.items():
        for col in v:
            if col[0] in keys: # tem relacao com alguma tabela. nao sei qual ainda.
                if not col[0] == meta[k][0][0]: # se essa coluna tem o mesmo nome da coluna da primeira lista da tabela q estamos iterando 
                   relationships[k] = keys[col[0]] # entao tem uma relacao e registramos isso
            print(" {}: {}".format(col[1], col[0]))

    opcao = prompt()
    while opcao != 's':
        if opcao == 'l':
            for entity_name in meta.keys(): # aki usamos somente as chaves ao inves de iterar k,v
                print(entity_name)
        elif opcao == 'd':
            entity_name = input('Nome da entidade: ')
            for col in meta[entity_name]:
                print(col)
        elif opcao == 'r':
            entity_name = input('Nome da entidade: ')
            other_entity = relationships[entity_name]
            print(other_entity)
        else:
            print(f"Inexistente {opcao}\n")
        opcao = prompt()

if __name__ == "__main__":
    main()
