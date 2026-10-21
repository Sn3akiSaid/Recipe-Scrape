from script import cleanup, finder, json_parser, url_input

TEST_URLS = {
    "1": "https://mykoreankitchen.com/korean-beef-bone-broth/",
    "2": "https://mykoreankitchen.com/korean-fried-chicken/",
    "3": "https://boldbeanco.com/blogs/beanspo-recipes/homemade-baked-beans?srsltid=AfmBOopkr11KNW1BU6rqKyp_RTdpiDcQQwREQuEX-g_a3bMmMPpiq8lB",
}


def test_url_input():
    try:
        URL = input("Input your recipe URL: ")
    except Exception as e:
        print(f"No valid url, error {e}")
    if URL:
        trial_db = cleanup(finder(json_parser(url_input(URL))))
    return trial_db
