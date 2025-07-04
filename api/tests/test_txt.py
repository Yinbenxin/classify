import unittest
import requests

class TestTxtClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_txt_url = f'{self.base_url}/classify/txt'

    def test_classify_txt_with_default_labels(self):
        """测试文本分类接口（仅使用默认标签）"""
        data = {"txt": "今天是一个十分适合旅游的天气，我们不如出去走一走？"}
        response = requests.post(self.classify_txt_url, json=data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("results", result)
        for group in result["results"]:
            if group:
                self.assertIsInstance(group, list)
                self.assertEqual(len(group), 2)
                label, score = group
                self.assertIsInstance(label, str)
                self.assertIsInstance(score, float)
                self.assertGreaterEqual(score, 0.0)
                self.assertLessEqual(score, 1.0)
            else:
                self.assertEqual(group, [])

if __name__ == '__main__':
    unittest.main()