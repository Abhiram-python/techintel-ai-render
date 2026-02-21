"""
TechIntel AI - Flask Backend
Complete backend integration for the premium modern SaaS frontend

This is a starter template showing how to integrate the frontend with Flask.
Customize the endpoints and logic based on your database and API requirements.
"""

import os

from flask import Flask, render_template, request, jsonify, session
# from flask_cors import CORS
from functools import wraps
import json
from datetime import datetime


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your-secret-key-change-this'

# Enable CORS for all routes (allows frontend on different domain)

# CORS(app)

from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://stupendous-yeot-7f0b3c.netlify.app","https://jazzy-choux-ffc9f1.netlify.app","https://glowing-conkies-bb77df.netlify.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

########## serp api and google gemini integration for hackathon data extraction and formatting

from google import genai

from serpapi import GoogleSearch

########### Using the SerpAPI to get search results for a query

# params = {
#   "q": "hackathons near me",
#   "location": "hyderabad, telangana, india",
#   "hl": "en",
#   "gl": "us",
#   "google_domain": "google.com",
#   "api_key": "7fcde04d134888de2c1e72749f75b98445a94420088b19a1249f3b5d970497c7"
# }

# search = GoogleSearch(params)
# results = search.get_dict()

############# Using the Google Gemini API to generate content based on the search results

# import os

print("GENAI_API_KEY:", os.getenv("GENAI_API_KEY"))  # Should not be None or empty

api_key = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents=f'''from the results of the search{results} go through all the sites and give a list or dictionarys which have id,name,date,location,organization,description and link of the hackathons.
#     i want all this in this format:
#     [
#         {{
#             "id": "1",
#             "name": "Hackathon 1",
#             "event_type": "Virtual",
#             "date": "2024-07-01",
#             "location": "Hyderabad, Telangana, India",
#             "organizer": "Organization 1",
#             "description": "Description of Hackathon 1",
#             "link": "https://example.com/hackathon1"
#         }},
#         {{
#             "id": "2",
#             "name": "Hackathon 2",
#             "event_type": "In-Person",
#             "date": "2024-08-15",
#             "location": "Hyderabad, Telangana, India",
#             "organizer": "Organization 2",
#             "description": "Description of Hackathon 2",
#             "link": "https://example.com/hackathon2"
#         }},
#     ] and note don't give any other text except the list of dictionarys. and date should only be on start date of the hackathon
#      and i want all which are listed in the search results like 10''',
# )

# print(response.text)

def search_results(q):
    params = {
        "q": q,
        "location": "hyderabad, telangana, india",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "7fcde04d134888de2c1e72749f75b98445a94420088b19a1249f3b5d970497c7"
    }

    search = GoogleSearch(params)
    results=search.get_dict()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f'''from the results of the search{results} go through all the sites and give a list or dictionarys which have id,name,date,location,organization,description and link of the Engagements.
        i want all this in this format:
        [
            {{
                "id": "1",
                "name": "Engagements 1",
                "event_type": "Virtual",
                "date": "2024-07-01",
                "location": "Hyderabad, Telangana, India",
                "organizer": "Organization 1",
                "description": "Description of Engagements 1",
                "link": "https://example.com/Engagements1"
            }},
            {{
                "id": "2",
                "name": "Engagements 2",
                "event_type": "In-Person",
                "date": "2024-08-15",
                "location": "Hyderabad, Telangana, India",
                "organizer": "Organization 2",
                "description": "Description of Engagements 2",
                "link": "https://example.com/Engagements2"
            }},
        ] and note don't give any other text except the list of dictionarys. and date should only be on start date of the Engagements and i want all which are listed in the search results like 10''',
    )

    return response.text

responsehackathons = search_results("hackathons in Hyderabad")
responsesummits = search_results("summits in hyderabad")
responseinternships = search_results("internships in Hyderabad")

# ============================================================================
# Authentication Middleware
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# Page Routes
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return "chad"

# @app.route('/hackathons')
# def hackathons():
#     """Hackathons page"""
#     return render_template('hackathons.html')

# @app.route('/summits')
# def summits():
#     """Tech Summits page"""
#     return render_template('summits.html')

