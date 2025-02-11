from typing import List, Tuple
import streamlit as st

def add_item(order_items: List, product: str, quantity: str, size: str) -> List: 
    """Adds an item to the order list and updates the quantity if the item is already in the list.

    Args:
        order_items (List): Items in the order
        product (str): Product name
        quantity (str): Quantity of the order
        size (str): Size of the product

    Returns:
        List: Updated order items
    """
    duplicate_found = False
    for item in order_items:
        if item['product'] == product and item['size'] == size:
            item['quantity'] += quantity
            duplicate_found = True
            break

    if not duplicate_found:
        order_items.append({"product": product, "quantity": quantity, "size": size})
    
    return order_items

def adjust_item(order_items: List, product: str, quantity: str, size: str) -> List:
    """Adjusts the quantity of an item in the order list.

    Args:
        order_items (List): Items in the order
        product (str): Product name
        quantity (str): Quantity of the order
        size (str): Size of the product

    Returns:
        List: Updated order items
    """
    if quantity == 0:
        order_items = [item for item in order_items if item['product'] != product or item['size'] != size]
    
    for item in order_items:
        if item['product'] == product and item['size'] == size:
            item['quantity'] = quantity
            break
    
    return order_items

def display_items(order_items: List) -> None:
    """Displays the current items in the order list.

    Args:
        order_items (List): Items in the order
    """
    for item in order_items:
        st.write(f"- {item['quantity']}x {item['size']} {item['product']}")