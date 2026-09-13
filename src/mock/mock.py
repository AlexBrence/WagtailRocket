""" 
Run these commands
1. python3 manage.py shell
2. from mock.mock import *
3. <any function from here>
"""

import datetime
import logging
import requests

from pathlib import Path
from faker import Faker

from wagtail.models import Site, Page
from wagtail.images.models import Image

from django.conf import settings
from django.core.files import File

from home.models import *
from flex.models import *
from products.models import (
    ProductListingPage, ProductCategoryListingPage, 
    ProductSubcategoryListingPage, ProductDetailPage)
from blogs.models import BlogListingPage, BlogCategoryListingPage, BlogDetailPage
from site_settings.models import (
    PhoneNumber, Contact, Email, 
    WorkDay, Location, OpeningHours, 
    SocialMedia)


logging.basicConfig(
    level=logging.INFO, 
    format='[%(levelname)s] %(funcName)s: %(message)s'
)

logger = logging.getLogger(__name__)
fkr = Faker()


BLOG_CATEGORIES = [
    "Programming", "Art", "Hardware", "Software", "Hacking", "Sports"
]

PRODUCT_CATEGORIES = {
    "Electronics": [
        "Smartphones", "Laptops", "Desktop Computers", "Tablets",
        "Smartwatches", "Headphones", "Bluetooth Speakers", "Cameras",
        "Televisions", "Gaming Consoles", "Monitors", "Routers",
    ],
    "Clothing": [
        "T-Shirts", "Jeans", "Jackets", "Sweaters", "Dresses",
        "Skirts", "Shorts", "Activewear", "Suits",
        "Underwear", "Socks", "Sleepwear",
    ],
    "Home & Kitchen": [
        "Cookware", "Bakeware", "Utensils", "Small Kitchen Appliances",
        "Storage Containers", "Bedding", "Pillows", "Blankets",
        "Furniture", "Home Decor", "Lighting", "Cleaning Supplies",
    ],
    "Beauty & Personal Care": [
        "Skincare", "Makeup", "Haircare", "Fragrances",
        "Shaving & Grooming", "Oral Care", "Bath & Body",
        "Nail Care", "Beauty Tools", "Personal Hygiene",
    ],
    "Sports & Outdoors": [
        "Fitness Equipment", "Yoga Gear", "Camping Equipment",
        "Hiking Gear", "Cycling Accessories", "Running Shoes",
        "Team Sports Equipment", "Water Sports", "Winter Sports",
        "Outdoor Clothing", "Backpacks",
    ],
    "Books": [
        "Fiction", "Non-Fiction", "Science Fiction", "Fantasy",
        "Biographies", "Self-Help", "Cookbooks",
        "Children's Books", "Educational", "Mystery & Thriller",
    ],
    "Toys & Games": [
        "Board Games", "Card Games", "Action Figures", "Dolls",
        "Puzzles", "Building Blocks", "Remote Control Toys",
        "Educational Toys", "Outdoor Play", "Video Games",
    ],
    "Automotive": [
        "Car Accessories", "Motorcycle Accessories", "Car Electronics",
        "Interior Accessories", "Exterior Accessories",
        "Car Care", "Oils & Fluids", "Tools & Equipment",
        "Replacement Parts", "Tires & Wheels",
    ],
    "Health & Wellness": [
        "Vitamins & Supplements", "Protein Powders", "Herbal Remedies",
        "Medical Supplies", "First Aid Kits",
        "Personal Protective Equipment", "Thermometers",
        "Blood Pressure Monitors", "Massagers", "Sleep Aids",
    ],
    "Pet Supplies": [
        "Dog Food", "Cat Food", "Pet Treats", "Pet Toys",
        "Collars & Leashes", "Aquariums", "Bird Cages",
        "Pet Grooming", "Pet Beds", "Litter & Accessories",
    ],
    "Office Supplies": [
        "Notebooks", "Pens & Pencils", "Printers", "Printer Ink",
        "Office Chairs", "Desks", "Filing Cabinets",
        "Calendars & Planners", "Staplers", "Paper Shredders",
    ],
    "Garden & Outdoor Living": [
        "Plants & Seeds", "Garden Tools", "Lawn Mowers",
        "Outdoor Furniture", "Grills & BBQ", "Patio Heaters",
        "Watering Equipment", "Planters",
        "Outdoor Lighting", "Pest Control",
    ],
    # "Baby & Maternity": [
    #     "Diapers", "Baby Clothing", "Strollers", "Car Seats",
    #     "Baby Monitors", "Feeding Supplies", "Cribs",
    #     "Nursery Furniture", "Maternity Wear", "Baby Toys",
    # ],
    # "Jewelry & Accessories": [
    #     "Necklaces", "Bracelets", "Rings", "Earrings",
    #     "Watches", "Sunglasses", "Handbags", "Wallets",
    #     "Belts", "Scarves",
    # ],
    # "Music & Instruments": [
    #     "Guitars", "Keyboards", "Drums", "Microphones",
    #     "DJ Equipment", "Studio Equipment", "Amplifiers",
    #     "Sheet Music", "Instrument Accessories", "Vinyl Records",
    # ],
    # "Food & Beverages": [
    #     "Snacks", "Coffee", "Tea", "Soft Drinks",
    #     "Energy Drinks", "Organic Foods", "Canned Goods",
    #     "Pasta & Rice", "Sauces & Condiments",
    #     "Baking Ingredients",
    # ],
    # "Travel & Luggage": [
    #     "Suitcases", "Carry-On Bags", "Travel Backpacks",
    #     "Travel Accessories", "Travel Pillows",
    #     "Packing Organizers", "Passport Holders",
    #     "Travel Toiletry Bags", "Duffel Bags", "Luggage Tags",
    # ],
    # "Hardware & Tools": [
    #     "Power Tools", "Hand Tools", "Tool Storage",
    #     "Safety Equipment", "Nails & Fasteners",
    #     "Paint & Supplies", "Electrical Supplies",
    #     "Plumbing Supplies", "Measuring Tools", "Ladders",
    # ],
}

