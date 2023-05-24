import os
import json

from pathlib import Path
from flask import Flask, send_file, request

app = Flask(__name__)

# old_image_dir = Path('/data/radiology_datas/agss-train/penet/images').resolve(strict=True)
# image_dir = Path('/home/macky/workspace/agss-1/data/penet/images').resolve(strict=True)
image_dir = Path('/data2/radiology_datas/agss/penet/images_jpg').resolve(strict=True)
# old_label_dir = Path('/home/macky/workspace/agss-1/data/penet/labels').resolve(strict=True)
# label_dir = Path('/home/macky/workspace/agss-1/data/penet/labels').resolve(strict=True)
old_label_dir = Path('/data2/radiology_datas/agss/penet/labels').resolve(strict=True)
label_dir = Path('/data2/radiology_datas/agss/penet/labels').resolve(strict=True)

image_ids = [os.path.splitext(os.path.basename(f))[0] for f in list(image_dir.glob("*.jpg"))]
# old_image_ids = [os.path.splitext(os.path.basename(f)) for f in list(old_image_dir.glob("*.jpg"))]

id2fn = dict()
fn2id = dict()

for i in range(len(image_ids)):
    id2fn[str(i).zfill(4)] = str(image_ids[i])
    fn2id[image_ids[i]] = str(i).zfill(4)

@app.get('/')
def root():
    return send_file('index.html')

@app.get('/images/<image_id>.jpg')
def image(image_id):
    image_id = id2fn[image_id]
    return send_file(image_dir / f'{image_id}.jpg')

@app.get('/old_labels/<image_id>.json')
def get_old_json(image_id):
    image_id = id2fn[image_id]
    return send_file(old_label_dir / f'{image_id}.json')

@app.get('/labels/<image_id>.json')
def get_json(image_id):
    image_id = id2fn[image_id]
    return send_file(label_dir / f'{image_id}.json')

@app.post('/labels/<image_id>.json')
def post_json(image_id):
    image_id = id2fn[image_id]
    json_path = label_dir / f'{image_id}.json'
    json_path.write_text(json.dumps(request.json, indent=4))
    return f'\"writing to {json_path}\"'

app.run(host='0.0.0.0', threaded=True)