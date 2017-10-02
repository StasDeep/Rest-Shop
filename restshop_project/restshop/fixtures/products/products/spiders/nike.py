from urllib.request import urlretrieve
from os import mkdir
from os.path import exists, join

import scrapy


class NikeSpider(scrapy.Spider):
    name = 'nike'
    images_dir = 'images'
    urls = [{
        'url': 'https://store.nike.com/us/en_us/pw/mens-lifestyle-shoes/7puZoneZoi3',
        'tags': ['men', 'lifestyle']
    }, {
        'url': 'https://store.nike.com/us/en_us/pw/mens-running-shoes/7puZ8yzZoi3',
        'tags': ['men', 'running']
    }, {
        'url': 'https://store.nike.com/us/en_us/pw/mens-basketball-shoes/7puZ8r1Zoi3',
        'tags': ['men', 'basketball']
    }]

    def start_requests(self):
        for x in self.urls:
            url = x['url']
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 meta={'tags': x['tags']})

    def parse(self, response):
        for item in response.css('.grid-item'):

            # Skip customizable items.
            if item.css('.customize-it'):
                continue

            multiple_color_options = item.css('.color-options li a')

            if multiple_color_options:
                for a_tag in multiple_color_options:
                    yield response.follow(a_tag,
                                          callback=self.parse_item,
                                          meta={'tags': response.meta['tags']})
            else:
                yield response.follow(item.css('.grid-item-image-wrapper a')[0],
                                      callback=self.parse_item,
                                      meta={'tags': response.meta['tags']})

    def parse_item(self, response):
        content = response.css('.exp-pdp-main-pdp-content')

        sku = content.css('.exp-style-color::text').extract_first().split(': ')[1]
        title = content.css('.exp-product-title::text').extract_first()
        price = content.css('.exp-product-info .exp-pdp-local-price::text').re_first(r'\$(.*)')
        sizes = content.css('select[name=skuAndSize] option:not(.selectBox-disabled)::text').extract()
        color = content.css('.colorText::text').extract_first().split('/')[0]
        links = content.css('.exp-pdp-alt-images-carousel img::attr(src)').extract()

        # Replace PDP_THUMB with PDP_HERO to get 620x620 image instead of 60x60 thumbnail
        links = [link.replace('PDP_THUMB', 'PDP_HERO') for link in links]

        images = self.download_and_get(links, sku)

        if price:
            price = round(float(price))

        if sizes:
            sizes = [size.strip() for size in sizes]

        yield {
            'sku': sku,
            'title': title,
            'price': price,
            'sizes': sizes,
            'color': color,
            'images': images,
            'tags': response.meta['tags']
        }

    def download_and_get(self, links, sku):
        """Download images and return their names"""
        if not exists(self.images_dir):
            mkdir(self.images_dir)

        names = []

        for i, link in enumerate(links):
            image_name = '{}_{}.jpg'.format(sku, str(i))
            path = join(self.images_dir, image_name)

            names.append(path)

            if link.startswith('//'):
                link = 'https:' + link

            urlretrieve(link, path)

        return names
