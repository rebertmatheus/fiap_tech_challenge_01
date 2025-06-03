# from scraper import get_available_years
# from .scraper import get_available_years, get_products
# from .utils.segment_enum import Segment
# from .utils.product import Product

from .api import app
import uvicorn

# def scrap_url():
#     url_str = config_target_url(Segment.SALES , "2020")
#     try:
#         driver = fetch_url(url_str)
    
#         if not driver:
#             print("[scrap_url] Falha ao carregar HTML.")
#             return
#         # year_range = YearRange.from_string(driver.find_element(By.CSS_SELECTOR, ".lbl_pesq").get_attribute('outerHTML'))
        
#         # print("Intervalo de anos: {}".format(year_range))
#         # print("Ano final: {}".format(end_year))
        
#         # soup = BeautifulSoup(driver.get_attribute('outerHTML'), 'html.parser')
#         # print("[scrap_url] HTML parseado com BeautifulSoup:")
#         # print(soup.prettify()[:1000])
        
#         data = extract_table(driver)
        
#         for row in data:
#             print(row)
        
#         products = convert_table_in_object(data)
#     except Exception as e:
#         print(f"[scrap_url] Erro durante o processamento: {str(e)}")
#         raise
#     finally:
#         # Garantir que o driver seja fechado após o processamento
#         if 'driver' in locals() and driver:
#             print("[scrap_url] Fechando o driver...")
#             driver.quit()

# if __name__ == "__main__":

def main():
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()

    
    # scrap_url()
    # years = get_available_years(Segment.SALES)
    
    # print(f"Years Range: {years.to_json()}")
    
    # products = get_products(Segment.SALES, '2020')
    
    # print(f"Products: {Product.products_to_json(products) }")
    
    # print(f"not nested Products: {Product.products_to_json(products, nested=False) }")