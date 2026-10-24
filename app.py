from flask import Flask,request,jsonify,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import shortuuid
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///urlshortner.db"
db=SQLAlchemy(app)
class Url(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    original_url=db.Column(db.String,nullable=True)
    short_code=db.Column(db.String,nullable=True,unique=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    click_count=db.Column(db.Integer,default=0)
    def __repr__(self):
            return f"({self.id}-{self.original_url})"
with app.app_context():
    db.create_all()
@app.post("/shorten")
def shorten():
    data=request.get_json()
    original_url=data.get("url")
    if not original_url:
        return jsonify({"error":"url is required"}),400
    short_code=shortuuid.uuid()[:6]
    new_url=Url(original_url=original_url,
                    short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    return jsonify ({"message":"url recived",
                 "original_url":original_url,
                 "short_code":short_code})
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
            "created_at":url.created_at,
            "click_count": url.click_count
        }
        for url in urls
    ])
if __name__=="__main__":
    app.run(debug=True,port=3434)
    