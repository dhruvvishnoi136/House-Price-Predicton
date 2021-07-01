from flask import Flask , render_template , url_for , request
from werkzeug.utils import redirect
from Main.Algo import Algos
app = Flask(__name__)

@app.route("/" , methods = ["GET" , "POST"])
@app.route("/home" , methods = ["GET" , "POST"])
def home():
    if request.method == "POST":
        if request.form["action"] =="Calculator":
            return redirect(url_for('calculator'))
        else:
            return render_template("home.html")
    elif request.method == "GET":
        return render_template("home.html")


@app.route("/calculator" , methods = ["GET" , "POST"])
def calculator():
    pridiction = ""
    if request.method == "POST":
        if request.form['action'] == "Calculate Price":
            areatype= int(request.form['areatype'])
            bedroom  = int(request.form['bedroom'])
            bath = int(request.form['bath'])
            availlability = int(request.form['availlability'])
            pincode = int(request.form['pincode'])
            sqft = int(request.form['total_sqft'])
            society = int(request.form['society'])
            obj1 = Algos(area_type = areatype,availability = availlability , sqft=sqft,location = pincode,size =bedroom ,society = society,bath = bath)
            pps = int(obj1.knn_predict())
            obj = Algos(area_type = areatype,availability = availlability,location = pincode,size =bedroom  , pps=pps,society = society,bath = bath)
            pridiction = obj.random_predict()
            return render_template("Result.html" ,pridiction = pridiction)
        elif request.form["action"] =="Calculator With Price per Square Feet":
            return redirect(url_for('calculator_pps' , ))
        else:
            return render_template("calculator.html")

    else:
        return render_template("calculator.html")

@app.route("/calculator_pps" , methods = ["GET" , "POST"])
def calculator_pps(areatype , bedroom, bath, availlability , pincode , society, sqft):
    pridiction = ""
    if request.method == "POST":
        if request.form['Calculate Price']:
            # areatype= int(request.form['areatype'])
            # bedroom  = int(request.form['bedroom'])
            # bath = int(request.form['bath'])
            # availlability = int(request.form['availlability'])
            # pincode = int(request.form['pincode'])
            # society = int(request.form['society'])
            # sqft = int(request.form['total_sqft'])
            pps = int(request.form['pps'])
            obj = Algos(area_type = areatype,availability = availlability,location = pincode,size =bedroom ,society = society,sqft= sqft,bath = bath,pps= pps)
            pridiction = obj.random_predict()
            return render_template("Result.html" , pridiction = pridiction)
        else:
            render_template("Result.html" , pridiction = pridiction)
    elif request.method == "GET":
        return render_template("calculator_pps.html" , pridiction = pridiction)

@app.route("/Result" , methods =["GET" , "POST"] )
def Result(pridiction):
    return render_template("Result.html" , pridiction)

if __name__ == "__main__":
    app.run(debug=True)