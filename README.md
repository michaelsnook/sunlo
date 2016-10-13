# Sunlo
Language learning with friends.
A user-generated, individually-curated phrase book to learn a language starting
from the most useful phrases, for you and your social circle. Named for the
first useful phrase I learned in Hindi "Sunlo iski baht", which I used to say,
"I don't understand your question, but my friend will answer you."

## Run Locally
1. Clone this repository
1. Set up a postgres database called `sunlo` or use sqlite
1. Set up a virtual environment and `pip install -r 'requirements.txt.'`
1. Set up the database and static files with
```bash
./manage.py migrate \
  && ./manage.py createsuperuser \
  && ./manage.py collectstatic \
  && ./manage.py loaddata cards/seed.json
```
1. Run your dev server with `./manage.py runserver`

## Run on Heroku
1. Run locally, install heroku toolbelt
1. Create your heroku app, provision your db, and `git push heroku`
1. Run the same setup steps on your heroku machine as you did on local:
```bash
heroku run ./manage.py migrate \
  && ./manage.py createsuperuser \
  && ./manage.py collectstatic \
  && ./manage.py loaddata cards/seed.json
```
1. For local development, copy or rename `.env.example` to `.env` for the option
to run with `foreman start` or `heroku local`

## Roadmap
1. [1/4] Add Users with public signup and forgot password link
  * [done] user login / logout
  * [todo] create user
  * [todo] reset password
  * [todo] forgot password
1. [done] Support SCSS for styles
1. Build view to add a new card
1. Build view to add new translation
1. Middleware to remember user settings on each page and associate that with
a specific Deck in the database
1. Create a new Deck, only one per language per user, and add cards to it
1. Build "Levels" interface where you peruse a set of cards with the same
difficulty rating
1. Build Levels overview page where you see how much of each level's cards
you've taken into your deck, learned, or skipped
