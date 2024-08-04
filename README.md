# Embeddings & Vector Search

With Python, HuggingFace and MongoDB Atlas.

## Running app manually

` flask run --host=0.0.0.0 --port=9050`

## What is going on ?

**Requirements, dreams & desires**: I am at the stage of building my MSC Advanced Computing
project. It is distributed app for education with some whistles, fountains and 
pretty flowers (but not really). I wanted to create Question/Post suggesting
system. I could build that bases on Question/Post (Q/P) tags, but that isn't very 
accurate, modern and hot. I wanted to use my (still poor) existing NLP skills
and use something much modern that SQL query to find Questions/Posts by tags. 

**Solution (?)** : Well ... I ended up (by now) with an attempt of using word embeddings
and vector search to find related Q/P. 

**How it works (or how it should work)**: On the UI side of adding a Q/P, when
one is being added the user has to type Q/P title (summary) and then he
goes to the body of the question. The Q/P title is being sent (in the background)
to this API here to the `'/embedding/search` endpoint. This endpoint creates
the Q/P title embedding and searches for similar ones in the MongoDB created for 
this purpose. 

Other possibilities:
- Q/P title can be sent to the `/embedding` endpoint just to get the embeddings
- Q/P can be sent to `/embedding/mongostore` endpoint to store it's embedding in MongoDB

## MongoDB Atlas Index

Index Name: QuestionSematicSearchIndex

Pick the correct db and collection and set the index JSON as below:

`{
  "mappings": {
    "dynamic": true,
    "fields": {
      "question_embedding": {
        "dimensions": 384,
        "similarity": "dotProduct",
        "type": "knnVector"
      }
    }
  }
}`

## Environment Variables & Settings

Create `.env` file. This file will hold all environment variables required 
for `docker-compose.yml` file.

It should contain below variables:

```
# Env variables for docker-compose
HF_TOKEN= 
API_TOKEN=
MONDO_CONN_STRING=
SEARCH_LIMITS_COUNT=
```

- `HF_TOKEN` - HuggingFace token (I got one but free version allow to make few FREE embeddings)
- `API_TOKEN` - token to secure api. One is set when running the Docker container based on the image.
  Create your own and set and docker image env.var or env var in your system if you're running 
  app manually. Example: `export API_TOKEN=hf_myHaPpYToKeNgOesHeRe` or `set API_TOKEN=hf_myHaPpYToKeNgOesHeRe`
  Same should be done for `HF_TOKEN`. 
- `SEARCH_LIMITS_COUNT` - how many MongDB records should be displayed in '/embedding/search' results'


When making the API request , set header `x-access-tokens` to match your
`API_TOKEN`. 

## How to run it ?

1. Add your values in `.env` file . For Hugging Face token, make a free account, go
to Your Profile -> Settings -> Access Tokens -> New Token
2. MongoDB Atlas connection string - Create free MongoDB Atlas account. Create Cluster. 
Create Database. Click Connect and copy connection string. 
3. For API_TOKEN - create any password you want, but use the same in you
API request headers as mentioned above.
4. Run command `docker compose up -d` (you must have Docker and Compose in your system)
