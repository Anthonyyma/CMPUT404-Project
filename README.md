# CMPUT404-Project

## Project Setup

1. Create a virtual environment (optional).
```
python -m venv venv
source venv/bin/activate # linux
venv/scripts/activate # windows
```

2. Install required packages.
```
pip install -r requirements.txt
```

3. Run database migrations
```
python manage.py migrate
```

4. If you are contributing, install the pre-commit hooks that are specified in `.pre-commit-config.yaml`
```
precommit install
```

This makes it so that before you commit to the repo, all changes will be automatically formatted (black) and linted (flake8). 
If any files are formatted, then you will have to stage the new changes.
If there is a linter error, it will prevent the commit from going through until you fix it.
You should try to fix any linter errors that pop up, but you can always bypass this by commenting out the contents of `.pre-commit-config.yaml`

5. If you are contributing, you should install the formatter `black`. 
It's listed in `.vscode/extensions.json` so if you are using vscode then it suggest the extension to you. 

## Run Server

```
# from /social
python manage.py runserver
```

### Testing

You can run the tests from `/social` by running `python manage.py test`