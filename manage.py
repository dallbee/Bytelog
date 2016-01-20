from flask.ext.script import Manager, Shell, prompt_bool
from flask.ext.assets import ManageAssets
from service import create_app
#from subprocess import Popen, call

"Main python process which allows database creation/modification and executes flask server"


app = create_app()

manager = Manager(app)
manager.add_command("assets", ManageAssets(app))


if __name__ == '__main__':
    manager.run()