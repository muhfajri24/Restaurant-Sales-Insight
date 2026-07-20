from pathlib import Path

from streamlit.testing.v1 import AppTest

BASE_DIR = Path(__file__).resolve().parents[1]


def test_streamlit_dashboard_import_and_five_tabs():
    app = AppTest.from_file(str(BASE_DIR / "app.py"), default_timeout=30)
    app.run()
    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Executive Overview",
        "Revenue Drivers",
        "Menu Intelligence",
        "Business Explorer",
        "Opportunity Matrix",
    ]
