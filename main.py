from app import create_app

app = create_app()

if __name__ == '__main__':
    #We're running the server locally. Debug=True mode means
    #  the server will restart itself if you change anything in the code!
    app.run(debug=True)