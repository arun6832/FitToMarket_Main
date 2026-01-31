from app.services.diagnoser import diagnose
import os

# Mock logic since we are running outside flask context, 
# but we just need to test the Groq API call.

def test():
    print("Testing Diagnoser...")
    
    # Check API Key
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("WARNING: GROQ_API_KEY not found in env.")
    else:
        print(f"API Key present: {key[:5]}...")

    resume_text = "Experienced Python Developer with 5 years in Flask and AWS."
    market_signals = "Required: Python, Flask, AWS, Docker, Kubernetes."
    
    print("\nCalling diagnose()...")
    result = diagnose(resume_text, market_signals)
    with open("error.log", "w", encoding="utf-8") as f:
        f.write(result)
    print("Result written to error.log")

if __name__ == "__main__":
    # Load env vars if needed (dotenv)
    from dotenv import load_dotenv
    load_dotenv()
    test()
