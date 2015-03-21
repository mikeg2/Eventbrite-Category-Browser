## Eventbrite Category Browser
Allows users to browse Eventbrite events by category. All data is fetched from Eventbrite's API. No data is stored by the program itself, except in the in-memory cache.

## Caching
Requests to Eventbrite's category API are cached in-memory using CacheControl, since the categories are unlikely to change and the data is used on every page.

I chose not to cache event searches because the number of possible requests (category combinations * pagination -> 20^3 * ?) is too large and the results change often (I assume). For the same reason, I chose not to use Django's caching system (django.core.cache) to cache the rendered pages themselves.

Since categories change so rarely, it would make sense to store the categories in a local database and sync the database with the eventbrite API periodically (say, once a day) using a Cron job. However, I wanted to limit the project to pure Django and Cron jobs have to be configered externally.

## Compatibility

## Debug vs. Production
WhiteNoise is used to serve static files on Heroku. Django sends the static files to the `staticfile` directory. All CSS files are compressed.

https://devcenter.heroku.com/articles/django-assets

[double check compress on upload]

## Technology Used
- Django
- Bootstrap
- Requests
- ConfigObj
- CacheControl