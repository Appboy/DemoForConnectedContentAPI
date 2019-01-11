# ConnectedContentExample

To get started, you'll need Postgres installed.

1. `pip install -r requirements.txt`
2. `./manage.py migrate`
3. `./manage.py runserver`

To get started with Heroku,

1. `heroku create`
2. `git push heroku develop:master`

Our first test:

- 5 minutes of about 3600 requests per minute == 18k requests
- We never set up a page, so everything was a 400 error
- Average response time of about 600ms, max of about 4s

What next?

Let's make a database model, generate some fake data, then make a
page that renders something from the database.

1. `./manage migrate`
2. `./mangage.py seed_data`
3. `./manage.py runserver`
4. Visit `http://127.0.0.1:8000/` and confirm you get a 140 character string

Now let's deploy this to Heroku:

1. `git push heroku develop:master`
2. Run `python manage.py seed_data` from a Heroku console
2. Visit your application, confirm it works

Our second test:

- 5 minutes of about 2000 requests per minute == 10k requests
- We set up a page now, so we should be getting all 200s
- Average response time of about 47ms, max around 150ms

Great! We're probably hitting the table cache every time in the database,
so we have some options for pushing our system:

- We could add more concurrent requests
- We could add way more seed data so that everything isn't cached in the database

Let's add more requests.

Our third test:

- 5 minutes of about 9k requests per minute = 45k requests
- Average response of 14 seconds

We have a couple ways we could scale out now:

- We could add additional dynos
- We could change our server application

We're going to do the second thing:

Gunicorn, with naive settings, is going to use a pool of workers and doesn't handle
concurrent requests very well. Let's install gevent and tell our server process to
use greenlets instead of synchronous workers.

Now let's deploy this change to Heroku:

1. `git push heroku develop:master`
2. Visit your application, confirm it works

Wow! What happened? Our fourth test:

- 5 minutes of about 1.8k requests per minute = 9k requests
- Error rate of almost 90%. Something is wrong

A caveat of using asynchronous workers on gunicorn is that each one is going to open
its own connection to the database. Checking our logs, we can see that we're throwing
exceptions because there are too many connections. Looking at the Postgres metrics
page, we can see that we opened FAR more connections than the first time. Let's try
something else.

Waitress is a pure-Python wsgi server that will buffer requests to a fixed pool of
workers, but still handle connections in an asynchronous way. Let's install that,
and change our Procfile accordingly.

Now let's deploy this change to Heroku:

1. `git push heroku develop:master`
2. Visit your application, confirm it works

Note: you may need to restart your dynos before deploying to free up database connections.
