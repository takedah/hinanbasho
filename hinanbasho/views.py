import os

from flask import Flask, escape, g, render_template, request, url_for

from hinanbasho.db import DB
from hinanbasho.errors import LocationError
from hinanbasho.models import CurrentLocation
from hinanbasho.services import EvacuationSiteService

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    response.headers.add(
        "Content-Security-Policy",
        "default-src 'self'; style-src 'self' 'unsafe-inline' \
                    stackpath.bootstrapcdn.com unpkg.com kit.fontawesome.com; \
                    script-src 'self' code.jquery.com cdnjs.cloudflare.com \
                    stackpath.bootstrapcdn.com unpkg.com kit.fontawesome.com; \
                    img-src 'self' *.tile.openstreetmap.org unpkg.com data:; \
                    connect-src ka-f.fontawesome.com; \
                    font-src ka-f.fontawesome.com;",
    )
    response.headers.add("X-Content-Type-Options", "nosniff")
    response.headers.add("X-Frame-Options", "DENY")
    response.headers.add("X-XSS-Protection", "1;mode=block")
    return response


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def connect_db():
    return DB()


def get_db():
    if not hasattr(g, "postgres_db"):
        g.postgres_db = connect_db()
    return g.postgres_db


def get_area_names():
    if not hasattr(g, "area_names"):
        service = EvacuationSiteService(get_db())
        g.area_names = service.get_area_names()
    return g.area_names


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "postgres_db"):
        g.postgres_db.close()


@app.route("/")
def index():
    title = "トップページ"
    return render_template("index.html", title=title, area_names=get_area_names())


@app.route("/search_by_gps", methods=["GET", "POST"])
def search_by_gps():
    if request.method == "GET":
        title = "旭川市避難場所検索"
        return render_template("index.html", title=title, area_names=get_area_names())
    else:
        title = "現在地から近い避難場所の検索結果"
        current_latitude = escape(request.form["current_latitude"])
        current_longitude = escape(request.form["current_longitude"])
        try:
            current_latitude = float(current_latitude)
            current_longitude = float(current_longitude)
            current_location = CurrentLocation(
                latitude=current_latitude, longitude=current_longitude
            )
        except (LocationError, ValueError):
            title = "検索条件に誤りがあります"
            error_message = "緯度経度が正しくありません。"
            return render_template(
                "error.html",
                title=title,
                area_names=get_area_names(),
                error_message=error_message,
            )

        service = EvacuationSiteService(get_db())
        near_sites = service.get_near_sites(current_location)
        results_length = len(near_sites)
        return render_template(
            "search_by_gps.html",
            title=title,
            area_names=get_area_names(),
            search_results=near_sites,
            current_latitude=current_latitude,
            current_longitude=current_longitude,
            results_length=results_length,
        )


@app.route("/site/<site_id>")
def site(site_id):
    site_id = escape(site_id)
    try:
        site_id = int(site_id)
    except ValueError:
        title = "検索条件に誤りがあります"
        error_message = "避難場所の連番が正しくありません。"
        return render_template(
            "error.html",
            title=title,
            area_names=get_area_names(),
            error_message=error_message,
        )

    service = EvacuationSiteService(get_db())
    result = service.find_by_site_id(site_id)
    if len(result) == 0:
        title = "検索条件に誤りがあります"
        error_message = "そのような避難場所連番はありません。"
        return render_template(
            "error.html",
            title=title,
            area_names=get_area_names(),
            error_message=error_message,
        )

    title = "避難場所「" + result[0].site_name + "」の情報"
    return render_template(
        "site.html",
        title=title,
        area_names=get_area_names(),
        result=result[0],
    )


@app.route("/area/<area_name>")
def area(area_name):
    area_name = escape(area_name)
    service = EvacuationSiteService(get_db())
    search_results = service.find_by_area_name(area_name)
    results_length = len(search_results)
    if results_length == 0:
        title = "検索条件に誤りがあります"
        error_message = "そのような住所の避難場所はありません。"
        return render_template(
            "error.html",
            title=title,
            area_names=get_area_names(),
            error_message=error_message,
        )

    title = "「" + area_name + "」の避難場所"
    return render_template(
        "area.html",
        title=title,
        area_names=get_area_names(),
        area_name=area_name,
        search_results=search_results,
        results_length=results_length,
    )


@app.route("/search_by_site_name")
def search_by_site_name():
    site_name = escape(request.args.get("site_name", None))
    title = "名称に「" + site_name + "」を含むの避難場所の検索結果"
    service = EvacuationSiteService(get_db())
    search_results = service.find_by_site_name(site_name)
    results_number = len(search_results)
    return render_template(
        "search_by_site_name.html",
        title=title,
        area_names=get_area_names(),
        site_name=site_name,
        search_results=search_results,
        results_number=results_number,
    )


@app.errorhandler(404)
def not_found(error):
    title = "404 Page Not Found."
    return render_template("404.html", title=title, area_names=get_area_names())


if __name__ == "__main__":
    app.run(debug=True)
