from flask_frozen import Freezer
from app import app, BLOG_CONTENT_DIR, WIKI_CONTENT_DIR
from os import listdir

freezer = Freezer(app)
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_BASE_URL'] = 'https://postmarketos.org/'

@freezer.register_generator
def blog_post():
    for f in listdir(BLOG_CONTENT_DIR):
        y, m, d, *title = f[:-3].split('-')
        slug = '-'.join(title)
        yield { 'y': y, 'm': m, 'd': d, 'slug': slug }

@freezer.register_generator
def wiki_page():
    for f in listdir(WIKI_CONTENT_DIR):
        slug = f[:-3]
        yield { 'slug': slug }

if __name__ == '__main__':
    freezer.freeze()
