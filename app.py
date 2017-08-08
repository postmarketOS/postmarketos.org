import markdown

from flask import Flask, render_template, url_for
from os import listdir

app = Flask(__name__)

BLOG_CONTENT_DIR = 'content/blog'
WIKI_CONTENT_DIR = 'content/wiki'

@app.route('/')
def home():
    return render_template('index.html')

def parse_post(post):
    y, m, d, *title = post[:-3].split('-')
    slug = '-'.join(title)
    return {'url': url_for('blog_post', y=y, m=m, d=d, slug=slug), 'title': ' '.join(title)}

@app.route('/blog/')
def blog():
    posts = sorted(listdir(BLOG_CONTENT_DIR), reverse=True)
    posts = map(parse_post, posts)
    return render_template('blog.html', posts=posts)

@app.route('/blog/<y>/<m>/<d>/<slug>/')
def blog_post(y, m, d, slug):
    post_path = f'{y}-{m}-{d}-{slug}'
    with open(f'{BLOG_CONTENT_DIR}/{post_path}.md', 'r') as f:
        text = f.read()
        _, header, body = text.split('---')
        for h in header.split('\n'):
            if h.startswith('title'):
                title = h.split('title:')[1].strip()
        html = markdown.markdown(body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        return render_template('blog-post.html', title=title, html=html)

def parse_page(page):
    slug = page[:-3]
    title = slug.replace('-', ' ')
    return {'url': url_for('wiki_page', slug=slug), 'title': title}

@app.route('/wiki/')
def wiki():
    pages = sorted(listdir(WIKI_CONTENT_DIR), reverse=True)
    pages = map(parse_page, pages)
    return render_template('wiki.html', pages=pages)

@app.route('/wiki/<slug>/')
def wiki_page(slug):
    with open(f'{WIKI_CONTENT_DIR}/{slug}.md') as f:
        text = f.read()
        title = slug.replace('-', ' ')
        html = markdown.markdown(text, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
        return render_template('wiki-page.html', title=title, html=html)

@app.route('/troubleshooting/')
def troubleshooting():
    return render_template('redirect.html', url='https://github.com/postmarketOS/pmbootstrap/wiki/Troubleshooting')

@app.route('/deviceinfo/')
def deviceinfo():
    return render_template('redirect.html', url='https://github.com/postmarketOS/pmbootstrap/wiki/deviceinfo-reference')

@app.route('/usbhook/')
def usbhook():
    return render_template('redirect.html', url='https://github.com/postmarketOS/pmbootstrap/wiki/Inspecting-the-initramfs/')
