# CORANNO
Corpus Annotation Tool

This is a tool for Natural Language Processing (NLP), which allows to create fully annotated corpora with classification and POS/Entities, portable and reusable.

features:
- Multiple datasets
- Entities Annotations
- Classification multilabel and multiclass
- Possibility to tag a selected text area
- Custom tags creation
- Search en dataset
- Filter dataset for project by tag
- Split sentences in project by regular expression
- Views progress and stats
- Corpus export in simple JSON format

Based on doccano https://github.com/chakki-works/doccano

## Prerequisites

- python3


## Installing

pip install -r requirements.txt


## Getting Started

1. Run server
python3 run.py 8000

2. go to page
http://localhost:8000/

3. enter login credentials:
user: admin
pass: admin

### Create Dataset

Now upload a dataset by click on "Create Dataset", complete the form and "create".

![Alt text](doc/dataset_view.png?raw=true "Create dataset")

Go to dataset by clicking on the name. Select upload mode and upload files.

Modes:
- TXT: each line should contain a text sentence.
- JSON: each line should contain a json object with at least one key 'text', which contains a text. can have an key "file", with the name of the file
- PLAIN: one or more documents with plain text


![Alt text](doc/dataset_uploads.png?raw=true "Dataset files")

### Create Project

Now create a tagging project that uses the previously created data set. To do this, click on "create project"

complete the form data

![Alt text](doc/create_project.png?raw=true "Create project")

Open the new project by clicking on the name of this.

First you must create the labels, for that click on "Edit data" in the top bar. Create your label, set a name, color and a shortcut key and go back to "annotate data".

start your annotations por classification or entities :)

Classification:

![Alt text](doc/classification.png?raw=true "classification")

Entities:

![Alt text](doc/entities.png?raw=true "entities")

### Corpus Export

export full annotated corpus in simple JSON format, go to "Dataset" in top bar and open the dataset.

In dataset left menu, click in "Export", select annotation projects to export and click in "Download JSON file".

All documents with annotations will be exported.

example format

```json
{
   "projects":[
      {
         "name":"News classification",
         "description":"news type classification",
         "split_pattern":"",
         "split_type":"split",
         "project_type":"DocumentClassification",
         "annotations":[
            {
               "label":"politics",
               "doc_id":1,
               "start":94,
               "end":316
            }
         ]
      },
      {
         "name":"News entities",
         "description":"news entities classification",
         "split_pattern":"",
         "split_type":"split",
         "project_type":"SequenceLabeling",
         "annotations":[
            {
               "label":"PERSON",
               "doc_id":1,
               "start":25,
               "end":47
            },
            {
               "label":"ORG",
               "doc_id":1,
               "start":85,
               "end":89
            },
            {
               "label":"DATE",
               "doc_id":1,
               "start":320,
               "end":329
            },
            {
               "label":"ORG",
               "doc_id":1,
               "start":348,
               "end":353
            },
            {
               "label":"ORG",
               "doc_id":1,
               "start":368,
               "end":398
            },
            {
               "label":"PERSON",
               "doc_id":1,
               "start":403,
               "end":415
            },
            {
               "label":"ORG",
               "doc_id":1,
               "start":520,
               "end":534
            }
         ]
      }
   ],
   "docs":[
      {
         "doc_id":1,
         "file":"new001.txt",
         "dataset":"news",
         "text":"In her video above, the Olympian Allyson Felix tells her story around pregnancy and Nike.\r\n\r\nIve always known that expressing myself could hurt my career. Ive tried not to show emotion, to anticipate what people expect from me and to do it. I dont like to let people down. But you cant change anything with silence.\r\n\r\nLast week, two of my former Nike teammates, the Olympian runners Alysia Montao and Kara Goucher, heroically broke their nondisclosure agreements with the company to share their pregnancy stories in a New York Times investigation.\r\n\r\nThey told stories we athletes know are true, but have been too scared to tell publicly: If we have children, we risk pay cuts from our sponsors during pregnancy and afterward. Its one example of a sports industry where the rules are still mostly made for and by men.\r\n"
      }
   ]
}
```













