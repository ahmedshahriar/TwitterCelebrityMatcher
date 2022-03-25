import numpy as np
from sentence_transformers import SentenceTransformer, util

sentences = ["This is an example sentence", "Each sentence is converted"]

model_path = "../models"

# download and save model
# model = SentenceTransformer('sentence-transformers/average_word_embeddings_komninos')

# model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
# model.save(model_path)

# load model offline
model = SentenceTransformer(model_path, device='cuda')
embeddings = model.encode(sentences)

# Sentences are encoded by calling model.encode()
emb1 = model.encode("This is a red cat with a hat.")
emb2 = model.encode("Have you seen my red cat?")

cos_sim = util.cos_sim(emb1, emb2)
print("Cosine-Similarity:", np.squeeze(cos_sim.numpy()))

# Two lists of sentences
sentences1 = ['The cat sits outside',
              'A man is playing guitar',
              'The new movie is awesome']
#
sentences2 = ['The dog plays in the garden',
              'A woman watches TV',
              'The new movie is so great']

# #Compute embedding for both lists
embeddings1 = model.encode(sentences1, convert_to_tensor=True)

embeddings2 = model.encode(sentences2, convert_to_tensor=True)

# #Compute cosine-similarits
cosine_scores = util.cos_sim(embeddings1, embeddings2)

# Output the pairs with their score
for i in range(len(sentences1)):
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
