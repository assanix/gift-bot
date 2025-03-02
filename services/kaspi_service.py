import requests
from config import KASPI_URL, KASPI_API_KEY

class KaspiService():
    def __init__(self):
        self.token = KASPI_API_KEY
        self.BASE_URL = KASPI_URL
        self.ORDER_URL = f"{self.BASE_URL}orders"
        
    def get_info_about_order(self, orderId: str):
        url = f"{self.ORDER_URL}"
        
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'X-Auth-Token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        params = {
            'filter[orders][code]': orderId
        }
        
        try:
            response = requests.get(
                url, 
                params=params, 
                headers=headers
            )
            
            return response.json()
        
        except requests.exceptions.Timeout:
            return {"error": "Timeout occurred"}
        except Exception as e:
            print(f"Ошибка: {e}")
            return None
        
kaspi_service = KaspiService()
