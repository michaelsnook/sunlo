Guidelines for Contributors
---------------------------

Welcome. If you're contributing to this application, thank you! Here are some
things to know before jumping in.

1. The first thing you can do is join the Slack team at
[slack.sunlo.co](http://slack.sunlo.co).
1. This Django application should be treated as a prototype. My plan right now
is to use Django to get as far as I can developing the user journeys and
workflows that make the app work, engage a small base of users, and get lots of
good feedback from different types of people, and then reimplement using
something like React that can easily be turned into a native Android or iOS app.
1. This Django application is about as "vanilla" as they come right now.
For example, it's not using Django's built-in forms or user registration pages.
If you'd like to help make the application a bit more "Django-y", that might be
a great way to help. Please raise it on the #dev channel in Slack, or open an
"issue" to discuss.

### Whenever you send a pull request:



### Front-end code:

1. When a page has only one action, the button gets a `btn-lg` class.
1. Use Bootstrap-4 utilities for margin and padding whenever possible. We're
keeping the `main.scss` styles as slim as possible at this time.
1. Form submit buttons get `btn-primary`, while links get `btn-outline-primary`.
