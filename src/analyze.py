import json
import os
import csv
import pandas as pd

from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection
import functional_utils as utils


def generate_report():

    with open('data/clients.json', 'r') as file:
        clients_data = json.load(file)

    sales_df = pd.read_csv('data/sales.csv')

    clients_list = [
        Client(**client)
        for client in clients_data
    ]

    sales_list = [
        Sale(**row)
        for row in sales_df.to_dict(orient='records')
    ]

    client_col = ClientCollection(clients_list)
    sales_col = SalesCollection(sales_list)


    # 1
    total_clients = len(clients_list)


    # 2
    total_sales = len(sales_list)

    total_revenue = round(
        sum(sale.amount for sale in sales_list),
        2
    )


    # 3, 4, 5
    clients_report = []

    for client in clients_list:

        total_spent = sales_col.total_amount_by_client(
            client.client_id
        )

        sale_count = len(
            sales_col.sales_by_client(
                client.client_id
            )
        )

        average_sale = (
            round(total_spent / sale_count, 2)
            if sale_count > 0
            else 0
        )

        clients_report.append({
            "client_id": client.client_id,
            "name": client.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": average_sale
        })


    # 6
    top_client_by_country = {}

    countries = utils.get_unique_countries(
        clients_list
    )

    for country in countries:

        country_clients = client_col.clients_by_country(
            country
        )

        best_client = max(
            country_clients,
            key=lambda client:
            sales_col.total_amount_by_client(
                client.client_id
            ),
            default=None
        )

        if best_client:
            top_client_by_country[country] = best_client.name


    # 7
    sales_by_category = (
        sales_df
        .groupby('category')['amount']
        .sum()
        .round(2)
        .to_dict()
    )


    # 8
    electronics_sales = utils.filter_sales_by_category(
        sales_list,
        'Electronics'
    )

    counts = {}

    for sale in electronics_sales:
        counts[sale.client_id] = (
            counts.get(sale.client_id, 0) + 1
        )


    # 9
    high_spending_clients = [
        client.name
        for client in clients_list
        if sales_col.total_amount_by_client(
            client.client_id
        ) > 500
    ]


    # 10
    sales_df['date'] = pd.to_datetime(
        sales_df['date']
    )

    monthly_sales = (
        sales_df
        .groupby(
            sales_df['date'].dt.to_period('M')
        )['amount']
        .sum()
        .round(2)
        .to_dict()
    )

    monthly_sales = {
        str(month): total
        for month, total in monthly_sales.items()
    }


    final_report = {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": total_revenue
        },

        "clients": clients_report,

        "top_client_by_country":
            top_client_by_country,

        "sales_by_category":
            sales_by_category,

        "high_spending_clients":
            high_spending_clients,

        "monthly_sales":
            monthly_sales
    }


    with open('report.json', 'w') as file:
        json.dump(final_report, file, indent=4)

    return final_report


if __name__ == "__main__":
    generate_report()