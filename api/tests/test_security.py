import unittest
import requests

class TestSecurityLevelAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.security_level_url = f'{self.base_url}/security/level'

    def test_environment_variable_low_risk(self):
        """测试环境变量在低风险等级中的得分"""
        test_data = {
            "category": "城市景观",
            "security_level": "高风险等级"
        }
        
        response = requests.post(self.security_level_url, json=test_data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        self.assertIn("category", result)
        self.assertIn("security_level", result)
        self.assertIn("level_value", result)
        self.assertIsInstance(result["level_value"], int)
        print(f"环境变量在低风险等级的得分: {result['level_value']}")

if __name__ == '__main__':
    unittest.main()