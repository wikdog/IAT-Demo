from django.shortcuts import render
from django.http import JsonResponse
import subprocess
import json
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from urllib.parse import unquote

def home(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name) 
            with open(image_path, 'wb+') as destination:
                for chunk in image.file.chunks():
                    destination.write(chunk)
            return JsonResponse({'success': True, 'image_path': image_path})
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    return render(request, 'home.html')

def process_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_path = data.get('image_id')
        point_coords = data.get('point_coords', '')
        print("image_path:",image_path)
        if image_path:
            model_script_path = os.path.join(settings.MODEL_ROOT, 'remove_anything.py')
            output_directory = os.path.join(settings.RESULTS_ROOT)
            model_command = [
                'python', model_script_path,
                '--input_img', '.'+image_path ,
                '--coords_type', 'key_in',
                '--point_coords', str(point_coords[0]),str(point_coords[1]),
                '--point_labels', '1',
                '--dilate_kernel_size', '15',
                '--sam_model_type', "vit_h",
                '--sam_ckpt', './pretrained_models/sam_vit_h_4b8939.pth',
                '--lama_config', './lama/configs/prediction/default.yaml',
                '--lama_ckpt', './pretrained_models/big-lama',
                '--output_dir', output_directory
            ]

            subprocess.run(model_command, check=True)  # 加上check=True以便命令失败时抛出异常

            # 获取生成的图片路径
            generated_image_path = os.path.join(settings.RESULTS_ROOT, image_path)
            print('generated_image_path:',generated_image_path)
            if 1:
                return JsonResponse({'success': True, 'image_path': generated_image_path})
            else:
                return JsonResponse({'error': 'Failed to generate image'}, status=500)
        else:
            return JsonResponse({'error': 'No image provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        print("uploaded_file_url:",uploaded_file_url)
        return JsonResponse({'success': True, 'image_path': uploaded_file_url})
    return JsonResponse({'error': 'Failed to upload image'}, status=400)

from django.http import JsonResponse
import os
from django.conf import settings

def list_images(request, image_path):
    # 从 URL 参数中删除可能的开头斜杠（如果有）
    image_path = image_path.lstrip('/')
    print("image_path:", image_path)

    # 构建完整的目录路径
    directory_path = os.path.join(settings.RESULTS_ROOT, image_path)
    print("directory_path:", directory_path)

    try:
        # 构建图片URL列表，将每个文件的完整路径转换为相对于 static 目录的路径
        images = [os.path.join('/static/images', image_path, f) for f in os.listdir(directory_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

        return JsonResponse({'success': True, 'images': images})
    except FileNotFoundError:
        return JsonResponse({'success': False, 'error': 'Directory not found'})



def list_results_images(request):
    results_dir = '/mnt/my_volume/Inpaint-Anything-main/samproject/results/scut'  # 绝对路径
    images = []

    if os.path.exists(results_dir):
        for file_name in os.listdir(results_dir):
            if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 可根据需要调整支持的文件类型
                image_path = os.path.join('results/scut', file_name)  # 使用相对路径
                images.append(image_path.replace("\\", "/"))  # 确保路径使用正斜杠
    else:
        return JsonResponse({'success': False, 'error': 'Directory not found'})

    return JsonResponse({'success': True, 'images': images})