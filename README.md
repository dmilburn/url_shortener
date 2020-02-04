# URL Shortener

This program is a JSON API with similar functionality to bit.ly, built in Django


## How do I run this application?

To run this application, you'll need to have set up locally:

- Python
- Pip
- Django


To actually run the application, you need to run the dev server. From the top level of the application run: `python manage.py runserver`

## What functionality does it have?


- Create a new ShortenedUrl
	- Parameters:
		- `url`: the `url` you would like the short link to redirect to
		- `slug` (optional): if you have a custom slug you would like to use, you can pass it here as well
	- To test:
		- This functionality uses a POST request, so to test locally you can use cURL
	- Example:
		- `curl -X POST -d "url=google.com" http://127.0.0.1:8000/api/urls` => `{"result": {"success": true, "slug": "pxp74nchv1"}}`
		- `curl -X POST -d "url=google.com&slug=banana" http://127.0.0.1:8000/api/urls` => `{"result": {"success": true, "slug": "banana"}}`
- Get redirected using an ShortenedUrl
	- After you've created a ShortenedUrl, you can test it by trying it out in the browser
	- Example:
		- https://localhost/banana => https://google.com
- See stats on a ShortenedUrl
	- After you've created a ShortenedUrl, you can see stats in the browser on its number of visits
	- Example:
		- https://localhost/api/urls/banana => 
			- `{"result": {
					"created_on": "2020-2-3 00:00:00",
					"total_visits": 1,
					"visit_count_by_day": {"2020-2-3 00:00:00": 1},
				}}`



## What kinds of decisions did you make writing this?

