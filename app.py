import os
import logging
import time
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI  # Using OpenAI SDK for compatibility
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'graspiq-secret-key-2024')

# Enable CORS
CORS(app)

# Initialize SambaNova client using OpenAI SDK
sambanova_client = None
SAMBA_API_KEY = os.getenv('SAMBA_API_KEY', '5f583be5-0004-41b8-9300-50f2a35d52c5').strip()

if SAMBA_API_KEY:
    try:
        # Remove < > brackets if present in the API key
        api_key_clean = SAMBA_API_KEY.strip('<>')
        
        sambanova_client = OpenAI(
            api_key=api_key_clean,
            base_url="https://api.sambanova.ai/v1",
        )
        logger.info("✅ SambaNova client initialized successfully with OpenAI SDK")
        
        # Test the connection
        try:
            test_response = sambanova_client.chat.completions.create(
                model="DeepSeek-V3.1-Terminus",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=0.1,
                top_p=0.1,
                max_tokens=10,
            )
            logger.info("✅ SambaNova API connection test successful")
        except Exception as test_error:
            logger.error(f"❌ SambaNova API test failed: {test_error}")
            logger.info("⚠️ Using enhanced local mode as fallback")
            sambanova_client = None
    except Exception as e:
        logger.error(f"❌ Failed to initialize SambaNova client: {e}")
        logger.info("⚠️ Using enhanced local mode")
        sambanova_client = None
else:
    logger.warning("⚠️ No SambaNova API key found in .env file")
    logger.info("📚 Using enhanced local knowledge base")

