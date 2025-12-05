# Email Spam & Scam Detector 🛡️

A simple web application that uses AI to detect spam, phishing, and social engineering attacks in emails. Analyze emails by pasting text or uploading PDF files.

## Features

- **Text Analysis**: Copy and paste email content for instant analysis
- **PDF Upload**: Upload multiple PDF files containing email content
- **AI-Powered Detection**: Uses Claude AI to identify:
  - Spam and phishing attempts
  - Social engineering tactics
  - Sender spoofing and impersonation
  - Suspicious links and attachments
  - Urgency and fear tactics
  - Grammar and language anomalies

- **Risk Assessment**: Categorizes emails by risk level (LOW, MEDIUM, HIGH, CRITICAL)
- **Detailed Analysis**: Provides comprehensive breakdown of red flags and suspicious indicators
- **Actionable Recommendations**: Clear guidance on how to handle each email

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Analyzing Text

1. Click on the "Paste Text" tab
2. Paste your email content into the text area
3. Click "Analyze Email"
4. View the detailed analysis results

### Analyzing PDFs

1. Click on the "Upload PDFs" tab
2. Click the upload area or drag and drop PDF files
3. Select one or multiple PDF files
4. Click "Analyze PDFs"
5. View analysis results for each file

## How It Works

The application uses Claude AI (Sonnet 4.5) with a specialized prompt designed to:

1. **Analyze sender authenticity** - Checks for spoofing, mismatched domains, and impersonation
2. **Detect urgency tactics** - Identifies pressure tactics, threats, and artificial deadlines
3. **Examine links and attachments** - Flags suspicious URLs and file requests
4. **Evaluate language patterns** - Analyzes grammar, tone, and professionalism
5. **Assess social engineering** - Detects manipulation tactics and information requests

Each email receives:
- **Risk Level**: LOW, MEDIUM, HIGH, or CRITICAL
- **Category**: LEGITIMATE, MARKETING, SPAM, PHISHING, SCAM, or SOCIAL_ENGINEERING
- **Confidence Score**: 0-100% confidence in the assessment
- **Red Flags**: Specific suspicious indicators found
- **Detailed Analysis**: Breakdown of each security aspect
- **Recommendation**: Clear action to take

## API Endpoints

- `GET /` - Web interface
- `POST /api/analyze/text` - Analyze text content
- `POST /api/analyze/pdf` - Analyze PDF files
- `GET /health` - Health check

## Security Notes

- PDF files are temporarily stored during processing and immediately deleted
- No email content is stored permanently
- All analysis is performed using Anthropic's Claude API
- Keep your API key secure and never commit it to version control

## Limitations

- Requires internet connection for AI analysis
- API usage is subject to Anthropic's rate limits and pricing
- PDF text extraction quality depends on PDF format
- Maximum file size: 16MB per request

## Cost Considerations

This application uses the Claude Sonnet 4.5 model. Each analysis consumes API tokens based on the email length. Monitor your API usage at [Anthropic Console](https://console.anthropic.com/).

## License

This is a prototype application. Use at your own discretion.

## Support

For issues or questions, please refer to:
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
