import os
from groq import Groq

def diagnose(resume_text, market_signals):
    """
    Compare resume vs market signals using Groq API.
    """
    api_key = os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_API_Key")
    if not api_key:
        return "Error: GROQ_API_KEY not found in environment variables."

    client = Groq(api_key=api_key)
    model_name = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

    system_prompt = """
    You are a BRUTALLY HONEST Technical Recruiter & Market Strategist.
    
    Task:
    Analyze the candidate's resume against LIVE MARKET SIGNALS.
    
    Generate a JSON response with this EXACT structure:
    {
        "scores": {
            "technical_match": 0-100,
            "experience_depth": 0-100,
            "market_relevance": 0-100,
            "soft_skills": 0-100
        },
        "market_drift": {
            "verdict": "Modern" | "Drifting" | "Obsolete",
            "explanation": "Detailed explanation of why (3-4 sentences)...",
            "obsolete_terms": ["list", "of", "dated", "terms"],
            "emerging_terms": ["list", "of", "missing", "modern", "terms"]
        },
        "personas": [
            {
                "name": "The Startup Founder",
                "focus": "Shipping, Speed, Ownership",
                "fit_score": 0-100,
                "reason": "Why they would/wouldn't hire..."
            },
            {
                "name": "The Enterprise HR",
                "focus": "Credentials, Tenure, Keywords",
                "fit_score": 0-100,
                "reason": "Why they would/wouldn't hire..."
            },
            {
                "name": "The Tech Lead",
                "focus": "Code Quality, System Design, Hard Skills",
                "fit_score": 0-100,
                "reason": "Why they would/wouldn't hire..."
            }
        ],
        "blind_spots": [
            "You likely know X because of Y, but didn't list it.",
            "You mentioned X project but missed quantifying impact."
        ],
        "diagnosis_html": "...The HTML report as before..."
    }
    
    HTML Guidelines:
    - <div class="diagnosis-report">...</div>
    - <h2><i class="fa-solid fa-triangle-exclamation"></i> Final Verdict: ...</h2>
    - Sections: 
        <h3><i class="fa-solid fa-circle-xmark"></i> Direct Feedback</h3>, 
        <h3><i class="fa-solid fa-flag"></i> Red Flags</h3>, 
        <h3><i class="fa-solid fa-rocket"></i> Strategic Fixes</h3>.
    - Be HARSH, DETAILED, and SPECIFIC.
    - CONTENT DENSITY RULE: Each of the 3 main sections (Direct Feedback, Red Flags, Strategic Fixes) MUST be at least 200 words long.
    - AVOID GENERIC ADVICE like "gain experience". Instead, specify "Build X using Y" or "Certify in Z".
    - Quote specific parts of the resume and contrast them with specific lines from the market signals.
    - provide "Deep Dive" explanations (3-4 sentences per point) rather than short bullet points.
    - DO NOT USE EMOJIS anywhere. Use FontAwesome icons if needed.
    
    JSON Format:
    {
        "scores": {
            "technical_match": 0-100,
            "experience_depth": 0-100,
            "market_relevance": 0-100,
            "soft_skills": 0-100
        },
        "market_drift": { ... },
        "personas": [ ... ],
        "career_pivot": {
            "alternative_roles": ["Role A", "Role B"],
            "reason": "Why these roles fit better..."
        },
        "target_companies": {
            "industries": ["Industry A", "Industry B"],
            "top_companies": ["Company X", "Company Y"],
            "culture_fit": "Description of ideal culture..."
        },
        "blind_spots": [ ... ],
        "diagnosis_html": "..."
    }
    
    Analyze candidate for FIT, DRIFT, PERSONAS, and CAREER STRATEGY.
    RETURN ONLY RAW JSON.
    """

    user_prompt = f"""
    CANDIDATE RESUME:
    {resume_text[:12000]} 
    
    LIVE MARKET SIGNALS:
    {market_signals[:12000]}
    
    PERFORM DRIFT ANALYSIS AND PERSONA SIMULATION.
    """

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2500,
            response_format={"type": "json_object"}
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        # Return a fallback JSON structure on error
        error_msg = str(e).replace('"', "'") # Escape quotes
        return f'{{"scores": {{"technical_match": 0, "experience_depth": 0, "market_relevance": 0, "soft_skills": 0}}, "market_drift": {{"verdict": "Error", "explanation": "System error", "obsolete_terms": [], "emerging_terms": []}}, "personas": [], "career_pivot": {{"alternative_roles": [], "reason": "N/A"}}, "target_companies": {{"industries": [], "top_companies": [], "culture_fit": "N/A"}}, "blind_spots": [], "diagnosis_html": "<div class=\'diagnosis-report\'><h2 style=\'color:red\'>System Error</h2><p>Failed to generate diagnosis.</p><p>Error: {error_msg}</p></div>"}}'
