import requests
import re
import os
import time
import hashlib


keywords = [
    "-tas-", "-bag-", "sling", "tote", "totebag", "slingbag", "pouch", "waistbag", "hand-bag", "tas-laptop", 
]


class PageExtractor:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()

    def generatePage(self, listShop: list):
        # generate data dictionary of complete URL of each shop
        new_data = dict()

        for shopData in listShop:
            shopName = shopData["name"]
            baseUrl = shopData["url"]
            page = shopData["page"]

            # collecting urls for from multiple-page shop
            pageUrls = []
            if page > 1:
                pageUrls.append(baseUrl)
                for i in range(2, page + 1):
                    pageUrls.append(f"{baseUrl}page/{i}")
                new_data[shopName] = pageUrls
            else:
                new_data[shopName] = [baseUrl]
        
        return new_data

    def getProductUrls(self, url):
        # sending request
        response = self.session.get(url, headers=self.headers)
        time.sleep(1)
        text = response.text

        # extracting urls
        pattern = r'"product_url":"(https://www\.tokopedia\.com/[^"]+)"'
        urls = re.findall(pattern, text)   

        # validate if the url contains any keyword  
        urls = [url for url in urls if any(keyword in url for keyword in keywords)] 

        return urls
    
    def getProductName(self, url):
        # from https://www.tokopedia.com/hawman/tas-micro-size-hawman-transparant?extParam=src%3Dshop%26whid%3D2496341
        productName = url.replace('https://www.tokopedia.com/', '')

        # hawman/tas-micro-size-hawman-transparant?extParam=src%3Dshop%26whid%3D2496341
        productName = productName.split('?')[0]

        # hawman/tas-micro-size-hawman-transparant
        productName = productName.split('/')[1]

        # tas-micro-size-hawman-transparant
        return productName
    
    def getImageUrls(self, url):
        # sending request of a product page
        response = self.session.get(url, headers=self.headers)

        # extracting image urls
        pattern = r'"URLMaxRes":"(https://images\.tokopedia\.net/img/cache/[^"]+)"'
        matches = re.findall(pattern, response.text)
        return matches
    
    def extractAll(self, listShop: list):
        # generate image urls for each product
        results = dict()      

        # generate list of shop page with pagination
        shopData = self.generatePage(listShop)

        # {"sovlo":["sovlo1", "sovlo2"]}
        for shopName, shopPages in shopData.items():
            pageCounter = len(shopPages)

            # sovlo1 -> product1, product2, ...
            for i, page in enumerate(shopPages):
                imagesPerProduct = dict()
                productUrls = self.getProductUrls(page)
                productCounter = len(productUrls)

                # product1 -> image1, image2, ...
                for ii, product in enumerate(productUrls):
                    productName = self.getProductName(product)
                    imageUrls = self.getImageUrls(product)

                    imagesPerProduct[productName] = imageUrls

                    print(f"{shopName} page: {i+1}/{pageCounter}, product: {ii+1}/{productCounter}, extracted: {len(imageUrls)} of image urls.")

                results[shopName] = imagesPerProduct

        return results

class ImageDownloader:
    def __init__(self, data: dict):
        self.data = data
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()

    def download(self, url, folder):
        #  get image content
        response = self.session.get(url, headers=self.headers)
        image = response.content

        # turn url into filename
        filename = hashlib.md5(url.encode()).hexdigest()

        # save image
        with open(f"{folder}/{filename}.jpg", "wb") as f:
            f.write(image)


    def downloadAll(self):
        for shopName, productList in self.data.items():
            productCount = len(productList)

            for i, (productName, imageUrls) in enumerate(productList.items()):
                folder = f"{shopName}/{productName}"
                imageCount = len(imageUrls)

                if not os.path.exists(folder):
                    os.makedirs(folder)

                for ii, image in enumerate(imageUrls):
                    self.download(image, folder)

                    print(f"{shopName} product no: {i+1}/{productCount} - {productName}, downloaded: {ii+1}/{imageCount} of images.")

    
        
