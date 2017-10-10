from collections import defaultdict
from random import randint
from os.path import join, basename


class FixtureCreator:

    PROPERTY = 'restshop.Property'
    PROPERTY_VALUE = 'restshop.PropertyValue'
    TAG = 'restshop.Tag'
    USER = 'auth.User'
    SELLER = 'restshop.Seller'
    PRODUCT = 'restshop.Product'
    UNIT = 'restshop.Unit'
    UNIT_IMAGE = 'restshop.UnitImage'

    def __init__(self, data, seller_name=None):
        """Initialize fixtures.

        Fixtures for each model are stored in self._fixtures dict,
        where the key is the name of the model.
        """
        self._data = data
        self._fixtures = defaultdict(list)
        self._auto_ids = defaultdict(int)
        self._seller = seller_name if seller_name is not None else 'Seller'

        self._init_properties()
        self._init_property_values()
        self._init_tags()
        self._init_seller()
        self._init_products()
        self._init_units()
        self._init_unit_images()

    def get_fixtures(self):
        """Return valid Django fixtures list."""
        result = []

        fixtures_order = [
            self.PROPERTY,
            self.PROPERTY_VALUE,
            self.TAG,
            self.USER,
            self.SELLER,
            self.PRODUCT,
            self.UNIT,
            self.UNIT_IMAGE,
        ]

        for key in fixtures_order:
            result += self._fixtures[key]

        return result

    def _auto_id(self, model_name):
        """Get id for new record (counted in ascending order from 1)."""
        self._auto_ids[model_name] += 1
        return self._auto_ids[model_name]

    def _get_id(self, model_name, fields):
        """Get id of a specific record.

        Returns the first matching record in 'model_name' model.
        """
        if not isinstance(fields, dict):
            raise AttributeError('Argument fields must be a dict')

        for model in self._fixtures[model_name]:
            if all(model['fields'][field] == fields[field]
                   for field in fields):
                return model['pk']

    def _exists(self, model_name, fields):
        """Check if a specific record exists."""
        return self._get_id(model_name, fields) is not None

    def _add_record(self, model_name, fields, pk=None):
        """Add a record to fixtures list."""
        self._fixtures[model_name].append({
                'model': model_name,
                'pk': self._auto_id(model_name) if pk is None else pk,
                'fields': fields
        })

    def _add_if_not_exists(self, model_name, fields):
        if not self._exists(model_name, fields):
            self._add_record(model_name, fields)

    def _init_properties(self):
        for property_name in ['Size', 'Color']:
            self._add_record(self.PROPERTY, {
                'name': property_name
            })

    def _get_tag_set(self, t):
        tag_map = {tag['fields']['name']: tag['pk']
                   for tag in self._fixtures[self.TAG]}

        return [tag_map[tag] for tag in t]

    def _init_property_values(self):
        color_property = self._get_id(self.PROPERTY, {'name': 'Color'})
        size_property = self._get_id(self.PROPERTY, {'name': 'Size'})

        for item in self._data:
            color = item['color']

            self._add_if_not_exists(self.PROPERTY_VALUE, {
                'value': color,
                'property': color_property
            })

            for size in item['sizes']:
                self._add_if_not_exists(self.PROPERTY_VALUE, {
                    'value': size,
                    'property': size_property
                })

    def _init_tags(self):
        for item in self._data:
            for tag in item['tags']:
                self._add_if_not_exists(self.TAG, {
                    'name': tag
                })

    def _init_seller(self):
        # Initialize with 2, because 1 can be hold by superuser.
        user_id = 2
        user_email = '{s}@{s}.com'.format(s=self._seller)

        self._add_record(self.USER, {
            'password': 'pbkdf2_sha256$36000$WCWdPeKfXD1J$pPuQAp5UR2f3MSptf4/F5sakvZyiJLH93WKgP2Tv/wg=',
            'username': user_email,
            'email': user_email,
            'is_staff': True
        }, pk=user_id)

        self._add_record(self.SELLER, {
            'user': user_id,
            'name': self._seller,
            'address': '{} str., 22'.format(self._seller)
        })

    def _init_products(self):
        seller_id = self._get_id(self.SELLER, {'name': self._seller})

        for item in self._data:
            self._add_if_not_exists(self.PRODUCT, {
                'title': item['title'],
                'tag_set': self._get_tag_set(item['tags']),
                'seller': seller_id,
                'description': item['description']
            })

    def _init_units(self):
        for item in self._data:
            product_id = self._get_id(self.PRODUCT, {
                                          'title': item['title'],
                                          'tag_set': self._get_tag_set(item['tags']),
                                          'description': item['description']
                                      })

            color_id = self._get_id(self.PROPERTY_VALUE, {'value': item['color']})

            for size in item['sizes']:
                sku = self.get_sku(item['sku'], size)
                size_id = self._get_id(self.PROPERTY_VALUE, {'value': size})

                self._add_record(self.UNIT, {
                    'product': product_id,
                    'value_set': [color_id, size_id],
                    'price': item['price'],
                    'num_in_stock': self.get_random_stock_num()
                }, sku)

    def _init_unit_images(self):
        for item in self._data:
            sku_set = [self.get_sku(item['sku'], size)
                       for size in item['sizes']]

            for i, image in enumerate(item['images']):
                # First image is always main.
                is_main = True if i == 0 else False

                self._add_record(self.UNIT_IMAGE, {
                    'unit_set': sku_set,
                    'image': join('product_images', basename(image)),
                    'is_main': is_main
                })

    @staticmethod
    def get_sku(sku, size):
        return '{}-{}'.format(sku, size)

    @staticmethod
    def get_random_stock_num():
        n = randint(0, 15)

        return n if n >= 8 else 0
