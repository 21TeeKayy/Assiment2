from src import create_app


def test_index():
    app = create_app('flask_test.cfg')
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert b"Type your NFT's address!" in response.data
        assert b"Send" in response.data