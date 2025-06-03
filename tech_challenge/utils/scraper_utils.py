import time
import re
from typing import List, Dict
from .segment_enum import Segment
from .sub_option_enum import SubOption
from .product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

def config_target_url(segment: Segment, year: str = None, sub_option: SubOption = None) -> str:
    url = f"{BASE_URL}opcao=opt_{segment.value}"
    
    if year:
        url = f"{url}&ano={year}"
    
    if sub_option:
        url = f"{url}&subopcao=subopt_{sub_option.value}"
    
    return url

def fetch_url(url: str) -> str:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    # table = driver.find_element(By.CSS_SELECTOR, ".tb_base.tb_dados")
    
    time.sleep(5)
    # print(f"dados encontrados: {table.get_attribute('outerHTML')}")
    # driver.quit()
    
    return driver

def extract_table(table) -> List[Dict[str, str]]:
    headers = []
    data = []
    
    soup = BeautifulSoup(table, 'html.parser')
    
    header_row = soup.select_one("thead tr")
    if header_row:
        for th in header_row.find_all("th"):
            headers.append(th.text.strip())
    
    if not headers:
        headers = ["Produto", "Quantidade", "Valor (US$)"]
    
    if "Grupo" not in headers:
        headers.append("Grupo")
        
    current_group = None
    
    for tr in soup.select("tbody tr"):
        row_data = {}
        cells = tr.find_all(['td'])
        
        is_main_item = False
        if cells and len(cells) > 0:
            cell_classes = cells[0].get("class", [])
            if "tb_item" in cell_classes:
                is_main_item = True
                current_group = cells[0].text.strip()
        
        for i, cell in enumerate(cells):
            if i < len(headers) - 1:
                cell_value = cell.text.strip()
                
                if i > 0 and cell_value == "-":
                    cell_value = "0"
                
                row_data[headers[i]] = cell_value
        
        if is_main_item:
            row_data["Grupo"] = ""
        else:
            row_data["Grupo"] = current_group
        
        if row_data:
            data.append(row_data)
    return data

def convert_table_in_object(table) -> List[Product]:
    products = [Product.from_dict(item) for item in table]
    
    categories_dict = {}
    for product in products:
        if product.is_category():
            categories_dict[product.name] = product

    for product in products:
        if not product.is_category() and product.group in categories_dict:
            categories_dict[product.group].add_sub_product(product)
    
    categories_list = list(categories_dict.values())
    
    return categories_list