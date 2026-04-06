# Trial 1: Gettysburg Address to TEI XML

## Trial Setup

Builds on Trial #1. Attempts to add to the output
* schema
* header: notes about when the output was generated, the LLM model
* image element for side-by-side view in LEAF writer
* TEI persName element

The prompt:

``` python
```

## Notes

* UofA DSC desktop used to run the LLM
* Trial uses a local LLM
* Qwen 3.5 local LLM used

## improvements


## References

* Peter Binkley's DSC workshops
* <https://huggingface.co/docs/transformers/v5.5.0/en/model_doc/auto#transformers.AutoModelForImageTextToText>
* <https://huggingface.co/docs/transformers/v5.5.0/en/model_doc/qwen3_vl#qwen3-vl>

## Output

``` bash
curl --output default.jpg https://tile.loc.gov/image-services/iiif/service:mss:mal:435:4356500:001/full/pct:12.5/0/default.jpg
# set HF_TOKEN
source venv/bin/activate
python src/handwriting_recognition_with_transformers_qwen_3.5.py --input_image ../default.jpg
```

``` txt
```