MOCK_DIR = Path(__file__).parent.resolve()


def _create_homepage_if_none() -> Page:
    if not HomePage.objects.exists():
        logger.warning("Homepage does not exist, creating one now")
        fake_homepage()
    
    homepage = HomePage.objects.first()
    return homepage


def _create_product_listing_page_if_none() -> Page:
    if not ProductListingPage.objects.exists():
        logger.warning("Product Listing Page instance does not exist, creating one now")
        fake_product_listing_page()

    product_listing_page = ProductListingPage.objects.first()
    return product_listing_page


def _create_product_category_listing_pages_if_none() -> list:
    if not ProductCategoryListingPage.objects.exists():
        logger.warning("Category Listing Page instance does not exist, creating few now")
        fake_product_category_listing_pages()

    categories = ProductCategoryListingPage.objects.all()
    return categories


def _get_image(width, height, force_fetch_online=False) -> Image:
    # Check whether the image exists in db
    if imgs := Image.objects.filter(width=width, height=height):
        return imgs[0]
    
    # Image doesn't exist yet, try load it from folder 
    width_str = str(width)
    height_str = str(height)
    img_name = "tmp_{}x{}.jpg".format(width, height)
    img_path = MOCK_DIR / img_name
    
    if img_path.exists():
        media_dir = Path(settings.MEDIA_ROOT) / "mock"
        media_dir.mkdir(parents=True, exist_ok=True)
        media_img_path = media_dir / img_name
        
        # Copy to media folder
        if not media_img_path.exists():
            media_img_path.write_bytes(img_path.read_bytes())

        with open(media_img_path, "rb") as f:
            image = Image.objects.create(
                title=f"random img ({width_str}x{height_str})",
                file=File(f, name=f"mock/{img_name}")
            )
        return image
    
    # No image found in local folder, fetch one from the internet if user agrees
    if not force_fetch_online:
        answer = input("No image with such size exists yet, fetch one from the internet (y/n)? ")

        while True:
            match answer.lower():
                case "y":
                    break
                case "n":
                    return None
                case _:
                    answer = input("Please answer with y/n: ")

    logger.info("Fetching image with size {}x{} from the internet".format(width_str, height_str))
    response = requests.get(f"https://picsum.photos/{width_str}/{height_str}").content
    img_path = Path(settings.MEDIA_ROOT) / "original_images" / f"tmp_{width_str}x{height_str}.jpg"

    with open(img_path, "wb") as f:
        f.write(response)

    image, _created = Image.objects.update_or_create(title=f"random img ({width_str}x{height_str})", file=str(img_path))
    return image