# Enhanced GraspIQ Knowledge Base
GRASPIQ_KNOWLEDGE = {
    "company": {
        "title": "🏢 COMPANIES GRASPIQ WORKS WITH",
        "content": """**FAANG COMPANIES:**
• Facebook/Meta
• Amazon
• Apple
• Netflix
• Google

**TECH GIANTS:**
• Microsoft
• Adobe
• Oracle
• Intel
• NVIDIA

**INDIAN IT COMPANIES:**
• TCS (Tata Consultancy Services)
• Infosys
• Wipro
• HCL Technologies
• Tech Mahindra
• Accenture
• Cognizant

**STARTUPS & PRODUCT COMPANIES:**
• Flipkart
• Ola
• Swiggy
• Zomato
• Paytm
• Uber
• Airbnb
• Spotify
• Salesforce
• LinkedIn

**FINANCE & CONSULTING:**
• Goldman Sachs
• Morgan Stanley
• JP Morgan
• McKinsey & Company
• Boston Consulting Group

**SERVICE-BASED COMPANIES:**
• Capgemini
• IBM
• Dell
• HP
• Cisco"""
    },
    "login": {
        "title": "🔐 GRASPIQ LOGIN INSTRUCTIONS",
        "content": """**Website:** https://graspiq.in
**Login Page:** https://graspiq.in/login
**Register:** https://graspiq.in/register

**STEP-BY-STEP LOGIN:**
1. Visit https://graspiq.in
2. Click Login button (top right corner)
3. Enter your registered email address
4. Enter your password
5. Click Sign In button

**FORGOT PASSWORD?**
1. Go to https://graspiq.in/login
2. Click Forgot Password?
3. Enter your registered email
4. Check email for reset link
5. Create new password

**NEW USER REGISTRATION:**
1. Visit https://graspiq.in/register
2. Fill in: Full Name, Email, Phone
3. Create secure password
4. Verify email address
5. Complete your profile

📞 Need help? Contact: support@graspiq.in"""
    },
    "courses": {
        "title": "📚 GRASPIQ COURSES & PROGRAMS",
        "content": """**TECHNICAL TRAINING:**
• Data Structures & Algorithms
• System Design & Architecture
• Object-Oriented Programming
• Database Management Systems
• Operating Systems
• Computer Networks
• Software Engineering

**INTERVIEW PREPARATION:**
• Mock Technical Interviews
• Coding Practice Sessions
• Problem Solving Strategies
• Behavioral Interview Training
• Communication Skills
• Resume Building Workshops

**COMPANY-SPECIFIC PROGRAMS:**
• FAANG Company Preparation
• Startup Interview Guides
• Service Company Patterns
• Product Company Strategies

**RESUME & PROFILE:**
• Professional Resume Building
• ATS-Optimized Templates
• LinkedIn Profile Optimization
• Portfolio Development

**MENTORSHIP:**
• 1:1 Expert Guidance Sessions
• Career Counseling
• Progress Tracking
• Doubt Resolution
• Personalized Roadmaps

Visit: https://graspiq.in/courses for detailed information."""
    },
    "support": {
        "title": "📞 GRASPIQ SUPPORT & CONTACT",
        "content": """**Email:** support@graspiq.in
**Phone:** +91-9876543210
**WhatsApp:** +91-9876543210
**Website:** https://graspiq.in/contact

**OFFICE HOURS:**
Monday - Saturday: 9:00 AM - 6:00 PM IST
Sunday: Closed

**TECHNICAL SUPPORT:**
For login issues, website problems, or technical difficulties:
1. Clear browser cache and cookies
2. Try using Google Chrome browser
3. Check your internet connection
4. Take screenshot of the issue
5. Email support with details

**QUICK RESOLUTION:**
Please include your:
• Registered email address
• Detailed description of issue
• Screenshot (if applicable)
• Browser and device information

We're committed to helping you succeed!"""
    },
    "about": {
        "title": "🎯 WHAT IS GRASPIQ?",
        "content": """Think of us as your personal placement coach—available 24/7, affordable, and designed specifically for YOUR college, YOUR branch, and YOUR dream company.

**The Problem We Solve:**
You're preparing for placements, but:
• Generic test platforms don't match actual company patterns
• You don't know if you're ready for TCS vs. Infosys vs. Wipro
• Mock tests feel nothing like the real thing
• Branch-specific preparation? Almost impossible to find!

**Our Solution:**
Grasp IQ gives you company-specific, branch-specific test series that mirror actual placement exams—down to the pattern, difficulty level, and time pressure.

**What Makes Us Different?**
✅ Company-Specific Tests – Practice exactly what TCS, Wipro, Infosys, or Accenture will ask
✅ Branch-Tailored – CSE, ECE, Mechanical, Civil—each gets relevant questions
✅ Fully Proctored – Real exam experience with AI monitoring
✅ Affordable Plans – Quality prep without burning a hole in your pocket
✅ Live Mentorship – Monthly guest lectures from industry experts

**In Simple Words:**
"We help you practice the EXACT tests your dream companies will give you—so on placement day, you walk in confident, not confused."

**Coming Soon:**
• Interview preparation modules
• Government exam prep
• Video solutions for every question
• Mobile app for practice on-the-go

👉 Follow us: https://www.instagram.com/_graspiq_"""
    }
}

def detect_intent(question):
    """Detect the intent of the question"""
    question_lower = question.lower()
    
    # Greetings
    if any(keyword in question_lower for keyword in ['hello', 'hi', 'hey', 'greetings']):
        return "greeting"
    
    # GraspIQ specific intents
    if any(keyword in question_lower for keyword in ['company', 'companies', 'hire', 'recruit', 'tcs', 'infosys', 'wipro', 'faang']):
        return "company"
    elif any(keyword in question_lower for keyword in ['login', 'sign in', 'password', 'register', 'account', 'website']):
        return "login"
    elif any(keyword in question_lower for keyword in ['course', 'program', 'training', 'learn', 'study', 'syllabus']):
        return "courses"
    elif any(keyword in question_lower for keyword in ['support', 'help', 'contact', 'email', 'phone']):
        return "support"
    elif any(keyword in question_lower for keyword in ['what is', 'about grasp', 'graspiq', 'platform']):
        return "about"
    
    return "general"

