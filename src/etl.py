import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
from database import create_sb_client

def extract_data_from_supabase(table_name: str, column_name: str) -> list[str]:
  try:
      supabase = create_sb_client()
      start = 0
      limit = 1000
      all_items = []
      
      while True:
          response = supabase.table(table_name).select('id', column_name).range(start, start + limit).execute()
          print(response)
      
          if response:
            data = response.data
            if data:
              for row in data:
                identifier = row['id']
                column = row[column_name]
                all_items.append({"id": identifier, column_name: column})
            else:
                print("No job descriptions found.")
                
            start += limit
            if len(data) < limit:
              break 
          else:
              print("Error: Empty response from Supabase.")
              break 
        
      return all_items
      
  except Exception as e:
      print("An error occurred:", e)
      
      
def nltk_to_wordnet_pos(nltk_tag):
    """
    Descr: Convert NLTK POS tag to WordNet POS tag.
    Input: nltk_tag
    Output: wordnet_pos
    """
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

      
def clean_and_lemmatize(data, column_name, cleaned_column):
  """
  Descr: Clean text data by removing punctuation, stopwords, and converting to lowercase.
          Additionally, perform lemmatization on the cleaned text.
  Input: data (text)
  Output: cleaned and lemmatized text
  """
  stop_words = set(stopwords.words('english'))
  lemmatizer = WordNetLemmatizer() 
  
  clean_and_lemmatized_data  = []
  
  for item in data:
    identifier = item['id']
    column = item[column_name]
    
    
    clean_data = re.sub(r"\{\{.*?\}\}", "", column)
    clean_data = word_tokenize(clean_data)
    clean_data = [w.lower() for w in clean_data]
    clean_data = [word for word in clean_data if word.isalpha()]
    clean_data = [word for word in clean_data if word not in stop_words]
  
    tokens = word_tokenize(' '.join(clean_data))
    pos_tags = pos_tag(tokens)
    lemmatized_words = [] 
    
    for word, tag in pos_tags:
      wn_tag = nltk_to_wordnet_pos(tag)
      if wn_tag is None: 
        lemmatized_word = lemmatizer.lemmatize(word)
      else:
        lemmatized_word = lemmatizer.lemmatize(word, pos=wn_tag)
      lemmatized_words.append(lemmatized_word)    
    clean_and_lemmatized_data.append({"id": identifier, cleaned_column: ' '.join(lemmatized_words)})  
  return clean_and_lemmatized_data


def load_cleaned_data_to_supabase(table_name: str, column_name: str, cleaned_data: list[dict]):
  try:
    supabase = create_sb_client()
    
    for item in cleaned_data:
      identifier = item['id']
      cleaned_col_data = item[column_name]
      data, count = supabase.table(table_name).update({column_name: cleaned_col_data}).eq("id", identifier).execute()
      
    print("Cleaned job descriptions loaded to Supabase successfully.")
  except Exception as e:
      print("An error occurred:", e)

def main():
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  
  table = 'User'
  column = 'resume'
  cleaned_column = 'cleaned_resume'
  
  data = extract_data_from_supabase(table, column)
  print('data', data)
  clean_and_lemmatized_data = clean_and_lemmatize(data, column, cleaned_column)
  print('Total cleaned job descriptions:', len(clean_and_lemmatized_data)) 
  load_cleaned_data_to_supabase(table, cleaned_column, clean_and_lemmatized_data)
      
if __name__ == '__main__':
  main()
