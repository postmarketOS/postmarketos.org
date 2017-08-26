import markdown

from flask import Flask, render_template, url_for
from os import listdir
import os
import re
import yaml

app = Flask(__name__)

BLOG_CONTENT_DIR = 'content/blog'

REGEX_SPLIT_FRONTMATTER = re.compile(r'^---$', re.MULTILINE)

WIKI_REDIRECTS = {
    "chat": "Matrix_and_IRC",
    "deviceinfo": "Deviceinfo_reference",
    "devices": "Supported_devices",
    "irc": "Matrix_and_IRC",
    "matrix": "Matrix_and_IRC",
    "troubleshooting": "Troubleshooting",
    "usbhook": "Inspecting_the_initramfs",
    "warning-repo": "Troubleshooting#Installed_version_newer_than_the_version_in_the_repositories",
    "warning-repo2": "Troubleshooting#Newer_version_in_binary_package_repositories_than_in_aports_folder",
    "wiki": "Main_page",
}


@app.route('/')
def home():
    return render_template('index.html')


def reading_time(content):
    content = re.sub('<[^<]+?>', '', content)
    words_per_minute = 200
    words = content.split(" ")
    return int(len(words) / words_per_minute)


def parse_post(post):
    with open(os.path.join(BLOG_CONTENT_DIR, post)) as handle:
        raw = handle.read()
    frontmatter, content = REGEX_SPLIT_FRONTMATTER.split(raw, 2)

    data = yaml.load(frontmatter)

    y, m, d, *title = post[:-3].split('-')
    slug = '-'.join(title)

    data['url'] = url_for('blog_post', y=y, m=m, d=d, slug=slug)
    data['reading_time'] = reading_time(content)

    return data


@app.route('/blog/')
def blog():
    posts = sorted(listdir(BLOG_CONTENT_DIR), reverse=True)
    posts = map(parse_post, posts)
    return render_template('blog.html', posts=posts)


@app.route('/blog/<y>/<m>/<d>/<slug>/')
def blog_post(y, m, d, slug):
    post_path = '-'.join([y, m, d, slug])
    with open('{}/{}.md'.format(BLOG_CONTENT_DIR, post_path), 'r') as f:
        text = f.read()
    frontmatter, body = REGEX_SPLIT_FRONTMATTER.split(text, 2)
    data = yaml.load(frontmatter)
    readingtime = reading_time(body)
    html = markdown.markdown(body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
    return render_template('blog-post.html', title=data["title"], html=html, reading_time=readingtime,
                           date=data["date"])


@app.route('/<slug>/')
def wiki_redirect(slug):
    """ WARNING: This must be the last route! """
    return render_template('redirect.html', url='https://wiki.postmarketos.org/wiki/' + WIKI_REDIRECTS[slug])
