import logging
import re
from typing import List, Text, Tuple

import lxml

from .. import utils

MAIN_PAGE = "Wikiquote:Accueil"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def extract_quotes(tree: lxml.html.HtmlElement, max_quotes: int) -> List[Text]:
    # French wiki uses a "citation" HTML class
    nodes = tree.xpath('//div[@class="citation"]')
    quotes = [utils.clean_txt(node.text_content()) for node in nodes]
    return quotes[:max_quotes]


def qotd_old_method(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:
    tree = html_tree.get_element_by_id("mf-cdj")
    tree = tree.xpath("div/div")[1].xpath("table/tbody/tr/td")[1]

    quote = tree.xpath("div/i")[0].text_content()
    author = tree.xpath("div/a")[0].text_content()
    return quote, author


def qotd_new_method(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:
    quote_element = html_tree.xpath('//blockquote/p')[0]
    quote_text = quote_element.text_content().strip().replace("«\xa0", ' ').replace("\xa0",'').replace("»",'')
    author_element = html_tree.xpath('//p[@style="margin:-0.7em 0 0.3em 6em"]/a')[0]
    author_text = author_element.text_content().strip()

    return quote_text, author_text



def qotd(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:
    try:
        return qotd_new_method(html_tree)
    except Exception as e:
        logger.warning("Could not extract French QOTD using new method due to: %s", e)

    return qotd_old_method(html_tree)
