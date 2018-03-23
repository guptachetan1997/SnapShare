import numpy as np
import base64
import sys

def base64_encode_image(image):
	return base64.b64encode(image).decode("utf-8")

def base64_decode_image(a, dtype, shape):
	a = bytes(a, encoding="utf-8")
	a = np.frombuffer(base64.decodestring(a), dtype=dtype)
	a = a.reshape(shape)
	return a