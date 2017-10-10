from urllib.request import urlretrieve
from os import mkdir
from os.path import exists, join

import scrapy


class NikeSpider(scrapy.Spider):
    name = 'nike'
    images_dir = 'product_images'
    urls = [{
        'url': 'https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3',
        'gender': 'Men'
    }, {
        'url': 'https://store.nike.com/us/en_us/pw/womens-shoes/7ptZoi3',
        'gender': 'Women'
    }]

    def start_requests(self):
        for x in self.urls:
            url = x['url']
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 meta={'gender': x['gender']})

    def parse(self, response):
        for a_tag in response.css('.exp-left-nav-category-list li:not(.exp-left-nav-more) a'):
            category = a_tag.css('::text').extract_first().split(' (')[0]

            yield response.follow(a_tag,
                                  callback=self.parse_category,
                                  meta={'tags': [
                                      response.meta['gender'],
                                      category
                                  ]})

    def parse_category(self, response):
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
        color = content.css('.colorText::text').extract_first()
        links = content.css('.exp-pdp-alt-images-carousel img::attr(src)').extract()
        description = response.css('.pi-pdpmainbody p::text').extract_first()

        if description is None:
            description = ''

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
            'description': description,
            'tags': response.meta['tags'],
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
