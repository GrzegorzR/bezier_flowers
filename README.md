
#Bézier Curves Animation + Instruct Pix2Pix Stable Diffusion

The objective of this project was to generate clean flower animations by utilizing basic geometric animations as input for [the instruct pix2pix stable diffusion model](https://github.com/timothybrooks/instruct-pix2pix). The goal was specifically to obtain clean flower animation, and after several experiments, the best prompt and model parameters were found to be:

```
CONFIG_DICT = {
    'prompt': "make it look like a watercolor painting of flowers with a plain background",
    'text_cfg_scale': 8.0,
    'image_cfg_scale': 1.5,
}
```

## Example output

https://user-images.githubusercontent.com/6661601/223214242-2e9ba6b9-1581-44ae-b65c-5f5d2e4abd4b.mp4


## Usage

Generate random input animation:
```
python3 generate_input.py -d data/geo_anim
```

Tranform bezier curves into flowers:
```
python3 bezier_to_flowers.py -i data/geo_anim -o data/out_anim
```

Images to animations ffmpeg command:
```
ffmpeg -r 60 -i data/geo_anim/%04d.png -vcodec mpeg4 -y -b 64000k  data/geometric_animation.mp4
ffmpeg -r 60 -i data/out_anim/%04d.png -vcodec mpeg4 -y -b 64000k  data/flower_animation.mp4
```

## Model source
https://github.com/timothybrooks/instruct-pix2pix 

