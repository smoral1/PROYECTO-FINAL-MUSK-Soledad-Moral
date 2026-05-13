def filter_sales_by_category(sales, category):
    return list(filter(lambda sale: sale.category == category, sales))

def filter_sales_by_amount(sales, min_amount):
    return list(filter(lambda sale: sale.amount >= min_amount, sales))

def get_unique_countries(clients):
    return list(set(map(lambda client: client.country, clients)))