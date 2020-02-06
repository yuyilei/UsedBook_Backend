from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from usedBook import db, app
from usedBook.models import User, Book, Comment

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
        Book = Book,
        Comment = Comment
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
