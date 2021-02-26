import requests
import yaml
from bs4 import BeautifulSoup as bs
import datetime
import os
import pprint

pp = pprint.PrettyPrinter(indent=1)

with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

session = requests.Session()
session.headers.update(config['headers'])


def save(data, name=None):
    if name is None:
        name = str(datetime.datetime.now())

    if not os.path.exists(config['history_folder'] + '/'):
        os.mkdir(config['history_folder'])

    with open(f'{config["history_folder"]}/{name}.yaml', 'w') as file:
        yaml.dump(data, file)


def decode(s: str):
    s = s.strip().encode("ascii", "ignore").decode()
    s = ''.join([c for c in s if c.isdigit()])
    return s


def parse_page(url, sale_start_class, price_class):
    page = session.get(url)

    if page.status_code != 200:
        raise NameError(f"Site {url} failed to load, check index.yaml")
    soup = bs(page.text, 'lxml')

    st = soup.find(class_=sale_start_class).text.strip()
    price = decode(soup.find(class_=price_class).text.strip())

    return {'status': st, "price": price}


def parse(save_res: bool = False):
    with open('index.yaml') as f:
        index = yaml.safe_load(f)

    res = {}

    for prod, stores in index['products'].items():
        res[prod] = {}
        for store, info in stores.items():
            res[prod][store] = parse_page(**info)

    if save_res:
        save(res)

    return res


if __name__ == "__main__":
    pp.pprint(parse(save_res=False))
