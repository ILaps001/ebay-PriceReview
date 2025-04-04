from EbayScraper import searchEbay
import os


catagories=["Vintage & Antique Brooches & Pins",
            "Vintage & Antique Bracelets & Charms",
            "Vintage & Antique Necklaces & Pendants",
            "Vintage & Antique Collections & Lots",
            "Vintage & Antique Earrings",
            "Decorative Pottery & Glassware",
            "Decorative Cookware, Dinnerware & Serveware",
            ]

for categorytopull in catagories:
    items_df=searchEbay(category=categorytopull)
    folderPath = "/Users/isabellalapsley/Desktop/ebay-PriceReview/data"
    path=os.path.join(folderPath, f'{categorytopull}.csv')
    items_df.to_csv(path)
