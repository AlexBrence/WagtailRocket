from django import template
from urllib.parse import parse_qs
from home.models import HomePage

register = template.Library()


@register.simple_tag(takes_context=False)
def build_url_filter(current_url: str, key: str, value: str):
    try:
        q = current_url.split("?")[1]
        q_dict = parse_qs(q)
        q_dict[key] = value
            
        # When ordering is changed go to the first page automatically
        if key == "order" and "page_num" in q_dict:
            del q_dict["page_num"]

        url = "?" + "&".join([f"{key}={value if not isinstance(value, list) else value[0]}" for key, value in q_dict.items()])
        return url

    except IndexError:
        return f"?{key}={value}"


@register.inclusion_tag('tags/nav_dropdown.html')
def create_nav_items():
    """ Fills dictionary with main menu items (children of HomePage) as key and a list of their children as a value """
    home_page = HomePage.objects.first()

    if home_page is None:
        return {} 

    nav_items = home_page.get_children().live().in_menu()
    items_dict = {}

    for nav_item in nav_items:
        nav_subitems = nav_item.get_children().live().in_menu()
        items_dict[nav_item] = [nav_subitem for nav_subitem in nav_subitems]
    
    return {
        "navbar": items_dict
    }
