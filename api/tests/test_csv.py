import unittest
import requests
import os
import io
import tempfile

class TestCSVClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_csv_url = f'{self.base_url}/classify/csv'
    
    def test_csv_classification(self):
        """测试CSV分类接口（仅使用默认标签）"""
        temp_csv_path = 'audio/个人财产信息.csv'
        # 确保文件存在
        self.assertTrue(os.path.exists(temp_csv_path), f"测试CSV文件不存在: {temp_csv_path}")
        
        # 发送请求
        with open(temp_csv_path, "rb") as csv_file:
            files = {"csv_file": (os.path.basename(temp_csv_path), csv_file, "text/csv")}
            response = requests.post(self.classify_csv_url, files=files)
        
        # 验证响应
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("results", result)
        
        # 验证结果格式
        for group in result["results"]:
            self.assertIsInstance(group, list)
            if group:  # 如果分类结果不为空
                self.assertEqual(len(group), 2)
                label, score = group
                self.assertIsInstance(label, str)
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)
        
        # 打印分类结果
        print("CSV分类结果:", result["results"])


if __name__ == '__main__':
    unittest.main()