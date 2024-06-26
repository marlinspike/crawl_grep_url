import unittest
from unittest.mock import patch, Mock
import app
import os

class TestCrawlGrepURL(unittest.TestCase):
    @patch('app.webdriver.Remote')
    def setUp(self, MockWebDriver: Mock) -> None:
        self.driver = MockWebDriver.return_value
        self.root_url = "https://example.com"
        self.links = ["https://example.com/page1", "https://example.com/page2"]

        # Mocking the find_elements call to return elements with the href attribute
        element1 = Mock()
        element1.get_attribute.return_value = "https://example.com/page1"
        element2 = Mock()
        element2.get_attribute.return_value = "https://example.com/page2"
        self.driver.find_elements.return_value = [element1, element2]

    def test_get_all_links(self) -> None:
        links = app.get_all_links(self.driver, self.root_url)
        self.assertEqual(links, self.links)

    def test_fetch_text_content(self) -> None:
        self.driver.find_element.return_value.text = "Sample text content"
        text_content = app.fetch_text_content(self.driver, self.root_url)
        self.assertEqual(text_content, "Sample text content")

    @patch('app.get_all_links')
    @patch('app.fetch_text_content')
    @patch('os.path.getsize')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_create_markdown_file(self, mock_open: Mock, mock_getsize: Mock, mock_fetch_text_content: Mock, mock_get_all_links: Mock) -> None:
        mock_get_all_links.return_value = self.links
        mock_fetch_text_content.side_effect = ["Content of Page 1", "Content of Page 2"]
        mock_getsize.return_value = 2048  # Mock file size to be 2 KB

        output_filename = "test_output.md"
        output_folder = "test_processed"
        app.create_markdown_file(self.root_url, output_filename, output_folder)

        mock_open.assert_called_with(os.path.join(output_folder, output_filename), 'w', encoding='utf-8')
        handle = mock_open()
        written_content = ''.join(call[0][0] for call in handle.write.call_args_list)

        self.assertIn("# Root URL: https://example.com\n\n", written_content)
        self.assertIn("## https://example.com/page1\nContent of Page 1\n\n", written_content)
        self.assertIn("## https://example.com/page2\nContent of Page 2\n\n", written_content)

if __name__ == '__main__':
    unittest.main()