def get_local_response(intent, question):
    """Get response from local knowledge base"""
    if intent in GRASPIQ_KNOWLEDGE:
        return GRASPIQ_KNOWLEDGE[intent]['content']
    
    # Greeting response
    if intent == "greeting":
        return """Hello! 👋 I'm your GraspIQ AI Assistant powered by SambaNova's DeepSeek-V3.1-Terminus!

I can help you with:
🏢 **Companies** - Which companies GraspIQ prepares for
🔐 **Login Help** - How to access your account
📚 **Courses** - Available training programs
📞 **Support** - Contact information
🎯 **Placement Tips** - Interview preparation advice
💼 **Career Guidance** - Resume building and interview skills
💻 **Technical Skills** - Coding and DSA guidance

What would you like to know about today?"""
    
    # General response
    return """I'm your AI Placement Assistant powered by SambaNova's DeepSeek-V3.1-Terminus! I can help you with:

🎯 **Placement & Career:**
• Interview preparation strategies
• Resume building and optimization
• Technical skill development (DSA, System Design)
• Company-specific guidance
• Career roadmap planning

🏢 **GraspIQ Services:**
• Company-specific test series
• Branch-tailored preparation (CSE, ECE, Mechanical, etc.)
• Mock interviews with feedback
• Expert mentorship programs
• Platform login and support

💡 **General Questions:**
Feel free to ask me anything about placements, technology, career advice, or general knowledge!

What would you like to know?"""

def query_sambanova_api(question, context=""):
    """Query SambaNova API using OpenAI SDK"""
    try:
        if context:
            system_prompt = f"""You are GraspIQ AI Assistant, an intelligent chatbot for the GraspIQ placement preparation platform.

CONTEXT INFORMATION:
{context}

YOUR ROLE:
1. Provide accurate, helpful information about GraspIQ services
2. For placement-related questions, offer practical, actionable advice
3. Format responses clearly with proper spacing and structure
4. Use bullet points only when listing multiple items
5. Keep responses professional, friendly, and student-focused
6. If asked about unrelated topics, provide helpful information or politely redirect

RESPONSE GUIDELINES:
- Start with a friendly greeting if appropriate
- Use clear headings with **bold** for important sections
- Keep paragraphs concise (2-3 lines maximum)
- End with a helpful suggestion or question
- Format lists with proper bullet points
- Be encouraging and supportive"""
        else:
            system_prompt = """You are GraspIQ AI Assistant, an intelligent career and placement advisor powered by SambaNova's DeepSeek-V3.1-Terminus.

YOUR CAPABILITIES:
1. Answer questions about placements, interviews, and career guidance
2. Provide technical and soft skills development advice
3. Offer study and preparation strategies
4. Help with resume building, LinkedIn optimization, and portfolio development
5. Guide on company research, interview preparation, and negotiation skills
6. Provide information about GraspIQ placement platform
7. Answer general knowledge questions with a focus on career relevance

RESPONSE STYLE:
- Professional yet approachable tone
- Practical, actionable advice
- Clear, organized formatting
- Concise paragraphs with proper spacing
- Use bullet points only for lists, not for single items
- Be encouraging, motivational, and supportive

SCOPE:
You can answer questions on any topic, but always try to relate it to career growth, skill development, or placement preparation when possible."""

        # Create messages for chat completion
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]

        # Using chat.completions.create for SambaNova
        completion = sambanova_client.chat.completions.create(
            model="DeepSeek-V3.1-Terminus",
            messages=messages,
            temperature=0.1,
            top_p=0.1,
            max_tokens=1024,
            stream=False
        )
        
        response = completion.choices[0].message.content
        return response
        
    except Exception as e:
        logger.error(f"SambaNova API query failed: {e}")
        return None

def clean_response(text):
    """Clean and format the response text"""
    if not text:
        return text
    
    # Remove excessive newlines
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    # Join with proper spacing
    return '\n\n'.join(cleaned_lines)

