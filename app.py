from flask import Flask, request
from flasgger import Swagger
from libversion.version_util import VersionUtil
app = Flask(__name__)
swagger = Swagger(app)

@app.route("/version", methods=["GET"])
def get_lib_version():
	"""
	Gets the version from the lib-version package.
	---
	responses:
		200:
			description: Version (v#.#.#) from lib-version.
		500:
			description: Version could not be retrieved.
	"""
	try:
		return VersionUtil.get_version()
	except Exception as e:
		print(e)
		return "Version not found", 500

app.run(host="0.0.0.0", port=8080)
