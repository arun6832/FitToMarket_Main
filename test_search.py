from duckduckgo_search import DDGS

def test():
    print("Testing DDGS Backends...")
    ddgs = DDGS()
    
    backends = ['api', 'html', 'lite']
    
    for backend in backends:
        print(f"\n--- Testing backend: {backend} ---")
        try:
            res = list(ddgs.text("Data Scientist job description", backend=backend, max_results=3))
            print(f"Result count: {len(res)}")
            if res:
                print(f"Sample: {res[0].get('title')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test()
