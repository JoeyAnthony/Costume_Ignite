# system
import os
from flask_server import app

# Initialisation
import backend

# initialise tests
from tests import RunAllTests
#RunAllTests()


from tests import quick_cosplay_led_test as qt
qt.endless_test()

# Initialise flask_server
# app.run(host='0.0.0.0', port='5000', debug=True)
if __name__ == "__main__":
    print("run main")
    app.run(host='0.0.0.0', port='5000', debug=False)


