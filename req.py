import requests
import re
import os
import random
import time
import hashlib


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.864.59 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/76.0.4017.123",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0"
]



def sendRequests(url):
    session = requests.Session()
    session.headers.update({"User-Agent": random.choice(user_agents)})
    response = session.get(url)
    if "images" in url:
        wait = 0
    else: 
        wait = 1
    time.sleep(wait)
    print(f"{response.status_code}: opening {url}")
    return response

def findProductUrl(text):
    pattern = r'"product_url":"(https://www\.tokopedia\.com/[^"]+)"'
    urls = set(re.findall(pattern, text))
    urls = list(urls)
    print(f"total products: {len(urls)}")
    return urls

def findImages(text):
    pattern = r'"URLMaxRes":"(https://images\.tokopedia\.net/img/cache/[^"]+)"'
    matches = set(re.findall(pattern, text))
    # print(f"total images: {len(matches)}")
    matches = list(matches)
    return matches

def generateHash(url):
    return hashlib.md5(url.encode()).hexdigest()

def saveImages(images, folder="images"):
    # Check if the folder exists and get the list of files in it
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # existing_files = os.listdir(folder)
    
    # # Skip saving if the number of files in the folder equals the number of images
    # if len(existing_files) == len(images):
    #     print(f"Skipping saving. The folder '{folder}' already contains {len(images)} images.")
    #     return

    # Save the images
    for image in images:

        # check if files already downloaded
        filename = f"{generateHash(image)}.jpg"
        # if filename not in existing_files:
        response = sendRequests(image)
        file_path = os.path.join(folder, filename)
            
        # Save the new image
        with open(file_path, 'wb') as f:
            f.write(response.content)


def getProductName(url):
    itemName = url.replace('https://www.tokopedia.com/', '')
    itemName = itemName.split('?')[0]
    itemName = itemName.split('/')[1]
    return itemName

# open shopList and get product url
def getProducts(shopUrl):
    response = sendRequests(shopUrl)
    time.sleep(1)
    text = response.text
    urls = findProductUrl(text)
    return urls

# open product url and get image url
def getImages(productUrl):
    response = sendRequests(productUrl)
    text = response.text
    images = findImages(text)
    return images

def getProductList(data:dict):
    shopName = data["name"]
    products = data["products"]
    page = data["page"]
    shopUrl = data["url"]
    productList = []

    while page > 0:
        productList.extend(getProducts(f"{shopUrl}page/{page}"))
        page -= 1
    
    print(f"{shopName}: {len(productList)} of {products} found")
    return productList

def allImages(productUrl, shopName):
    productName = getProductName(productUrl)
    images = getImages(productUrl)
    if not os.path.exists(shopName):
        os.makedirs(shopName)
    folder = f"{shopName}/{productName}"
    saveImages(images, folder=folder)

def main(shopList:list):
    for shop in shopList:
        shopName = shop["name"]
        productList = getProductList(shop)
        folders = [name for name in os.listdir(shopName) if os.path.isdir(os.path.join(shopName, name))]

        for i, product in enumerate(productList):
            print(f"{shopName}: {i+1}/{len(productList)}")
            productName = getProductName(product)

            if productName not in folders:
                # check folders
                allImages(product, shopName)


if __name__ == "__main__":
    shopList = [{"name":"sovlo",
                 "products": 507,
                 "page":7,
                 "url":"https://www.tokopedia.com/sovlo/product/"},
                {"name":"kamalika_artprints",
                "products":1588,
                "page":20,
                "url":"https://www.tokopedia.com/kamalikaartprints/product/"},
                {"name":"pamole",
                "products":181,
                "page":3,
                "url":"https://www.tokopedia.com/pamole/product/"}
                ]
    

    # shopListRev = [shopList[1]]
    # main(shopList)

    shopPageList = [
        "https://www.tokopedia.com/kamalikaartprints/etalase/pawai",
        "https://www.tokopedia.com/kamalikaartprints/etalase/foldable-bag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/totebag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/pouch",
        "https://www.tokopedia.com/kamalikaartprints/etalase/pouch/page/2",
        "https://www.tokopedia.com/kamalikaartprints/etalase/sling-bags",
        "https://www.tokopedia.com/kamalikaartprints/etalase/shoulder-bag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/key-pouch",
        "https://www.tokopedia.com/kamalikaartprints/etalase/laptop-bag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/backpack",
        "https://www.tokopedia.com/kamalikaartprints/etalase/tas-bekal",
        "https://www.tokopedia.com/kamalikaartprints/etalase/drawstring-bag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/handbag",
        "https://www.tokopedia.com/kamalikaartprints/etalase/granada",
        "https://www.tokopedia.com/kamalikaartprints/etalase/waistbag",

    ]

    shopName = "kamalika_artprints"
    # for i in shopPageList:
    # print(f"page {i}")
    productList = getProducts(shopPageList[-10])

    for ii, product in enumerate(productList):
        print(f"{shopName}: {ii+1}/{len(productList)}")
        allImages(product, shopName)