# @app.route('/internships')
# def internships():
#     """Internships listing page"""
#     return render_template('internships.html')

# @app.route('/resume')
# def resume():
#     """Resume upload page"""
#     return render_template('resume.html')

# @app.route('/recommendations')
# def recommendations():
#     """AI Recommendations page"""
#     return render_template('recommendations.html')

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     """User dashboard page"""
#     return render_template('dashboard.html')

# @app.route('/login')
# def login():
#     """Login page"""
#     return render_template('login.html')

# @app.route('/signup')
# def signup():
#     """Signup page"""
#     return render_template('signup.html')

# ============================================================================
# API Routes - Authentication
# ============================================================================

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login endpoint"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # TODO: Implement actual authentication with database
    # This is a placeholder - implement with your user model
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Example: Verify credentials against database
    # user = User.query.filter_by(email=email).first()
    # if user and user.check_password(password):
    #     session['user_id'] = user.id
    #     return jsonify({'token': generate_token(user), 'user': user.to_dict()})

    session['user_id'] = 'user_123'  # Replace with actual user ID
    return jsonify({
        'token': 'sample-jwt-token',
        'user': {
            'id': 'user_123',
            'email': email,
            'name': 'User Name'
        }
    })

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """User signup endpoint"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    university = data.get('university')

    if not all([name, email, password]):
        return jsonify({'error': 'name, email, and password required'}), 400

    # TODO: Implement user creation
    # Check if user exists
    # Hash password
    # Create user in database
    # user = User.create(name=name, email=email, password=password, university=university)

    session['user_id'] = 'user_new_123'
    return jsonify({
        'token': 'sample-jwt-token',
        'user': {
            'id': 'user_new_123',
            'name': name,
            'email': email
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """User logout endpoint"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

# ============================================================================
# API Routes - Hackathons
# ============================================================================

@app.route('/api/hackathons', methods=['GET'])
def api_hackathons():
    """Get all hackathons"""

    data_list = json.loads(responsehackathons)  # now it's a Python list of dicts

    return jsonify({'data': data_list})

# ============================================================================
# API Routes - Summits
# ============================================================================

@app.route('/api/summits', methods=['GET'])
def api_summits():
    """Get all tech summits"""

    data_list= json.loads(responsesummits)

    return jsonify({'data': data_list})

# ============================================================================
# API Routes - Internships
# ============================================================================

@app.route('/api/internships', methods=['GET'])
def api_internships():
    """Get all internships"""
    
    data_list= json.loads(responseinternships)

    return jsonify({'data': data_list})

@app.route('/api/internships/search', methods=['GET'])
def api_search_internships():
    """Search internships with filters"""
    location = request.args.get('location', '').lower()
    job_type = request.args.get('type', '').lower()

    # Get all internships and filter
    # TODO: Implement database query with filters
    internships = [
        {
            'id': 1,
            'company': 'Google',
            'role': 'Software Engineer Intern',
            'location': 'Mountain View, CA',
            'type': 'Onsite',
            'salary': '$50,000 - $65,000',
            'description': 'Join Google\'s engineering team and work on world-class projects.',
            'apply_link': 'https://google.com/careers'
        }
    ]

    # Filter by location if provided
    if location:
        internships = [j for j in internships if location in j['location'].lower()]

    # Filter by type if provided
    if job_type:
        internships = [j for j in internships if job_type == j['type'].lower()]

    return jsonify({'data': internships})

# ============================================================================
# API Routes - Resume & Recommendations
# ============================================================================

@app.route('/api/resume/upload', methods=['POST'])
def api_upload_resume():
    """Handle resume upload and store data"""
    # TODO: Store file and user preferences
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    file = request.files['resume']
    location = request.form.get('location', '')
    internship_type = request.form.get('internship_type', '')
    expected_salary = request.form.get('expected_salary', '')
    additional_info = request.form.get('additional_info', '')

    # TODO: Save file to storage
    # TODO: Parse resume with AI
    # TODO: Extract skills and experience
    # TODO: Generate recommendations

    session['user_id'] = 'user_from_resume'
    session['preferences'] = {
        'location': location,
        'type': internship_type,
        'salary': expected_salary
    }

    return jsonify({
        'success': True,
        'message': 'Resume uploaded successfully',
        'file': file.filename
    })

