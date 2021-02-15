# venv

+ Virtualenv keeps your Python packages in a virtual environment localized to \
your project, instead of forcing you to install your packages system-wide.
[source](https://stackoverflow.com/questions/23948317/why-is-virtualenv-necessary)

+ The venv module provides support for creating lightweight “virtual environments” \
with their own site directories, optionally isolated from system site directories. \
Each virtual environment has its own Python binary (which matches the version \
of the binary that was used to create this environment) and can have its own \
independent set of installed Python packages in its site directories.
[source](https://docs.python.org/3/library/venv.html)

```shell
python3 -m venv venv_name
```


# requiremets

+ flask
+ ansible
+ ansible_runner
+ python-dotenv
+ flask-wtf

```python
pip install flask
pip install ansible
pip install ansible_runner
pip install python-dotenv
pip install flask-wtf
```

# flask

+ debug mode
```shell
export FLASK_DEBUG=1
```

### files

+ __init__.py

+ routes.py