def fake_homepage():
    root = Page.get_first_root_node()
    old_homepage = HomePage.objects.first() 

    homepage = HomePage(title="Homepage", slug="", path="/", depth=root.get_depth() + 1)

    logger.info("Adding child to root")
    root.add_child(instance=homepage)

    try:
        site = Site.objects.get(is_default_site=True)
        site.root_page = homepage
        site.save()
        logger.info("HomePage set as site root.")
    except Site.DoesNotExist: # should not happen 
        logger.warning("No default site set for Site, creating one now")
        Site.objects.create(hostname="localhost", port=80, root_page=homepage, is_default_site=True)

    try:
        welcome_page = Page.objects.get(title__startswith="Welcome") # Wagtail's default welcome page
        logger.info("Deleting welcome page")
        welcome_page.delete()
    except Page.DoesNotExist:
        logger.info("Welcome page not found")

    if old_homepage:
        logger.info("Deleting old homepage")
        old_homepage.delete()

    assert HomePage.objects.exists()


def decorate_homepage():
    img = _get_image(width=1000, height=500)
    img_cards = _get_image(width=400, height=400)
    img_carousel = _get_image(width=2000, height=1000, force_fetch_online=True)

    homepage = HomePage.objects.first()

    homepage.content = [
            ("carousel", {
                "slides": [
                    {
                        "image": img_carousel,
                        "title": "Product 0 news",
                        "description": "Description 0, click for more",
                        "page_chooser": ProductDetailPage.objects.first()
                    },
                    {
                        "image": img_carousel,
                        "title": "News 1",
                        "description": "Description 1, click for more",
                        "page_chooser": BlogDetailPage.objects.first()
                    },
                    {
                        "image": img_carousel,
                        "title": "Incoming product 2",
                        "description": "Description 2, click for more",
                        "page_chooser": ProductDetailPage.objects.last()
                    },
                ]
            }),
            ("title_and_text", {
                "title": fkr.sentence(5),
                "text": fkr.paragraph(3)
            }),
            ("carousel_celebrity", {
                "title": "Our happy customers",
                "slides": [
                    {
                        "image": img,
                        "title": "HP",
                        "description": "happy happy"
                    },
                    {
                        "image": img,
                        "title": "Thinkpad",
                        "description": "very much happy"
                    },
                ]
            }),
            ("cards", {
                "title": "Our products",
                "cards": [
                    {
                        "image": img_cards,
                        "title": "Product 0",
                        "text": "Description 0",
                        "button_page": ProductDetailPage.objects.first()
                    },
                    {
                        "image": img_cards,
                        "title": "Product 1",
                        "text": "Description 1",
                        "button_page": ProductDetailPage.objects.last()
                    },
                    {
                        "image": img_cards,
                        "title": "Product 2",
                        "text": "Description 2",
                        "button_page": ProductDetailPage.objects.all()[1]
                    },
                ]
            }),
        ]
    homepage.save()


def fake_flex_page():
    homepage = _create_homepage_if_none()

    FlexPage.objects.all().delete()
    img = _get_image(width=1000, height=500)
    img_cards = _get_image(width=400, height=400)
    img_carousel = _get_image(width=1000, height=1000, force_fetch_online=True)

    about_us_page = FlexPage(
        title="About us", 
        subtitle="This is a FlexPage",
        show_in_menus=True,
        content=[
            ("full_rich_text", fkr.sentence(500)),
            ("title_and_text", {
                "title": fkr.sentence(5),
                "text": fkr.paragraph(3)
            }),
            ("carousel_celebrity", {
                "title": "Our happy customers",
                "slides": [
                    {
                        "image": img,
                        "title": "HP",
                        "description": "happy happy"
                    },
                    {
                        "image": img,
                        "title": "Thinkpad",
                        "description": "very much happy"
                    },
                ]
            }),
            ("cards", {
                "title": "Our products",
                "cards": [
                    {
                        "image": img_cards,
                        "title": "Product 0",
                        "text": "Description 0",
                        "button_page": ProductDetailPage.objects.first()
                    },
                    {
                        "image": img_cards,
                        "title": "Product 1",
                        "text": "Description 1",
                        "button_page": ProductDetailPage.objects.last()
                    },
                    {
                        "image": img_cards,
                        "title": "Product 2",
                        "text": "Description 2",
                        "button_page": ProductDetailPage.objects.all()[1]
                    },
                ]
            }),
            ("horizontal_rule", {}),
            ("title_and_text", {
                "title": fkr.sentence(5),
                "text": fkr.paragraph(3)
            }),
            ("carousel", {
                "slides": [
                    {
                        "image": img_carousel,
                        "title": "Service 0",
                        "description": "Description 0"
                    },
                    {
                        "image": img_carousel,
                        "title": "Service 1",
                        "description": "Description 1"
                    },
                    {
                        "image": img_carousel,
                        "title": "Service 2",
                        "description": "Description 2"
                    },
                ]
            })
        ]
    )
    homepage.add_child(instance=about_us_page)


