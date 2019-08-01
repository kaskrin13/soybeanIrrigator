from flask import Flask
from flask import render_template 
import evapotranspiration as et
 
app = Flask(__name__)
 
hourlyTableData = []
chart = []

@app.route("/")
def index():
    tableData = et.Threader(et.HourlyData, et.hourlyHtmlUrls)
    for item in tableData:
        hourlyTableData.append(item)
    locations = [x[1:] for x in et.dailyHtmlUrls]
    return render_template("index.html", locationInfo=locations, tableData=tableData)

@app.route("/station<index>")
def detailed(index):
    # Uncomment to test render_template output for errors and unexpected results
    #output = render_template("detailed.html", fields=detailed)
    #with open("test.html", "w") as f:
    #    f.write(output)
    index = int(index)
    chart = et.DailyChart(et.dailyHtmlUrls[index])
    legend = [["Temperature", "Degrees"], ["Rainfall", "Inches"], ["Humidity", "Percent"], ["Evapotranspiration", "Inches"]]
    return render_template("detailed.html", coords=[et.dailyHtmlUrls[index][1],et.dailyHtmlUrls[index][2]], 
            hourlyData=hourlyTableData[index], dailyData=chart, legend=legend, labels=chart[1])
 
 
if __name__ == "__main__":
    app.run(debug=True)