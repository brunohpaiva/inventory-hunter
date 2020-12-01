import logging

from scraper.common import ScrapeResult, Scraper, ScraperFactory


class KabumScrapeResult(ScrapeResult):
    def parse(self):
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('h1', class_='titulo_det')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            logging.warning(f'missing title: {self.url}')

        buy_button = self.soup.body.select_one('div[class^=\'box_botao\']')

        if buy_button is None:
            logging.warning(f'missing buy button: {self.url}')
            return

        is_in_stock = 'box_botao-cm' in buy_button["class"] or 'comprar_detalhes.png' in buy_button.find('img')["src"]

        if is_in_stock:
            price_str = None

            # check if not in sale
            price_box = self.soup.body.find('div', class_='box_preco')
            if price_box:
                price_str = self.set_price(price_box.find('div', class_='preco_normal'))

            # check if is in sale
            price_box = self.soup.body.find('div', class_='box_preco-cm')
            if price_box:
                price_str = self.set_price(price_box.find('div', class_='preco_desconto-cm'))

            if price_str:
                alert_subject = f'In Stock for {price_str}'
            else:
                logging.warning(f'missing price: {self.url}')
                return

            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class KabumScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'kabum'

    @staticmethod
    def get_result_type():
        return KabumScrapeResult

    @staticmethod
    def generate_short_name(url):
        parts = [i for i in url.path.split('/') if i]
        if parts:
            return parts[1]
