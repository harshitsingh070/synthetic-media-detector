#!/usr/bin/env python3

import requests
import json
import time
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APITester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/detect"
        self.ml_url = "http://localhost:8000"

    def test_health_endpoints(self):
        logger.info("Testing health endpoints...")
        try:
            resp = requests.get(f"{self.api_url}/health", timeout=10)
            if resp.status_code == 200:
                logger.info("✅ Backend health check passed")
            else:
                logger.error(f"❌ Backend health check failed: {resp.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Backend health check error: {e}")
            return False

        try:
            resp = requests.get(f"{self.ml_url}/health", timeout=10)
            if resp.status_code == 200:
                logger.info("✅ ML service health check passed")
            else:
                logger.error(f"❌ ML service health check failed: {resp.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ ML service health check error: {e}")
            return False

        return True

    def test_web_interface(self):
        logger.info("Testing web interface...")
        try:
            resp = requests.get(self.base_url, timeout=10)
            if resp.status_code == 200 and "Synthetic Media Detector" in resp.text:
                logger.info("✅ Web interface accessible")
                return True
            else:
                logger.error(f"❌ Web interface test failed: {resp.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Web interface test error: {e}")
            return False

    def create_test_files(self):
        test_dir = Path("test_files")
        test_dir.mkdir(exist_ok=True)
        test_image = test_dir / "test_image.png"
        if not test_image.exists():
            png_data = (
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
                b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00'
                b'\x90wS\xde\x00\x00\x00\tpHYs'
                b'\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18'
                b'\x00\x00\x00\x0cIDATx\x9cc`\x00\x00\x00\x02\x00\x01'
                b'\xdd\x8d\xb4\x1c\x00\x00\x00\x00IEND\xaeB`\x82'
            )
            with open(test_image, 'wb') as f:
                f.write(png_data)
        return {"image": str(test_image)}

    def test_image_detection(self):
        logger.info("Testing image detection...")
        files_map = self.create_test_files()
        try:
            with open(files_map["image"], 'rb') as f:
                files = {'file': ('test_image.png', f, 'image/png')}
                resp = requests.post(f"{self.api_url}/image", files=files, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                logger.info("✅ Image detection test passed")
                logger.info(f"Result: {json.dumps(result, indent=2)}")
                return True
            else:
                logger.error(f"❌ Image detection test failed: {resp.status_code}")
                logger.error(f"Response: {resp.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Image detection test error: {e}")
            return False

    def test_invalid_requests(self):
        logger.info("Testing invalid request handling...")
        try:
            resp = requests.post(f"{self.api_url}/image", timeout=10)
            if resp.status_code == 400:
                logger.info("✅ No file handling test passed")
            else:
                logger.warning(f"⚠️ Unexpected status for no file: {resp.status_code}")
        except Exception as e:
            logger.error(f"❌ No file test error: {e}")
            return False

        try:
            files = {'file': ('test.txt', b'test', 'text/plain')}
            resp = requests.post(f"{self.api_url}/image", files=files, timeout=10)
            if resp.status_code == 400:
                logger.info("✅ Invalid file type handling test passed")
            else:
                logger.warning(f"⚠️ Unexpected status for invalid file: {resp.status_code}")
        except Exception as e:
            logger.error(f"❌ Invalid file test error: {e}")
            return False

        return True

    def run_all_tests(self):
        logger.info("🧪 Starting API tests...")
        tests = [
            ("Health Endpoints", self.test_health_endpoints),
            ("Web Interface", self.test_web_interface),
            ("Image Detection", self.test_image_detection),
            ("Invalid Requests", self.test_invalid_requests),
        ]
        passed = 0
        for name, func in tests:
            logger.info(f"🔍 Running: {name}")
            if func():
                passed += 1
                logger.info(f"✅ {name}: PASSED")
            else:
                logger.error(f"❌ {name}: FAILED")
        total = len(tests)
        logger.info(f"📊 Test Results: {passed}/{total} tests passed")
        return passed == total

def wait_for_services(timeout=60):
    logger.info("⏳ Waiting for services to be ready...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            b = requests.get("http://localhost:8080/api/detect/health", timeout=5)
            m = requests.get("http://localhost:8000/health", timeout=5)
            if b.status_code == 200 and m.status_code == 200:
                logger.info("✅ Services are ready")
                return True
        except:
            pass
        time.sleep(2)
    logger.error("❌ Services did not become ready in time")
    return False

def main():
    if not wait_for_services():
        sys.exit(1)
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
