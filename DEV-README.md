# DEV README

This README is separated into logic sections.  It's organized in a way to explore the repository and explain the thinking along the way.

Conceptually, I tried to think of this as a single pull request. I took broad strokes and gradually refined in the best way possible in order to keep moving forward and add all of the features.  The commit ordering reflects that. I didn't squash any commits and in order to preserve how things happened. 


## Global Dependencies

Python

- [python3](https://www.python.org/downloads/)

Javascript

- [node](https://nodejs.org/en/)
- [yarn](https://yarnpkg.com/)
- [ember-cli](https://www.emberjs.com/)

Database

- [PostgreSQL](https://www.postgresql.org/)


## How to run project

Once all above global dependencies are installed, to build the project and install all dependencies for Ember and Django, from the project home:

```
# create virualenv and install pip dependencies
cd Rover-Django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# build project
bash ../setup.sh

# run project
cd ../Rover-Django/rover/
./manage.py runserver
```

### Run Django tests

From `Rover-Django/rover/` dir:

```
./manage.py test
```

Django code coverage, From `Rover-Django/rover/` dir:

```
coverage run --source='.' manage.py test
coverage report
```

### Run Ember tests

From `Rover-Ember/rover/` dir:

```
ember test
```

## Initial Overview

### First

I first took an overview of the `README.md` for all requirements and what the goals are. Then I started exploring the `reviews.csv`

### Data exploration

I started with exploring the data using the Python [Pandas](https://pandas.pydata.org/) library. The Jupyter notebook for this is at `notebooks/pandasy.ipynb` and can be run by:

```
# from project home
cd notebooks
ipython notebook
```

I was thinking that the unique key was the Owner or Sitter name. But, upon exploring the data these were the unique counts:

- sitter - 100
- sitter_email - 100
- owner - 186
- owner_email - 189

The name `Tony L.` appeared as a Owner and Sitter.

Looking at the emails, both `sitter_email` and `owner_email` where prefixed with `user<number>`. Also both were unique across regardless of being an Owner or Sitter, where as the names were not, so I took the `email` as the unique key for Owner or Sitter.

Each has a Django `User` one-to-one relationship. The `email` is stored as the Django `username`, which is the only required field on the Django `User` model.

I initially wrote group by's, count, average logic for calculating Sitter scores in Pandas, with the idea to write it to a CSV and upload to a database table, but I thought that this would better be in Django code, so didn't end up using it.

Pandas was helpful for data exploration.

### Overall Sitter Rank

This will be the default page ordering.

Sitter Scores must be kept up to date.

Things that would change it:

- new stay
- new rating
- change in name (optional)

### Sitter List View and API Endpoint

Since the main goal was to build a end-to-end List View with sort, order, and filtering logic, I wrote down what data and functionality the List View should have.

Fields

- id
- name
- photo
- ratings score

Default ordering

- Overall Sitter Rank

Must be able to scale

- pagination or infinity scroll (I chose pagination)

Filtering

- min ratings_score
- name

Ordering

- name
- ratings_score

Search

- name

I will need UI for the User to set a `min ratings score` and filter out all Users below that score

Also for `name` search.

Basic UI for ordering exists with the `ember-light-table` add-on, so just the component logic of what API request to call needs to be written.

## Backend

For the backend I used [Django](https://www.djangoproject.com/) and [django-rest-framework](http://www.django-rest-framework.org/). At my previous position, this was our API backend, so this is very familiar.

I wrote out the below sketch of the apps that I wanted to have.  From the `README.md`, there was a little bit of uncertainty here because it said to design a database schema based upon the `reviews.csv`, but a full database schema isn't needed to support a single List View and API endpoint. In the end, I took it as a requirement and built out an initial schema from what was in `reviews.csv` even if it wasn't viewable by the end user.

I used [django-extensions](https://github.com/django-extensions/django-extensions) for prototyping the `csv.DictReader` CSV upload to the `RawReview` table. I also used if for prototyping the Django ORM queries for counting `stays` and `sitter_scores` before putting the logic in code with tests. Sometimes I like to do this because the feedback loop is quicker depending on what it is.

I used [model-mommy](https://github.com/vandersonmota/model_mommy) for some test fixtures.

[isort](https://github.com/timothycrosley/isort) and [pylint](https://pypi.python.org/pypi/pylint) for sorting imports and linting files.

[coverage](https://pypi.python.org/pypi/coverage) for Django code coverage checking.

### Initial sketch of Django apps

2 apps to start

- customer

	- User(Django)

		- username
		- email

	- AbstractCustomer

		- name
		- phone_number
		- image
		- user - OneToOneField - User(Django)
		
	- Sitter(AbstractCustomer)

		- stays
		- ratings_score
		- sitter_score
		- overall_score

	- Owner(AbstractCustomer)

		- dogs - HStoreField ?? (w/o this field, maybe use SQLite?)
	
- review

	- RawReview upload of `reviews.csv`

	- Review
	
		- normalized
		- with foreign keys to `Owner` and `Sitter`

### Generating of the Scores and populating the database

This logic is in the Django `models.py` files.

Some thoughts about this, is that Django Manager methods are being called to do the data imports, so the logic can be in custom Manager methods. Another thought is that this represents a database `seeding` concept, and if one wanted to keep the Django Manager classes as production code only, since a database `seed` only happense once and isn't production logic, then for example a separate `seed` app could be created to encapsulate this logic. 

### Testing

Pretty strait forward unit tests, and end to end tests that filter logic works and returned properly sorted, filter, ordered data. Unit tests for methods and so on.

### Debugging

Used Python standard debugger `pdb`

## Frontend

I chose [EmberJs](https://www.emberjs.com/). Our app at my previous position was built with EmberJs and this is the single page app framework that I'm the most familiar with.

Some hurdles that I ran into were that a lot of  internal app structure that we had we custom built and didn't use Ember 3rd partly libaries for. I used some 3rd party libraries in place of our custom logic.

- Table Grid - [ember-light-table](https://github.com/offirgolan/ember-light-table)

	- this is a pretty popular solution in the community and one of our EmberJs developers even said that we could have used it instead of building our own

- Client data store - [Ember Data](https://github.com/emberjs/data)

	- defacto EmberJs data store
	- we used [ember-cli-simple-store](https://github.com/toranb/ember-cli-simple-store) but had to hand roll adapters, serializers and ajax logic

- Fixtures - [ember-cli-mirage](https://github.com/samselikoff/ember-cli-mirage)

	- defacto for EmberJs test or localhost fixtures
	- we used static or partially dynamically generated Javascipt objects

- Select box for "min ratings score" filter - [ember-power-select]()

	- we used this add-on

- Rating score formatting - [ember-cli-accounting](https://github.com/cibernox/ember-cli-accounting)

	- we used this add-on
	- wraps [accounting.js](http://openexchangerates.github.io/accounting.js/)


### Styling

Disclaimer, I am a backend developer. This app probably has the best styling that I've ever done. I usually use templates from [themeforest.net](https://themeforest.net/) on personal projects. One of the requirements was an appealing UI, so I did my best to do that. And also, if the UI is no good, to a certain point it doesn't matter if the backend is great because no one wants to use it right!  I didn't use a ThemeForest template because that would be bloat for a single view, and I didn't feel right about that vs. using open source Javascript, Python, libraries etc... which is different.

Used [ember-boostrap](http://www.ember-bootstrap.com/) for styling and CSS grid, container.

Used Rover green.

Created a spinner with Rover green on [loading.io](https://loading.io/)

[ember-font-awesome](https://github.com/martndemus/ember-font-awesome) for fa-icons

Wrote app wide CSS and used [ember-component-css](https://github.com/ebryn/ember-component-css) for component specific CSS

### Testing

I wrote tests for the `start-page` and `end-page` helper function because they involved a variety of cases and math, so this was the fastest way to iterate.

The `sitter-table` is end-to-end manually tested. This was the faster way to iterate on the functionality, but obvious automated tests are needed for scaling. There are some initial component and unit tests. I ran out of time here. This should be acceptance that the User clicks are generating the correct xhr requests that match what the API expects.

### Debugging

Used Chrome debug tools.

In EmberJs used `debugger` and `assert.async()` with `qunit`
