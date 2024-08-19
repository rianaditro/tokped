from main import *
import json

if __name__ == "__main__":
    shopList = [{"name":"sovlo",
                 "page":7,
                 "url":"https://www.tokopedia.com/sovlo/product/"},
                {"name":"kamalika_artprints",
                "page":20,
                "url":"https://www.tokopedia.com/kamalikaartprints/product/"},
                {"name":"pamole",
                "page":3,
                "url":"https://www.tokopedia.com/pamole/product/"},
                {"name":"hawman",
                 "page":1,
                 "url":"https://www.tokopedia.com/hawman/product/"}
                ]
    
    # shopList = [{"name":"sovlo",
    #              "page":1,
    #              "url":"https://www.tokopedia.com/sovlo/product/"},
    #             {"name":"kamalika_artprints",
    #             "page":1,
    #             "url":"https://www.tokopedia.com/kamalikaartprints/product/"}
    #             ]
    
    
    # shopUrl = shopList[-1]["url"]

    productUrl = "https://www.tokopedia.com/hawman/tas-micro-size-hawman-transparant?extParam=src%3Dshop%26whid%3D2496341"

    extractor = PageExtractor()
    imageUrls = extractor.extractAll(shopList)

    with open("finalUrls.json", "w") as f:
        json.dump(imageUrls, f)
    
    downloader = ImageDownloader(imageUrls)
    downloader.downloadAll()
