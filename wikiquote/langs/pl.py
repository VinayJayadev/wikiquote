from typing import List, Text, Tuple
import lxml

from .. import utils

MAIN_PAGE = "Strona_główna"

class MissingQOTDException(Exception):
    pass

def extract_quotes(tree: lxml.html.HtmlElement, max_quotes: int) -> List[Text]:
    q_lst = utils.extract_quotes_li(tree, max_quotes)
    return [utils.remove_credit(q) for q in q_lst]


def qotd(html_tree: lxml.html.HtmlElement) -> Tuple[Text, Text]:

  quote_element = html_tree.xpath("//div[@class='tresc']//table//tr[1]//td//i//b")[0]
  quote = quote_element.text_content().strip()
  author_element = html_tree.xpath("//div[@class='tresc']//table//tr[2]//td//a")[0]
  author = author_element.text_content().strip()
  return  quote, author
