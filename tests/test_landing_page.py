import unittest

from app.generate_frontend.generate_landing_page import (
    generate_landing_page_html,
    generate_landing_page_views,
)


class TestLandingPageFunctions(unittest.TestCase):
    def test_generate_landing_page_html(self):
        # Call the function
        result = generate_landing_page_html()

        # Assert render_template was called with the correct template and context
        self.assertIn("model", result)
        self.assertIn("<h1>Landing Page</h1>", result)
        self.assertIn("<h2>Models Available</h2>", result)

    def test_generate_landing_page_views(self):
        # Call the function
        result = generate_landing_page_views([])

        # Assert render_template was called with the correct template and context
        self.assertIn("model", result)
        self.assertIn("def landing_page(request):", result)
        self.assertIn("model_info", result)
