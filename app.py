from flask import Flask,render_template,request,make_response,session
import numpy as np
import base64
from io import BytesIO
from matplotlib.figure import Figure
from ln import ln
from scipy.interpolate import make_interp_spline
import math
app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html')
@app.route("/predict",methods = ["POST","GET"])
def ln_():
    global forward
    global backward
    forward = int(request.form['forward'])
    backward = int(request.form['backward'])
    x_val = float(request.form['x-value'])
    y_val = float(request.form['y-value'])
    # New x and y array with forecasted val
    x_new = sorted(ln(forward, backward)[0])
    y_new = sorted(ln(forward, backward)[1])
    a = round(ln(forward, backward)[2],4)
    b = round(ln(forward, backward)[3],4)


    # find y based on x
    # since y = a * ln(x) + b
    y_predicted = round(a * np.log(x_val) + b, 2)
    # predict x based on y
    # since y = a * ln(x) + b x = e^((y-b)/a)
    #formula

    x_pred = math.exp((y_val - b) / a)
    return render_template('predicted.html', x_new=x_new,y_new=y_new,
                           a=a,
                           b=b, x_pred=x_pred,y_pred=y_predicted)
@app.route("/plot",methods = ["POST","GET"])
def plot():
    x = sorted(ln(forward, backward)[0])
    y = sorted(ln(forward, backward)[1])
    print(x)
    print(y)
    fig = Figure()
    ax = fig.subplots()
    ax.scatter(x, y)
    z = np.array(x)
    z = sorted(z.flatten())
    if len(x) > 2 :
        x_new = np.linspace(min(z), max(z), 10)
        a_BSpline = make_interp_spline(z, y, k=2)
        y_new = a_BSpline(x_new)
        ax.grid(True)
        ax.set_title("Water consumption")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        print(x_new)
        print(y_new)
        ax.plot(x_new, y_new)
        buf = BytesIO()
        fig.savefig(buf, format="png")
    else:
        ax.grid(True)
        ax.set_title("Water consumption")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.plot(x, y)
        buf = BytesIO()
        fig.savefig(buf, format="png")


    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"



if __name__ == "__main__":
    app.run(debug=True)