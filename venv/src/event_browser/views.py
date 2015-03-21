from django.shortcuts import render
from django.http import HttpResponse
from eventbrite_api import fetch_events_by_category, fetch_all_categories, FailedApiRequest
from eventbrite_app_1.settings import BASE_DIR
from django.contrib.messages import constants as messages
from django.contrib import messages
from configobj import ConfigObj
import os

BROWSER_VIEW_CONFIG_URL = os.path.join(BASE_DIR, 'event_browser/event_browser.cfg')
config = ConfigObj(BROWSER_VIEW_CONFIG_URL)['views']

def category(request):
    context = {
        'request': request,  # Used for pagination
    }
    context_for_category_list(request, context)
    context_for_eventlist_search(request, context)
    return render(request, 'browse_categories.html', context)

def context_for_category_list(request, context=None):
    if context is None:
        context = {}
    try:
        categories = fetch_all_categories(True)
        context['categories'] = categories
    except FailedApiRequest:
        messages.add_message(request, messages.ERROR, config['eventbrite_api_error_message'])
    return context

def context_for_eventlist_search(request, context=None):
    if context is None:
        context = {}
    browse_categories = context['sel_cat'] = request.GET.getlist('cat')
    if browse_categories:
        context_for_eventlist_results(request, browse_categories, context)
    return context

def context_for_eventlist_results(request, categories, context=None):
    if context is None:
        context = {}
    page_number = request.GET.get('page', 1)
    initial_request_time = request.GET.get('req_time') or current_utc_string() # Used to ensure pagination results are stable
    context['req_time'] = initial_request_time
    try:
        fetched_events_data = fetch_events_by_category(
            categories, page_number, initial_request_time)
        context['events'] = fetched_events_data['events']
        context['pagination'] = fetched_events_data['pagination']
    except FailedApiRequest:
        messages.add_message(request, messages.ERROR, config['eventbrite_api_error_message'])
    return context

def current_utc_string():
    import datetime
    utc_datetime = datetime.datetime.utcnow()
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")