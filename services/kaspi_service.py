import requests
from config import KASPI_URL

class KaspiService():
    def __init__(self, token: str):
        self.token = token
        self.BASE_URL = KASPI_URL 
        self.ORDER_URL = f"{self.BASE_URL}/orders"
            
    def get_info_about_order(self, orderId: str):
        url = f"{self.ORDER_URL}/{orderId}/entries"
        
        headers = {
            'ContentType': 'application/vnd.api+json',
            'X-Auth-Token': self.token,
        }
        
        response = requests.get(url, headers=headers)
        
        return response.json()
        
kaspi_service = KaspiService()
