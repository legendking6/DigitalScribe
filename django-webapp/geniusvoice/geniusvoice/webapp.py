from django.shortcuts import render
import os, io
from google.cloud import vision_v1
import pandas as pd


def button(request):

    return render(request,'geniusvoice.html')

def output(request):
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/Users/priyapatel/Desktop/env/ServiceAccountToken.json"

	client = vision_v1.ImageAnnotatorClient()

	file_name = 'pic1.jpeg'
	folder_path = r'/Users/priyapatel/Desktop/env/Images'


	with io.open(os.path.join(folder_path, file_name), 'rb') as image_file:
	    content = image_file.read()

	# construct an iamge instance
	image = vision_v1.types.Image(content=content)

	"""
	# or we can pass the image url
	image = vision.types.Image()
	image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
	"""

	# annotate Image Response
	response = client.text_detection(image=image)  # returns TextAnnotation
	df = pd.DataFrame(columns=['locale', 'description'])

	texts = response.text_annotations
	for text in texts:
	    df = df.append(
	        dict(
	            locale=text.locale,
	            description=text.description
	        ),
	        ignore_index=True
	    )
	#print("\n")
	output_data = (df['description'][0])
	    #output_data = "Genius Voice eliminates friction. For years people have had to learn to interact with computers, we turn this around. We teach computers how to interact with humans through voice. This creates a seamless experience without losing the human touch."
	    
	return render(request,"geniusvoice.html",{"output_data":output_data})
	    
