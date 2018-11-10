import mainapp


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application = main.create_app()
    application.debug = True
    application.run()