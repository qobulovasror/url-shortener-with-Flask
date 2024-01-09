import hashlib
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

urls = [{
    "full": "https://getbootstrap.com/docs/5.3/forms/layout/#utilities",
    "short": "2asd132d1fsd",
    "clicks": 0
}]

@app.route("/")
def main_page():
    return render_template("index.html", urls=urls)

@app.get("/shorter")
def shorter_url():
    url = request.args.get("url")
    if url=="":
        return render_template("index.html", urls=urls, error="url not found")
    
    urls.append({"full": url, "short": hashlib.md5(url.encode()).hexdigest()[:10], "clicks": 0})
    return render_template("index.html", urls=urls)

@app.get("/<slug>/")
def redirect_to_original(slug: str):
    org_url = [url for url in urls if url["short"]==slug][0]
    if org_url :
        urls[urls.index(org_url)]["clicks"] = int(org_url["clicks"])+1
        return redirect(org_url["full"])
    return render_template("index.html", urls=urls, error="This url is invalid")


if __name__ == "__main__":
    app.run(port=4200, debug=True)