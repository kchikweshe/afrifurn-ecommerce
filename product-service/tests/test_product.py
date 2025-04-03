# import os
# import unittest
# from unittest.mock import AsyncMock, patch, MagicMock
# import asyncio
# import unittest.mock
# from fastapi import UploadFile

# # Assuming these functions and constants are defined somewhere
# def allowed_file(filename: str) -> bool:
#     return filename.lower().endswith(('.png', '.jpg', '.jpeg'))

# def readImage(contents: bytes):
#     return contents  # Mock implementation

# def convert_to_webp(img: bytes) -> bytes:
#     return img  # Mock implementation

# def save_image(contents: bytes, file_path: str):
#     pass  # Mock implementation

# class HTTPException(Exception):
#     def __init__(self, status_code, detail):
#         self.status_code = status_code
#         self.detail = detail

# IMAGES_DIR = "/mock_images"


# class TestProcessImage(unittest.TestCase):
#     @patch('os.makedirs')
#     @patch('builtins.open', new_callable=unittest.mock.mock_open)
#     @patch('readImage', return_value=b'processed_image_content')
#     @patch('convert_to_webp', return_value=b'webp_image_content')
#     @patch('save_image')
#     def test_process_image_success(self, mock_save_image, mock_convert_to_webp, mock_read_image, mock_open, mock_makedirs):
#         class MockUploadFile:
#             filename = 'test.jpg'
#             async def read(self):
#                 return b'test_image_content'

#         class MockProduct:
#             inserted_id = 123

#         image = MockUploadFile()
#         inserted_product = MockProduct()
        
#         loop = asyncio.get_event_loop()
#         file_path = loop.run_until_complete(process_image(image, 1, inserted_product))

#         expected_file_path = os.path.join(IMAGES_DIR, '123', 'image1.webp')
#         self.assertEqual(file_path, expected_file_path)
#         mock_makedirs.assert_called_once_with(os.path.join(IMAGES_DIR, '123'), exist_ok=True)
#         mock_save_image.assert_called_once_with(b'webp_image_content', expected_file_path)

#     @patch('readImage', return_value=b'processed_image_content')
#     @patch('convert_to_webp', return_value=b'webp_image_content')
#     @patch('save_image')
#     def test_process_image_invalid_file(self, mock_save_image, mock_convert_to_webp, mock_read_image):
#         class MockUploadFile:
#             filename = 'test.txt'
#             async def read(self):
#                 return b'test_image_content'

#         class MockProduct:
#             inserted_id = 123

#         image = MockUploadFile()
#         inserted_product = MockProduct()

#         with self.assertRaises(HTTPException) as context:
#             loop = asyncio.get_event_loop()
#             loop.run_until_complete(process_image(image, 1, inserted_product))
        
#         self.assertEqual(context.exception.status_code, 400)
#         self.assertEqual(context.exception.detail, "Only PNG, JPG, and JPEG files are allowed")
#         mock_save_image.assert_not_called()

# if __name__ == '__main__':
#     unittest.main()
