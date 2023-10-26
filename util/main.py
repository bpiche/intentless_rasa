"""
"""
import os
from ai import similarity
from dotenv import load_dotenv
from flask import Flask, request


app = Flask(__name__)
load_dotenv = ('.env')


similarity_df = similarity.vectorize_faqs('csv', './ai/data')


@app.route('/similarity', methods=['POST'])
def get_similarity():
    """
    """
    query = request.get_json('text').get('text')
    app.logger.info(f'input: {query}')
    response = similarity.compare_faqs(query, similarity_df)
    app.logger.info(f'intentless response: {response}')
    return response


@app.route('/livez', methods=['GET'])
def live():
    return "Live", 200


if __name__ == "__main__":
    """
    """
    print('Running the server on port 5006')
    sslctx = 'adhoc' if (os.environ.get('SERVE_HTTPS') 
                         in ['true', 'True', 'TRUE', True]
                     ) else None;
    app.run(host='0.0.0.0', port=5006, debug=True, ssl_context=sslctx)
    