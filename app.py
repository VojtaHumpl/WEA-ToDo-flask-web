from app import create_app

"""
app startup
"""

app = create_app()

if __name__ == "__main__":
    app.run()