def fake_contact():
    contact_settings = Contact.objects.get_or_create(site_id=1)[0]

    # Clean up if data was already populated before
    logger.info("Cleanup")
    PhoneNumber.objects.all().delete()
    Email.objects.all().delete()
    Location.objects.all().delete()

    logger.info("Creating phone numbers")
    PhoneNumber.objects.bulk_create([
        PhoneNumber(contact=contact_settings, description=fkr.name(), phone_number=fkr.phone_number()),
        PhoneNumber(contact=contact_settings, description=fkr.name(), phone_number=fkr.phone_number()),
        PhoneNumber(contact=contact_settings, description=fkr.name(), phone_number=fkr.phone_number()),
    ])

    logger.info("Creating emails")
    Email.objects.bulk_create([
        Email(contact=contact_settings, email=fkr.email()),
        Email(contact=contact_settings, email=fkr.email()),
        Email(contact=contact_settings, email=fkr.email()),
    ])

    logger.info("Creating location")
    Location.objects.create(contact=contact_settings, street="The Cuban Way", maps_url="https://www.google.com/maps/place/Cuba/@21.4996043,-82.2037947,7z/data=!3m1!4b1!4m6!3m5!1s0x88cd49070f7a4cb5:0x798cf7529110a41a!8m2!3d21.521757!4d-77.781167!16zL20vMGQwNHo2?entry=tts&g_ep=EgoyMDI2MDIxOC4wIPu8ASoASAFQAw%3D%3D&skid=cc83e45a-adec-4932-89f1-44d28928426f")


def fake_opening_hours():
    opening_hours_settings = OpeningHours.objects.get_or_create(id=1)[0]

    # Clean up if data was already populated before
    logger.info("Cleanup")
    WorkDay.objects.all().delete()

    logger.info("Creating workdays")
    WorkDay.objects.bulk_create([
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.MON, from_hour=datetime.time(hour=7), to_hour=datetime.time(hour=15)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.TUE, from_hour=datetime.time(hour=7), to_hour=datetime.time(hour=15), from_hour2=datetime.time(hour=18), to_hour2=datetime.time(hour=23)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.WED, from_hour=datetime.time(hour=7), to_hour=datetime.time(hour=15)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.THU, from_hour=datetime.time(hour=7), to_hour=datetime.time(hour=15), from_hour2=datetime.time(hour=18), to_hour2=datetime.time(hour=23)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.FRI, from_hour=datetime.time(hour=7), to_hour=datetime.time(hour=15)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.SAT, from_hour=datetime.time(hour=8), to_hour=datetime.time(hour=13)),
        WorkDay(opening_hours=opening_hours_settings, day=WorkDay.Days.SUN, is_closed=True),
    ])


def fake_social_media():
    social_media = SocialMedia.objects.get_or_create(site_id=1)[0]

    logger.info("Settings socials")
    if not social_media.X:
        social_media.X = "https://www.x.com"
    if not social_media.youtube:
        social_media.youtube = "https://www.youtube.com"
    if not social_media.facebook:
        social_media.facebook = "https://www.facebook.com"
    if not social_media.instagram:
        social_media.instagram = "https://www.instagram.com"
    if not social_media.tiktok:
        social_media.tiktok = "https://www.tiktok.com"

    logger.info("Saving social media settings")
    social_media.save()


def fake_product_listing_page():
    homepage = _create_homepage_if_none()
    
    logger.info("Creating product listing page")
    product_listing_page = ProductListingPage(title="Products", show_in_menus=True)

    logger.info("Adding product listing page as a child of homepage")
    homepage.add_child(instance=product_listing_page)


def fake_product_category_listing_pages():
    # Delete old categories
    ProductCategoryListingPage.objects.all().delete()

    _create_homepage_if_none()

    if not ProductListingPage.objects.exists():
        logger.info("Product listing page does not yet exist, creating one")
        fake_product_listing_page()

    product_listing_page = ProductListingPage.objects.first()
    if not product_listing_page:
        raise ValueError("Could not create product listing page, how did this happen?")

    for category_name in PRODUCT_CATEGORIES.keys():
        category = ProductCategoryListingPage(title=category_name, show_in_menus=True)
        product_listing_page.add_child(instance=category)


