from langchain.utilities import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")

        
        for result in res.get("organic_results", []):
            link = result.get("link", "")
            if "linkedin.com/in/" in link:
                return link

        return "No LinkedIn profile found."


def get_profile_url(name: str):
    search = CustomSerpAPIWrapper()
    try:
        res = search.run(f"{name} site:linkedin.com")
        return res
    except Exception as e:
        print(f"⚠️ Error during search: {e}")
        return None
