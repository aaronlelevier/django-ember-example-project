# Rover Requirements

## Overview

### Overall Sitter Rank

must be kept up to date

Things that would change it:

- new stay
- new rating
- (optional) change in name

### ListView

Fields

- name
- photo
- ratings score

Order By

- Overall Sitter Rank

Must be able to scale

- pagination
- sitter rank and other fields should be columns so they can be ordered by

	- check if there should be an index on `overall sitter rank`?

Filtering Sitters by min `ratings score`

- need UI for the User to set a min `ratings score` and filter out all Users below that score

Other features

- search by name
- sort by name
- sort by ratings score


## Backend

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

	- Review - normalized


## Postgres

```
CREATE ROLE rover WITH LOGIN PASSWORD 'rover';
ALTER ROLE rover SUPERUSER;
```


