# postmarketos.org

## Dev

### Update Wiki Content

```bash
$ git submodule update --recursive --remote 
```

### Dev Server

```bash
$ FLASK_DEBUG=1 FLASK_APP=app.py flask run
```

### Build

```bash
$ python freeze.py
```
