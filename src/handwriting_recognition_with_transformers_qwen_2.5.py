
import argparse
import torch
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoModelForImageTextToText, AutoProcessor
from qwen_vl_utils import process_vision_info

def parse_arguments():

    parser = argparse.ArgumentParser(description="Handwriting Recognition with OlmOCR")

    parser.add_argument("--image_path", type=str, default="/tmp/congress_letter_image1.jpg", help="Path to the input image")
    return parser.parse_args()


def run_qwen25_ocr(image_path, model_size="7B"):
    """
    Performs OCR on handwritten text using the Qwen 2.5 VL architecture.
    model_size: Choose "2B" for low VRAM (8GB) or "7B" for high accuracy (16GB+).
    """
    model_id = f"Qwen/Qwen2.5-VL-{model_size}-Instruct"

    # 1. Initialize Model with bfloat16 for speed and memory efficiency
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    processor = AutoProcessor.from_pretrained(model_id)

    # 2. Build the Prompt
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {
                    "type": "text",
                    "text": "Transcribe the handwriting in this image. "
                            "If there are crossed-out words, ignore them. "
                            "Maintain the exact layout and indentation."
                },
            ],
        }
    ]

    # 3. Processing & Inference
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, _ = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        padding=True,
        return_tensors="pt"
    ).to("cuda")

    generated_ids = model.generate(**inputs, max_new_tokens=1024)

    # Trim the prompt from the output
    trimmed_ids = [out[len(ins):] for ins, out in zip(inputs.input_ids, generated_ids)]
    output = processor.batch_decode(trimmed_ids, skip_special_tokens=True)[0]

    return output


def run_qwen35_ocr(image_path, model_size="9B"):
    """
    Performs OCR on handwritten text using the Qwen 3.5 VL architecture.
    """
    model_id = f"Qwen/Qwen3.5-{model_size}"

    # 1. Initialize Model with bfloat16 for speed and memory efficiency
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    processor = AutoProcessor.from_pretrained(model_id, trust_romote_code=True)

    # 2. Build the Prompt
    # Qwen 3.5 is much better at following complex formatting instructions.
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {
                    "type": "text",
                    "text": "Transcribe the handwriting in this image. "
                            "If there are crossed-out words, ignore them. "
                            "Maintain the exact layout and indentation."
                            "If uncertain add a '[?]'."
                            "output: tei xml."
                },
            ],
        }
    ]

    # 3. Processing & Inference
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, _ = process_vision_info(messages)

    inputs = processor(
        text=[text],
        images=image_inputs,
        padding=True,
        return_tensors="pt"
    ).to("cuda")

    # Qwen 3.5 handles longer sequences better (up to 256k context),
    # but for a single page, 1024 tokens is plenty.
    generated_ids = model.generate(**inputs, max_new_tokens=1024)

    # Trim the prompt from the output
    trimmed_ids = [out[len(ins):] for ins, out in zip(inputs.input_ids, generated_ids)]
    output = processor.batch_decode(trimmed_ids, skip_special_tokens=True)[0]

    return output

if __name__ == "__main__":
    args = parse_arguments()

    print(f"--- Loading Qwen to process {args.image_path} ---")
    try:
        transcription = run_qwen35_ocr(args.image_path, model_size="9B")
        # transcription = run_qwen25_ocr(args.image_path, model_size="7B")
        print("\n--- Transcription Result ---\n")
        print(transcription)
    except Exception as e:
        print(f"Error: {e}")
