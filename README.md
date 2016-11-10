# wsp-bkl

## Prerequisite
- Python3
- Django==1.10.1
- psycopg2==2.6.2
- postgresql v9.x
- libpq-dev python3-dev

## Installation
``` sh
git clone https://github.com/raksit31667/wsp-bkl.git
```

redirect to wsp-bkl and then
``` sh
pip install -r requirements.txt
```

## Create the new feature / branch
``` sh
git checkout <base_branch>
git checkout -b <task_name>
```
Then add, commit and push from that branch.

Next, do the merge in GitHub.

Example, in Use case "View the movie list" and you would like to edit the templates:
``` sh
git checkout -b show_list/templates
```

## Features (Cycle 1)
push to these following branches

- view-list-movies (momo)
- view-movie-description (momo)
- watch-movie (tan)
- login (boss)
- register (boss)
- download-movie (peak)
- search (tan)
- filter (earth)
- admin-login
- admin-add
- admin-delete
- admin-edit

## Features (Cycle 2)
push to these following branches

- refillment (boss)
- purchase (peak)
- reception (tan)
- ratings (earth)
- library (momo)
- recommended-movies

## Specific Feature
push to the branch ```master```
- default css
- default templates
