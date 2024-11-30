import sys
from zero import ZeroClient


def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <search_query>")
        sys.exit(1)

    # Get search query from command line
    query = " ".join(sys.argv[1:])
    print(f"Query: {query}")

    # Create client connection to server
    client = ZeroClient("localhost", 6000)

    try:
        # Call remote google method
        result = client.call("google", query)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
