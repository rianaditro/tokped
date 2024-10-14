# Product Image Scraping Script

This repository contains a Python script designed to scrape product images from multiple shops. Each shop can have multiple products, and each product can have multiple images. The script is highly flexible, allowing the use of both **requests** or **Selenium** for automation, depending on the complexity of the website being scraped. Additionally, it implements Object-Oriented Programming (OOP) principles to ensure scalability and modularity.

## 📦 Features

- **Supports Multiple Shops and Products**: The script is designed to scrape images from multiple shops, and for each shop, all product images will be downloaded.
- **Download Images from Each Product**: For each product in the shop, all available images are downloaded.
- **Avoid Redownloading Images**: The script uses **hashing** to rename and store downloaded images. This ensures that duplicate images are not downloaded again, saving bandwidth and time.
- **Request or Selenium Automation**: 
  - If the website is simple and does not rely heavily on JavaScript, the script uses the **requests** library.
  - If the website requires interaction with JavaScript or is dynamic, **Selenium** can be used to automate the browsing and scraping.
- **OOP Architecture**: The script is designed using Object-Oriented Programming principles, making it easy to extend and maintain.

## 🛠️ How It Works

1. **Shop Scraping**: The script loops through a list of shops to collect product details.
2. **Product Scraping**: For each shop, it iterates over all products and collects image URLs.
3. **Image Downloading**: The images are downloaded and saved locally. Each image is hashed and renamed based on its hash value to prevent duplicates.
4. **Avoid Redownloading**: Before downloading an image, the script checks if the hash of the image exists in the local storage to avoid redownloading the same image.

## 🏗️ Project Structure

```

|-- main.py                # Contains main class for PageExtractor and ImageDownloader
|-- req.py                 # Main functions that runs the script and list of url using requests
|-- sel.py                 # Selenium automation for click images. for kampus tasks and learning resources
|-- README.md              # Documentation (this file)
|-- requirements.txt       # Required libraries and dependencies
```

## 🚀 Getting Started

### Prerequisites
Ensure you have **Python 3.10** installed along with the required libraries. You can install the dependencies using:

```bash
pip install -r requirements.txt
```

## 🧰 Dependencies

- **requests**: For simple HTTP requests to download static content.
- **selenium**: For automating browsers in dynamic web pages that require JavaScript interaction.
- **hashlib**: To hash image files and avoid downloading duplicates.
- **beautifulsoup4**: For parsing HTML and extracting data from pages.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## 📚 How Hashing Works to Prevent Redownload

Each image file is hashed using **SHA-256** before it is saved. If the hash already exists in the directory, the script skips downloading the file again. This ensures that the same images from different products or shops are not downloaded multiple times.

Example Code for Hashing:
```python
import hashlib

filename = hashlib.md5(url.encode()).hexdigest()
```

## 🛠️ Future Improvements

- **Multi-threading**: Speed up scraping by implementing multi-threading to handle multiple shops and products simultaneously.
- **Database Integration**: Store shop, product, and image details in a database for better data management.
- **Progress Logging**: Implement detailed logging of scraping progress and errors.
  
## 🖇️ Contributing

Feel free to submit pull requests, create issues, or provide suggestions for improvements. Contributions are always welcome!

---

### License
This project is licensed under the MIT License.

---

### Contact
For questions or support, you can reach out at [rianaditro@gmail.com].
