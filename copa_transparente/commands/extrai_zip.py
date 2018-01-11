# coding: utf-8

import os
import zipfile
import sys

def main(path):
    ''' Caso nao tenha tratamento de exception use esse if
    if not os.path.exists(path):
        print("Arquivo {} não existe".format(path))
        sys.exit(-1)
    else:
    '''
    try:
        zfile = None
        zfile = zipfile.ZipFile(path)
    except (FileNotFoundError, PermissionError) as e:
        print("Algum problema ao ler o arquivo " + e.filename)
    else:
        zfile.extractall()
        print("Arquivos extraídos")
    finally:
        if zfile != None:
            print('fechando arquivo')
            zfile.close()

if __name__ == "__main__":
    main(sys.argv[1])
