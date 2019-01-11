# ConnectedContentExample

To get started, you'll need Postgres installed.

1. `pip install -r requirements.txt`
2. `./manage.py migrate`
3. `./manage.py runserver`

To get started with Heroku,

1. `heroku create`
2. `git push heroku develop:master`

Our first test:

- 500 users
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

- 500 users
- 5 minutes of about 2000 requests per minute == 10k requests
- We set up a page now, so we should be getting all 200s
- Average response time of about 47ms, max around 150ms

Great! We're probably hitting the table cache every time in the database,
so we have some options for pushing our system:

- We could add more concurrent requests
- We could add way more seed data so that everything isn't cached in the database

Let's add more requests.

Our third test:

- 5000 users
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

- 5000 users
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

Our fifth test:

- 5k concurrent users
- 5 minutes of about 20k requests per minute = 100k requests
- 0% error rate, 178ms average response time

AWESOME! Let's add more concurrent requests - we weren't taxing this at all!

Our sixth test:

- 10k concurrent users
- 5 minutes of about 21.5k requests per minute = 108k requests
- We probably hit peak concurrency in this range: errors went up and response time
  spiked to about 9 seconds on average

Let's try scaling up by adding an additional dyno.

Our seventh test:

- 10k concurrent users
- 5 minutes of 36k requests per minute = 180k requests
- Back down to 215ms response time

Great! Let's try increasing the load just a little bit more.

Our eighth test:

- 15k concurrent users
- 5 minutes of about 30k requests per minute = 150k requests
- Response time went up to 11s

Somewhere in there we've hit peak concurrency. This next time though, we'll
try a new strategy - let's not hit the database, but let's hit Redis instead.
