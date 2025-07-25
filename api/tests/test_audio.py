import unittest
import requests
import os

class TestAudioClassificationAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.classify_audio_url = f'{self.base_url}/classify/audio'
        self.audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../audio/06_life_services_1_information_inquiry_01.wav'))
        self.assertTrue(os.path.exists(self.audio_path), f"测试音频文件不存在: {self.audio_path}")
    def test_classify_audio_with_default_labels(self):
        """测试音频分类接口（仅使用默认标签）"""
        with open(self.audio_path, 'rb') as f:
            files = {'audio': (os.path.basename(self.audio_path), f, 'audio/wav')}
            response = requests.post(self.classify_audio_url, files=files)
        self.assertEqual(response.status_code, 200)
        result = response.json()
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