def fake_product_subcategory_listing_pages():
    # Delete old subcategories
    ProductSubcategoryListingPage.objects.all().delete()

    _create_homepage_if_none()
    _create_product_listing_page_if_none()
    categories = _create_product_category_listing_pages_if_none()

    for category in categories:
        subcategories = PRODUCT_CATEGORIES[category.title]

        for subctg_name in subcategories:
            subctg = ProductSubcategoryListingPage(title=subctg_name)
            category.add_child(instance=subctg)


def fake_product_detail_pages():
    # Create few products directly under category 
    if not ProductCategoryListingPage.objects.exists():
        logger.warning("No categories exist yet, creating them now")
        fake_product_category_listing_pages()

    logger.info("Fetching a random image for thumbnail")
    thumbnail = _get_image(width=400, height=400)

    logger.info("Generating products")
    categories = ProductCategoryListingPage.objects.all()
    PRODUCTS_PER_CATEGORY = 5

    for category in categories:
        product_id = 0

        for _ in range(PRODUCTS_PER_CATEGORY):
            composed_title = "{} Product {}".format(category.title[0:3], product_id)
            product = ProductDetailPage(title=composed_title, thumbnail_image=thumbnail, price=fkr.random.randint(0, 1000))
            category.add_child(instance=product)
            product_id += 1

    subcategories = ProductSubcategoryListingPage.objects.all()
    PRODUCTS_PER_SUBCATEGORY = 20

    for subctg in subcategories:
        product_id = 0

        for _ in range(PRODUCTS_PER_SUBCATEGORY):
            composed_title = "{} Product {}".format(subctg.title[0:3], product_id)
            product = ProductDetailPage(title=composed_title, thumbnail_image=thumbnail, price=fkr.random.randint(0, 1000))
            subctg.add_child(instance=product)
            product_id += 1


def fake_blog_listing_page():
    homepage = _create_homepage_if_none()
    
    logger.info("Creating blog listing page")
    blog_listing_page = BlogListingPage(title="Blog", show_in_menus=True)

    logger.info("Adding blog listing page as a child of homepage")
    homepage.add_child(instance=blog_listing_page)


def fake_blog_category_listing_pages():
    # Delete old categories
    BlogCategoryListingPage.objects.all().delete()

    _create_homepage_if_none()

    if not BlogListingPage.objects.exists():
        logger.info("Blog listing page does not yet exist, creating one")
        fake_blog_listing_page()

    blog_listing_page = BlogListingPage.objects.first()
    if not blog_listing_page:
        raise ValueError("Could not create product listing page, how did this happen?")

    for category_name in BLOG_CATEGORIES:
        category = BlogCategoryListingPage(title=category_name, show_in_menus=True)
        blog_listing_page.add_child(instance=category)


def fake_blog_detail_pages():
    # Create few products directly under category 
    if not BlogCategoryListingPage.objects.exists():
        logger.warning("No categories exist yet, creating them now")
        fake_blog_category_listing_pages()

    logger.info("Fetching a random image for thumbnail")
    thumbnail = _get_image(width=1000, height=500)

    logger.info("Generating blog posts")
    categories = BlogCategoryListingPage.objects.all()
    POSTS_PER_CATEGORY = 30

    for category in categories:
        for idx in range(POSTS_PER_CATEGORY):
            title = "{} Post {}".format(category.title[0:3], idx)
            post = BlogDetailPage(title=title, thumbnail_image=thumbnail, content=[("full_rich_text", fkr.sentence(1000))])
            category.add_child(instance=post)


def cleanup():
    logger.info("Deleting images")
    Image.objects.all().delete()


def fake_all():
    cleanup()

    # Home
    fake_homepage()

    # Products
    fake_product_listing_page()
    fake_product_category_listing_pages()
    fake_product_subcategory_listing_pages()
    fake_product_detail_pages()

    # Blog
    fake_blog_listing_page()
    fake_blog_category_listing_pages()
    fake_blog_detail_pages()

    # Now that blog posts and products are available, we can decorate homepage
    decorate_homepage()

    # Site settings
    fake_contact()
    fake_opening_hours()
    fake_social_media()

    # Flex page
    fake_flex_page()

