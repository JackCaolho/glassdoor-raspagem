import pandas as pd
import nltk

# Certifique-se de que o arquivo 'avaliacoes.xlsx' está na mesma pasta do script
df = pd.read_excel('avaliacoes.xlsx')

# Verifique se as colunas necessárias estão presentes
required_columns = ['Contras', 'Data', 'Cargos Categorizados']
if all(column in df.columns for column in required_columns):
    # Converter a coluna "Contras" para strings (caso não esteja)
    df['Contras'] = df['Contras'].astype(str)
    
    # Definir stopwords em português
    stop_words = set(nltk.corpus.stopwords.words('portuguese'))
    
    # Função para tokenização e remoção de stopwords
    def process_text(text):
        # Tokenizar o texto
        words = nltk.word_tokenize(text)
        
        # Remover pontuações e converter para minúsculas
        words = [word.lower() for word in words if word.isalpha()]
        
        # Remover stopwords
        filtered_words = [word for word in words if word not in stop_words]
        
        return filtered_words
    
    # Aplicar a função na coluna "Contras"
    df['Processed_Contras'] = df['Contras'].apply(process_text)
    
    # Preparar os dados para a nova planilha
    new_data = []
    for index, row in df.iterrows():
        for word in row['Processed_Contras']:
            new_data.append({
                'Palavra': word,
                'Data': row['Data'],
                'Cargos Categorizados': row['Cargos Categorizados']
            })
    ""
    # Criar um novo DataFrame com os dados preparados
    new_df = pd.DataFrame(new_data)
    
    # Salvar o novo DataFrame em uma nova planilha
    new_df.to_excel('palavras_extraidas.xlsx', index=False)
    
    print("Nova planilha 'palavras_extraidas.xlsx' criada com sucesso.")
else:
    print("Uma ou mais colunas necessárias não foram encontradas na planilha.")
