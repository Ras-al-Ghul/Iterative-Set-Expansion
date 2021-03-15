import os
import spacy
from spanbert import SpanBERT

import spacy_help_functions as shf

def get_entities_of_interest(r):
    if(r==1):
        return ['PERSON', 'ORGANIZATION']
    if(r==2):
        return ['PERSON', 'ORGANIZATION']
    if(r==3):
        return ['PERSON', 'LOCATION', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY']
    if(r==4):
        return ['ORGANIZATION', 'PERSON']

def relation_type(r):
    if (r == 1):
        return {"Type": ["per:schools_attended"], "Subject": ['PERSON'], "Object": ['ORGANIZATION']}
    if (r == 2):
        return {"Type": ["per:employee_of"], "Subject": ['PERSON'], "Object": ['ORGANIZATION']}
    if (r == 3):
        return {#"Type": ["per:countries_of_residence", "per:cities_of_residence", "per:stateorprovinces_of_residence"],
            "Type": ["per:cities_of_residence"],
                "Subject": ['PERSON'], "Object": ['LOCATION', 'CITY', 'STATE_OR_PROVINCE', 'COUNTRY']}
    if (r == 4):
        return {"Type": ["org:top_members/employees"], "Subject": ['ORGANIZATION'], "Object": ['PERSON']}

def print_data(sentence, value, t):
    print('========Extracted Relation============')
    print("Sentence :", sentence)
    print("Confidence:", value['Confidence'], 'Subject:', value['Subject'], 'Object:', value['Object'])
    if(value['Confidence'] >= t):
        print("Adding to set of extracted relations")
    else:
        print("Confidence is lower than threshold confidence. Ignoring this.")
    print("=================")

def process(results, r, t):
    # TODO: filter entities of interest based on target relation
    entities_of_interest = get_entities_of_interest(r)
    relation = relation_type(r)

    # Load spacy model
    nlp = spacy.load("en_core_web_lg")  

    # Load pre-trained SpanBERT model
    spanbert = SpanBERT("{}/pretrained_spanbert".format(os.path.abspath(__file__)[:-7]))
    bert_result = []

    for idx in range(0, len(results)):
        result = results[idx]
        print('url (', idx, '/10)', result['url'])
        doc = nlp(result["content"])

        sentence_count = 0
        for sentence in doc.sents:
            #print("\n\nProcessing sentence: {}".format(sentence))
            #print("Tokenized sentence: {}".format([token.text for token in sentence]))
            ents = shf.get_entities(sentence, entities_of_interest)
            #print("spaCy extracted entities: {}".format(ents))
            
            # create entity pairs
            candidate_pairs = []
            sentence_entity_pairs = shf.create_entity_pairs(sentence, entities_of_interest)
            for ep in sentence_entity_pairs:
                if ep[1][1] in relation['Subject'] and ep[2][1] in relation['Object']:
                    candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
                if ep[2][1] in relation['Subject'] and ep[1][1] in relation['Object']:
                    candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject


            #print("Candidate entity pairs:")
            #for p in candidate_pairs:
            #    print("Subject: {}\tObject: {}".format(p["subj"][0:2], p["obj"][0:2]))
            #print("Applying SpanBERT for each of the {} candidate pairs. This should take some time...".format(len(candidate_pairs)))

            if len(candidate_pairs) == 0:
                continue

            predict = spanbert.predict(candidate_pairs)
            #print(predict)
            for i in range(0, len(candidate_pairs)):
                if predict[i][0] in relation['Type']:
                    value = {
                            'Subject': candidate_pairs[i]['subj'][0],
                            'Object': candidate_pairs[i]['obj'][0],
                            'Relation': predict[i][0],
                            'Confidence': predict[i][1]}
                    print_data(sentence.text, value, t)
                    if value['Confidence'] >= t:
                        bert_result.append(value)

            sentence_count += 1
            if sentence_count%5 == 0:
                print("Processed", sentence_count," sentences")

    return bert_result
