class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        return [
            sale for sale in self.sales
              if sale.client_id == client_id
        ]
    
    def total_amount_by_client(self, client_id):
        sales = self.sales_by_client(client_id)

        return sum(sale.amount for sale in sales)
    
    def total_amount_by_category(self, category):
        category_sales = [
            sale for sale in self.sales
            if sale.category == category
        ]

        return sum(sale.amount for sale in category_sales)
        
    def average_sale_by_client(self, client_id):
        sales = self.sales_by_client(client_id)

        if not sales:
            return 0

        total = sum(sale.amount for sale in sales)

        return total / len(sales)