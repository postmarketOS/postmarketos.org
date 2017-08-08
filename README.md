# postmarketos.org

## Dev

### Python Requirements Setup

Install all requirements, preferably within a virtualenv:

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

### Update Wiki Content

Wiki content is pulled and updated automagically as a git submodule from the [pmbootstrap wiki](https://github.com/postmarketOS/pmbootstrap/wiki).

```bash
$ git submodule update --init --recursive
$ git pull --recurse-submodules
```

### New Blog Content

Blog content is written in markdown format with metadata in the file header. Filename syntax is `yyyy-mm-dd-slug.md`.

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

Run the dev server during local development, changes are auto reloaded:

```bash
(venv)$ FLASK_DEBUG=1 FLASK_APP=app.py flask run
```

### CSS

CSS is compiled via `lessc`:

```bash
$ npm install -g less
$ lessc static/css/main.less static/css/main.css
```

### Build

To run a static site build, run:

```bash
(venv)$ python freeze.py
```

This will generate a static version in `docs/`. Any manual changes to the `docs/` directory will be overridden in the next build.
