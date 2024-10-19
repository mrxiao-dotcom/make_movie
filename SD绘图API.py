## -- api调用示例代码 -- ##
import json
import base64
import requests
import os

# 发送请求
def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


# 解码并保存图片
def save_encoded_image(b64_image: str, output_path: str):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))


def draw_image_by_prompt(prompt,negative_prompt,width,height,output_image_path,sae = 'DPM++ SDE',steps=20):
    txt2img_url = r'http://127.0.0.1:7860//sdapi/v1/txt2img'
    data = {'prompt': prompt,
            'negative_prompt': negative_prompt,
            'sampler_index': sae,
            'seed': 1234,
            'steps': steps,
            'width': width,
            'height': height,
            'cfg_scale': 8,
            "n_iter": 1,
            "batch_size": 1
            }
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], output_image_path)

def draw_image_by_prompt_change_model(new_model,prompt,negative_prompt,width,height,output_image_path,sae = 'DPM++ SDE',steps=20):
    txt2img_url = r'http://127.0.0.1:7860//sdapi/v1/txt2img'
    data = {'prompt': prompt,
            'negative_prompt': negative_prompt,
            'sampler_index': sae,
            'seed': 1234,
            'steps': steps,
            'width': width,
            'height': height,
            'cfg_scale': 8,
            "n_iter": 1,
            "override_settings": {
                "sd_model_checkpoint": new_model,  # 指定大模型
                "sd_vae": "Automatic",  # 指定vae 默认自动
                },
            "override_settings_restore_afterwards": True  # override_settings 是否在之后恢复覆盖的设置 默认是True
            }
    response = submit_post(txt2img_url, data)
    save_encoded_image(response.json()['images'][0], output_image_path)



if __name__ == '__main__':

    #当前底模
    url = "http://127.0.0.1:7860/sdapi/v1/sd-models"
    res = requests.get(url)
    print(res.json())


    #用底模进行文生图

    save_image_path = r'tmp.png'
    #draw_image_by_prompt('a dog wearing a hat, blue eyes',"",512,512,save_image_path,20)
    draw_image_by_prompt_change_model("【万象熔炉】anything-v5-PrtRE",'a dog wearing a hat, blue eyes',"",512,512,save_image_path,20)

