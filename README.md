## Intentless Rasa

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

There's a csv with 98 mental health FAQs in it, in the `util/ai/data/` subdirectory [0]. If you open it, you'll notice that it has 'Question' and 'Answer' columns. You can add more csvs to this directory, and if they contain 'Question' and 'Answer' columns, they will get included and added to the vectorized collection of FAQs when you run `docker-compose`.

[0] https://www.kaggle.com/discussions/general/188285

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