# postmarketos.org

## Dev

### Python Requirements Setup

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Update Wiki Content

```bash
$ git submodule update --init --recursive
$ git pull --recurse-submodules
```

### New Blog Content

```bash
$ cat >content/blog/2017-12-31-happy-new-year.md << EOF
> ---
> title: Happy New Year!
> ---
>
> This is a *markdown* **formatted** post.
> EOF
```

### Dev Server

```bash
$ FLASK_DEBUG=1 FLASK_APP=app.py flask run
```

### Build

```bash
$ python freeze.py
```
