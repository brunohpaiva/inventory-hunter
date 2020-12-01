import logging

from scraper.common import ScrapeResult, Scraper, ScraperFactory


class KabumScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('h1', class_='titulo_det')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            logging.warning(f'missing title: {self.url}')

        preco_traco = self.soup.body.find('div', class_='preco_traco')
        if preco_traco:
            # get listed price
            tag = preco_traco.find('div', class_='preco_normal')
            price_str = self.set_price(tag)
            if price_str:
                alert_subject = f'In Stock for {price_str}'
            else:
                logging.warning(f'missing price: {self.url}')

            # check for add to cart button
            tag = self.soup.body.select_one('div.botao-comprar > img')
            if tag and 'comprar_detalhes.png' in tag['src']:
                self.alert_subject = alert_subject
                self.alert_content = f'{alert_content.strip()}\n{self.url}'
        else:
            logging.warning(f'missing preco_traco div: {self.url}')


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
