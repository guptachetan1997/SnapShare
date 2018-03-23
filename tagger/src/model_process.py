from keras.applications import VGG16, imagenet_utils
import numpy as np
import settings
import helpers
import time
import json
import redis

db = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def tag_process():
	print("* Loading model .....")
	model = VGG16(weights="imagenet")
	print("* Model loaded")

	while True:
		queue = db.lrange(settings.IMAGE_QUEUE, 0, settings.BATCH_SIZE -1)
		imageIDs = []
		batch = None
		for q in queue:
			q = json.loads(q.decode("utf-8"))
			image = helpers.base64_decode_image(q["image"], settings.IMAGE_DTYPE, (1, settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH, settings.IMAGE_CHANS))

			if batch is None:
				batch = image
			else:
				batch = np.vstack([batch, image])
			
			imageIDs.append(q["id"])
		
		if len(imageIDs) > 0:
			print("* Batch size : {}".format(batch.shape))
			preds = model.predict(batch)
			results = imagenet_utils.decode_predictions(preds, top=settings.VGG_TOP_CLASSES)

			for (imageID, resultSet) in zip(imageIDs, results):
				tags = []
				for (_, label, prob) in resultSet:
					tags.append(label)
			
				db.set(imageID, json.dumps(tags))
			
			db.ltrim(settings.IMAGE_QUEUE, len(imageIDs), -1)
		
		time.sleep(settings.SERVER_SLEEP)


if __name__ == '__main__':
	tag_process()