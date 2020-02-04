# URL Shortener

This program is a JSON API with similar functionality to bit.ly, built in Django


## How do I run this application?

To run this application, you'll need to have set up locally:

- Python3
- Pip
- Django

To run the dev server: `python manage.py runserver`
To run the migrations: `python manage.py migrate`
To run tests, you need to run `python manage.py test api`

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

### Technologies

Given the time constraint, I thought it would be wise to use a framework that I was quite comfortable with. So I decided to go with Django. With more time, I would have considered using a lighter web framework since we didn't end up needing most of Django's functionality.

I also decided to lean towards finishing more of the application functionality vs. trying to make the application truly ready to deploy. A few changes that would need to be made include using a database like Postgres instead of SQLite and turning the django easy debugging off.

### Models

I decided to create two models to hold the necessary data: one to hold the connections between URLs and the shortcode slugs we use to redirect to them and another to hold onto when a user visits a site.


### Short code generation

Short code generation lives in the model that holds the short codes, ShortenedUrl. I thought this would follow OOP principles best. To generate the short codes, I decided that random generation would fit this use case fairly well. There's a low likelihood of collisions up to a certain scale. An approach I decided against was using UUID generation. While this would make the likelihood of collisions much lower, UUIDs are quite long and kind of ruins the point of a "short" code.