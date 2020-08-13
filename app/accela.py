from flask import Flask, render_template, abort, send_file, request
from flask_caching import Cache
from pathlib import Path
from settings import Config
from werkzeug.exceptions import HTTPException
import markdown
import re
import yaml

CONFIG = Config()

app = Flask(__name__)
app.config.from_mapping(CONFIG.CACHE_CONFIG)
cache = Cache(app)

BASE_DIR = Path(__file__).parent / "data"

md = markdown.Markdown(
    extensions=["meta", "extra", "wikilinks", "codehilite", "sane_lists", "admonition"]
)


@app.template_filter("deslash")
def deslash(s):
    if s.endswith("/"):
        return s[:-1]
    return s


@app.template_filter("parent")
def get_parent(s):
    return str(Path(s).parent).replace("\\", "/")


@app.errorhandler(HTTPException)
def handle_exception(e):
    return (
        "{} : {}".format(e.code, e.name),
        e.code,
        {"Content-Type": "text/plain; charset=utf-8"},
    )


def timestamp(f):
    # if CONFIG.get("timestamp"):
    #     return datetime.fromtimestamp(f.stat().st_mtime).strftime(
    #         CONFIG.get("date_format")
    #     )
    return ""


def remove_digits(f):
    return re.sub(r"\d+\.", "", f.name)


def list_directories(path):
    # get total set of ignored contents
    ignored = CONFIG.IGNORED_FILES.copy()
    if CONFIG.IGNORE_FILE and (path / CONFIG.IGNORE_FILE).exists():
        with open(path / CONFIG.IGNORE_FILE, "r") as f:
            ignored.extend([line.strip() for line in f.readlines()])

    dirs = sorted(filter(lambda x: x.name not in ignored, path.iterdir()), key=lambda y: y.name)

    ret = [*map(lambda x: (remove_digits(x), timestamp(x.name)), dirs)]
    return ret


def get_meta(md_meta, content):
    d = dict([(i, *j) for (i, j) in md_meta.items()])
    # fallback
    d["author"] = CONFIG.AUTHOR
    d["description"] = d.get(
        "description", re.sub("<.*?>", "", content).replace("\n", " ")
    )
    d["title"] = d.get("title", re.sub("<.*?>", "", content.split("\n")[0]))
    return d


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@cache.cached(query_string=True)
def http(path):
    md.reset()
    website_dir = BASE_DIR
    if path:  # if not root
        for i in Path(path).parts:
            # optional number prefix
            r = re.compile(f"^((\d+\.))?{i}$")
            subdirs = [*website_dir.iterdir()]
            found = [*filter(r.match, [o.name for o in subdirs])]
            if not len(found):
                abort(404)
            website_dir = website_dir / found[0]

    # don't display hidden files
    if website_dir.name in CONFIG.IGNORED_FILES or not website_dir.exists():
        abort(404)

    # send files
    if not website_dir.is_dir():
        return send_file(str(website_dir), mimetype="text/plain")

    # get index.md information
    try:
        with open(website_dir / "index.md", "r", encoding="utf-8") as f:
            content = md.convert(f.read())
    except IOError:
        content = ""

    param = request.args.get("s")
    if param:
        style = f"?s={param}"
    else:
        style = ""

    return (
        render_template(
            "default.html",
            style=style,
            dirs=list_directories(website_dir),
            content=content,
            path=path,
            meta=get_meta(md.Meta, content),
        ),
        {"Content-Type": "text/html; charset=utf-8"},
    )


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
