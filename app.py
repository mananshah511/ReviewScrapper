from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup as bs
from flask_cors import CORS,cross_origin

app = Flask(__name__)


@app.route('/', methods= ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")


@app.route("/FlipcartReview", methods = ['POST'])
@cross_origin()
def review_scrapper():
    product_name = request.form['content']
    url = "https://www.flipkart.com/search?q=" + product_name
    get_url = requests.get(url)
    main_html = bs(get_url.content, 'html.parser')
    links = links=main_html.find_all("div",{"class":["_2kHMtA","_4ddWXP"]})
    reviews = []
    for i in range(len(links)):
        product_url = "https://www.flipkart.com" + links[i].a['href']
        product_url.encode(encoding="UTF-8")
        product_requests = requests.get(product_url)
        html_review = bs(product_requests.content, 'html.parser')
        review_data = html_review.find_all("div", {"class": ["t-ZTKy"]})
        rating_star = html_review.find_all("div", {"class": "_3LWZlK _1BLPMq"})
        customer_name = html_review.find_all("p", {"class": "_2sc7ZR _2V5EHH"})
        review_title = html_review.find_all("p", {"class": "_2-N8zT"})
        for j in range(len(review_data)):
            try:
                rd = review_data[j].div.div.text
            except:
                rd = "review data is not available"
            try:
                rs = rating_star[j].text
            except:
                rs = "rating is not available"
            try:
                cn = customer_name[j].text
                cn.encode(encoding="UTF-8")
            except:
                cn = "customer name is not available"
            try:
                rt = review_title[j].text
            except:
                rt="review is not available"
            mydict = {"Product": product_name, "Product_url": product_url, "CustomerName": cn, "Rating": rs, "Review": rt, "Comment": rd}
            reviews.append(mydict)
    return render_template("results.html", reviews=reviews)


if __name__ == "__main__":
    app.run()
