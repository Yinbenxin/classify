import unittest
import requests
import os

class TestImageClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_image_url = f'{self.base_url}/classify/image'

    def test_classify_image(self):
        """测试图片分类接口（仅使用默认标签）"""
        image_path = "audio/food.jpeg"
        self.assertTrue(os.path.exists(image_path), f"测试图片文件不存在: {image_path}")
        with open(image_path, "rb") as img_file:
            files = {"image": (os.path.basename(image_path), img_file, "image/jpeg")}
            response = requests.post(self.classify_image_url, files=files)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        print(result)
        self.assertIn("results", result)
        for group in result["results"]:
            self.assertIsInstance(group, list)
            self.assertEqual(len(group), 2)
            label, score = group
            self.assertIsInstance(label, str)
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

if __name__ == '__main__':
    unittest.main()