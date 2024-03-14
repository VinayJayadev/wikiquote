from typing import List, Text, Tuple

import lxml

from .. import utils

WORD_BLOCKLIST = ["Iturria:", "Jatorrizkoan ", "Testuingurua:"]
MAIN_PAGE = "Azala"
HEADINGS = ["kanpo loturak", "erreferentziak"]


def extract_quotes(tree: lxml.html.HtmlElement, max_quotes: int) -> List[Text]:
    q_lst = utils.extract_quotes_li(tree, max_quotes, HEADINGS, WORD_BLOCKLIST)
    return [utils.remove_credit(q) for q in q_lst]


class MissingQOTDException(Exception):
    pass

def qotd(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:
    # Check if the HTML contains the string "Txantiloi"
    if "Txantiloi" in html_tree.text_content():
        # Find the element containing "Txantiloi:2012-11 aipua"
        element = html_tree.xpath("//a[contains(@title, 'Txantiloi')]")
        # Extract the text of the element if found, otherwise return "No quotes available"
        if element:
            return element[0].text.strip(), " - No quotes available"
        else:
            return "No quotes available", ""
    else:
        quote_element = html_tree.xpath('//blockquote/p')[0]
        quote_text = quote_element.text_content().strip()
        author_element = html_tree.xpath('//p[@style="margin:-0.7em 0 0.3em 6em"]/a')[0]
        author_text = author_element.text_content().strip()

        return quote_text, author_text


