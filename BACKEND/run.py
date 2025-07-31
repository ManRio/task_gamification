from flask import Flask
from flask_migrate import Migrate
from app import db, create_app, models

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)

# Esto asegura que los modelos se importen cuando se use Flask CLI
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "models": models}