def generate_response(question):
    """Generate response using SambaNova API with local fallback"""
    start_time = time.time()
    
    # First, check for specific GraspIQ intents
    intent = detect_intent(question)
    
    # If it's a GraspIQ specific question, provide local context
    context = ""
    if intent in GRASPIQ_KNOWLEDGE:
        context = GRASPIQ_KNOWLEDGE[intent]['content']
    
    # Try to use SambaNova API
    if sambanova_client:
        try:
            sambanova_response = query_sambanova_api(question, context)
            if sambanova_response:
                response_time = time.time() - start_time
                logger.info(f"✅ SambaNova AI response generated in {response_time:.2f}s")
                cleaned_response = clean_response(sambanova_response)
                return cleaned_response, "ai_generated"
        except Exception as e:
            logger.warning(f"⚠️ SambaNova API failed, using fallback: {e}")
    
    # Fallback to local response
    local_response = get_local_response(intent, question)
    response_time = time.time() - start_time
    logger.info(f"📚 Local response generated in {response_time:.2f}s (intent: {intent})")
    
    return local_response, intent

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'answer': 'Please enter a question.'})
        
        logger.info(f"📨 User question: {question[:100]}...")
        
        # Generate response
        response, intent = generate_response(question)
        
        return jsonify({
            'answer': response,
            'intent': intent,
            'status': 'success',
            'api_available': sambanova_client is not None,
            'response_source': 'sambanova' if intent == 'ai_generated' else 'local',
            'model': 'DeepSeek-V3.1-Terminus' if sambanova_client else 'local_knowledge'
        })
        
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            'answer': "I'm here to help you with placement preparation, career guidance, and GraspIQ services. What would you like to know?",
            'status': 'success',
            'api_available': sambanova_client is not None,
            'response_source': 'fallback'
        })

@app.route('/stream', methods=['POST'])
def stream_chat():
    """Streaming chat endpoint for real-time responses"""
    def generate():
        try:
            data = request.json
            question = data.get('question', '').strip()
            
            if not question:
                yield "data: " + json.dumps({"error": "Please enter a question"}) + "\n\n"
                return
            
            if not sambanova_client:
                response = "I can help you with placement preparation and GraspIQ services. Please ask me any question."
                yield f"data: {json.dumps({'content': response})}\n\n"
                yield "data: [DONE]\n\n"
                return
            
            system_prompt = """You are GraspIQ AI Assistant, a helpful AI career and placement advisor.
            Provide professional, practical advice on placements, interviews, career development, and GraspIQ services.
            Format responses clearly and concisely."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
            
            stream = sambanova_client.chat.completions.create(
                model="DeepSeek-V3.1-Terminus",
                messages=messages,
                temperature=0.1,
                top_p=0.1,
                max_tokens=1024,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: {json.dumps({'content': "I can help with placement guidance. Please ask me a question."})}\n\n"
            yield "data: [DONE]\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions"""
    suggestions = [
        "How to prepare for technical interviews?",
        "What companies does GraspIQ work with?",
        "How to build a strong resume?",
        "Tell me about GraspIQ courses",
        "How to improve coding skills?",
        "What is System Design?",
        "How to crack FAANG interviews?",
        "Best DSA resources for beginners",
        "How GraspIQ helps with placements",
        "Soft skills for interviews",
        "How to login to GraspIQ?",
        "Company-specific preparation tips",
        "What is machine learning?",
        "How to learn Python programming?",
        "Career options for CS graduates"
    ]
    return jsonify({'suggestions': suggestions})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    samba_status = "connected" if sambanova_client else "disconnected"
    status_details = {
        'status': 'healthy',
        'service': 'GraspIQ AI Assistant',
        'mode': 'sambanova_ai' if sambanova_client else 'local_mode',
        'sambanova_status': samba_status,
        'model': 'DeepSeek-V3.1-Terminus' if sambanova_client else 'enhanced_local',
        'response_speed': 'fast' if sambanova_client else 'instant',
        'capabilities': [
            'Placement guidance & counseling',
            'Interview preparation strategies',
            'Resume building assistance',
            'Technical skills development',
            'Company-specific information',
            'GraspIQ platform guidance',
            'Career roadmap planning',
            'General knowledge queries'
        ],
        'features': [
            'AI-powered responses',
            'Enhanced knowledge base',
            'Professional advice',
            'Student-focused guidance',
            'Streaming responses available'
        ],
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(status_details)

@app.route('/api-status', methods=['GET'])
def api_status():
    """Check API status"""
    if sambanova_client:
        try:
            # Quick test
            start_time = time.time()
            test_response = sambanova_client.chat.completions.create(
                model="DeepSeek-V3.1-Terminus",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=0.1,
                top_p=0.1,
                max_tokens=10,
            )
            response_time = (time.time() - start_time) * 1000
            
            return jsonify({
                'status': 'active',
                'provider': 'SambaNova Cloud',
                'model': 'DeepSeek-V3.1-Terminus',
                'response_time_ms': round(response_time, 2),
                'capabilities': 'Full AI conversation on any topic',
                'streaming_supported': True,
                'sdk': 'OpenAI Python SDK'
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'provider': 'SambaNova Cloud',
                'error': str(e),
                'fallback_mode': True,
                'local_capabilities': 'Enhanced placement guidance'
            })
    else:
        return jsonify({
            'status': 'local_mode',
            'provider': 'Enhanced Knowledge Base',
            'capabilities': 'Complete placement and career guidance',
            'response_time': 'Instant',
            'knowledge_coverage': [
                'Placement strategies',
                'Interview techniques',
                'Resume building',
                'Technical skills',
                'Company information',
                'GraspIQ services'
            ]
        })

@app.route('/test-sambanova', methods=['GET'])
def test_sambanova():
    """Test SambaNova API connection"""
    if not sambanova_client:
        return jsonify({
            'status': 'error',
            'message': 'SambaNova client not initialized. Check your API key in .env file',
            'solution': 'Add SAMBA_API_KEY=your_key_here to your .env file'
        })
    
    try:
        start_time = time.time()
        
        response = sambanova_client.chat.completions.create(
            model="DeepSeek-V3.1-Terminus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'SambaNova API is working with OpenAI SDK!'"}
            ],
            temperature=0.1,
            top_p=0.1,
            max_tokens=20,
        )
        
        response_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'status': 'success',
            'message': 'SambaNova API is working correctly!',
            'response': response.choices[0].message.content,
            'response_time_ms': round(response_time, 2),
            'model': 'DeepSeek-V3.1-Terminus',
            'sdk_method': 'OpenAI Python SDK'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'SambaNova API test failed',
            'error': str(e),
            'solution': 'Check your API key and internet connection'
        })

