# Rover Requirements

## Dependencies

Python

- [python3](https://www.python.org/downloads/)

Javascript

- [node](https://nodejs.org/en/)
- [yarn](https://yarnpkg.com/)
- [ember-cli](https://www.emberjs.com/)

Database

- [PostgreSQL](https://www.postgresql.org/)


## How to run project

Once all above global dependencies are installed, to build the project and install all dependencies for Ember and Django, from the project home run:

```
./setup.sh
```

### Run Django tests

From Rover-Django/rover/:

```
./manage.py test
```

Django code coverage:

```
coverage run --source='.' manage.py test
coverage report
```

### Run Ember tests

From Rover-Ember/rover/

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

I initially wrote group by's, count, average logic for calculating Sitter scores in Pandas, then writing the new table to a CSV and uploading it to a database table, but I thought that this would better be in Django code, so didn't end up using it.

Pandas was helpful for data exploration.

### Overall Sitter Rank

These are my rough notes from what was in the `README.md`

Sitter Scores must be kept up to date

Things that would change it:

- new stay
- new rating
- (optional) change in name

### Sitter API List Endpoint

Since the main goal was to build a end-to-end List View with sort, order, and filtering logic, I wrote down what data and functionality the List View should have.

Fields

- name
- photo
- ratings score

Order By

- Overall Sitter Rank

Must be able to scale

- pagination

Filtering Sitters by `min ratings score`

- need UI for the User to set a `min ratings score` and filter out all Users below that score

Other features

- search by name
- sort by name
- sort by ratings score


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

	- Review - normalized - with foreign keys to Owner and Sitter

### Generating of the Scores and populating the database

This logic is in the Django `models.py` files.

Some thoughts about this, is that Django Manager methods are being called to do the data imports, so the logic can be custom Manager methods. Another thought is that this represents a database `seeding` concept, and if one wanted to keep the Django Manager classes as production code only, since a database `seed` only happense once and isn't production logic, then for example a separate `seed` app could be created to encapsulate this logic. 

### Testing

Pretty strait forward unit tests, and end to end tests that filter logic works and returned properly sorted, filter, ordered data. Unit tests for methods and so on.

## Frontend

Chose [EmberJs](https://www.emberjs.com/). Our app at my previous position was built with EmberJs and this is the single page app framework that I'm the most familiar with.

Some hurdles that I ran into were that a lot of internal app structure that we had we custom built and didn't use Ember 3rd partly libaries for. I used some 3rd party libraries in place of our custom logic.

- Table Grid - [ember-light-table](https://github.com/offirgolan/ember-light-table)

	- this is a pretty popular solution in the community and one of our EmberJs developers even said that we could have used it instead of building our own

- Client data store - [Ember Data](https://github.com/emberjs/data)

	- defacto EmberJs data store
	- we used [ember-cli-simple-store](https://github.com/toranb/ember-cli-simple-store) but had to hand roll adapters, serializers and ajax logic

- Fixtures - [ember-cli-mirage](https://github.com/samselikoff/ember-cli-mirage)

	- defacto for EmberJs test or localhost fixtures
	- we used static or partially dynamically generated Javascipt objects

- Select box for "min ratings score" filter - [ember-power-select]()

- Rating score formatting - [ember-cli-accounting](https://github.com/cibernox/ember-cli-accounting)

	- wraps [accounting.js](http://openexchangerates.github.io/accounting.js/)

### Testing

I wrote tests for the `start-page` and `end-page` helper function because they involved a variety of cases and math, so this was the fastest way to iterate.

The `sitter-table` is manually tested. I ran out of time here. This should be acceptance that the User clicks are generating the correct xhr requests.



