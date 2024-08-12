import json
from datetime import datetime
from random import randint


def json_encode(data):
    if isinstance(data, datetime):
        return data.isoformat()
    if isinstance(data, (dict, list)):
        return json.dumps(data)


def json_serializer(data):
    return json.dumps(data, default=str).encode("utf-8")


def json_deserializer(data):
    return json.loads(data.decode("utf-8"))


def generate_sales_data():
    return {
        'product_id': f"P0{randint(100, 999)}",
        'store_id': f"S0{randint(100, 999)}",
        'date': datetime.now().date(),
        'sales': randint(0, 10),
        'revenue': randint(155, 10000) / 100,
        'stock': randint(0, 100),
        'price': randint(155, 389) / 100
    }
