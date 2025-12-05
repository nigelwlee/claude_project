import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import anthropic
from pdf_parser import extract_text_from_pdf
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Lazy initialization of Anthropic client
_client = None

def get_client():
    """Get or create Anthropic client"""
    global _client
    if _client is None:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key or api_key == 'your_api_key_here':
            raise ValueError("Please set a valid ANTHROPIC_API_KEY in your .env file")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client

ANALYSIS_PROMPT = """You are an expert email security analyst specializing in detecting spam, scams, and social engineering attacks.

Analyze the following email content and provide a comprehensive security assessment.

Email Content:
{email_content}

Provide your analysis in the following JSON format:
{{
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "category": "LEGITIMATE|MARKETING|SPAM|PHISHING|SCAM|SOCIAL_ENGINEERING",
  "confidence": 0-100,
  "summary": "Brief 1-2 sentence summary of the email",
  "red_flags": [
    "List of specific suspicious indicators found"
  ],
  "analysis": {{
    "sender_authenticity": "Analysis of sender legitimacy",
    "urgency_tactics": "Any pressure or urgency tactics used",
    "suspicious_links": "Analysis of links or attachments",
    "language_patterns": "Grammar, tone, and language analysis",
    "impersonation": "Any signs of impersonation"
  }},
  "recommendation": "Clear action recommendation for the user"
}}

Be thorough and look for:
- Sender spoofing or impersonation
- Urgency and fear tactics (threats, deadlines, account closures)
- Requests for sensitive information (passwords, SSN, financial data)
- Suspicious links or attachments
- Grammar and spelling errors
- Generic greetings vs personalized
- Too-good-to-be-true offers
- Mismatched sender domains
- Social engineering tactics

Respond ONLY with valid JSON, no other text."""


def analyze_email(content):
    """Analyze email content using Claude API"""
    try:
        message = get_client().messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(email_content=content)
                }
            ]
        )

        response_text = message.content[0].text

        # Parse JSON response
        result = json.loads(response_text)
        return result

    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse AI response: {str(e)}",
            "risk_level": "UNKNOWN",
            "category": "ERROR"
        }
    except Exception as e:
        return {
            "error": f"Analysis failed: {str(e)}",
            "risk_level": "UNKNOWN",
            "category": "ERROR"
        }


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze pasted email text"""
    try:
        data = request.get_json()
        email_text = data.get('text', '').strip()

        if not email_text:
            return jsonify({"error": "No text provided"}), 400

        result = analyze_email(email_text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze/pdf', methods=['POST'])
def analyze_pdf():
    """Analyze uploaded PDF files"""
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400

        files = request.files.getlist('files')
        results = []

        for file in files:
            if file.filename == '':
                continue

            if not file.filename.lower().endswith('.pdf'):
                results.append({
                    "filename": file.filename,
                    "error": "Only PDF files are supported",
                    "risk_level": "ERROR"
                })
                continue

            # Save file temporarily
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                # Extract text from PDF
                text = extract_text_from_pdf(filepath)

                if not text.strip():
                    results.append({
                        "filename": file.filename,
                        "error": "Could not extract text from PDF",
                        "risk_level": "ERROR"
                    })
                else:
                    # Analyze the extracted text
                    analysis = analyze_email(text)
                    analysis["filename"] = file.filename
                    results.append(analysis)

            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    return jsonify({
        "status": "ok",
        "api_key_configured": bool(api_key and api_key != 'your_api_key_here')
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
