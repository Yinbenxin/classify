import unittest
import requests

class TestClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_url = f'{self.base_url}/classify'
        self.health_url = f'{self.base_url}/health'

    def test_health_check(self):
        """测试健康检查接口"""
        response = requests.get(self.health_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})

    def test_classify_text(self):
        """测试文本分类接口"""
        payload = {
            "text": "世界那么大，我想去看看",
            "labels": ["旅游", "故事", "游戏", "军事", "科技", "家居"],
            "num_results": 3
        }
        response = requests.post(self.classify_url, json=payload)
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

    def test_classify_empty_input(self):
        """测试空输入"""
        payload = {
            "text": "",
            "labels": ["旅游", "故事"]
        }
        response = requests.post(self.classify_url, json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["labels"], [])
        self.assertEqual(result["scores"], [])

    def test_classify_empty_labels(self):
        """测试空标签列表"""
        payload = {
            "text": "测试文本",
            "labels": []
        }
        response = requests.post(self.classify_url, json=payload)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["labels"], [])
        self.assertEqual(result["scores"], [])

if __name__ == '__main__':
    unittest.main()