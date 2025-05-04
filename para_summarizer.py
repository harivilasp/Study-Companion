from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
import numpy as np
import networkx as nx

#2. Generate clean sentences
def read_article(filedata):
    article = filedata.split(". ")
    sentences = []
    for sentence in article:
        clean = sentence.replace("[^a-zA-Z]", " ").split(" ")
        if len([w for w in clean if w.strip()]) > 2:  # Only add if not empty
            sentences.append(clean)
    if sentences:
        sentences = [s for s in sentences if any(w.strip() for w in s)]
    return sentences

#3. Similarity matrix
def sentence_similarity(sent1, sent2, stopwords=None):    
    if stopwords is None:
        stopwords = []     
    sent1 = [w.lower() for w in sent1]    
    sent2 = [w.lower() for w in sent2]     
    all_words = list(set(sent1 + sent2))    
    vector1 = [0] * len(all_words)    
    vector2 = [0] * len(all_words)     
    # build the vector for the first sentence   
    for w in sent1:       
        if w in stopwords:            
            continue        
        vector1[all_words.index(w)] += 1     
    # build the vector for the second sentence    
    for w in sent2:        
        if w in stopwords:           
            continue        
        vector2[all_words.index(w)] += 1     
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

#4. Generate Summary Method
def generate_summary(file_name, top_n=1):
    stop_words = stopwords.words('english')
    summarize_text = []
    # Step 1 - Read text and tokenize
    sentences = read_article(file_name)
    if not sentences or len(sentences) < 2:
        return ["Input text is too short for summarization. Please provide a longer or more detailed input."]
    # Step 2 - Generate Similarity Matrix across sentences
    try:
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
        # Step 3 - Rank sentences in similarity matrix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)
        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
        for i in range(min(top_n, len(ranked_sentence))):
            summarize_text.append(" ".join(ranked_sentence[i][1]))
        return summarize_text
    except Exception as e:
        return [f"Summarization failed: {str(e)}"]

