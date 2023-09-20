from website import create_app
#so whenever we import create_app, it will run it from __init__.py

app = create_app()

if __name__ == '__main__': #only if we run not file it will be execute, not import
    app.run(debug=True)