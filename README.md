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
