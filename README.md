# WagtailRocket 🚀 

A boilerplate for CMS websites developed in Wagtail to save you tens of hours of work.
See [all features](https://wagtailrocket.carrd.co/)

## 📸 Demo 
You can see a real-life example for a [motorcycle shop](https://mototim.si/) which was an inspiration for developing the boilerplate. It was derived from the project and improved in many aspects.
There is [another example here](https://wagtailrocket.com/)

## ❓ Why this came to life
Back when the [motorcycle shop](https://mototim.si/) was still running on Wordpress, it was painful to change simple settings on the website, such as opening hours. Not to mention how slow everything was because of the plugins. 

This is why I decided to develop the website using Wagtail and since I spent a lot of time developing basic components like breadcrumbs, pagination etc. I decided to make it into a boilerplate to save us hours of redundant work.


## 📦 Installation

### Development TODO
On your PC, clone the repo, create virtual environment and install dependencies:
```bash
git clone https://github.com/AlexBrence/WagtailRocket.git # or git@github.com:AlexBrence/WagtailRocket.git 
cd WagtailRocket
python -m venv venv
source venv/bin/activate
cd src/
pip install -r requirements.txt

# Open .env_tempate and change the SECRET_KEY, SQL_PASSWORD and whatever else you desire. 
# Then rename it from .env_template to .env

# Now apply migrations, create superuser, run the server and you're good to go
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Production 
On your hosting server, run these commands:
```bash
git clone https://github.com/AlexBrence/WagtailRocket.git # or git@github.com:AlexBrence/WagtailRocket.git if you have ssh configured
cd WagtailRocket
python -m venv venv
source venv/bin/activate
cd src/

# IMPORTANT: Copy your .env file into the src/ folder before proceeding
scp <path_to_local_env> <server_username>@<server_IP>:<path_to_WagtailRocket_src>
# example: scp .env www-data@91.98.75.145:~/web/WagtailRocket/src/.

# IMPORTANT: Find all CHANGE_ME comments in the src/ folder and change it before proceeding.
# You'll either have to fill in your domain name or your email, suffixes were left in to help you determine which one it is

# After the following command, nginx will open up port 80 since there is no certificate yet
docker compose up -d

chmod +x get_certificate.sh
./get_certificate.sh

# Now that we have a certificate, reload nginx container and the https config file will be used
docker compose restart nginx
```

## 🛠 Tips and Tricks
### Reload the server after code update

#### Option 1
Only Django code or templates have changed.

This will send a `Hangup` signal  to the master process. Existing requests will be handled by the workers and all of the new workers will already run the updated code.
```sh
docker compose exec web pkill -HUP -f gunicorn
```

#### Option 2
Static file was added/changed.
```sh
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web pkill -HUP -f gunicorn
```

#### Option 3
Migrations need to run.
```sh
docker compose restart web
```


## ✨ Features
- End-user will be able to control most of the stuff from the admin panel, such as:
    I. Currency shown
    II. Navbar menu ordering
    III. Homepage and other non-listing pages looks to some extent
    IV. Opening hours, contact, socials
    V. Adding custom pages, like About us
    VI. Much more as provided from Wagtail, please refer to their [documentation](https://guide.wagtail.org/en/)
- Product listing page that works out-of-the-box with pagination, fuzzy searching, sorting, categories and subcategories implemented
- Multiple images possible on product detail page
- Shows 3 random items on every product detail page to keep the user engaged
- Blog listing page that works out-of-the-box with pagination, categories implemented
- Uses HTMX for quicker refreshing 
- Build your own homepage by putting components together (carousel, cards, ...) from admin panel
- Promote your products with Carousel or Cards blocks with link to the actual product or to external website
- Product description with RichText block and possibility to attach documents as well
- Easy-to-access website settings, like opening hours, contacts, etc. from the admin panel
- Easily extendible with base listing page & detail page classes implemented 
- Deploy in minutes with docker

## 🧰 Tech stack 
- Python 
- Wagtail
- PostgreSQL
- SQLite (for development only)
- Nginx
- Docker
- Gunicorn
- Bootstrap
- HTMX