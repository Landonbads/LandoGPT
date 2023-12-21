# import create_app function from website folder
from website import create_app

app = create_app()

# limits running to only this file
if __name__ == '__main__':
    app.run(debug=True)