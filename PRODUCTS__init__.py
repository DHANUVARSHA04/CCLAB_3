from products import dao
from typing import List, Optional


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @classmethod
    def load(cls, data: Optional[tuple]):
        """
        Factory method to create a Product instance from a database row.
        Ensures data integrity by checking row length.
        """
        if not data or len(data) < 4:
            raise ValueError("Invalid product data")
        
        id, name, description, cost = data[:4]
        qty = data[4] if len(data) > 4 else 0

        return cls(id=id, name=name, description=description, cost=cost, qty=qty)


def list_products() -> List[Product]:
    """
    Retrieve all products and return them as a list of Product instances.
    """
    return [Product.load(product) for product in dao.list_products()]


def get_product(product_id: int) -> Product:
    """
    Retrieve a single product by its ID.
    Raises an exception if the product is not found.
    """
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)


def add_product(product: dict):
    """
    Add a new product to the database.
    Validates the input dictionary before passing it to the DAO layer.
    """
    required_keys = {"id", "name", "description", "cost", "qty"}
    if not required_keys.issubset(product.keys()):
        raise ValueError(f"Product data must include keys: {required_keys}")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Update the quantity of a specific product.
    Ensures the quantity is non-negative before updating.
    """
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    dao.update_qty(product_id, qty)
