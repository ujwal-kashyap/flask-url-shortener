from flask import Flask,request,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import shortuuid
import os
from urllib.parse import urlparse
app=Flask(__name__)
if os.environ.get("TESTING")=="1":
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///urlshortner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
class Url(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    original_url=db.Column(db.String,nullable=True)
    short_code=db.Column(db.String,nullable=True,unique=True)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    click_count=db.Column(db.Integer,default=0)
    def __repr__(self):
            return f"({self.id}-{self.original_url})"


@app.post("/shorten")
def shorten():
    data=request.get_json(silent=True) or {}
    original_url=data.get("url", "")
    if not isinstance(original_url, str) or not original_url.strip():
        return jsonify({"error": "URL is required"}), 400
    original_url =original_url.strip()
    parsed_url=urlparse(original_url)
    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.hostname
        or "." not in parsed_url.hostname
    ):
        return jsonify({"error": "Invalid URL"}), 400
    short_code=shortuuid.uuid()[:6]
    new_url = Url(
        original_url=original_url,
        short_code=short_code
    )
    db.session.add(new_url)
    db.session.commit()
    return jsonify({
        "message": "URL received",
        "original_url": original_url,
        "short_code": short_code
    }), 201

@app.get("/<short_code>")
def redirect_to_url(short_code):
    url=Url.query.filter_by(short_code=short_code).first()
    if not url:
         return jsonify ({"message":"short url not found"}),404
    url.click_count+=1
    db.session.commit()

    return redirect(url.original_url)
@app.get("/urls")
def get_all_url():
     urls=Url.query.all()
     return jsonify([
        {
            "id":url.id,
            "original_url":url.original_url,
            "short_code":url.short_code,
            "created_at":url.created_at.isoformat(),
            "click_count": url.click_count
        }
        for url in urls
    ])
@app.get("/analytics")
def analytics():
    total_urls=Url.query.count()
    total_clicks=db.session.query(db.func.sum(Url.click_count)).scalar() or 0
    most_click=Url.query.order_by(Url.click_count.desc()).first()
    return jsonify({"total_clicks":total_clicks,
                    "total_urls":total_urls,
                    "most_click":({
                         "short_code":most_click.short_code,
                         "original url":most_click.original_url,
                         "click count":
                         most_click.click_count}
                         if most_click else None)}),200
                    
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=3434)
    