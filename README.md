django-kevin
============

![Django 1.7.3](http://img.shields.io/badge/Django-1.7.3-brightgreen.svg)
![Stablility Status](http://img.shields.io/badge/Stability-Stable-brightgreen.svg)
[![Requirements Status](https://requires.io/github/imkevinxu/django-kevin/requirements.svg?branch=master)](https://requires.io/github/imkevinxu/django-kevin/requirements/?branch=master)
[![Dependencies Status](https://david-dm.org/imkevinxu/django-kevin.svg)](https://david-dm.org/imkevinxu/django-kevin)
[![MIT License](https://img.shields.io/cocoapods/l/AFNetworking.svg)](http://opensource.org/licenses/MIT)

A heavily personalized project template for Django 1.7.3 using Postgres for development and production. Ready to deploy on Heroku with a bunch of other goodies.

Forked from the original [django-two-scoops-project](https://github.com/twoscoops/django-twoscoops-project)

Creating Your Project
=====================

*Prerequisites: django*

To create a new Django project, run the following command replacing PROJECT_NAME with your actual project name:

    django-admin.py startproject --template=https://github.com/imkevinxu/django-kevin/archive/master.zip --extension=py,md,html,json,coveragerc PROJECT_NAME

Afterwards please reference the actual `README.md` you just created in your new project folder, all the references to yesterday will be changed accordingly.

Make virtual environments
-------------------------

*Prerequisites: virtualenv, virtualenvwrapper*

    cd yesterday
    mkvirtualenv yesterday-dev && add2virtualenv `pwd`
    mkvirtualenv yesterday-prod && add2virtualenv `pwd`
    mkvirtualenv yesterday-test && add2virtualenv `pwd`

Install python packages
-----------------------

For development:

    workon yesterday-dev
    pip install --upgrade pip
    pip install --upgrade setuptools
    sudo env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
    pip install -r requirements/dev.txt

For production:

    workon yesterday-prod
    pip install --upgrade pip
    pip install --upgrade setuptools
    sudo env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
    pip install -r requirements.txt

For testing:

    workon yesterday-test
    pip install --upgrade pip
    pip install --upgrade setuptools
    sudo env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
    pip install -r requirements/test.txt

Install node packages
---------------------

*Prerequisites: node*

    sudo npm install

One-time system installs
------------------------

*Prerequisites: homebrew*

In order to use the grunt task runner you need to install it globally:

    sudo npm install -g grunt-cli

In order to be able to lint SCSS files locally you need `ruby` on your local system and a certain gem. See [https://github.com/ahmednuaman/grunt-scss-lint#scss-lint-task](https://github.com/ahmednuaman/grunt-scss-lint#scss-lint-task)

    gem install scss-lint

In order to use django-pipeline for post-processing, you need `yuglify` installed on your local system:

    sudo npm install -g yuglify

In order for grunt to notify you of warnings and when the build is finished, you need a [notification system](https://github.com/dylang/grunt-notify#notification-systems) installed. Below is the Mac OSX notification command-line tool:

    brew install terminal-notifier

In order to use Redis for caching and queuing, you need to download it and have it running in the background. This will also set `redis-server` to automatically run at launch:

    brew install redis
    ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
    launchctl start ~/Library/LaunchAgents/homebrew.mxcl.redis.plist

Development Mode
================

Set .env.dev variable for dev
-----------------------------

The environment variables for development sets the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Necessary for Foreman and other worker processes

*`.env.dev` is not version controlled so the first person to create this project needs to create a `.env.dev` file for Foreman to read into the environment. Future collaboraters need to email the creator for it.*

    echo DJANGO_SETTINGS_MODULE=config.settings.dev >> .env.dev
    echo PYTHONPATH=yesterday >> .env.dev
    echo PYTHONUNBUFFERED=True >> .env.dev
    echo PYTHONWARNINGS=ignore:RemovedInDjango18Warning >> .env.dev
    echo CACHE=dummy >> .env.dev

Recommended to use foreman to use development environment variables and processes:

    echo "env: .env.dev" > .foreman
    echo "procfile: Procfile.dev" >> .foreman

Create local postgres database for dev
--------------------------------------

*Prerequisites: Postgres and Heroku Toolbelt*

Install Postgres for your OS [here](http://www.postgresql.org/download/). For Max OSX the easiest option is to download and run [Postgres.app](http://postgresapp.com/).

    # Make sure Postgres.app is running
    workon yesterday-dev
    createdb yesterday-dev
    foreman run django-admin.py migrate

Run project locally in dev environment
--------------------------------------

Use the right virtual environment:

    workon yesterday-dev

Start the server with:

    foreman start

Create a local super user with:

    foreman run django-admin.py createsuperuser

To run one-off commands use:

    foreman run django-admin.py COMMAND

To enable Live Reload, download and turn on a [browser extension](http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-).

Production Mode
===============

Set .env variable for prod
--------------------------

The environment variables for production must contain a separate `SECRET_KEY` for security and the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Hacky use of `date | md5` to generate a pseudo-random string.

*`.env` is not version controlled so the first person to create this project needs to create a `.env` file for Foreman and Heroku to read into the environment. Future collaboraters need to email the creator for it.*

    echo SECRET_KEY=`date | md5` >> .env
    echo DJANGO_SETTINGS_MODULE=config.settings.prod >> .env
    echo PYTHONPATH=yesterday >> .env
    echo WEB_CONCURRENCY=3 >> .env
    echo PYTHONUNBUFFERED=True >> .env
    echo PYTHONWARNINGS=ignore:RemovedInDjango18Warning >> .env
    echo BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-multi.git >> .env

Deploy to Heroku
----------------

*Prerequisites: Heroku Toolbelt and heroku-config*

First step is to deploy to Heroku with the `post_compile` script in `/bin` so that node functions can be installed for python to call them.

    git init
    git add .
    git commit -m "Ready for initial Heroku deploy"
    heroku create
    heroku config:push
    git push heroku master

After `post_compile` is successful, uncomment the line with the variable `STATICFILES_STORAGE` in `/yesterday/config/settings/base.py` to enable django-pipeline and push again.

    git commit -am "Enabled django-pipeline"
    git push heroku master
    heroku run django-admin.py migrate
    heroku open

To run one-off commands like `createsuperuser` use:

    heroku run django-admin.py COMMAND

Run project locally in prod environment
---------------------------------------

Set the `.foreman` file to use production environment variables and processes:

    echo "env: .env" > .foreman
    echo "procfile: Procfile" >> .foreman

Use the right virtual environment:

    workon yesterday-prod

This is meant to mimic production as close as possible using both the production database and environment settings so proceed with caution.

**WARNING**: If this project has SSL turned on, [localhost:5000](http://localhost:5000) won't work anymore because it will always try to redirect to [https://localhost:5000](https://localhost:5000). To fix this comment out the SECURITY CONFIGURATION section in `/yesterday/config/settings/prod.py`

    heroku config:pull
    foreman run django-admin.py collectstatic --noinput
    foreman start

The site will be located at [localhost:5000](http://localhost:5000)

Testing Mode
============

Set .env.test variable for test
------------------------------

The environment variables for testing sets the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Necessary for Foreman and other worker processes

*`.env.test` is not version controlled so the first person to create this project needs to create a `.env.test` file for Foreman to read into the environment. Future collaboraters need to email the creator for it.*

    echo DJANGO_SETTINGS_MODULE=config.settings.test >> .env.test
    echo PYTHONPATH=yesterday >> .env.test
    echo PYTHONUNBUFFERED=True >> .env.test
    echo PYTHONWARNINGS=ignore:RemovedInDjango18Warning >> .env.test

Run tests locally in test environment
-------------------------------------

Set the `.foreman` file to use testing environment variables and processes:

    echo "env: .env.test" > .foreman
    echo "procfile: Procfile.test" >> .foreman

Use the right virtual environment:

    workon yesterday-test

And have static assets prepared (for coverage tests):
    
    foreman run django-admin.py collectstatic --noinput

Automatically run all tests and linters and watch files to continuously run tests:

    foreman start

You can view the results of the tests in HTML at [localhost:9000/tests](http://localhost:9000/tests)

You can specifically view the results of Django coverage tests at [localhost:9000/tests/django](http://localhost:9000/tests/django)

Jasmine JS Unit Tests
---------------------

Grunt automatically compiles Jasmine tests written in CoffeeScript at `/yesterday/static/js/tests/coffee` and runs the tests upon every save.

You can specifically view the results of Jasmine JS unit tests at [localhost:9000/tests/jasmine](http://localhost:9000/tests/jasmine)

You can specifically view the results of JS coverage tests at [localhost:9000/tests/jasmine/coverage.html](http://localhost:9000/tests/jasmine/coverage.html)

Add-ons & Services
==================

SSL
---
Enable SSL via Heroku, Cloudflare, or your DNS provider and then uncomment the SECURITY CONFIGURATION section in `/yesterday/config/settings/prod.py` to enable django-secure and other security best practices for production.

Invoke
------
Scripts can be programmed to be run on the command-line using [Invoke](https://github.com/pyinvoke/invoke) for repeated tasks like deployment, building, or cleaning. Write your tasks in `tasks.py`.

Redis Cloud Caching
-------------------
In order to enable redis for caching and queues, add [Redis Cloud](https://devcenter.heroku.com/articles/rediscloud) to Heroku.

    heroku addons:add rediscloud:25

Redis Queue Worker
------------------
Add a [Redis Queue](https://github.com/ui/django-rq) worker process to Procfile:

    echo "worker: django-admin.py rqworker high default low" >> Procfile

Push the changed Procfile to Heroku:

    git add Procfile
    git commit -m "Added worker process to Procfile, pushing to Heroku"
    git push heroku master

Turn on background job worker with this one-liner:

    heroku scale worker=1

Redis Queue Scheduler
---------------------
Add a [RQ Scheduler](https://github.com/ui/rq-scheduler) process to Procfile:

    echo "scheduler: rqscheduler --url \$REDISCLOUD_URL" >> Procfile

Push the changed Procfile to Heroku:

    git add Procfile
    git commit -m "Added scheduler process to Procfile, pushing to Heroku"
    git push heroku master

Turn on background job scheduler with this one-liner:

    heroku scale scheduler=1

Amazon S3
---------
To use Amazon S3 as a static and media file storage, create a custom Group and User via IAM and then a custom static bucket and media bucket with public read policies.

Add the following config variables to Heroku:

    heroku config:set AWS_ACCESS_KEY_ID=INSERT_ACCESS_KEY_ID
    heroku config:set AWS_SECRET_ACCESS_KEY=INSERT_SECRET_ACCESS_KEY
    heroku config:set AWS_STATIC_STORAGE_BUCKET_NAME=yesterday-static
    heroku config:set AWS_MEDIA_STORAGE_BUCKET_NAME=yesterday-media

PG Backups
----------
[PG Backups](https://devcenter.heroku.com/articles/pgbackups) is a Heroku add-on for automatic Postgres database backups. Enable with the following one-liner:

    heroku addons:add pgbackups:auto-month

Monitoring
----------
- [Librato](https://devcenter.heroku.com/articles/librato) for Heroku performance monitoring
- [New Relic](https://devcenter.heroku.com/articles/newrelic) for server performance monitoring (protip: set [availability monitoring](https://coderwall.com/p/u0x3nw) on to avoid Heroku idling)
- [RedisMonitor](https://devcenter.heroku.com/articles/redismonitor) for Redis server monitoring
- [Logentries](https://devcenter.heroku.com/articles/logentries) provides logging backups as well as search and notifications. Can also additionally backup to S3
- [Sentry](https://devcenter.heroku.com/articles/sentry) for error tracking with [Raven](http://raven.readthedocs.org/en/latest/index.html) as the client. Make sure to use a [synchronous blocking transport](http://python-rq.org/patterns/sentry/).
- [Ranger](https://devcenter.heroku.com/articles/ranger) to alert you when your app is down

Testing
-------
- [Rainforest RQ](https://devcenter.heroku.com/articles/rainforest) for simple integration testing
- [Tinfoil Security](https://devcenter.heroku.com/articles/tinfoilsecurity) for regularly scanning your app for security vulnerabilities
- [Loader.io](https://devcenter.heroku.com/articles/loaderio) for load testing

Continuous Integration
----------------------
Includes a fancy badge for GitHub README

- [Travis CI](https://travis-ci.org/) for continuous integration testing
- [Coveralls.io](https://coveralls.io/) for coverage testing
- [Requires.io](https://requires.io/) for dependency management

Utilities
---------
- [Filepicker](https://devcenter.heroku.com/articles/filepicker) for file uploading and content management
- [Twilio](http://www.twilio.com/) for sending SMS, MMS, and Voice. Recommended to use [`django-twilio`](http://django-twilio.readthedocs.org/en/latest/)
- [Mailgun](https://devcenter.heroku.com/articles/mailgun) or [Sendgrid](https://devcenter.heroku.com/articles/sendgrid) for email sending. Here are some useful [email templates](http://blog.mailgun.com/transactional-html-email-templates/)
- [MailChimp](http://mailchimp.com/) for email newsletters or create your own [custom newsletter emails](http://zurb.com/playground/responsive-email-templates)

Libraries
=========

Python 2.7.9
============

Currently using [Django 1.7.3](https://docs.djangoproject.com/en/1.7/) for the app framework

base.txt
--------
- [bpython 0.13.2](http://docs.bpython-interpreter.org/) - Advanced python interpreter/REPL
- [defusedxml 0.4.1](https://bitbucket.org/tiran/defusedxml) - Secure XML parser protected against XML bombs
- [dj-static 0.0.6](https://github.com/kennethreitz/dj-static) - Serve production static files with Django
- [django-authtools 1.0.0](http://django-authtools.readthedocs.org/en/latest/) - Custom User model classes such as `AbstractEmailUser` and `AbstractNamedUser`
- [django-braces 1.4.0](http://django-braces.readthedocs.org/en/v1.4.0/) - Lots of custom mixins
- [django-extensions 1.4.9](http://django-extensions.readthedocs.org/en/latest/) - Useful command line extensions (`shell_plus`, `create_command`, `export_emails`)
- [django-floppyforms 1.3.0](http://django-floppyforms.readthedocs.org/en/latest/) - Control of output of form rendering
- [django-model-utils 2.2](https://django-model-utils.readthedocs.org/en/latest/) - Useful model mixins and utilities such as `TimeStampedModel` and `Choices`
- [django-pipeline 1.4.3](http://django-pipeline.readthedocs.org/en/latest/) - CSS and JS compressor and compiler. Also minifies HTML
- [django-redis 3.8.2](https://django-redis.readthedocs.org/en/latest/) - Enables redis caching
- [django-rq 0.7.0](https://github.com/ui/django-rq) - Django integration for RQ
- [invoke 0.9.0](https://github.com/pyinvoke/invoke) - Python task execution in `tasks.py`
- [logutils 0.3.3](https://pythonhosted.org/logutils/) - Nifty handlers for the Python standard library’s logging package
- [project-runpy 0.3.1](https://github.com/crccheck/project_runpy) - Helpers for Python projects like ReadableSqlFilter
- [psycopg2 2.5.4](http://pythonhosted.org/psycopg2/) - PostgreSQL adapter
- [python-magic 0.4.6](https://github.com/ahupp/python-magic) - Library to identify uploaded files' headers
- [pytz 2014.10](http://pytz.sourceforge.net/) - World timezone definitions
- [requests 2.5.1](http://docs.python-requests.org/en/latest/) - HTTP request API
- [rq-scheduler 0.5.0](https://github.com/ui/rq-scheduler) - Job scheduling capabilities to RQ
- [six 1.9.0](http://pythonhosted.org/six/) - Python 2 and 3 compatibility utilities
- [static 1.1.1](https://github.com/lukearno/static) - Serves static and dynamic content
- [unicode-slugify 0.1.3](https://github.com/mozilla/unicode-slugify) - A slugifier that works in unicode

dev.txt
-------
- [Werkzeug 0.9.6](http://werkzeug.pocoo.org/) - WSGI utility library with powerful debugger
- [django-debug-toolbar 1.2.2](http://django-debug-toolbar.readthedocs.org/en/1.2/) - Debug information in a toolbar
- [django-sslserver 0.14](https://github.com/teddziuba/django-sslserver) - SSL localhost server

prod.txt
--------
- [Collectfast 0.2.1](https://github.com/antonagestam/collectfast) - Faster collectstatic
- [boto 2.35.2](https://boto.readthedocs.org/en/latest/) - Python interface to AWS
- [dj-database-url 0.3.0](https://github.com/kennethreitz/dj-database-url) - Allows Django to use database URLs for Heroku
- [django-secure 1.0.1](http://django-secure.readthedocs.org/en/v0.1.2/) - Django security best practices
- [django-storages 1.1.8](http://django-storages.readthedocs.org/en/latest/index.html) - Custom storage backends; using S3
- [gunicorn 19.1.0](https://github.com/benoitc/gunicorn) - Production WSGI server with workers

test.txt
--------
- [coverage 3.7.1](http://nedbatchelder.com/code/coverage/) - Measures code coverage
- [nose-exclude 0.2.0](https://bitbucket.org/kgrandis/nose-exclude) - Easily specify directories to be excluded from testing
- [django-nose 1.3](https://github.com/django-nose/django-nose) - Django test runner using nose
- [factory-boy 2.4.1](https://github.com/rbarrois/factory_boy) - Test fixtures replacement for Python
- [flake8 2.3.0](http://flake8.readthedocs.org/en/latest/) - Python style checker

config/lib
----------
- [colorstreamhandler.py](http://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output/1336640#1336640) - Colored stream handler for python logging framework
- [tdaemon.py](https://github.com/brunobord/tdaemon) - Test daemon in Python modified to work with django-admin.py, django-nose, and coverage

Node 0.10.X
===========

post_compile
------------
Using `post_compile` script for the Heroku python environment to recognize node packages

- [yuglify 0.1.4](https://github.com/yui/yuglify) - UglifyJS and cssmin compressor

package.json
------------
Locally using node and grunt to watch and compile frontend files

- [coffee-script ^1.8.0](http://coffeescript.org/) - Cleaner JavaScript
- [grunt ~0.4.5](http://gruntjs.com/) - Automatic Task Runner
- [grunt-autoprefixer ^2.0.0](https://github.com/nDmitry/grunt-autoprefixer) - Parse CSS and add vendor-prefixed CSS properties
- [grunt-coffeelint 0.0.13](https://github.com/vojtajina/grunt-coffeelint) - Lint your CoffeeScript
- [grunt-concurrent ^1.0.0](https://github.com/sindresorhus/grunt-concurrent) - Run grunt tasks concurrently
- [grunt-contrib-clean ^0.6.0](https://github.com/gruntjs/grunt-contrib-clean) - Clear files and folders
- [grunt-contrib-coffee ^0.12.0](https://github.com/gruntjs/grunt-contrib-coffee) - Compile CoffeeScript files to JavaScript
- [grunt-contrib-connect ^0.9.0](https://github.com/gruntjs/grunt-contrib-connect) - Start a static web server
- [grunt-contrib-copy ^0.7.0](https://github.com/gruntjs/grunt-contrib-copy) - Copy files and folders
- [grunt-contrib-imagemin ^0.9.1](https://github.com/gruntjs/grunt-contrib-imagemin) - Minify PNG, JPEG, GIF, and SVG images
- [grunt-contrib-jasmine ^0.8.0](https://github.com/gruntjs/grunt-contrib-jasmine) - Run jasmine specs headlessly through PhantomJS
- [grunt-contrib-watch ^0.6.1](https://github.com/gruntjs/grunt-contrib-watch) - Run tasks whenever watched files change
- [grunt-newer ^1.0.0](https://github.com/tschaub/grunt-newer) - Configure Grunt tasks to run with changed files only
- [grunt-notify ^0.4.1](https://github.com/dylang/grunt-notify) - Automatic desktop notifications for Grunt
- [grunt-open ^0.2.3](https://github.com/jsoverson/grunt-open) - Open urls and files from a grunt task
- [grunt-sass ^0.17.0](https://github.com/sindresorhus/grunt-sass) - Compile Sass to CSS
- [grunt-scss-lint ^0.3.3](https://github.com/ahmednuaman/grunt-scss-lint) - Lint your SCSS
- [grunt-shell ^1.1.1](https://github.com/sindresorhus/grunt-shell) - Run shell commands
- [grunt-template-jasmine-istanbul ^0.3.0](https://github.com/maenu/grunt-template-jasmine-istanbul) - Code coverage template mix-in for grunt-contrib-jasmine, using istanbul
- [grunt-text-replace ^0.4.0](https://github.com/yoniholmes/grunt-text-replace) - General purpose text replacement for grunt
- [load-grunt-config ^0.16.0](https://github.com/firstandthird/load-grunt-config) - Grunt plugin that lets you break up your Gruntfile config by task
- [time-grunt ^1.0.0](https://github.com/sindresorhus/time-grunt) - Display the elapsed execution time of grunt tasks

Static Assets
=============

Fonts
-----
- [SS-Standard 1.005](https://symbolset.com/icons/standard) - Standard icon library as a font. Documentation located locally at `/yesterday/static/css/fonts/ss-standard/documentation.html`

CSS
---
- [Bootstrap 3.3.0](http://getbootstrap.com) - CSS/JS starting framework

JS
--
- [jQuery 1.11.1](https://api.jquery.com/) - Useful JS functions
- [Bootstrap 3.3.0](http://getbootstrap.com) - CSS/JS starting framework
- [Underscore.js 1.7.0](http://underscorejs.org) - Very useful functional programming helpers
- [CSRF.js](https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax) - Django Cross Site Request Forgery protection via AJAX

Jasmine
-------
- [Jasmine-Ajax 2.0.1](http://github.com/pivotal/jasmine-ajax) - Set of helpers for testing AJAX requests with Jasmine
- [Jasmine-jQuery 2.0.5](https://github.com/velesin/jasmine-jquery) - Set of jQuery helpers for Jasmine

Acknowledgements
================

![Two Scoops of Django](http://twoscoops.smugmug.com/Two-Scoops-Press-Media-Kit/i-C8s5jkn/0/O/favicon-152.png "Two Scoops Logo")

This project follows best practices as espoused in [Two Scoops of Django: Best Practices for Django 1.6](http://twoscoopspress.org/products/two-scoops-of-django-1-6).

Many thanks to:
---------------

- [Daniel Greenfield](https://twitter.com/pydanny) and [Audrey Roy](https://twitter.com/audreyr) for writing the book
- All of the [contributors](https://github.com/twoscoops/django-twoscoops-project/blob/master/CONTRIBUTORS.txt) to the original fork
