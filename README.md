## Intentless Rasa

This project implements something similar to rasa pro's intentless fallback policy, as described in a press release from February [0] and this very recent documentation [1]. If I understand the feature described in [0] and [1] properly, they allow a user to upload a csv of Question and Answer pairs, which is then somehow used to answer questions without adding any new intents or their training utterances to the `nlu.yml`. How exactly this is performed is not described in that post, so we use our imagination. But a sequence2sequence cosine similarity solution is a pretty reasonable bet.

So all I did here was configure rasa to use a fallback intent, and that fallback intent itself triggers a rasa action server, and that action server calls another endpoint (the `util` image) that hosts a simple spacy vector 'database' full of vectorized FAQs. When you talk to rasa, you can tell it 'hello' or 'goodbye' and it will respond appropriately. But if you ask it anything about mental health: the confidence score for intent prediction will be below our threshold. The fallback intent will kick in and call the action server, and the action server will call the `util` image. The `util` image will vectorize the unrecognized user input, compare it to a pre-vectorized set of question embeddings, and return the answer associated with the most similar question.

This simple baseline is just using spacy's nlp object to embed FAQs as well as user input. I think this is down to spacy's limitations, but this design choice means that we currently have to store everything in memory. Perhaps if I used FAISS it would be possible to store this stuff on the disk, more persistently.

[0] https://rasa.com/blog/breaking-free-from-intents-a-new-dialogue-model/ <br>
[1] https://rasa.com/docs/rasa/next/llms/llm-intentless/

### Training the rasa model

```
$> sudo apt install python3-venv
$> python3.10 -m venv ~/.venv/rasa
$> source ~/.venv/rasa/bin/activate
(rasa) $> python -m pip install --upgrade pip
(rasa) $> pip install -r rasa/requirements.txt
(rasa) $> cd rasa/training/
(rasa) $> rasa train --domain domain/faq_domain_intentless.yml --config config_intentless.yml --data data --fixed-model-name=wellness-bot
(rasa) $> deactivate
$> cd ../../
```

### Mental Health FAQ data

There's a csv with 98 mental health FAQs in it, in the `util/ai/data/` subdirectory [2]. If you open it, you'll notice that it has 'Question' and 'Answer' columns. You can add more csvs to this directory, and if they contain 'Question' and 'Answer' columns, they will get included and added to the vectorized collection of FAQs when you run `docker-compose`.

[2] https://www.kaggle.com/discussions/general/188285

### Building the docker containers

```
$> docker-compose up --build -d
```

### Interacting with the bot

API endpoint (POST):
`http://127.0.0.1:5000/rasa_nlu`

Parameters:

In Postman/Insomnia, go to 'Body' > 'form-data'
```
Key: text
Value: "What causes mental illness?"
```