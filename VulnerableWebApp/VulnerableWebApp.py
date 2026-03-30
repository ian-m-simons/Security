from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/")
def index():
    val = request.args.get("address", "")
    if val:
        sol = expand(val)
    else:
        sol= ""
    return( 
        """<form action="" method="get">
                <input type="text" name="address" />
                <input type="submit" value="expand" />
            </form>"""
        + sol
    )
#@app.route("/<address>")
def expand(address):
    addressArray = address.split(":")
    if len(addressArray) < 8:
        quartetsToAdd = ""
        for i in range(9-len(addressArray)):
            quartetsToAdd = quartetsToAdd + "0000:"
        quartetsToAdd = ":" + quartetsToAdd
        addressHalfs = address.split("::")
        newAddress = addressHalfs[0] + quartetsToAdd + addressHalfs[1]
        addressArray = newAddress.split(":")
    for i in range(len(addressArray)):
        while (len(addressArray[i])<4):
            addressArray[i] = "0" + addressArray[i]
    finalAddress = addressArray[0]
    for i in range(1,len(addressArray)):
        finalAddress = finalAddress + ":" + addressArray[i]
    return finalAddress

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
