# DebunkBot
A bot that debunks claims shared on social media by sharing a fact check. Powered by Google Sheets and the rains in Africa. Accessible at https://debunkbot.codeforafrica.org/

## Development

Gitignore is standardized for this project using [gitignore.io](https://www.gitignore.io/) to support various development platforms.
To get the project up and running:

- Clone this repo

### Virtual environment

- Use virtualenv to create your virtual environment; `virtualenv venv`
- Activate the virtual environment; `source venv/bin/activate`
- Install the requirements; `pip install -r requirements.txt`
- Create a debunkbot database
- Copy the `.env.sample` to `.env` and fill in the environment variables.
- Migrate the database: `python manage.py migrate`
- Run the server: `python manage.py runserver`

#### Runing tasks
Ensure reddis server is running and start the tasks by running 
`celery -A debunkbot beat -l info `
then 
`celery -A debunkbot worker -l info`

### Docker

Using docker compose:

- Build the project; `docker-compose build`
- Run the project; `docker-compose up -d`
