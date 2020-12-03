# venv

+ Virtualenv keeps your Python packages in a virtual environment localized to \
your project, instead of forcing you to install your packages system-wide.
(https://stackoverflow.com/questions/23948317/why-is-virtualenv-necessary)[source]

+ The venv module provides support for creating lightweight “virtual environments” \
with their own site directories, optionally isolated from system site directories. \
Each virtual environment has its own Python binary (which matches the version \
of the binary that was used to create this environment) and can have its own 
independent set of installed Python packages in its site directories.

```shell
python3 -m venv venv_name
```
