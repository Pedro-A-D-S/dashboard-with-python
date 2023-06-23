from pathlib import Path
from typing import List
import pandas as pd
import numpy as np
import os
import logging
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')

class DataIngestion:
    """
    A class for data ingestion and consolidation.
    """
    
    def __init__(self, folder_path: str):
        """
        Initialize the DataIngestion object.
        
        Args:
            folder_path (str): Path to the folder containing the data files.
        """
        self.folder_path = folder_path
    
    @staticmethod    
    def bytes_to_mega(bytes_: int) -> float:
        """
        Convert bytes to megabytes.
        
        Args:
            bytes: Size in bytes.
        
        Returns:
            float: Size in megabytes.
        """
        megabytes = bytes_ / (1024 * 1024)
        return megabytes
     
    def load_data(self) -> List[str]:
        """
        Load data files from the specified folder path.
        
        Returns:
            list: List of file paths.
        """
        logging.info('Loading data from folder: %s', self.folder_path)
        path_dir = Path(self.folder_path)
        try:
            files = list(map(str, path_dir.iterdir()))
            logging.info('Loaded %d file(s) from folder: %s', len(files), self.folder_path)
            return files
        except FileNotFoundError:
            logging.error('Folder not found: %s', self.folder_path)
            return None
            
     
    def get_data_size(self) -> None:
        """
        Calculate the size of each data file and display the total data size.
        """
        files = self.load_data()
        total_mb: float = 0
        for loop in files:
            
            size = os.path.getsize(str(loop))
            
            conversion = self.bytes_to_mega(size)
            
            file_name = str(loop).split('\\')[-1]
            print(f'{file_name} : {conversion:.2f} MB')
            print('-' * 20)
            total_mb = total_mb + size

        print(f'Temos ao todo {round(self.bytes_to_mega(total_mb), 2)} MBs de dados')
        
        return None

    def merge_data(self, files: List[str]) -> pd.DataFrame():
        """
        Merge data from multiple files into a single DataFrame.
        
        Args:
            files (list): List of file paths.
        
        Returns:
            pd.DataFrame: Merged data as a DataFrame.
        """
        logging.info('Merging data...')
        try:
            merged_data = pd.DataFrame()
            for counter, Arq in enumerate(files):
                print(counter, Arq)
            
                if counter == 0:
                    data = pd.read_csv(Arq, error_bad_lines = False, sep = ';', encoding = 'latin-1')
                    merged_data = data
                
                else:
                    data = pd.read_csv(Arq, error_bad_lines = False, sep = ';', encoding = 'latin-1')
                    merged_data = pd.concat([merged_data, data])
            logging.info('Merged data successfully!')
            return merged_data
        except:
            logging.error('Data not merged.')
            return None
    
    def save_data(self, file_path: str, data: pd.DataFrame()) -> None:
        """
        Save merged data to a Parquet file.
        
        Args:
            file_path (str): Path to save the Parquet file.
            merged_data (pd.DataFrame): Merged data as a DataFrame.
        """
        try:
            for col in data.columns:
                data[col] = merged_data[col].astype(str)
                
            data.to_parquet(file_path, index = False, compression = 'gzip')
            logging.info('Data saved successfully!')
        except:
            logging.error('Data was not saved in {}', file_path)
            return None

        
    def scrapping(self, url: str) -> pd.DataFrame():
        """
        Scrapes url for tables and save into Pandas DataFrame
        
        Args:
            url (str): URL to scrap data
            
        Returns:
            pd.DataFrame: Scraped data
        """
        try:
            url = url
            data = pd.DataFrame()
            for i in range(1, 24):
                
                link = f'{url}{i}'
                logging.info('Scrapping data from: %s', link)
                web_data = pd.read_html(link)[0]
                
                data = pd.concat([data, web_data])
            logging.info('Scrapping realised correctly and saved into dataframe.')
            return data
        except Exception as e:
            logging.error('An error occurred during scraping: %s', str(e))
            return None
    
    def prepare_web_data(self, data: pd.DataFrame()) -> pd.DataFrame():
        """
        Prepare web data by performing data cleaning and transformation.

        Args:
            data (pd.DataFrame): Input data as a pandas DataFrame.

        Returns:
            pd.DataFrame: Processed data with calculated mean values based on 'Código da Infração'.
        """
        try:
            data['Valor'] = pd.to_numeric(data['Valor'], errors = 'coerce')
            
            data = data.dropna(subset = ['Valor'])
            
            data['Valor'] = data['Valor'] / 100
            
            data.rename(columns = {'Código': 'Código da Infração'}, inplace = True)
            
            data['Código da Infração'] = data['Código da Infração'].astype('int64')
            
            price_table = data.groupby(by = ['Código da Infração'])['Valor'].apply(lambda x: np.mean(x.astype(float))).reset_index()
            
            logging.info('table price created!')
            return price_table
        except:
            logging.error('price table was not created.')
            return None
    
    def concat_data(self, merged_data: pd.DataFrame, price_table: pd.DataFrame) -> pd.DataFrame():
        """
        Concatenate merged_data and price_table based on 'Código da Infração' column.

        Args:
            merged_data (pd.DataFrame): Merged data as a pandas DataFrame.
            price_table (pd.DataFrame): Price table data as a pandas DataFrame.

        Returns:
            pd.DataFrame: Merged data with price information.
        """
        try:
            merged_full_data = pd.merge(merged_data, price_table, on = 'Código da Infração', how = 'left')
            logging.info('Data was merged successfully with web data!')
            return merged_full_data
        except:
            logging.error('Data was not merged successfully with web data.')
            return None
        
        
if __name__ == "__main__":
    
    di = DataIngestion(folder_path = 'data/ajustados_2022/')
    files = di.load_data()
    di.get_data_size()
    merged_data = di.merge_data(files = files)
    di.save_data(file_path = 'data/base_consolidada/base_consolidada2.parquet',
                 data = merged_data)
    data = di.scrapping(url = 'https://www.detran.mg.gov.br/infracoes/consultar-tipos-infracoes/index/index/index/index/index/index/index/index/index/index/index/index/index/lista-de-infracoes?artigo=&descricao=&page=')
    if data is not None:
        price_table = di.prepare_web_data(data = data)
        if price_table is not None:
            merged_full_data = di.concat_data(merged_data = merged_data, price_table = price_table)
            di.save_data(file_path = 'data/base_consolidada/base_consolidada_scraped.parquet',
                 data = merged_full_data)
    
    
      
    