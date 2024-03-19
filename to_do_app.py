from app import app, db
from app.models import User, ToDo

# Funktion definieren, um Kontext für das Python-Shell-Environment bereitzustellen
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'ToDo': ToDo}
