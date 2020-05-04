import os
import requests
import json
from flask import Flask, request, jsonify
from google.cloud import vision
from nlp_helper import sent_tokenize, _create_dictionary_table, _calculate_sentence_scores, _calculate_average_score, _get_article_summary

TOKEN = os.environ["TOKEN"]
URL = "https://vision.googleapis.com/v1/images:annotate?key={}".format(TOKEN)


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

# receivce: {"content": "..."}
# response: {"labels":["..."]}
@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        image_base_content = request.json['content']
        print("\n/test received image, processing...")
        vision_result = get_vision_result(image_base_content)
        # paring response, error handling to be added
        items = json.loads(vision_result)["responses"][0]["textAnnotations"]
        response = [item["description"] for item in items]
        max_content = max(response, key=len)
        max_content = max_content.split('\n')
        max_content = ' '.join(max_content)
        print("max_content: ", max_content)
        # labels: [l1, l2, l3, l4]
    return jsonify(labels=[max_content])

# receive: {"raw_text":"...."}
# response: {""}
@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        print("/summary received raw text, summarizing...")
        article_content = request.json['raw_text']
        sentences = sent_tokenize(article_content)
        frequency_table = _create_dictionary_table(article_content)
        sentence_scores = _calculate_sentence_scores(sentences, frequency_table)
        threshold = _calculate_average_score(sentence_scores)
        article_summary = _get_article_summary(sentences, sentence_scores, 1.1 * threshold)
        summary_text=article_summary
        print("summary_text: ", summary_text)
    return jsonify(summary_text=summary_text)

# helper function
def get_vision_result(image_base_content):
    data = {
      "requests": [
        {
          "image": {
            "content": image_base_content # "base64-encoded-image"
          },
          "features": [
            {
              "maxResults": 5,
              "type": "DOCUMENT_TEXT_DETECTION" # "LABEL_DETECTION"
            }
          ]
        }
      ]
    }
    r = requests.post(URL, json=data)
    return r.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
