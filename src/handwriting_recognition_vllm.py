"""
This example demonstrates how to use the OlmOCR model for handwriting recognition.
Make sure to install the required dependencies in requirements.txt before running this code.
"""

import argparse


def parse_arguments():

    parser = argparse.ArgumentParser(description="Handwriting Recognition with OlmOCR")

    parser.add_argument("--image_path", type=str, default="/tmp/congress_letter_image1.jpg", help="Path to the input image")
    return parser.parse_args()

def main():
    """
    Docstring for main
    Based on code from Genini

    export LD_LIBRARY_PATH=$(dirname $(find $(pwd)/venv -name "libcudart.so.13")):$LD_LIBRARY_PATH
    """

    from vllm import LLM, SamplingParams
    from PIL import Image

    args = parse_arguments()

    # 1. Initialize the model directly in your script
    # Note: olmOCR-2-7B-1025 is a 7B model. 
    # Use the FP8 version if you have <24GB of VRAM.
    model_name = "allenai/olmOCR-2-7B-1025" 
    model_name = "allenai/olmOCR-2-7B-1025-FP8"

    llm = LLM(
        model=model_name,
        max_model_len=2048,   # Adjust based on image complexity/VRAM
        trust_remote_code=True,
        limit_mm_per_prompt={"image": 1},
        gpu_memory_utilization=0.5,
         enforce_eager=True,

    )

    # 2. Define your handwriting-specific custom prompt
    # olmOCR-2 follows the Qwen2-VL chat template
    custom_prompt = (
        "USER: <image>\n"
        "Transcribe the handwriting in this image. "
        "Preserve the original layout, indentations, and line breaks. "
        "If a word is unclear, use [?]. Output in Markdown.\n"
        "ASSISTANT:"
    )

    # 3. Load and prepare the image
    image = Image.open(args.image_path).convert("RGB")

    # 4. Run inference
    sampling_params = SamplingParams(
        temperature=0.1,  # Low temperature is best for accurate OCR
        max_tokens=1024,
    )

    outputs = llm.generate(
        {
            "prompt": custom_prompt,
            "multi_modal_data": {"image": image},
        },
        sampling_params=sampling_params
    )

    # 5. Output the result
    for output in outputs:
        print(output.outputs[0].text)

def main_4():

    import olmocr
    from olmocr.modeling_olmocr import OlmOCRForConditionalGeneration
    from olmocr.processing_olmocr import OlmOCRProcessor
    from PIL import Image
    import torch
    
    args = parse_arguments()

    processor = OlmOCRProcessor.from_pretrained("allenai/olmOCR-2-7B-1025")
    model = OlmOCRForConditionalGeneration.from_pretrained(
        "allenai/olmOCR-2-7B-1025",
        torch_dtype=torch.float16,
        device_map="auto"
    )

    image = Image.open(args.image_path).convert("RGB")

    prompt = "Extract all text from this image. Return plain text only."

    inputs = processor(
        images=image,
        text=[prompt],
        return_tensors="pt"
    ).to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=2048,
        temperature=0.1
    )

    print(processor.batch_decode(output, skip_special_tokens=True)[0])

def main_3():
    from transformers import AutoProcessor, AutoModelForVision2Seq
    from PIL import Image
    import torch

    args = parse_arguments()

    processor = AutoProcessor.from_pretrained("allenai/olmOCR-2-7B-1025")
    model = AutoModelForVision2Seq.from_pretrained(
        "allenai/olmOCR-2-7B-1025",
        torch_dtype=torch.float16,
        device_map="auto"
    )

    image = Image.open(args.image_path).convert("RGB")

    prompt = "Extract all text from this image. Return plain text only."

    inputs = processor(
                        images=image,
                        text=[prompt],
                        prompt=prompt,
                        return_tensors="pt"
        ).to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=2048,
        temperature=0.1
    )

    print(processor.batch_decode(output, skip_special_tokens=True)[0])


def main_2():
    from olmocr import OlmOCR
    from PIL import Image

    args = parse_arguments()

    ocr = OlmOCR.from_pretrained("allenai/olmOCR-2-7B-1025")

    image = Image.open(args.image_path)

    custom_prompt = """
    You are a handwriting OCR assistant.
    Extract ALL text from the image.
    Do not summarize.
    Do not add punctuation.
    Return plain text only.
    """

    result = ocr.generate(
        image=image,
        prompt=custom_prompt,
        max_new_tokens=2048,
        temperature=0.0
    )

    print(result)

if __name__ == "__main__":
    main()
