rm -rf media/product_images
cd restshop/fixtures/products
rm -rf product_images
rm -rf nike.json
scrapy crawl nike -o nike.json
cd ..
python process_raw.py -i products/nike.json -o nike.json
cd ../..
mv restshop/fixtures/products/product_images media/product_images
python manage.py flush --noinput
python manage.py loaddata nike