@app.route('/models', methods=['GET'])
def get_models():
    """Get available SambaNova models"""
    if not sambanova_client:
        return jsonify({
            'status': 'error',
            'message': 'SambaNova client not initialized'
        })
    
    try:
        # Return common SambaNova models
        models = [
            {
                'id': 'DeepSeek-V3.1-Terminus',
                'name': 'DeepSeek V3.1 Terminus',
                'description': 'Powerful model with high performance on coding and reasoning tasks',
                'max_tokens': 32768,
                'context_window': 32768
            },
            {
                'id': 'Llama-3.2-3B-Instruct',
                'name': 'Llama 3.2 3B Instruct',
                'description': 'Lightweight model for fast inference',
                'max_tokens': 8192,
                'context_window': 8192
            },
            {
                'id': 'Llama-3.1-8B-Instruct',
                'name': 'Llama 3.1 8B Instruct',
                'description': 'Balanced model for general purpose tasks',
                'max_tokens': 8192,
                'context_window': 8192
            },
            {
                'id': 'Llama-3.1-70B-Instruct',
                'name': 'Llama 3.1 70B Instruct',
                'description': 'High-performance model for complex reasoning',
                'max_tokens': 8192,
                'context_window': 8192
            }
        ]
        
        return jsonify({
            'status': 'success',
            'models': models,
            'default_model': 'DeepSeek-V3.1-Terminus'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch models',
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info("=" * 50)
    logger.info("🚀 Starting GraspIQ AI Assistant")
    logger.info(f"🔧 Mode: {'SambaNova AI Enabled' if sambanova_client else 'Local Mode'}")
    logger.info(f"🐛 Debug: {debug_mode}")
    logger.info(f"🔌 Port: {port}")
    logger.info(f"🤖 Model: {'DeepSeek-V3.1-Terminus' if sambanova_client else 'Enhanced Local'}")
    logger.info(f"📦 SDK: {'OpenAI Python SDK' if sambanova_client else 'Local'}")
    logger.info("=" * 50)
    
    if not sambanova_client:
        logger.warning("⚠️  WARNING: SambaNova API key not found or invalid!")
        logger.info("💡 Tip: Add SAMBA_API_KEY=your_key_here to your .env file")
        logger.info("📚 Using enhanced local knowledge base for now")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)