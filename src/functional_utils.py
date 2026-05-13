def filter_sales_by_category(sales, category):
    return list(
        filter(lambda sale: sale.category == category, sales)
    )

def filter_sales_by_client(sales, client_id):
    return list(
        filter(lambda sale: sale.client_id == client_id, sales)
    )

def map_sales_to_amounts(sales):
    return list(
        map(lambda sale: sale.amount, sales)
    )

def get_unique_countries(clients):
    return list(
        set(client.country for client in clients)
    )