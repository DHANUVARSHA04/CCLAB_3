import json
from typing import List, Optional
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        contents = json.loads(data['contents']) if isinstance(data['contents'], str) else data['contents']
        return Cart(data['id'], data['username'], contents, data['cost'])


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []
    
    product_ids = []
    for cart_detail in cart_details:
        contents = cart_detail['contents']
        product_ids.extend(json.loads(contents))

    # Fetch all products in a single call if supported
    return [get_product(product_id) for product_id in product_ids]


def add_to_cart(username: str, product_id: int) -> None:
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    dao.delete_cart(username)
