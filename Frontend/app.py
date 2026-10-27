import streamlit as st
import requests
import sys
import os
import json
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Shared.pdf_generator import generate_pdf

# Initialize session state for persistent data
if 'career_plan_generated' not in st.session_state:
    st.session_state['career_plan_generated'] = False
if 'pdf_bytes' not in st.session_state:
    st.session_state['pdf_bytes'] = None
if 'pdf_filename' not in st.session_state:
    st.session_state['pdf_filename'] = None

# Page configuration
st.set_page_config(
    page_title="AI Career Path Recommender",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clean design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        animation: slideInDown 1s ease-out;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .career-card {
        background: #1e1e2e;
        color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #2d2d44;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .career-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        border-color: #667eea;
    }
    
    .career-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .career-number {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .skill-tag {
        background: #2d2d44;
        color: #ffffff;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
        border: 1px solid #3d3d54;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    .form-container {
        background: #1e1e2e;
        color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #2d2d44;
        margin-bottom: 2rem;
    }
    
    .pdf-section {
        background: #1e1e2e;
        color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #2d2d44;
    }
    
    .insight-section {
        background: #2d2d44;
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .loading-container {
        background: #1e1e2e;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid #2d2d44;
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .download-btn {
        background: linear-gradient(90deg, #4CAF50, #45a049) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .download-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Career Insights")
    
    st.markdown("### 📈 Market Trends")
    st.markdown("""
    - **AI/ML**: 40% growth expected
    - **Cloud Computing**: 35% growth expected  
    - **Cybersecurity**: 30% growth expected
    - **Data Science**: 25% growth expected
    """)
    
    st.markdown("### 💰 Salary Ranges")
    st.markdown("""
    - **Entry Level**: $50K - $80K
    - **Mid Level**: $80K - $120K
    - **Senior Level**: $120K - $200K+
    """)
    
# Main header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; text-align: center; margin: 0;">🚀 AI-Powered Career Path Recommender</h1>
    <p style="color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;">
        Discover your perfect career path with AI-driven insights and personalized recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# Form
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    with st.form("career_form", clear_on_submit=False):
        st.markdown("### 📝 Tell Us About Yourself")
        
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_area("🛠️ Your Skills & Technologies", 
                                placeholder="e.g., Python, JavaScript, Machine Learning, AWS, React...")
            interests = st.text_area("🎯 Your Interests & Passions", 
                                   placeholder="e.g., AI, Web Development, Data Analysis, Cybersecurity...")
            personality = st.text_area("🧠 Your Personality Traits", 
                                     placeholder="e.g., Analytical, Creative, Leadership, Problem-solving...")
        
        with col2:
            location = st.text_input("📍 Your Location", placeholder="e.g., New York, Remote, India...")
            education = st.selectbox("🎓 Education Level", 
                                   ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Self-taught"])
            experience = st.selectbox("💼 Years of Experience", 
                                    ["0-1 years", "2-3 years", "4-6 years", "7-10 years", "10+ years"])
            salary_expectation = st.selectbox("💰 Salary Expectation", 
                                            ["$30K-$50K", "$50K-$80K", "$80K-$120K", "$120K-$200K", "$200K+"])
        
        submitted = st.form_submit_button("🚀 Get AI Recommendations", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Function to render recommendations - SIMPLE AND CLEAN
def render_enhanced_recommendations(data: dict, user_input: dict = None) -> None:
    """Simple, clean UI for career recommendations."""
    
    # Simple metrics
    st.markdown("## 🎯 Your Career Roadmap")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Career Paths", "4", "Recommended")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Market Demand", "High", "Growing")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Salary Range", "$80K-$150K", "Average")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Growth Rate", "25%", "Annual")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Get career paths
    career_paths = []
    if isinstance(data, dict):
        career_paths = data.get("careerPaths") or data.get("paths") or []
    
    if not career_paths and isinstance(data, dict):
        st.json(data)
        return
    
    # Ensure exactly 4 career paths
    if len(career_paths) < 4:
        placeholder_paths = [
            {"careerTitle": "Software Engineer", "skillsToDevelop": ["Programming", "System Design"], "shortTermGoals": ["Learn new technologies"], "longTermGoals": ["Become tech lead"]},
            {"careerTitle": "Data Analyst", "skillsToDevelop": ["SQL", "Python"], "shortTermGoals": ["Build portfolio"], "longTermGoals": ["Lead data projects"]},
            {"careerTitle": "Product Manager", "skillsToDevelop": ["Product Strategy", "User Research"], "shortTermGoals": ["Get PM certification"], "longTermGoals": ["Launch successful products"]},
            {"careerTitle": "DevOps Engineer", "skillsToDevelop": ["Cloud Platforms", "Automation"], "shortTermGoals": ["Learn AWS/Azure"], "longTermGoals": ["Architect cloud solutions"]}
        ]
        career_paths.extend(placeholder_paths[:4-len(career_paths)])
    
    # Display career paths - SIMPLE AND CLEAN
    for idx, path in enumerate(career_paths[:4]):
        title = path.get("careerTitle", f"Career Option {idx + 1}")
        
        st.markdown(f'<div class="career-card">', unsafe_allow_html=True)
        
        # Clean header
        st.markdown(f'''
        <div class="career-header">
            <h3 style="margin: 0; font-size: 1.3rem;">🎯 {title}</h3>
            <div class="career-number">#{idx + 1}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Skills section - SIMPLE
        skills = path.get("skillsToDevelop") or []
        if skills:
            st.markdown("**🛠️ Key Skills to Develop**")
            skill_tags = " ".join([f'<span class="skill-tag">{skill}</span>' for skill in skills[:6]])
            st.markdown(skill_tags, unsafe_allow_html=True)
            st.markdown("---")
        
        # Simple expandable sections
        with st.expander(f"📚 Detailed Roadmap for {title}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                # Short-term goals
                short_goals = path.get("shortTermGoals") or []
                if short_goals:
                    st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                    st.markdown("**🎯 Short-term Goals (3-6 months)**")
                    for goal in short_goals:
                        st.markdown(f"• {goal}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Certifications
                certs = path.get("recommendedCertifications") or []
                if certs:
                    st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                    st.markdown("**🎓 Recommended Certifications**")
                    for cert in certs:
                        st.markdown(f"• {cert}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                # Long-term goals
                long_goals = path.get("longTermGoals") or []
                if long_goals:
                    st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                    st.markdown("**🚀 Long-term Goals (1-3 years)**")
                    for goal in long_goals:
                        st.markdown(f"• {goal}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Market insights
                market = path.get("marketInsights")
                if market:
                    st.markdown('<div class="insight-section">', unsafe_allow_html=True)
                    st.markdown("**📈 Market Insights**")
                    st.info(market)
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # Motivational advice - SIMPLE
        advice = path.get("motivationalAdvice")
        if advice:
            st.markdown("**💡 Motivational Advice**")
            st.markdown(advice)
            st.markdown("---")
        
        # Simple progress indicators
        st.markdown("**📊 Progress Indicators**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Technical Skills**")
            st.progress(0.7)
            st.markdown("*70%*")
        with col2:
            st.markdown("**Market Demand**")
            st.progress(0.8)
            st.markdown("*High*")
        with col3:
            st.markdown("**Salary Potential**")
            st.progress(0.6)
            st.markdown("*Growing*")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Career Plan Download section - SIMPLE AND RELIABLE
    st.markdown('<div class="pdf-section">', unsafe_allow_html=True)
    st.markdown("## 📄 Download Your Career Plan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **🎯 Generate a comprehensive career plan** including:
        
        ✨ **Career Analysis**
        - Detailed career path recommendations
        - Skills gap analysis and development roadmap
        - Market insights and salary projections
        
        🚀 **Action Plan**
        - Short-term and long-term goals
        - Recommended certifications and courses
        - Networking and portfolio building strategies
        """)
    
    with col2:
        st.markdown("### 📥 Download Options")
        
        # Generate Career Plan button - SIMPLE AND RELIABLE
        if st.button("🎯 Generate Career Plan", use_container_width=True, type="primary", key="generate_plan_inside"):
            try:
                with st.spinner("🔄 Generating your career plan..."):
                    # Create data for the file
                    plan_data = {
                        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                        "career_paths": career_paths,
                        "user_input": user_input or {}
                    }
                    
                    plan_input = json.dumps(plan_data, indent=2)
                    
                    # Generate PDF with simple error handling
                    try:
                        st.info(f"🔍 Debug: career_paths has {len(career_paths)} items")
                        st.info(f"🔍 Debug: plan_data created with {len(plan_input)} characters")
                        
                        file_path = generate_pdf(plan_input)
                        st.success("✅ Career plan generated successfully!")
                        
                        # Store the file path in session state
                        if file_path and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                            st.session_state['pdf_file_path'] = file_path
                            st.session_state['pdf_filename'] = os.path.basename(file_path)
                            st.session_state['career_plan_generated'] = True
                            
                            st.info("💡 **Tip**: Your PDF is ready! Check the download section below.")
                            
                            # Show success info
                            file_name = os.path.basename(file_path)
                            downloads_folder = os.path.dirname(file_path)
                            st.success(f"📁 **File saved successfully!**")
                            st.success(f"📂 **Location**: `{downloads_folder}`")
                            st.success(f"📄 **Filename**: `{file_name}`")
                            st.success(f"📊 **File size**: {os.path.getsize(file_path)} bytes")
                            
                        else:
                            st.error("❌ File was not created successfully or is empty")
                            if file_path:
                                st.error(f"File path: {file_path}")
                                st.error(f"File exists: {os.path.exists(file_path)}")
                                if os.path.exists(file_path):
                                    st.error(f"File size: {os.path.getsize(file_path)} bytes")
                        
                    except Exception as file_error:
                        st.error(f"❌ File generation error: {file_error}")
                        st.info("Please try again or contact support if the issue persists.")
                    
            except Exception as e:
                st.error(f"❌ General error: {e}")
                st.info("Please try again or contact support if the issue persists.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
# GLOBAL DOWNLOAD SECTION - Simple and Reliable
if st.session_state.get('career_plan_generated', False) and st.session_state.get('pdf_file_path'):
    st.markdown("---")
    st.markdown("## 📥 Your Career Plan PDF is Ready!")
    
    # Show file information
    file_path = st.session_state['pdf_file_path']
    file_name = st.session_state['pdf_filename']
    
    if file_path and os.path.exists(file_path):
        # Get file size
        file_size = os.path.getsize(file_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        st.success("✅ **PDF Generated Successfully!**")
        
        # File details
        col1, col2, col3 = st.columns(3)
    with col1:
            st.metric("📄 File Name", file_name)
            with col2:
                st.metric("📊 File Size", f"{file_size_mb} MB")
            with col3:
                st.metric("📍 Location", "downloads folder")
            
        # Instructions
            st.info("""
            **📥 How to Download Your PDF:**
            
            1. **Open File Explorer** (Windows key + E)
            2. **Navigate to**: `C:\\Users\\OM\\Desktop\\career_recommender\\downloads\\`
            3. **Find your file**: `{file_name}`
            4. **Right-click** and select "Copy" or drag to your desired folder
            
            **💡 Alternative**: Use the "Open Downloads Folder" button below!
            """.format(file_name=file_name))
            
            # Action buttons
            col1, col2 = st.columns(2)
            
    with col1:
            if st.button("📂 Open Downloads Folder", use_container_width=True, key="open_folder"):
                import subprocess
                import platform
                try:
                    downloads_folder = os.path.dirname(file_path)
                    if platform.system() == "Windows":
                        subprocess.run(["explorer", downloads_folder])
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", downloads_folder])
                    else:  # Linux
                        subprocess.run(["xdg-open", downloads_folder])
                    st.success("📂 Downloads folder opened!")
                except Exception as e:
                    st.error(f"Could not open folder: {e}")
        
    with col2:
            if st.button("🔄 Generate New Plan", use_container_width=True, key="clear_plan"):
                # Clear session state
                for key in ['pdf_file_path', 'pdf_filename', 'career_plan_generated']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        # File preview info
                st.info(f"**🔍 File Details**: `{file_path}`")
        
            else:
                 st.error("❌ PDF file not found. Please try generating again.")
        # Clear invalid session state
            for key in ['pdf_file_path', 'pdf_filename', 'career_plan_generated']:
                if key in st.session_state:
                    del st.session_state[key]

# Main recommendation logic - ONLY RUNS ONCE
if submitted:
    # Add a container for better loading state
    with st.container():
        st.markdown('<div class="loading-container">', unsafe_allow_html=True)
        
        with st.spinner("🤖 AI is analyzing your profile and generating personalized recommendations..."):
            # Simple loading animation
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simple steps
            steps = [
                "Analyzing your profile...",
                "Generating career paths...",
                "Creating recommendations...",
                "Finalizing results..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(step)
                progress = int((i + 1) * 100 / len(steps))
                progress_bar.progress(progress)
                time.sleep(0.2)  # Fast loading
            
            try:
                response = requests.post(
                    "http://localhost:8000/recommend",
                    json={
                        "skills": skills,
                        "interests": interests,
                        "personality": personality,
                        "location": location,
                        "education": education,
                        "experience": experience,
                        "salary_expectation": salary_expectation
                    },
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
            except Exception as exc:
                st.error(f"❌ Backend request failed: {exc}")
                data = {"ok": False, "error": str(exc)}

        def _strip_code_fences(text: str) -> str:
            t = text.strip()
            if t.startswith("```"):
                first_newline = t.find("\n")
                if first_newline != -1:
                    t = t[first_newline + 1 :]
                if t.endswith("```"):
                    t = t[: -3]
            return t.strip()

        def _clean_json_string(text: str) -> str:
            """Clean and fix common JSON formatting issues"""
            text = text.strip()
            if text.startswith("v"):
                text = text[1:]
            text = text.replace("\\n", " ")
            text = text.replace("\\t", " ")
            text = text.replace("\\r", " ")
            import re
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

        if data.get("ok"):
            st.success("✅ AI Analysis Complete!")
            
            rec_text = str(data.get("recommendations", "")).strip()
            cleaned = _strip_code_fences(rec_text)
            cleaned = _clean_json_string(cleaned)
            
            try:
                parsed = json.loads(cleaned)
                # Pass user input to the function
                user_input_data = {
                    "skills": skills,
                    "interests": interests,
                    "personality": personality,
                    "location": location,
                    "education": education,
                    "experience": experience,
                    "salary_expectation": salary_expectation
                }
                # Call the function ONCE
                render_enhanced_recommendations(parsed, user_input_data)
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON parsing error: {e}")
                st.markdown("### 📊 Raw Recommendations")
                st.markdown(rec_text)
            except Exception as e:
                st.error(f"❌ Error processing recommendations: {e}")
                st.markdown("### 📊 Your Career Recommendations")
                st.markdown(rec_text)
        else:
            st.error(f"❌ {data.get('error', 'Unknown error')}")
        
            st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; opacity: 0.8;">
    <p>🚀 Powered by AI • Built with Streamlit • Your Career Journey Starts Here</p>
    <p>Generated on: {}</p>
</div>
""".format(datetime.now().strftime("%B %d, %Y at %I:%M %p")), unsafe_allow_html=True)

