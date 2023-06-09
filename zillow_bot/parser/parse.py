import math
import os

from pyairtable import Table

AIR_TABLE_API_KEY = os.getenv("AIR_TABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_ID = os.getenv("TABLE_ID")

# Mortgage
TAX_RATE = 0.02  # Get this dynamically through another API
INSURANCE = 100
HOA = 0

# Utilities
GAS_AND_ELECTRICITY = 0
WATER = 0
SEWER = 0
GARBAGE = 0
LAWN_AND_SNOW = 0

# Property Management
MANAGEMENT_FEE = 0.1
VACANCY_RATE = 0.05
MAINTENANCE = 0.05

table = Table(AIR_TABLE_API_KEY, BASE_ID, TABLE_ID)


def parse_properties(home_properties):
    print("Parsing properties...")
    deals = []
    for home_property in home_properties:
        address = home_property["address"]
        price = home_property["price"]
        rentZestimate = home_property["rentZestimate"]
        bedrooms = home_property["bedrooms"]
        bathrooms = home_property["bathrooms"]
        if rentZestimate and price:
            operating_cost = get_total_operating_expenses(price, rentZestimate)
            monthly_net_operating_income = rentZestimate - operating_cost
            annualized_net_operating_income = monthly_net_operating_income * 12
            cap_rate = annualized_net_operating_income / price

            print(
                "Cap rate: %s and Monthly NOI: %s"
                % (cap_rate, monthly_net_operating_income)
            )

            # Send to AirTable is certain conditions are met such as cap rate over 10%
            # if cap_rate > 0.10:
            deals.append(
                {
                    "Property Address": address,
                    "Price": price,
                    "Monthly Rent": rentZestimate,
                    "Operating Cost": operating_cost,
                    "Monthly NOI": monthly_net_operating_income,
                    "Capitalization Rate": cap_rate,
                    "Bedrooms": bedrooms,
                    "Bathrooms": bathrooms,
                }
            )

    table.batch_create(deals)


def get_owner_paid_utilities_costs():
    return GAS_AND_ELECTRICITY + WATER + SEWER + GARBAGE + LAWN_AND_SNOW


def get_total_management_costs(rentZestimate):
    return math.ceil(
        (
            (MANAGEMENT_FEE * rentZestimate)
            + (VACANCY_RATE * rentZestimate)
            + (MAINTENANCE * rentZestimate)
        )
    )


def get_monthly_property_tax(price):
    return math.ceil((TAX_RATE * price) / 12)


def get_total_operating_expenses(price, rentZestimate):
    return (
        get_owner_paid_utilities_costs()
        + INSURANCE
        + HOA
        + get_monthly_property_tax(price)
        + get_total_management_costs(rentZestimate)
    )
