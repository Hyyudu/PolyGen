from collections import defaultdict

from tools import *
from gen_config import gen_config
import math

from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader("gen_main"),
    autoescape=False
)


def split_list(lst: list, N: int) -> list[list]:
    return [lst[i:i + N] for i in range(0, len(lst), N)]


def fetch_all_data() -> dict[str, list[dict]]:
    result = {}
    dataz_to_fetch = set()
    for config_key, config in gen_config.items():
        if config.skip:
            continue
        dataz_to_fetch.add(config_key)
        for key in config.additional_data.keys():
            dataz_to_fetch.add(key)
    for config_key in dataz_to_fetch:
        config = gen_config[config_key]
        if config.googlesheet_id:
            print("Getting data for " + config_key)
            gamedata = googlesheet_data(
                sheet_id=config.googlesheet_id,
                page=config.googlesheet_page
            )
        else:
            content_file = config.content_file or config_key + '.csv'
            gamedata = parse_csv(f'content/{content_file}')
        result[config_key] = gamedata
    return result

def generate():
    total_data: dict[str, list[dict]] = fetch_all_data()
    total_cards_count = defaultdict(int)

    for config_key, config in gen_config.items():
        if config.skip:
            continue
        output_filename = 'results/' + config_key + 's.html'
        template_file = config.template_file or config_key + '.htm'
        template = env.get_template(template_file)
        css_files = config.css or [config_key + '.css']

        gamedata = total_data[config_key]
        additional_data = {}
        if config.additional_data:
            for key, field in config.additional_data.items():
                additional_data[key] = {item[field]: item for item in total_data[key]}
        rendered = []
        for item in gamedata:
            if item['print']:
                if item.setdefault('print', 1) == 0:
                    continue
            text = template.render(**item, entity=item, **additional_data)
            rendered.extend([text] * item['print'])
            total_cards_count[config.items_per_page] += item['print']
        chunks = split_list(rendered, config.items_per_page)

        output = env.get_template('main.html').render(
            chunks=chunks,
            css_files=css_files,
            wrapper_class=config.wrapper_class,
        )

        print(config_key + " generated")
        open(output_filename, 'w', encoding='utf-8').write(output)

    qty_text = ""
    for ipp, qty in total_cards_count.items():
        qty_text += str(ipp) + " items per page: " + str(qty) + " cards (" + str(
            math.ceil(qty / ipp)) + " pages total)\n"
    with open("pages_count.txt", "w") as f:
        f.write(qty_text)


if __name__ == '__main__':
    generate()
