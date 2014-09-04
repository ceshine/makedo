MakeDO
======

A simple command line interface for DigitalOcean based on [poseidon](https://github.com/changhiskhan/poseidon) and [click](http://click.pocoo.org).

This project was developed under Python 2.7. Python 3.X support is not guaranteed.


A work in progress.. 

Install
------
Clone the repository, and run one of the following commands in the project folder:

```
pip install .
```

```
python setup.py
```

Usage
-------
Get help and find all available commands:

```
makedo --help
```

Get detailed argument descriptions for a subcommand (e.g. list):

```
makedo list --help
```

Examples
--------
Make a snapshot named **snap1** and then destory the droplet **test**:

```
makedo destroy --snapshot snap1 test
```
