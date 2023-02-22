import os
import math
import argparse
import PIL
import torch
from PIL import Image, ImageOps
from diffusers import StableDiffusionInstructPix2PixPipeline

CONFIG_DICT = {
    'prompt': "make it look like a watercolor painting of flowers with a plain background",
    'seed': 21377,
    'text_cfg_scale': 8.0,
    'image_cfg_scale': 1.5,
}


def load_im(im_path):
    image = PIL.Image.open(im_path)
    image = PIL.ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    return image


def transform_to_flowers(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    model_id = "timbrooks/instruct-pix2pix"

    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16",
                                                                  safety_checker=None)

    pipe.to("cuda")
    pipe.enable_attention_slicing()

    prompt = CONFIG_DICT['prompt']
    seed = CONFIG_DICT['seed']
    text_cfg_scale = CONFIG_DICT['text_cfg_scale']
    image_cfg_scale = CONFIG_DICT['image_cfg_scale']

    img_list = os.listdir(input_dir)

    for im in list(sorted(img_list)):
        print(im)
        generator = torch.manual_seed(seed)

        input_image = load_im(os.path.join(input_dir, im))
        width, height = input_image.size
        factor = 512 / max(width, height)
        factor = math.ceil(min(width, height) * factor / 64) * 64 / min(width, height)
        width = int((width * factor) // 64) * 64
        height = int((height * factor) // 64) * 64
        input_image = ImageOps.fit(input_image, (width, height))
        edited_image = pipe(
            prompt, image=input_image,
            guidance_scale=text_cfg_scale, image_guidance_scale=image_cfg_scale,
            num_inference_steps=50, generator=generator,
        ).images[0]
        edited_image.save(os.path.join(output_dir, im))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', help='Bezier images dir', type=str, default='data/input_imgs/3')
    parser.add_argument('-o', '--output_dir', type=str, default='data/output_imgs/3')

    args = parser.parse_args()

    transform_to_flowers(args.input_dir, args.output_dir)
