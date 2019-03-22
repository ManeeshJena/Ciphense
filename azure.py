import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
#import matplotlib.pyplot as plt
#from PIL import Image
#from io import BytesIO
import json
from gtts import gTTS
import os

subscription_key = "2862a4f80edd4424afb54b2df875c446"
assert subscription_key


vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

analyze_url = vision_base_url + "analyze"


image_path = input("Enter the image path\n")


image_data = open(image_path, "rb").read()
headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}


params     = {'visualFeatures': 'Categories,Description,Color,ImageType,Objects,Tags,Adult,Brands,Faces'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()


analysis = json.loads(json.dumps(response.json()))
print(analysis)
print()

s = ""
cat = ""
l=analysis["description"]["tags"]
k=analysis["categories"]
for i in l:
	s = s + i +", "


res = 0;
maxdic = {};

for stri in k:
	if res<float(stri["score"]):
		res=float(stri["score"])
		maxdic = stri



ans=""
ans=ans+"The category is "+maxdic['name']+"\n"

if 'detail' in maxdic:
	#print("yes")
	if 'celebrities' in maxdic['detail']:
		#print("yes")
		ll=""
		for l in maxdic['detail']['celebrities']:
			ll = ll + l['name']+" "	
		ans=ans+"The celebs are "+ll+"\n"

	if 'landmarks' in maxdic['detail']:
		#print("yes")
		ll=""
		for l in maxdic['detail']['landmarks']:
			ll = ll + l['name']+" "	
		ans=ans+"The landmarks are "+maxdic['landmarks']+"\n"

if analysis['adult']['isAdultContent']:
	ans = ans+"Adult content present\n"
else:
	ans = ans+"Adult content absent\n"

if analysis['adult']['isRacyContent']:
	ans = ans+"Racy content present\n"
else:
	ans = ans+"Racy content absent\n"

ans = ans  + "The foreground color is "+ analysis['color']['dominantColorForeground']+"\n"
ans = ans  + "The background color is "+ analysis['color']['dominantColorBackground']+"\n"

if analysis['color']['isBWImg']:
	ans = ans+"black and white image\n"
else:
	ans = ans+"Color Image\n"

ans = ans+"Tags are "+ s+"\n"

ans = ans+"Description of the image is "+analysis['description']['captions'][0]['text']+"\n"

ctr = 0+1

for i in analysis['faces']:
	ans = ans + "object "+ str(ctr)+" age is "+str(i['age'])+" , gender is "+i['gender']+"\n"
	ctr=ctr+1
ans=ans+"height of image is "+ str(analysis['metadata']['height'])+",the width of image is "+str(analysis['metadata']['width'])+",the format is "+analysis['metadata']['format']+"\n"

pm=input("Enter the file path where text is to be stored\n")
file = open(pm+"ans.txt","w")
file.write(ans)
file.close()


  

language = 'en'
  

myobj = gTTS(text=ans, lang=language, slow=False) 
  

fg=input("Enter the file path where speech is to be stored\n")
myobj.save(fg+"speech.mp3") 
   

print(ans)



