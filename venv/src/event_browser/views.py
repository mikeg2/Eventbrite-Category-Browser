from django.shortcuts import render
from django.http import HttpResponse
from eventbrite_api import fetch_events_by_category, fetch_all_categories, FailedApiRequest
from eventbrite_app_1.settings import BASE_DIR
from django.contrib.messages import constants as messages
from django.contrib import messages

# TODO: Consider putting in config
API_ERROR_MSG = "Eventbrite Returned an Error"

def category(request):
    browse_categories = request.GET.getlist('cat')
    context = {
        'request': request,  # Used for pagination
        'sel_cat': browse_categories
    }
    if browse_categories:
        page_number = request.GET.get('page', 1)
        initial_request_time = request.GET.get('req_time') or current_utc_string()
        context['req_time'] = initial_request_time
        try:
            fetched_events_data = fetch_events_by_category(
                browse_categories, page_number, initial_request_time)
            context['events'] = fetched_events_data['events']
            context['pagination'] = fetched_events_data['pagination']
        except FailedApiRequest:
            messages.add_message(request, messages.ERROR, API_ERROR_MSG)
    try:
        categories = fetch_all_categories(True)
        context['categories'] = categories
    except FailedApiRequest:
        messages.add_message(request, messages.ERROR, API_ERROR_MSG)
    return render(request, 'browse_categories.html', context)

def current_utc_string():
    import datetime
    utc_datetime = datetime.datetime.utcnow()
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")