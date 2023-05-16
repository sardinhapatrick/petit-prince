from prince import app

if __name__=='__main__':
    # app.config["APPLICATION_ROOT"] = "/projet_19-20/petit_prince"
    app.config["APPLICATION_ROOT"] = "/"
    app.run(debug=True)
