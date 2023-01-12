# book-comparison

In this repository there are some scripts to compare sentences meaning similarity. My idea is to use it to compare
book notes similarities. 

## Content

Here, there are some example of use:
 - "markdown_read.py": Example of markdown read for books notes.
 - "sentences_compare.py": Little sentences compare cosine similarity example.
 - "spacy_example.py": Little Spacy Model example.

Then, there are two main scripts, one with Sentences Transformers and other with Spacy Models.
 - "main_spacy.py": Spacy script.
 - "main_st.py": Sentences transformer script.
 
## Installation

Install all dependencies with "requirements.txt" file:

```
pip install -r requirements.txt
```

If you are gonna use Spacy, install model:

```
python3 -m spacy download en_core_web_lg
```

## Usage

Both scripts do the same, receive two parameters from console, being two books filepaths. Then, compare and after
it, save results in a "data/metric" file.

```
python main_st.py book1_filepath book2_filepath

python main_spacy.py book1_filepath book2_filepath
```
