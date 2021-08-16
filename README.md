# DebunkBot
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/CodeForAfrica/DebunkBot/master.svg)](https://results.pre-commit.ci/latest/github/CodeForAfrica/DebunkBot/master)

A bot that debunks claims shared on social media by sharing a fact check. Powered by Google Sheets and the rains in Africa. Accessible at https://debunkbot.codeforafrica.org/

## Development

Gitignore is standardized for this project using [gitignore.io](https://www.gitignore.io/) to support various development platforms.
To get the project up and running:

### Quick Start

This guide will show you how to set up the project using virtual environment or docker.

#### Using Virtualenv

- Clone this repo
- Use virtualenv to create your virtual environment; `virtualenv venv`
- Activate the virtual environment; `source venv/bin/activate`
- Install the requirements; `pip install -r requirements.txt`
- Create a debunkbot database
- Copy the `.env.sample` to `.env` and fill in the environment variables.
- Migrate the database: `python manage.py migrate`
- Run the server: `python manage.py runserver`

### Running Tests and linting

Assuming virtualenv is already installed and activated
```
pip install -Ur requirements.txt
black .
isort .
flake8 . --exclude venv
```

Also run `pre-commit install` to install the pre-commit hooks.

#### Runing tasks
Ensure reddis server is running and start the tasks by running
`celery -A debunkbot beat -l info `
then
`celery -A debunkbot worker -l info`

### Docker

- Build the project; `make build`
- Run the project; `make run`
- Stop the project; `make stop`


### Running the project.
- Create a super user by executing `make createsuperuser` and fill in all the required details.
- Navigate to `{url}:8000/admin` and login using the credentials you created above.
- Get/Create a service account on google developer console. Using the generated json, create a google sheet credentials on the admin page which will be used to interract with all the google sheet operations we will be performing.
- Next on the admin dashboard, add one or more Google sheet claims database. In cases where the sheet doesn't have all the fields as shown on the admin page, supply an empty string.
- Lastly, to force the the system to pull the claims from the new claims databases, navigate to `{url}:8000/claims/update`.
