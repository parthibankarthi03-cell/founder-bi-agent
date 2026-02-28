import requests
from app.config import MONDAY_API_TOKEN, MONDAY_API_URL

def fetch_board_data(parsed_query, trace):

    query = """
    query ($board_id: ID!) {
      boards(ids: [$board_id]) {
        items_page {
          items {
            name
            column_values {
              id
              text
            }
          }
        }
      }
    }
    """

    variables = {"board_id": parsed_query["board_id"]}

    headers = {
        "Authorization": MONDAY_API_TOKEN,
        "Content-Type": "application/json"
    }

    trace.add("Calling Monday API", {"board_id": parsed_query["board_id"]})

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )

    return response.json()