@app.route('/api/recommendations', methods=['GET'])
def api_recommendations():
    """Get AI-powered internship recommendations"""
    # TODO: Fetch user's resume data
    # TODO: Run AI matching algorithm
    # TODO: Rank internships by match score
    
    recommendations = [
        {
            'id': 1,
            'company': 'Google',
            'role': 'Software Engineer Intern',
            'location': 'Mountain View, CA',
            'salary': '$50,000 - $65,000',
            'description': 'Join Google\'s engineering team.',
            'match_score': 95,
            'reason': 'Excellent match with your backend development skills and experience with Python.',
            'apply_link': 'https://google.com/careers'
        },
        {
            'id': 2,
            'company': 'Microsoft',
            'role': 'AI/ML Intern',
            'location': 'Remote',
            'salary': '$45,000 - $60,000',
            'description': 'Develop AI solutions with Microsoft.',
            'match_score': 88,
            'reason': 'Strong match based on your machine learning projects.',
            'apply_link': 'https://microsoft.com/careers'
        },
        {
            'id': 3,
            'company': 'Meta',
            'role': 'Full Stack Intern',
            'location': 'Menlo Park, CA',
            'salary': '$55,000 - $70,000',
            'description': 'Build scalable systems at Meta.',
            'match_score': 85,
            'reason': 'Good fit for your full-stack development experience.',
            'apply_link': 'https://meta.com/careers'
        }
    ]
    return jsonify({'data': recommendations})

# ============================================================================
# API Routes - Dashboard
# ============================================================================

@app.route('/api/dashboard', methods=['GET'])
@login_required
def api_dashboard():
    """Get user dashboard data"""
    # TODO: Fetch from database based on session user_id
    dashboard_data = {
        'user': {
            'id': session.get('user_id'),
            'name': 'John Doe',
            'email': 'john@example.com',
            'location': 'San Francisco, CA',
            'joined_date': 'January 2026'
        },
        'applications_count': 5,
        'interviews_count': 2,
        'saved_jobs_count': 12,
        'profile_views': 8,
        'resume_updated': 'Today',
        'recent_applications': [
            {
                'company': 'Google',
                'role': 'Software Engineer Intern',
                'status': 'Interview',
                'applied_date': '2 days ago'
            },
            {
                'company': 'Microsoft',
                'role': 'AI/ML Intern',
                'status': 'Applied',
                'applied_date': '5 days ago'
            }
        ],
        'recommended_companies': [
            {
                'name': 'Google',
                'open_positions': 5,
                'website': 'https://google.com'
            },
            {
                'name': 'Microsoft',
                'open_positions': 3,
                'website': 'https://microsoft.com'
            },
            {
                'name': 'Meta',
                'open_positions': 4,
                'website': 'https://meta.com'
            }
        ]
    }
    return jsonify(dashboard_data)

# ============================================================================
# API Routes - User Profile
# ============================================================================

@app.route('/api/user/profile', methods=['GET'])
@login_required
def api_get_profile():
    """Get user profile"""
    # TODO: Fetch from database
    return jsonify({
        'id': session.get('user_id'),
        'name': 'John Doe',
        'email': 'john@example.com',
        'university': 'Stanford University',
        'location': 'San Francisco, CA'
    })

# ============================================================================
# API Routes - Internship Applications
# ============================================================================

@app.route('/api/internships/<int:internship_id>/apply', methods=['POST'])
@login_required
def api_apply_internship(internship_id):
    """Apply for an internship"""
    # TODO: Create application record in database
    return jsonify({
        'success': True,
        'message': 'Application submitted successfully',
        'internship_id': internship_id,
        'user_id': session.get('user_id')
    })

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Run Application
# ============================================================================

# if __name__ == '__main__':
#     # Development
#     app.run(debug=True, host='0.0.0.0', port=5000)

#     # Production: Use gunicorn
#     # gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
