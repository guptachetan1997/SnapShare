from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from flask import Flask, request, jsonify
from PIL import Image
import redis
import numpy as np
import io
import uuid
import json
import settings
import time
import helpers

app = Flask(__name__)
db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def preprocess_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")
	image = image.resize(target_size)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)
	return image

@app.route("/")
def homepage():
	return "Hello World"


@app.route("/tag", methods=["POST"])
def get_tags():
	data = { "success" : False }
	if request.method == "POST":
		if request.files.get("image"):
			image = request.files["image"].read()
			image = Image.open(io.BytesIO(image))
			image = preprocess_image(image, (settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT))
			image = image.copy(order="C")

			image_id = str(uuid.uuid4())
			image = helpers.base64_encode_image(image)
			image_dict = {
				"id" : image_id,
				"image" : image	}
			db.rpush(settings.IMAGE_QUEUE, json.dumps(image_dict))

			while True:
				output = db.get(image_id)

				if output is not None:
					output = output.decode("utf-8")
					data["tags"] = json.loads(output)
					db.delete(image_id)
					break
				time.sleep(settings.CLIENT_SLEEP)
			data["success"] = True
	return jsonify(data)


if __name__ == '__main__':
	print("Starting model server.")
	app.run()