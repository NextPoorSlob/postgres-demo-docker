import argparse
import csv
import json
import random

import pytz
from faker import Faker
import faker_commerce

OUTPUT_DIRECTORY = '../initdb.d/'
CUSTOMER_COUNT = 2000
PRODUCT_COUNT = 10000
ORDER_COUNT = 20000000

PROBABILITY_HIGH = 1.0 - 0.75
PROBABILITY_MEDIUM = 1.0 - 0.5
PROBABILITY_LOW = 1.0 - 0.25
PROBABILITY_VERY_LOW = 1.0 - 0.10

fake = Faker()
fake.add_provider(faker_commerce.Provider)


def is_selected(probability):
    """
    Given a probability value, determine whether it is a selected or not.    
    :param probability: the limit for a probability.
    :return: true if it is selected, false otherwise.
    """
    return random.random() > probability


def create_customer_data(customer_count):
    """
    Creates the customer data file used to populate the database.
    :param customer_count: number of customers to create.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "customers.csv"
    columns = ['first_name', 'last_name', 'organization_name', 'addresses']

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for _ in range(customer_count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            organization_name = fake.company()
            addresses = {}
            if is_selected(PROBABILITY_MEDIUM):
                addresses['email'] = fake.email()
            if is_selected(PROBABILITY_HIGH):
                addresses['phone'] = fake.phone_number()
            if is_selected(PROBABILITY_LOW):
                addresses['cellphone'] = fake.phone_number()
            if is_selected(PROBABILITY_MEDIUM):
                address = {'street': fake.street_address(), 'city': fake.city(), 'state': fake.state(),
                           'zip': fake.zipcode(), 'country': fake.country()}
                addresses['mailing_address'] = address
            if is_selected(PROBABILITY_VERY_LOW):
                addresses['note'] = fake.text()
            address_data = json.dumps(addresses)
            writer.writerow([first_name, last_name, organization_name, address_data])


def create_additional_information():
    """
    Generates additional information about the product.
    :return: Stringifies JSON data for the product.
    """
    information = {}
    if is_selected(PROBABILITY_MEDIUM):
        measurements = {'height': f" {random.random() * 24:.2f} \"", 'width': f" {random.random() * 32:.2f} \""}
        if is_selected(PROBABILITY_MEDIUM):
            measurements['depth'] = f" {random.random() * 24:.2f} \""
        information['measurements'] = json.dumps(measurements)
    if is_selected(PROBABILITY_HIGH):
        information['color'] = fake.color_name()
    if is_selected(PROBABILITY_LOW):
        information['variant'] = is_selected(PROBABILITY_MEDIUM)

    return json.dumps(information)


def create_product_data(product_count):
    """
    Creates the product data file used to populate the database.
    :param product_count: number of products to create.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "products.csv"
    columns = ['name', 'description', 'cost', 'category', 'additional_information']

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for _ in range(product_count):
            name = fake.ecommerce_name()
            description = fake.sentence()
            cost = fake.ecommerce_price(False)
            category = fake.ecommerce_category()
            additional_information = create_additional_information()
            writer.writerow([name, description, cost, category, additional_information])


def create_order_data(customer_count, product_count, order_count):
    """
    Combines the customer and product data to form orders in the database.
    :param customer_count: number of customers created.
    :param product_count: number of products created.
    :param order_count: number of orders to create.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "orders.csv"
    columns = ['customer_id', 'product_id', 'quantity', 'authorization', 'notes']

    timezone = pytz.timezone('America/Chicago')
    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for index in range(order_count):
            customer_id = random.randint(1, customer_count)
            product_id = random.randint(1, product_count)
            quantity = random.randint(1, 100)
            authorization = {'authorized_by': fake.name(), 'authorized_at': fake.date_time(timezone).strftime('%Y-%m-%dT%H:%M:%S.%f%z')}
            if is_selected(PROBABILITY_LOW):
                authorization['reauthorized_by'] = fake.name()
                authorization['reauthorized_at'] = fake.date_time(timezone).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            notes = {'notes': [fake.text()]}
            if is_selected(PROBABILITY_LOW):
                notes['notes'].append(fake.text())
            if is_selected(PROBABILITY_VERY_LOW):
                notes['notes'].append(fake.text())
            writer.writerow([customer_id, product_id, quantity, authorization, notes])
            if index % 50000 == 0:
                print(f"Generated {index} orders...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--customers", type=int, default=CUSTOMER_COUNT,
                        help=f"Number of customers to generate. Default is {CUSTOMER_COUNT}")
    parser.add_argument("-p", "--products", type=int, default=PRODUCT_COUNT,
                        help=f"Number of products to generate. Default is {PRODUCT_COUNT}")
    parser.add_argument("-o", "--orders", type=int, default=ORDER_COUNT,
                        help=f"Number of orders to generate. Default is {ORDER_COUNT}")
    args = parser.parse_args()

    create_customer_data(args.customers)
    create_product_data(args.products)
    create_order_data(args.customers, args.products, args.orders)
    print("Done.")
