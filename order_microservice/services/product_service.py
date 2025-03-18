from typing import Protocol

import requests


class ProductService(Protocol):
    async def query_product(self, product_id: str) -> dict:
        ...

class ProductServiceImpl(ProductService ):
    def query_product(self, product_id: str) -> dict:
        response = requests.get(f"http://product-service/api/products/{product_id}")
        return response.json()

    def query_variant(self, variant_id: str) -> dict:
        response = requests.get(f"http://product-service/api/variants/{variant_id}")
        return response.json()