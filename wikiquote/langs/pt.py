from typing import List, Text, Tuple

import lxml
import lxml.html
from .. import utils

MAIN_PAGE = "Página_principal"
WORD_BLOCKLIST = ["Fonte"]
HEADINGS = ["Veja também", "Referências"]


def extract_quotes(tree: lxml.html.HtmlElement, max_quotes: int) -> List[Text]:

    dl_list = tree.xpath("//dl")
    for dl in dl_list:
        dl.getparent().remove(dl)

    return utils.extract_quotes_li(tree, max_quotes, HEADINGS, WORD_BLOCKLIST)

def qotd(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:

    quote_div = html_tree.xpath("(//div[@class='inhalt'])[1]//div[@style='background: #fff5f5; padding-top: 0.4em; padding-bottom: 0.3em; text-align:center;']")[0]
    quote_text = quote_div.xpath(".//p//b//text()")[0].strip()
    author_text = quote_div.xpath(".//p/a/text()")[-1].strip()

    return quote_text, author_text










