import unittest
import requests
import os
import time
from PIL import Image
from io import BytesIO

class TestImageClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_image_url = f'{self.base_url}/classify/image'
        
        # 等待服务启动
        max_retries = 5
        for i in range(max_retries):
            try:
                requests.get(f'{self.base_url}/health')
                break
            except requests.exceptions.ConnectionError:
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    raise Exception('API service is not available')
        
        # 测试图片URL
        self.test_image_url = 'https://img2.baidu.com/it/u=2048195462,703560066&fm=253&fmt=auto&app=138&f=JPEG'
        
        # 预先下载测试图片
        response = requests.get(self.test_image_url)
        self.test_image = Image.open(BytesIO(response.content)).convert('RGB')
        
        # 保存为临时文件用于测试
        self.temp_image_path = 'test_image.jpg'
        self.test_image.save(self.temp_image_path)

    def tearDown(self):
        # 清理临时文件
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def test_classify_image(self):
        """测试图像分类接口"""
        # 准备测试数据
        with open(self.temp_image_path, 'rb') as f:
            files = {'image': ('test_image.jpg', f, 'image/jpeg')}
            data = {
                'labels': '["风景", "人物", "动物", "建筑", "食物"]',
                'num_results': '3'
            }
            
            # 使用 files 和 form-data 格式发送请求
            response = requests.post(
                self.classify_image_url,
                files=files,
                data=data
            )
            

            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            
            # 检查返回结果格式
            self.assertIn('labels', result)
            self.assertIn('scores', result)
            self.assertEqual(len(result['labels']), 3)  # 验证结果数量
            self.assertEqual(len(result['scores']), 3)
            
            # 验证分数是否为浮点数且在0-1之间
            for score in result['scores']:
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)

    def test_classify_image_without_labels(self):
        """测试没有标签的情况"""
        with open(self.temp_image_path, 'rb') as f:
            files = {'image': ('test_image.jpg', f, 'image/jpeg')}
            data = {}
            
            response = requests.post(
                self.classify_image_url,
                files=files,
                data=data
            )
            
            self.assertEqual(response.status_code, 200)
            result = response.json()
            self.assertEqual(result["labels"], [])
            self.assertEqual(result["scores"], [])

    def test_classify_image_invalid_file(self):
        """测试无效的文件类型"""
        files = {'image': ('test.txt', b'invalid image content', 'text/plain')}
        data = {
            'labels': '["风景", "人物"]'
        }
        
        response = requests.post(
            self.classify_image_url,
            files=files,
            data=data
        )
        
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()