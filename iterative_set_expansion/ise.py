import spacy
from spanbert import SpanBERT

import spacy_help_functions as shf

def get_entities_of_interest(r):
    if(r==1):
        return ["PERSON", "ORGANIZATION"]
    if(r==2):
        return ["PERSON", "ORGANIZATION"]
    if(r==3):
        return ["PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
    if(r==4):
        return ["ORGANIZATION", "PERSON"]

def relation_type(r):
    if (r == 1):
        return {"Subject": ["PERSON"], "Object": ["ORGANIZATION"]}
    if (r == 2):
        return {"Subject": ["PERSON"], "Object": ["ORGANIZATION"]}
    if (r == 3):
        return {"Subject": ["PERSON"], "Object": ["LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]}
    if (r == 4):
        return {"Subject": ["ORGANIZATION"], "Object": ["PERSON"]}

def process(results, r):
    # TODO: filter entities of interest based on target relation
    entities_of_interest = get_entities_of_interest(r)
    relation = relation_type(r)

    # Load spacy model
    nlp = spacy.load("en_core_web_lg")  

    # Load pre-trained SpanBERT model
    spanbert = SpanBERT("./pretrained_spanbert")

    for result in results:
        doc = nlp(result["content"])
        for sentence in doc.sents:
            print("\n\nProcessing entence: {}".format(sentence))
            print("Tokenized sentence: {}".format([token.text for token in sentence]))
            ents = shf.get_entities(sentence, entities_of_interest)
            print("spaCy extracted entities: {}".format(ents))
            
            # create entity pairs
            candidate_pairs = []
            sentence_entity_pairs = shf.create_entity_pairs(sentence, entities_of_interest)
            for ep in sentence_entity_pairs:
                # TODO: keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
                if(ep[1][2] in relation['Subject'] and ep[2][2] in relation['Object']):
                    candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
                if(ep[2][2] in relation['Subject'] and ep[1][2] in relation['Object']):
                    candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject
            

            # Classify Relations for all Candidate Entity Pairs using SpanBERT
            #candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]  # ignore subject entities with date/location type

            print("Candidate entity pairs:")
            for p in candidate_pairs:
                print("Subject: {}\tObject: {}".format(p["subj"][0:2], p["obj"][0:2]))
            print("Applying SpanBERT for each of the {} candidate pairs. This should take some time...".format(len(candidate_pairs)))

            if len(candidate_pairs) == 0:
                continue

            predict = spanbert.predict(candidate_pairs)
            print(predict)

