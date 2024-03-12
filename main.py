from flask import Flask, render_template, request, redirect, send_file
from scrap import Playwright
from file import CSVWriter

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template('home.html')

db = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        job_db = db[keyword]
    else:
        script = Playwright(keyword)
        script.initialize_browser()
        script.create_page()
        script.goto_url()


        script.access_to_data_page()
        script.scrap_data()
        
        script.exit_browser()
        
        db[keyword] = script.results
        job_db = db[keyword]
        
    return render_template('search.html', keyword=keyword, jobs=job_db)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save = CSVWriter(keyword)
    save.write_file(db[keyword])
    return send_file(save.filename, as_attachment=True)

app.run()