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
1. Button and modal for "Pronunciation help"
1. Share this card on various 1-to-1 messengers
1. Button, form, and view to "Link this card to a related phrase"
1. Button, form, and view to "Add a new phrase related to this card"
1. Menu item and screen to "Search cards" / "Search deck"
1. "Levels" interface where you peruse a set of cards with the same
difficulty rating

## Chores
1. Add Users with public signup and forgot password link
  * ~~user login / logout~~
  * ~~create user~~
  * ~~reset password~~
  * forgot password

## Yak-shaving
1. Track session info like which deck we're currently working on
1. Compile bootstrap locally with mixins/vars
