## Eventbrite Category Browser
Allows users to browse Eventbrite events by category. All data is fetched from Eventbrite's API. No data is stored by the program itself, except in the in-memory cache.

## Caching
Requests to Eventbrite's category API are cached in-memory using CacheControl, since the categories are unlikely to change and the data is used on every page.

Since categories change so rarely, it would make sense to store the categories in a local database and sync the database with the eventbrite catagory API periodically using a Cron job. However, I wanted to limit the project to pure Django and Cron jobs have to be configered externally.

I chose not to cache event search results because the number of possible requests (category combinations * pagination * possible-time-ranges = ~8,000 * ~100 * infinity) is too large and the results change often.

## Compatibility
Some CSS3 rules were used for styling, but the pages should still work with most browsers.

## Debug vs. Production
Static files are served using dj-static. Django sends the static files to the `staticfile` directory. All CSS files are minified by Django Compressor.

## Technology Used
- Django (+ extensions)
- Requests
- ConfigObj
- CacheControl