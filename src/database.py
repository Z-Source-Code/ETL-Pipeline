import os
from supabase import create_client, Client
import nltk

def extract_data_from_supabase(table_name, column_name):
  try:
      url: str = os.environ.get("SUPABASE_PROJECT_URL")
      key: str = os.environ.get("SUPABASE_API_KEY")

      supabase: Client = create_client(url, key)
      response = supabase.table(table_name).select(column_name).execute()
      
      print(response)
      
      if response:
        data = response.data
        if data:
          job_titles = [job['job_title'] for job in data]
          print(job_titles)
        else:
          print('No job title found.')
      else:
        print('Error:', response.content)
      
  except Exception as e:
      print("An error occurred:", e)
      
      
def main():
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  
  data = extract_data_from_supabase('Job Postings', 'job_title')
      
if __name__ == '__main__':
  main()

