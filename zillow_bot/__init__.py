__version__ = "0.1.0"
from dotenv import load_dotenv
from .api.properties import fetch_properties
from .parser.parse import parse_properties

load_dotenv()


def main():
    properties = fetch_properties()
    parse_properties(properties)
