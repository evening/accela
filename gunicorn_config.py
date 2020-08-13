import os

bind = "%s:%s" % (os.environ.get("HOST", "0.0.0.0"), os.environ.get("PORT", "5000"))

workers = int(os.environ.get("GUNICORN_WORKERS", 2))
