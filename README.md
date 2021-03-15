# Iterative-Set-Expansion
An implementation using BERT to iteratively find the tuples of a given relation.
## Files
<ol>
<li>iterative_set_expansion
  <ul>
    <li>__init__.py</li>
    <li>__main__.py</li>
    <li>config.py</li>
    <li>download_finetuned.sh</li>
    <li>example_relations.py</li>
    <li>search_scrape.py</li>
    <li>ise.py</li>
    <li>realtions.txt</li>
    <li>requirements.txt</li>
    <li>search_scrape.py</li>
    <li>spacy_help_functions.py</li>
    <li>spanbert.py</li>
    <li>pytorch_pretrained_bert</li>
      <ul>
        <li>__init.py__</li>
        <li>file_utils.py</li>
        <li>modeling.py</li>
        <li>optimization.py</li>
        <li>tokenization.py</li>
      </ul>
  </ul>
</li>
<li>README.md</li>
<li>.gitignore</li>
</ol>

## Steps to install and run

<p> Install the requirements from requirements.txt present in iterative_set_expansion using the below command.</p>

```
 pip3 install -r requirements.txt
```

<p>Run the program using the following command.</p>

```
python3 iterative_set_expansion <r> <t> <q> <k>

r - int with values 1,2,3,4. where 1 is Schools_Attended, 2 - Work_For, 3 - Live_In, 4- Top_Member_Emloyee  
t - float between 0 and 1 indicating extraction confidence threshold
q - string seed query of plausible tuple
k - int greater than 0 indicating number of tuples wanted

For example,

python3 iterative_set_expansion 4 0.7 "bill gates microsoft" 10
```

## Design

<ol>
<li>search_scrape.py :
   <ul>
    <li>Sends a Google query.</li> 
    <li>Extracts the contents of the query results.</li>
   </ul>
</li>
<li>ise.py
  <ul>
    <li>Uses Spacy to extract the named entities of the content.</li>
    <li>Uses a pretrained BERT model to identify the relations between the named entities.</li>
  </ul>
</li>
<li>__main__.py
  <ul>
    <li>Gets the google search results.</li>
    <li>Processes using Iterative Set Expansion.</li>
    <li>If the required number of tuples are extracted, the process stops.</li>
    <li>Else, picks the next unused tuple with highest confidence from the results to extract more tuples.</li>
  </ul>
</li>
</ol>

## Process:
1. Input plausible query, confidence threshold of each tuple, required number of tuples.
2. The goal is to extract the required number of relation tuples with minimum number of iterations
3. Steps:
<li>Get the content of the top 10 Google results and truncate the content to 20000 characters for perfomance reasons.</li>
<li>Using spacy, extract the named entities, which are valid according to the relation chosen, from the content.</li>
<li>Form subject-object candidate pairs from the extracted named entities.</li>
<li>Run the pretrained SpanBERT on these candidate pairs to get the confidence.</li>
<li>Filter the relation tuples with confidence greater than the input threshold.</li>
<li>If the extracted relation tuples are greater than number of tuples to be extracted, stop the process</li>
<li>Else, pick the relation tuple with highest confidence, which is not already used to query, from the above result and redo the above steps until the required number of tuples are extracted.</li>
<li>We do not remove special characters other than '\n' and '\t' as that results in fewer tuples being extracted.
