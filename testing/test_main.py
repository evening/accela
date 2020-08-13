from pathlib import Path
import sys
import pytest

HERE = Path(__file__).parent
sys.path.append(str(HERE / ".." / "app"))
import accela


@pytest.fixture
def test_client():
    return accela.app.test_client()


def test_home_page(test_client):
    res = test_client.get("/")
    assert res.status_code == 200
    assert "accela" in str(res.data)
    assert '="/posts">' in str(res.data)  # ensure links work


def test_trailing_slash(test_client):
    res_no_slash = test_client.get("/posts/hello")
    res_slash = test_client.get("/posts/hello/")
    # ensure trailing slash does cause issues with links
    assert (
        str(res_no_slash.data).split("title")[2]
        == str(res_slash.data).split("title")[2]
    )

    # ensure parent link works
    assert '[<a href="/posts">up</a>' in str(res_slash.data)


def test_error_page(test_client):
    res = test_client.get("/123")
    assert res.status_code == 404
    assert "404" in str(res.data)


# handle files
