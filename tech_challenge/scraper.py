import json
from .utils.segment_enum import Segment
from .utils.scraper_utils import config_target_url, fetch_url, extract_table, convert_table_in_object
from .utils.year_range import YearRange
from selenium.webdriver.common.by import By
from typing import List, Dict
from .utils.product import Product

def get_available_years(segment: Segment) -> YearRange:
    url = config_target_url(segment)
    
    try:
        driver = fetch_url(url)
        
        if not driver:
            raise ValueError(f"Erro ao obter dados!")
        
        elements = driver.find_element(By.CSS_SELECTOR, ".lbl_pesq")
        html = elements.get_attribute('outerHTML')
        
        return YearRange.from_string(html)
    except Exception as e:
        print(f"[scrap_url] Erro durante o processamento: {str(e)}")
        raise
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

def get_products(segment: Segment, year: str = None, sub_option: str = None) -> list[Product]:
    url = config_target_url(segment, year, sub_option)
    
    try:
        driver = fetch_url(url)
        
        if not driver:
            raise ValueError(f"Erro ao obter dados!")

        elements = driver.find_element(By.CSS_SELECTOR, ".tb_base.tb_dados")
        html = elements.get_attribute('outerHTML')
        
        table = extract_table(html)
        products = convert_table_in_object(table)
        
        return products
    except Exception as e:
        print(f"[scrap_url] Erro durante o processamento: {str(e)}")
        raise
    finally:
        if 'driver' in locals() and driver:
            driver.quit()
