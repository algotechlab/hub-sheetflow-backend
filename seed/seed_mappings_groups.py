import pandas as pd
import httpx
from src.core.domain.dtos.groups import GroupsMappingsDto

df = pd.read_excel('seed/database.xlsx', sheet_name='SAMARCO', engine='openpyxl')

# Limpar espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Mostrar os nomes das colunas para debug
print("Colunas encontradas no Excel:")
print(df.columns.tolist())
print("\nPrimeiras linhas:")
print(df.head())
print("\n")

### url de produção
url = 'http://31.97.247.57:8000/api/v1/groups/77cb8144-f3a0-44fe-b8f8-b0e201db9710/users'

def str_to_bool(value):
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['sim', 'yes', 'true', '1', 's', 'y']
    return bool(value)

# Função auxiliar para acessar colunas de forma segura
def get_column_value(row, column_name):
    """Tenta encontrar a coluna mesmo com variações de espaços"""
    if column_name in row.index:
        value = row[column_name]
        return value if pd.notna(value) else None
    
    # Tenta encontrar com espaços extras
    for col in row.index:
        if col.strip() == column_name.strip():
            value = row[col]
            return value if pd.notna(value) else None
    
    return None

for index, row in df.iterrows():
    try:
        groups_mappings_dto = GroupsMappingsDto(
            name=get_column_value(row, 'NOME'),
            contato=get_column_value(row, 'CONTATO'),
            documento=get_column_value(row, 'CPF'),
            localidade=get_column_value(row, 'LOCALIDADE'),
            numero_processo=get_column_value(row, 'Nº PROCESSO'),
            pasta_drive=str_to_bool(get_column_value(row, 'PASTA DRIVE') or False),
            origem=get_column_value(row, 'ORIGEM'),
            senha=get_column_value(row, 'SENHA PORTAL/GOV'),
            orgao_julgador=get_column_value(row, 'ÓRGÃO JULGADOR'),
            contra_parte=get_column_value(row, 'CONTRA PARTE'),
            a_ser_feito=get_column_value(row, 'A SER FEITO'),
            andamento=get_column_value(row, 'ANDAMENTO'),
            observacao=get_column_value(row, 'OBSERVAÇÃO'),
            prazo=None,
        )
        response = httpx.post(url, json=groups_mappings_dto.model_dump())
        print(f"Linha {index + 1}: {response.status_code} - {response.text}")
    except Exception as e:
        print(e)
        print(f"Erro na linha {index + 1}: {str(e)}")
        continue