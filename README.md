# Handwriting Recogntion and Transcription via LLMs

A repository for testing LLMs with handwriting recognition. This is meant as a personal learning journey and to record forays into LLMs.

## Setup

``` sh
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements/requirements.txt
```

.env.sample: fill in HF_TOKEN

``` bash
source .env
```

If small home directory then move where .cache and HF models are stored

```
   cd /mnt/handwriting_recognition/
   pip install --cache-dir /mnt/.cache -r requirements/requirements_transformers.txt
   export HF_HOME="/mnt/handwriting_recognition/"
```

## Samples

1.  `curl --output default.jpg https://tile.loc.gov/image-services/iiif/service:mss:mal:435:4356500:001/full/pct:12.5/0/default.jpg`
2. [LEAF-Writer sample](https://leaf-writer.leaf-vre.org/edit?sample=To%20Congress%20on%20women%27s%20suffrage%20(letter))
    * `curl https://raw.githubusercontent.com/LEAF-VRE/leaf_workshops/main/exercises/Congress_Letter/congress_letter_image1.jpg`

## Trials

1. Question: can Qwen 3.5 transcribe a scan of handwriting and output as TEI XML that can be loaded into [LEAF-Writer](https://leaf-writer.leaf-vre.org/) [/trials/test_1.md](./trials/test_1.md)?

2. Question: build upon trial #1 and enhance the prompt to enforce well-formed XML, TEI Header with indicating what generated the transcription with a timestamp. An attempt to tag some named entity references. [./trials/test_2.md](./trials/test_2.md)?

3. Trials 3 & 4 refine the prompt.
