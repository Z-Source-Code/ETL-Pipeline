import os
import re
from supabase import create_client, Client
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize


def extract_data_from_supabase(table_name: str, column_name: str, page_size: int, page_number: int) -> list[str]:
  try:
      url: str = os.environ.get("SUPABASE_PROJECT_URL")
      key: str = os.environ.get("SUPABASE_API_KEY")

      supabase: Client = create_client(url, key)
      from_index = (page_number - 1) * page_size 
      to_index = from_index + page_size - 1
      print(from_index, to_index)
      response = supabase.table(table_name).select(column_name).range(1000, 1400).execute()
      
      if response:
        data = response.data
        print(len(data))
        if data:
          job_descriptions = [job for job in data]
          
          return job_descriptions, len(job_descriptions)
        else:
          print('No job title found.')
      else:
        print('Error:', response.content)
      
  except Exception as e:
      print("An error occurred:", e)
      
def clean_data(data):
  """
  Descr: Clean text data by removing punctuation, stopwords, and converting to lowercase.
  Input: text
  Output: cleaned text
  """
  description = re.sub(r"\{\{.*?\}\}", "", data)
  description = word_tokenize(description)
  description = [w.lower() for w in description]
  description = [word for word in description if word.isalpha()]
  stop_words = set(stopwords.words('english'))
  description = [word for word in description if word not in stop_words]
  return ' '.join(description)



  
      
      
def main():
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  
  page_size = 100
  page_number = 26
  
  data, length = extract_data_from_supabase('Job Postings', 'job_description', page_size, page_number)
  # print(data, length)
  # cleaned_data = clean_data(data)
  # print(cleaned_data) 
      
if __name__ == '__main__':
  main()

