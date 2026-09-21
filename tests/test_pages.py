import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from accounts import AccountError
from streamlit.testing.v1 import AppTest


class PageTests(unittest.TestCase):
    def app(self, page=None, logged_in=False):
        app = AppTest.from_file(str(ROOT / "src/app.py"), default_timeout=30)
        if logged_in:
            app.session_state.logged_in = True
            app.session_state.username = "alice"
        app.run()
        if page:
            app.switch_page(f"pages/{page}.py").run()
        self.assertFalse(app.exception)
        return app

    def click(self, app, label):
        next(button for button in app.button if button.label == label).click().run()
        self.assertFalse(app.exception)

    def test_direct_landing_page_renders(self):
        app = self.app("landing_page")
        self.assertTrue(any(button.key == "hpp_landing_start" for button in app.button))

    def test_predict_preserves_destination_for_login(self):
        app = self.app()
        self.click(app, "Predict")
        self.assertEqual(app.session_state.page, "predict")
        self.assertTrue(any("Login" in title.value for title in app.title))

    def test_profile_requires_login_on_direct_access(self):
        app = self.app("profile")
        self.assertEqual(app.session_state.page, "profile")
        self.assertTrue(any("Login" in title.value for title in app.title))

    def test_login_validation_and_database_failure_are_visible(self):
        app = self.app("login")
        self.click(app, "Login")
        self.assertTrue(app.error)
        app.text_input[0].input("alice")
        app.text_input[1].input("secret")
        with patch("accounts.authenticate", side_effect=AccountError("Database unavailable")):
            self.click(app, "Login")
        self.assertEqual(app.error[0].value, "Database unavailable")
        self.assertFalse(app.session_state.logged_in)

    def test_login_success_redirects_home(self):
        app = self.app("login")
        app.text_input[0].input("alice")
        app.text_input[1].input("secret")
        with patch("accounts.authenticate", return_value="alice"):
            self.click(app, "Login")
        self.assertTrue(app.session_state.logged_in)
        self.assertEqual(app.session_state.username, "alice")
        self.assertTrue(any(button.label == "Profile" for button in app.button))

    def test_registration_confirmation_survives_redirect(self):
        app = self.app("register")
        app.text_input[0].input("alice")
        app.text_input[1].input("secret")
        with patch("accounts.register_account", return_value="alice"):
            self.click(app, "Register")
        self.assertTrue(any("Account created" in message.value for message in app.success))
        self.assertTrue(any("Login" in title.value for title in app.title))

    def test_profile_failure_preserves_session_identity(self):
        app = self.app("profile", logged_in=True)
        app.text_input[0].input("bob")
        with patch("accounts.update_account", side_effect=AccountError("Could not save")):
            self.click(app, "Update")
        self.assertEqual(app.session_state.username, "alice")
        self.assertEqual(app.error[0].value, "Could not save")

    def test_profile_success_refreshes_username(self):
        app = self.app("profile", logged_in=True)
        app.text_input[0].input("bob")
        with patch("accounts.update_account", return_value="bob"):
            self.click(app, "Update")
        self.assertEqual(app.session_state.username, "bob")
        self.assertEqual(app.info[0].value, "Username: bob")
        self.assertTrue(app.success)

    def test_logout_clears_identity_and_returns_home(self):
        app = self.app(logged_in=True)
        self.click(app, "Profile")
        self.click(app, "Logout")
        self.assertFalse(app.session_state.logged_in)
        self.assertNotIn("username", app.session_state)
        self.assertEqual(app.session_state.page, "home")

    def test_home_does_not_load_model(self):
        with patch("joblib.load", side_effect=FileNotFoundError) as load:
            self.app()
        load.assert_not_called()

    def test_prediction_page_still_runs_with_saved_model(self):
        app = self.app(logged_in=True)
        self.click(app, "Predict")
        estimate = next(button for button in app.button if "Estimate Price" in button.label)
        estimate.click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Estimated Price" in message.value for message in app.success))

    def test_landing_action_returns_to_prediction_after_login(self):
        app = self.app("landing_page")
        app.button(key="hpp_landing_start").click().run()
        self.assertEqual(app.session_state.page, "predict")
        # AppTest keeps the page selected by switch_page across test runs.
        # Select the redirect destination before interacting with its widgets.
        app.switch_page("pages/login.py").run()
        app.text_input[0].input("alice")
        app.text_input[1].input("secret")
        with patch("accounts.authenticate", return_value="alice"):
            self.click(app, "Login")
        self.assertTrue(
            any("Estimate Price" in button.label for button in app.button),
            ([button.label for button in app.button], [error.value for error in app.error]),
        )


if __name__ == "__main__":
    unittest.main()
