from django.shortcuts import render
from django.http import HttpRespons
from eventbrite_api import fetch_all_categories, fetch_categories
import ConfigParser

BROWSER_VIEW_CONFIG_URL = './event_browser.cfg'
config = ConfigParser.ConfigParser().readfp(open(BROWSER_VIEW_CONFIG_URL))['views']
# Create your views here.

# Notes:
# Views shouldn't care where API is coming from, unless templates are views in MVC

def index(request):
    context = {}
    browse_categories = request.GET['browse_categories']
    if(browse_categories):
        context.page_number = request.GET.get(0, 'ev_page') or 0
        context.events = fetch_all_categories(browse_categories, context.page, context.page_length)
    categories = fetch_categories()
    context.categories = categories
    return render(request, 'browse_categories', context)