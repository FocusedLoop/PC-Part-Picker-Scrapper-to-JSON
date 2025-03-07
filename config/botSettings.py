BOT_SETTING = {
    "mouse_speed": (0.5, 3), # Lowest possible mouse speed, Highest possible mouse speed
    "Re_box_position": [(820, 755), (855, 790)], # ReCapture - Top left box corner, Bottom right box corner
    "Cloud_box_position":  [(305, 545), (335, 580)], # Cloudflare - Top left box corner, Bottom right box corner
}

URL_SCRAPPING_SETTINGS = {
    "pages": 500, # Number of pages to scrap URLS from
    "random_delay": (3, 5) # Set delay between pages - Lowest possible delay, Maximum possible delay
}

BUILD_SCRAPPING_SETTINGS = {
    "url_amount": 3000, # How many urls from the url file to scrap
    "random_delay": (5, 7) # Set delay between pages - Lowest possible delay, Maximum possible delay
}