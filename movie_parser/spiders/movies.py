import scrapy
import re
from scrapy import signals 

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def __init__(self, *args, **kwargs):
        super(MoviesSpider, self).__init__(*args, **kwargs)
        self.items_count = 0  

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(cls, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider

    def item_scraped(self, item, response, spider):
        self.items_count += 1
        self.logger.info(f"ПРОГРЕСС: Собрано {self.items_count} фильмов")

    def parse(self, response):
        links = response.css('div.mw-category-group ul li a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_movie)

        next_page = response.xpath('//a[contains(text(), "Следующая страница")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_movie(self, response):
        title_raw = response.css('h1#firstHeading *::text').getall()
        title = "".join(title_raw).strip()

        def get_card_data(label_list):
            if isinstance(label_list, str):
                label_list = [label_list]
                
            for label in label_list:
                path = f'//th[contains(., "{label}")]/following-sibling::td'
                data = response.xpath(f'{path}//text()[not(ancestor::style) and not(ancestor::sup) and not(ancestor::div[contains(@class, "navbox")])]').getall()
                
                if data:
                    text = ", ".join(dict.fromkeys([t.strip() for t in data if len(t.strip()) > 1]))
                    text = re.sub(r'\[\d+\]', '', text) 
                    return text.replace(" ,", ",").strip()
            return "Нет данных"

        imdb_id = "N/A"
        imdb_link = response.xpath('//a[contains(@href, "imdb.com/title/tt")]/@href').get()
        if imdb_link:
            match = re.search(r'tt\d+', imdb_link)
            if match:
                imdb_id = match.group()

        raw_year = get_card_data("Год")
        year_match = re.search(r'\d{4}', raw_year)
        clean_year = year_match.group(0) if year_match else raw_year

        yield {
            'title': title,
            'year': clean_year,
            'country': get_card_data(["Страна", "Стран", "Производство"]),
            'director': get_card_data("Режиссёр"),
            'genre': get_card_data("Жанр"),
            'imdb_id': imdb_id
        }