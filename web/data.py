"""
Static product data — converted from frontend_source/src/data/products.ts
This serves as the local data source, bypassing ERPNext for the template frontend.
"""


PRODUCTS = [
    {
        "id": "1",
        "slug": "dell-latitude-5520-i7-11th",
        "name": {"ar": "ديل لاتيتيود 5520 - i7 الجيل 11", "en": "Dell Latitude 5520 - i7 11th Gen"},
        "brand": "Dell",
        "priceEGP": 14500,
        "oldPriceEGP": 16000,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 11th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1185G7",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 4-6 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal", "Best Seller"],
    },
    {
        "id": "2",
        "slug": "hp-elitebook-840-g8-i5-11th",
        "name": {"ar": "HP إليت بوك 840 G8 - i5 الجيل 11", "en": "HP EliteBook 840 G8 - i5 11th Gen"},
        "brand": "HP",
        "priceEGP": 11500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 11 - رام 16 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i5 11th Gen - 16GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1135G7",
            "ram": "16GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Best Seller"],
    },
    {
        "id": "3",
        "slug": "dell-precision-3561-i7-11th",
        "name": {"ar": "ديل بريسيجن 3561 - i7 الجيل 11", "en": "Dell Precision 3561 - i7 11th Gen"},
        "brand": "Dell",
        "priceEGP": 16500,
        "oldPriceEGP": 18000,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 32 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 11th Gen - 32GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-11850H",
            "ram": "32GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "NVIDIA T600 4GB",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 4-5 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal"],
    },
    {
        "id": "4",
        "slug": "lenovo-thinkpad-t14-gen2-i5",
        "name": {"ar": "لينوفو ثينك باد T14 الجيل 2 - i5", "en": "Lenovo ThinkPad T14 Gen 2 - i5"},
        "brand": "Lenovo",
        "priceEGP": 10500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 11 - رام 16 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i5 11th Gen - 16GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1145G7",
            "ram": "16GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "5",
        "slug": "dell-latitude-5540-i5-13th",
        "name": {"ar": "ديل لاتيتيود 5540 - i5 الجيل 13", "en": "Dell Latitude 5540 - i5 13th Gen"},
        "brand": "Dell",
        "priceEGP": 15000,
        "oldPriceEGP": 16500,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 13 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i5 13th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1345U",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Excellent - 6-8 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Best Seller"],
    },
    {
        "id": "6",
        "slug": "hp-probook-450-g9-i5-12th",
        "name": {"ar": "HP بروبوك 450 G9 - i5 الجيل 12", "en": "HP ProBook 450 G9 - i5 12th Gen"},
        "brand": "HP",
        "priceEGP": 12000,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 12 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i5 12th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1235U",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "7",
        "slug": "dell-precision-5560-i7-11th",
        "name": {"ar": "ديل بريسيجن 5560 - i7 الجيل 11", "en": "Dell Precision 5560 - i7 11th Gen"},
        "brand": "Dell",
        "priceEGP": 22000,
        "oldPriceEGP": 25000,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 32 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD+"],
            "en": ["i7 11th Gen - 32GB RAM", "512GB SSD - 15.6\" FHD+ Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-11800H",
            "ram": "32GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "NVIDIA RTX A2000 4GB",
            "screen": "15.6\" FHD+ IPS (1920x1200)",
            "battery": "Good - 4-6 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal"],
    },
    {
        "id": "8",
        "slug": "lenovo-thinkpad-x1-carbon-gen9",
        "name": {"ar": "لينوفو ثينك باد X1 كاربون الجيل 9", "en": "Lenovo ThinkPad X1 Carbon Gen 9"},
        "brand": "Lenovo",
        "priceEGP": 18000,
        "oldPriceEGP": 20000,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": False,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 512 - شاشة 14 بوصة FHD+"],
            "en": ["i7 11th Gen - 16GB RAM", "512GB SSD - 14\" FHD+ Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1185G7",
            "ram": "16GB LPDDR4x",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD+ IPS (1920x1200)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "9",
        "slug": "dell-latitude-3540-i5-13th",
        "name": {"ar": "ديل لاتيتيود 3540 - i5 الجيل 13", "en": "Dell Latitude 3540 - i5 13th Gen"},
        "brand": "Dell",
        "priceEGP": 12500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": False,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 13 - رام 8 جيجا", "SSD 256 - شاشة 15.6 بوصة FHD"],
            "en": ["i5 13th Gen - 8GB RAM", "256GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1335U",
            "ram": "8GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD TN (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "10",
        "slug": "hp-elitebook-850-g8-i7-11th",
        "name": {"ar": "HP إليت بوك 850 G8 - i7 الجيل 11", "en": "HP EliteBook 850 G8 - i7 11th Gen"},
        "brand": "HP",
        "priceEGP": 14000,
        "oldPriceEGP": 15500,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 11th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1185G7",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 4-6 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal", "Best Seller"],
    },
    {
        "id": "11",
        "slug": "dell-precision-3590-i7-13th",
        "name": {"ar": "ديل بريسيجن 3590 - i7 الجيل 13", "en": "Dell Precision 3590 - i7 13th Gen"},
        "brand": "Dell",
        "priceEGP": 19500,
        "oldPriceEGP": 22000,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 13 - رام 32 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 13th Gen - 32GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1370P",
            "ram": "32GB DDR5",
            "storage": "512GB NVMe SSD",
            "gpu": "NVIDIA RTX A500 4GB",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal"],
    },
    {
        "id": "12",
        "slug": "lenovo-thinkpad-l14-gen3-i5",
        "name": {"ar": "لينوفو ثينك باد L14 الجيل 3 - i5", "en": "Lenovo ThinkPad L14 Gen 3 - i5"},
        "brand": "Lenovo",
        "priceEGP": 9000,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 12 - رام 8 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i5 12th Gen - 8GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1245U",
            "ram": "8GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "13",
        "slug": "hp-zbook-firefly-15-g8-i7",
        "name": {"ar": "HP ZBook Firefly 15 G8 - i7", "en": "HP ZBook Firefly 15 G8 - i7"},
        "brand": "HP",
        "priceEGP": 17000,
        "oldPriceEGP": 19000,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 32 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 11th Gen - 32GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1185G7",
            "ram": "32GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "NVIDIA T500 4GB",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 4-6 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Best Seller"],
    },
    {
        "id": "14",
        "slug": "dell-latitude-7420-i7-11th",
        "name": {"ar": "ديل لاتيتيود 7420 - i7 الجيل 11", "en": "Dell Latitude 7420 - i7 11th Gen"},
        "brand": "Dell",
        "priceEGP": 13500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i7 11th Gen - 16GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1185G7",
            "ram": "16GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "15",
        "slug": "lenovo-thinkpad-t15-gen2-i7",
        "name": {"ar": "لينوفو ثينك باد T15 الجيل 2 - i7", "en": "Lenovo ThinkPad T15 Gen 2 - i7"},
        "brand": "Lenovo",
        "priceEGP": 13000,
        "oldPriceEGP": 14500,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 11th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1165G7",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "16",
        "slug": "hp-probook-440-g8-i5-11th",
        "name": {"ar": "HP بروبوك 440 G8 - i5 الجيل 11", "en": "HP ProBook 440 G8 - i5 11th Gen"},
        "brand": "HP",
        "priceEGP": 8500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "C",
        "includesCharger": False,
        "keyboardLayout": "AR",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 11 - رام 8 جيجا", "SSD 256 - شاشة 14 بوصة HD"],
            "en": ["i5 11th Gen - 8GB RAM", "256GB SSD - 14\" HD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1135G7",
            "ram": "8GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" HD TN (1366x768)",
            "battery": "Fair - 3-5 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "17",
        "slug": "dell-latitude-5530-i7-12th",
        "name": {"ar": "ديل لاتيتيود 5530 - i7 الجيل 12", "en": "Dell Latitude 5530 - i7 12th Gen"},
        "brand": "Dell",
        "priceEGP": 16000,
        "oldPriceEGP": 17500,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 12 - رام 16 جيجا", "SSD 512 - شاشة 15.6 بوصة FHD"],
            "en": ["i7 12th Gen - 16GB RAM", "512GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1265U",
            "ram": "16GB DDR4",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Best Seller"],
    },
    {
        "id": "18",
        "slug": "lenovo-thinkpad-e15-gen4-ryzen5",
        "name": {"ar": "لينوفو ثينك باد E15 الجيل 4 - Ryzen 5", "en": "Lenovo ThinkPad E15 Gen 4 - Ryzen 5"},
        "brand": "Lenovo",
        "priceEGP": 9500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج Ryzen 5 5625U - رام 8 جيجا", "SSD 256 - شاشة 15.6 بوصة FHD"],
            "en": ["Ryzen 5 5625U - 8GB RAM", "256GB SSD - 15.6\" FHD Display"],
        },
        "specs": {
            "cpu": "AMD Ryzen 5 5625U",
            "ram": "8GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "AMD Radeon Graphics",
            "screen": "15.6\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "19",
        "slug": "dell-latitude-7430-i7-12th",
        "name": {"ar": "ديل لاتيتيود 7430 - i7 الجيل 12", "en": "Dell Latitude 7430 - i7 12th Gen"},
        "brand": "Dell",
        "priceEGP": 17500,
        "oldPriceEGP": 19000,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": False,
        "condition": "imported-refurbished",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 12 - رام 16 جيجا", "SSD 512 - شاشة 14 بوصة FHD+"],
            "en": ["i7 12th Gen - 16GB RAM", "512GB SSD - 14\" FHD+ Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1265U",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD+ IPS (1920x1200)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "20",
        "slug": "hp-elitebook-845-g9-ryzen7",
        "name": {"ar": "HP إليت بوك 845 G9 - Ryzen 7", "en": "HP EliteBook 845 G9 - Ryzen 7"},
        "brand": "HP",
        "priceEGP": 15500,
        "oldPriceEGP": 17000,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج Ryzen 7 PRO 6850U - رام 16 جيجا", "SSD 512 - شاشة 14 بوصة FHD"],
            "en": ["Ryzen 7 PRO 6850U - 16GB RAM", "512GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "AMD Ryzen 7 PRO 6850U",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD",
            "gpu": "AMD Radeon 680M",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Excellent - 7-9 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": ["Hot Deal"],
    },
    {
        "id": "21",
        "slug": "dell-latitude-5440-i5-13th",
        "name": {"ar": "ديل لاتيتيود 5440 - i5 الجيل 13", "en": "Dell Latitude 5440 - i5 13th Gen"},
        "brand": "Dell",
        "priceEGP": 13000,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/dell-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "B",
        "includesCharger": True,
        "keyboardLayout": "AR-EN",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 13 - رام 16 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i5 13th Gen - 16GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1345U",
            "ram": "16GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "22",
        "slug": "lenovo-thinkpad-x13-gen2-i7",
        "name": {"ar": "لينوفو ثينك باد X13 الجيل 2 - i7", "en": "Lenovo ThinkPad X13 Gen 2 - i7"},
        "brand": "Lenovo",
        "priceEGP": 14000,
        "oldPriceEGP": 15500,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج i7 الجيل 11 - رام 16 جيجا", "SSD 512 - شاشة 13.3 بوصة FHD"],
            "en": ["i7 11th Gen - 16GB RAM", "512GB SSD - 13.3\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i7-1165G7",
            "ram": "16GB LPDDR4x",
            "storage": "512GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "13.3\" FHD IPS (1920x1080)",
            "battery": "Good - 5-7 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "23",
        "slug": "hp-probook-645-g4-ryzen5",
        "name": {"ar": "HP بروبوك 645 G4 - Ryzen 5", "en": "HP ProBook 645 G4 - Ryzen 5"},
        "brand": "HP",
        "priceEGP": 10500,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/hp-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "A",
        "includesCharger": True,
        "keyboardLayout": "EN",
        "shortSpecs": {
            "ar": ["معالج Ryzen 5 5650U - رام 16 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["Ryzen 5 5650U - 16GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "AMD Ryzen 5 5650U",
            "ram": "16GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "AMD Radeon Graphics",
            "screen": "14\" FHD IPS (1920x1080)",
            "battery": "Good - 6-8 hours",
            "warranty": "30 days functional warranty",
        },
        "tags": [],
    },
    {
        "id": "24",
        "slug": "lenovo-thinkpad-e14-gen3-i5",
        "name": {"ar": "لينوفو ثينك باد E14 الجيل 3 - i5", "en": "Lenovo ThinkPad E14 Gen 3 - i5"},
        "brand": "Lenovo",
        "priceEGP": 7000,
        "oldPriceEGP": None,
        "images": ["/static/web/images/products/lenovo-laptop.png"],
        "inStock": True,
        "condition": "imported-used",
        "grade": "C",
        "includesCharger": True,
        "keyboardLayout": "Unknown",
        "shortSpecs": {
            "ar": ["معالج i5 الجيل 11 - رام 8 جيجا", "SSD 256 - شاشة 14 بوصة FHD"],
            "en": ["i5 11th Gen - 8GB RAM", "256GB SSD - 14\" FHD Display"],
        },
        "specs": {
            "cpu": "Intel Core i5-1135G7",
            "ram": "8GB DDR4",
            "storage": "256GB NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "screen": "14\" FHD TN (1920x1080)",
            "battery": "Fair - 3-5 hours",
            "warranty": "14 days functional warranty",
        },
        "tags": [],
    },
]


ASSIUT_CENTERS = [
    {"value": "assiut-city", "label": {"ar": "مدينة أسيوط", "en": "Assiut City"}},
    {"value": "dayrout", "label": {"ar": "ديروط", "en": "Dayrout"}},
    {"value": "el-qusya", "label": {"ar": "القوصية", "en": "El Qusya"}},
    {"value": "manfalut", "label": {"ar": "منفلوط", "en": "Manfalut"}},
    {"value": "abnub", "label": {"ar": "أبنوب", "en": "Abnub"}},
    {"value": "el-fateh", "label": {"ar": "الفتح", "en": "El Fateh"}},
    {"value": "sahel-selim", "label": {"ar": "ساحل سليم", "en": "Sahel Selim"}},
    {"value": "abou-tig", "label": {"ar": "أبو تيج", "en": "Abou Tig"}},
    {"value": "el-ghanayem", "label": {"ar": "الغنايم", "en": "El Ghanayem"}},
    {"value": "sedfa", "label": {"ar": "صدفا", "en": "Sedfa"}},
    {"value": "el-badari", "label": {"ar": "البداري", "en": "El Badari"}},
]

BRANDS = ["Dell", "HP", "Lenovo"]
RAM_OPTIONS = ["8GB", "16GB", "32GB"]
CPU_FAMILIES = ["i5", "i7", "Ryzen 5", "Ryzen 7"]
GPU_TYPES = ["Integrated", "Dedicated"]
SCREEN_SIZES = ['13.3"', '14"', '15.6"']
GRADES = ["A", "B", "C"]
KEYBOARD_LAYOUTS = ["AR", "EN", "AR-EN", "Unknown"]
CONDITIONS = ["imported-used", "imported-refurbished", "used"]

WHATSAPP_NUMBER = "201066537666"
WHATSAPP_DISPLAY = "01066537666"
STORE_PHONE = "01066537666"
WORKING_HOURS = "12:00 PM – 12:00 AM"


def get_whatsapp_link(message=""):
    base = f"https://wa.me/{WHATSAPP_NUMBER}"
    if message:
        from urllib.parse import quote
        return f"{base}?text={quote(message)}"
    return base


def format_price(price):
    return f"{price:,}"


def get_product_by_slug(slug):
    for p in PRODUCTS:
        if p["slug"] == slug:
            return p
    return None


def get_products_by_tag(tag):
    return [p for p in PRODUCTS if tag in (p.get("tags") or [])]


def filter_products(
    brand=None, ram=None, cpu=None, screen=None,
    grade=None, keyboard=None, in_stock=None,
    charger=None, gpu_type=None, q=None,
    sort_by="newest",
):
    """Filter and sort products based on criteria."""
    results = list(PRODUCTS)

    if q:
        q_lower = q.lower()
        results = [
            p for p in results
            if q_lower in p["name"]["en"].lower()
            or q_lower in p["name"]["ar"]
            or q_lower in p["brand"].lower()
            or q_lower in p["specs"]["cpu"].lower()
            or q_lower in p["specs"]["ram"].lower()
            or q_lower in p["specs"]["gpu"].lower()
            or q_lower in p["slug"].lower()
        ]

    if brand:
        brands = brand if isinstance(brand, list) else [brand]
        results = [p for p in results if p["brand"] in brands]

    if ram:
        rams = ram if isinstance(ram, list) else [ram]
        results = [p for p in results if p["specs"]["ram"].startswith(tuple(rams))]

    if cpu:
        cpus = cpu if isinstance(cpu, list) else [cpu]
        results = [p for p in results if any(c.lower() in p["specs"]["cpu"].lower() for c in cpus)]

    if screen:
        screens = screen if isinstance(screen, list) else [screen]
        results = [p for p in results if any(s in p["specs"]["screen"] for s in screens)]

    if grade:
        grades = grade if isinstance(grade, list) else [grade]
        results = [p for p in results if p["grade"] in grades]

    if keyboard:
        kbs = keyboard if isinstance(keyboard, list) else [keyboard]
        results = [p for p in results if p["keyboardLayout"] in kbs]

    if in_stock:
        results = [p for p in results if p["inStock"]]

    if charger:
        results = [p for p in results if p["includesCharger"]]

    if gpu_type:
        if gpu_type == "Dedicated":
            results = [p for p in results if "NVIDIA" in p["specs"]["gpu"] or "Radeon" in p["specs"]["gpu"]]
        elif gpu_type == "Integrated":
            results = [p for p in results if "Intel" in p["specs"]["gpu"] and "NVIDIA" not in p["specs"]["gpu"]]

    # Sort
    if sort_by == "price_asc":
        results.sort(key=lambda p: p["priceEGP"])
    elif sort_by == "price_desc":
        results.sort(key=lambda p: p["priceEGP"], reverse=True)
    # newest = default order

    return results
