import csv
import json
import random

from faker import Faker
import faker_commerce

OUTPUT_DIRECTORY = '../initdb.d/'
CUSTOMER_COUNT = 200
PRODUCT_COUNT = 2000
ORDER_COUNT = 2000000

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


def create_customer_data():
    """
    Creates the customer data file used to populate the database.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "customers.csv"
    columns = ['first_name', 'last_name', 'organization_name', 'addresses']

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for _ in range(CUSTOMER_COUNT):
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


def create_product_data():
    """
    Creates the product data file used to populate the database.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "products.csv"
    columns = ['name', 'description', 'cost', 'category', 'additional_information']

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for _ in range(PRODUCT_COUNT):
            name = fake.ecommerce_name()
            description = fake.sentence()
            cost = fake.ecommerce_price(False)
            category = fake.ecommerce_category()
            additional_information = create_additional_information()
            writer.writerow([name, description, cost, category, additional_information])


def create_order_data():
    """
    Combines the customer and product data to form orders in the database.
    :return: void
    """
    output_file_name = OUTPUT_DIRECTORY + "orders.csv"
    columns = ['customer_id', 'product_id', 'quantity', 'authorization', 'notes']

    with open(output_file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for index in range(ORDER_COUNT):
            customer_id = random.randint(1, CUSTOMER_COUNT)
            product_id = random.randint(1, PRODUCT_COUNT)
            quantity = random.randint(1, 100)
            authorization = {'authorized_by': fake.name(), 'authorized_at': fake.date_time()}
            if is_selected(PROBABILITY_LOW):
                authorization['reauthorized_by'] = fake.name()
                authorization['reauthorized_at'] = fake.date_time()
            notes = {'notes': [fake.text()]}
            if is_selected(PROBABILITY_LOW):
                notes['notes'].append(fake.text())
            if is_selected(PROBABILITY_VERY_LOW):
                notes['notes'].append(fake.text())
            writer.writerow([customer_id, product_id, quantity, authorization, notes])
            if index % 10000 == 0:
                print(f"Generated {index} orders...")


if __name__ == '__main__':
    create_customer_data()
    create_product_data()
    create_order_data()
    print("Done.")
