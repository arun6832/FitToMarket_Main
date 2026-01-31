import os
from groq import Groq
from duckduckgo_search import DDGS

def scan_market(job_title, company=None):
    """
    Search for live job postings. If search fails, generate a synthetic market profile using LLM.
    """
    # ... (Keep existing search logic) ...
    
    query = f"{job_title} job description"
    if company:
        query += f" at {company}"
    
    print(f"Searching for: {query}")
    
    # [EXISTING SEARCH LOGIC REMAINS - Simplified for diff brevity]
    # We will wrap the search attempt and fallback if it returns specific "No results" message or empty.
    
    search_results = []
    try:
        ddgs = DDGS()
        # Attempt 1: Past Month
        results_gen = ddgs.text(query, region='wt-wt', safesearch='off', timelimit='m', max_results=10)
        search_results = list(results_gen) if results_gen else []
        
        # Attempt 2: Past Year
        if not search_results:
             results_gen = ddgs.text(query, region='wt-wt', safesearch='off', timelimit='y', max_results=10)
             search_results = list(results_gen) if results_gen else []
             
        # Attempt 3: No Limit
        if not search_results:
             results_gen = ddgs.text(query, region='wt-wt', safesearch='off', max_results=10)
             search_results = list(results_gen) if results_gen else []

    except Exception as e:
        print(f"Search failed: {e}")
        search_results = []

    if search_results:
        market_data = []
        for res in search_results:
            title = res.get('title', '')
            body = res.get('body', '')
            href = res.get('href', '')
            market_data.append(f"Source: {title}\nURL: {href}\nSnippet: {body}\n")
        return "\n---\n".join(market_data)

    # --- FALLBACK: LLM SIMULATION ---
    print("Search returned no results. Falling back to LLM Simulation.")
    return _generate_simulated_signals(job_title, company)

def _generate_simulated_signals(job_title, company):
    """
    Generates a realistic job description based on LLM knowledge.
    """
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_Key")
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    if not api_key:
        return "Error: No API Key for fallback generation."

    client = Groq(api_key=api_key)
    
    company_str = f"at {company}" if company else "at a top-tier tech company"
    
    prompt = f"""
    Generate a detailed, realistic, and modern Job Description for a '{job_title}' role {company_str}.
    Include:
    - Key Responsibilities (seniority appropriate)
    - Required Technical Skills (current market stack)
    - "Nice to Have" skills that are trending
    - Behavioral/Leadership expectations
    
    Format it as raw text suitable for analysis.
    """
    
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        return "NOTE: LIVE SEARCH FAILED. ANALYSIS BASED ON LLM KNOWLEDGE OF MARKET TRENDS.\n\n" + completion.choices[0].message.content
    except Exception as e:
        return f"Error generating fallback signals: {str(e)}"
