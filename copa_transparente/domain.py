from decimal import Decimal

class DataTable:
    """Representa uma Tabela de dados.

        Essa classe representa uma tabela de dados do portal
        da transparência. Deve ser capaz de validar linhas
        inseridas de acordo com as colunas que possui. As
        linhas inseridas ficam registradas dentro dela.

        Attributes:
        name: Nome da tabela
        columns: [Lista de colunas]
        data: [Lista de dados]
    """
    def __init__(self, name):
        """Construtor
            Args:
            name: Nome da Tabela
        """
        self._name = name
        self._columns = []
        self._data = []
        self._references = [] # tabelas q essa tabela aponta
        self._referenced = [] # tabelas q apontam para essa tabela

    """
        adiciona coluna
    """
    def add_column(self, name, kind, description=""):
        column = Column(name, kind, description=description)
        self._columns.append(column)
        return column

    def add_references(self, name, to, on):
        """Cria uma referencia dessa tabela para uma outra tabela
        Args:
        name: nome da relação
        to: instância da tabela apontada
        on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, self, to, on)
        self._references.append(relationship)

    def add_referenced(self, name, by, on):
        """Cria uma referência para outra tabela que aponta para essa.
        Args:
        name: nome da relação
        by: instância da tabela que aponta para essa
        on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, by, self, on)
        self._referenced.append(relationship)

    def _get_name(self):
        return self._name
        
    def _set_name(self, _name):
        self._name = _name
    
    def _del_name(self):
        raise AttributeError('esse atributo nao pode ser deletado')

    # encapsulamento pythonico vc pode chamar a funcao, atribuir com = x, e chamar del atributo
    name = property(_get_name, _set_name, _del_name)

class Relationship:
    """Classe que representa um relacionamento entre DataTables
    Essa classe tem todas as informações que identificam um
    relacionamento entre tabelas. Em qual coluna ele existe,
    de onde vem e pra onde vai.
    """
    def __init__(self, name, _from, to, on):
        """Construtor
        Args:
        name: Nome
        from: Tabela de onde sai
        to: Tabela pra onde vai
        on: instância de coluna onde existe
        """
        self._name = name
        self._from = _from
        self._to = to
        self._on = on

class InvalidDataTypeException(Exception):
    pass

class Column:
    """Representa uma coluna em um DataTable

    Essa classe contém as informações de uma coluna
    e deve validar um dado de acordo com o tipo de
    dado configurado no construtor.

    Attributes:
    name: Nome da Coluna
    king: Tipo do Dado (varchar, bigint, numeric)
    description: Descrição da coluna
    """
    def __init__(self, name, kind, description=""):
        """Construtor
        Args:
        name: Nome da Coluna
        kind: Tipo do dado (varchar, bigint, numeric)
        description: Descrição da coluna
        """
        self._name = name
        self._kind = kind
        self._description = description
        self._is_pk = False

    def __str__(self): # tipo to_string do java
        _str = "Col: {} : {} {}".format(self._name,self._kind,self._description)
        return _str

    @staticmethod
    def validate(kind, data):
        if not kind in ('bigint', 'numeric', 'varchar'):
            raise InvalidDataTypeException("Tipo inválido")
        if kind == 'bigint':
            if isinstance(data, int):
                return True
            return False
        elif kind == 'varchar':
            if isinstance(data, str):
                return True
            return False
        elif kind == 'numeric':
            try:
                Decimal(data)
            except:
                return False
            return True

"""
    Exemplo de heranca, PrimaryKey herda de Column
"""
class PrimaryKey(Column):
    def __init__(self, table, name, kind, description=None):
        super().__init__(name, kind, description=description)
        self._is_pk = True

    def __str__(self):
        _str = "Col: {} : {} {}".format(self._name,self._kind,self._description)
        return "{} - {}".format('PK', _str)
