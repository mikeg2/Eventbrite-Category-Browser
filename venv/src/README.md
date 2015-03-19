## Eventbrite Category Browser
Allows users to browse Eventbrite events by category. All data is fetched from Eventbrite's API. No data is stored by the program itself, except in the in-memory cache.

## Cacheing
Requests to Eventbrites category API are cached in-memory, since the categories are unlikely to change and the data is used on every page.

## Technology Used
- Django
- Bootstrap
- Requests
- ConfigObj
- CacheControl