from app import app,db

with app.app_context(): # Creates all the database tables defined in the SQLAlchemy models. This is a one-time operation usually done during application initialization.
    db.create_all()




if __name__ == '__main__':
    app.run(debug=True) #Starts the Flask development server. The debug=True argument enables the development mode, providing more detailed error messages and auto-restarting the server on code changes.