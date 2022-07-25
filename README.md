# binary
A package implementing the revolutionary BinarySequence for python

# Set Up

Set up a python virtual environment:

```sh

python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
pip install -U pip

```

For testing or development you should also install the dev-requirements.

```sh
pip install -r dev-requirements.txt

```

Then go to the location where you want to install the package and:

```sh

git clone https://github.com/LeSasse/binary.git
cd binary
pip install -e .

```

Now you can easily use the package but also adapt the code to your liking.
Run tests to see if everything works as expected:

```sh
python3 -m pytest
```

