import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import requests
import json

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .main-header h1 { margin: 0; font-size: 2.2rem; }
    .main-header p  { margin: 0.5rem 0 0; opacity: 0.9; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📄 AI Resume & Portfolio Builder</h1>
    <p>Powered by Google Gemini 2.0 Flash — Build stunning resumes in seconds</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get free key at https://aistudio.google.com/"
    )
    if api_key:
        st.success("✅ API Key saved")
    else:
        st.warning("⚠️ Enter your Gemini API key")
        st.markdown("[Get free API key →](https://aistudio.google.com/)")

    st.divider()
    st.markdown("### 📋 Features")
    st.markdown("""
- 📝 Resume Builder
- 💼 Portfolio Builder
- 🔍 ATS Score Checker
- 💌 Cover Letter Generator
- 🔗 LinkedIn Summary
- 📊 Skills Gap Analyser
""")

# ─────────────────────────────────────────────
# Helper: Call Gemini via REST API (no SDK needed)
# ─────────────────────────────────────────────
def call_gemini(prompt: str) -> str:
    if not api_key:
        return "⚠️ Please enter your Gemini API key in the sidebar first."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "maxOutputTokens": 2048,
                "temperature": 0.7
            }
        }
        response = requests.post(url, headers=headers, json=body, timeout=60)
        data = response.json()

        if response.status_code != 200:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            if "API_KEY" in error_msg.upper() or "invalid" in error_msg.lower():
                return "❌ Invalid API key. Get yours at https://aistudio.google.com/"
            elif "quota" in error_msg.lower():
                return "❌ API quota exceeded. Check your Google AI Studio quota."
            else:
                return f"❌ API Error: {error_msg}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.Timeout:
        return "❌ Request timed out. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Resume",
    "💼 Portfolio",
    "🔍 ATS Checker",
    "💌 Cover Letter",
    "🔗 LinkedIn",
    "📊 Skills Gap"
])

# ═══════════════════════════════════════════
# TAB 1 — RESUME BUILDER
# ═══════════════════════════════════════════
with tab1:
    st.header("📝 Resume Builder")
    st.markdown("Fill in your details and get a professional resume instantly.")

    with st.expander("👤 Personal Information", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("Full Name *", placeholder="Sravani Reddy")
            email    = st.text_input("Email *", placeholder="sravani@email.com")
            phone    = st.text_input("Phone *", placeholder="+91 98765 43210")
        with c2:
            location = st.text_input("Location", placeholder="Hyderabad, Telangana")
            linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/sravani")
            github   = st.text_input("GitHub URL", placeholder="github.com/sravani")

    with st.expander("🎯 Career Objective", expanded=True):
        objective = st.text_area("Career Objective / Summary", height=100,
            placeholder="Motivated final-year B.Tech CSE student seeking a software development role...")

    with st.expander("🎓 Education", expanded=True):
        education = st.text_area("Education Details", height=120,
            placeholder="B.Tech CSE, RGUKT RK Valley — 2021 to 2025, CGPA: 8.7\nIntermediate, Narayana JC — 2019-2021, 95%")

    with st.expander("💼 Work Experience", expanded=True):
        experience = st.text_area("Internships / Work Experience", height=130,
            placeholder="Software Intern — ABC Tech (Jun–Aug 2024)\n- Built REST APIs with FastAPI\n- If fresher, write: Fresher")

    with st.expander("🛠️ Skills", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            tech_skills = st.text_area("Technical Skills", height=100,
                placeholder="Python, Java, React.js, Node.js, SQL, MongoDB, Git, Docker")
        with c2:
            soft_skills = st.text_area("Soft Skills", height=100,
                placeholder="Problem Solving, Team Leadership, Communication")

    with st.expander("🚀 Projects", expanded=True):
        projects = st.text_area("Projects", height=150,
            placeholder="AI Resume Builder\n- Built with Streamlit + Gemini API\n- Tech: Python, Streamlit\n\nE-Commerce Website\n- Full stack with React + Node.js")

    with st.expander("🏆 Achievements & Certifications", expanded=False):
        achievements = st.text_area("Achievements / Certifications", height=100,
            placeholder="AWS Cloud Practitioner Certified\n2nd Place — State Hackathon 2024\nGoogle Data Analytics Certificate")

    with st.expander("⚙️ Resume Settings", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            job_role = st.text_input("Target Job Role *", placeholder="Backend Developer")
        with c2:
            resume_style = st.selectbox("Resume Style", [
                "ATS-Optimised (Recommended)", "Professional",
                "Fresher / Entry-Level", "Creative", "Technical / Engineering"
            ])
        with c3:
            experience_level = st.selectbox("Experience Level", [
                "Fresher (0 years)", "Junior (1-2 years)",
                "Mid-Level (3-5 years)", "Senior (5+ years)"
            ])

    if st.button("✨ Generate My Resume", key="gen_resume"):
        if not name or not email or not job_role:
            st.error("Please fill in Name, Email, and Target Job Role.")
        else:
            with st.spinner("🤖 Gemini is crafting your resume..."):
                prompt = f"""You are an expert resume writer. Create a complete, professional, ATS-friendly resume.

Style: {resume_style} | Target Role: {job_role} | Level: {experience_level}

CANDIDATE DETAILS:
Name: {name} | Email: {email} | Phone: {phone} | Location: {location}
LinkedIn: {linkedin} | GitHub: {github}

Objective: {objective}

Education:
{education}

Experience:
{experience}

Technical Skills: {tech_skills}
Soft Skills: {soft_skills}

Projects:
{projects}

Achievements:
{achievements}

INSTRUCTIONS:
1. Use clear sections: CONTACT INFO, OBJECTIVE, EDUCATION, EXPERIENCE, SKILLS, PROJECTS, ACHIEVEMENTS
2. Use bullet points with strong action verbs (Built, Developed, Designed, Implemented)
3. Quantify achievements where possible
4. Include ATS keywords for role: {job_role}
5. Format cleanly for direct copy into Word/Google Docs
6. One page worth of content

Generate the complete resume now:"""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ Resume generated!")
                    st.text_area("Your Resume — copy and paste into Word/Google Docs:", result, height=550)
                    st.download_button("⬇️ Download as .txt", result,
                        file_name=f"{name.replace(' ', '_')}_Resume.txt", mime="text/plain")

# ═══════════════════════════════════════════
# TAB 2 — PORTFOLIO BUILDER
# ═══════════════════════════════════════════
with tab2:
    st.header("💼 Portfolio Builder")
    st.markdown("Generate compelling content for your personal portfolio website.")

    c1, c2 = st.columns(2)
    with c1:
        p_name    = st.text_input("Your Name *", key="p_name", placeholder="Sravani Reddy")
        p_role    = st.text_input("Your Title *", key="p_role", placeholder="Full Stack Developer")
        p_email   = st.text_input("Email", key="p_email", placeholder="sravani@email.com")
        p_github  = st.text_input("GitHub", key="p_github", placeholder="github.com/sravani")
    with c2:
        p_linkedin = st.text_input("LinkedIn", key="p_linkedin")
        p_location = st.text_input("Location", key="p_location", placeholder="Hyderabad, India")
        p_tone     = st.selectbox("Portfolio Tone", [
            "Professional & Clean", "Casual & Friendly", "Creative & Bold", "Minimalist"
        ])

    p_bio      = st.text_area("About You", height=80, key="p_bio",
                               placeholder="I'm a passionate developer who loves building innovative solutions...")
    p_skills   = st.text_area("Skills & Technologies", key="p_skills",
                               placeholder="Python, React, Node.js, SQL, AWS, Docker...")
    p_projects = st.text_area("Key Projects", height=130, key="p_projects",
                               placeholder="Project Name — description\nTech: Python, React\n\nProject 2 — description\nTech: Node.js, MongoDB")
    p_achievements = st.text_area("Achievements", key="p_ach",
                                   placeholder="AWS Certified, Hackathon winner, Open source contributor...")

    if st.button("🎨 Generate Portfolio Content", key="gen_portfolio"):
        if not p_name or not p_role:
            st.error("Please enter your Name and Title.")
        else:
            with st.spinner("🤖 Creating your portfolio content..."):
                prompt = f"""You are a professional portfolio copywriter for developers.

Generate complete, engaging portfolio website content.

Name: {p_name} | Title: {p_role} | Location: {p_location}
Email: {p_email} | GitHub: {p_github} | LinkedIn: {p_linkedin}
Bio: {p_bio}
Skills: {p_skills}
Projects: {p_projects}
Achievements: {p_achievements}
Tone: {p_tone}

Generate ALL these sections:

1. HERO SECTION — punchy headline + subheadline + CTA button text
2. ABOUT ME — 3-4 engaging paragraphs with personal story and goals
3. SKILLS — grouped by category with brief descriptions
4. PROJECTS — for each: title, 3-4 sentence description, key features (3 bullets), tech stack, impact
5. ACHIEVEMENTS — formatted with context
6. CONTACT — engaging call-to-action text

Make it compelling, human, and tailored for {p_role} opportunities. Tone: {p_tone}"""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ Portfolio content generated!")
                    st.markdown(result)
                    st.download_button("⬇️ Download Portfolio Content", result,
                        file_name=f"{p_name.replace(' ', '_')}_Portfolio.txt", mime="text/plain")

# ═══════════════════════════════════════════
# TAB 3 — ATS CHECKER
# ═══════════════════════════════════════════
with tab3:
    st.header("🔍 ATS Resume Checker")
    st.markdown("Check how well your resume matches a job description.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**📄 Your Resume**")
        ats_resume = st.text_area("Paste resume here", height=350, key="ats_resume",
            placeholder="Paste your complete resume text here...", label_visibility="collapsed")
    with c2:
        st.markdown("**📋 Job Description**")
        ats_jd = st.text_area("Paste JD here", height=350, key="ats_jd",
            placeholder="Paste the complete job description here...", label_visibility="collapsed")

    if st.button("🔎 Analyse ATS Score", key="ats_check"):
        if not ats_resume or not ats_jd:
            st.error("Please paste both your resume and the job description.")
        else:
            with st.spinner("🤖 Analysing ATS compatibility..."):
                prompt = f"""You are an expert ATS specialist and career coach.

Analyse this resume against the job description and provide a detailed report.

RESUME:
{ats_resume}

JOB DESCRIPTION:
{ats_jd}

Provide this exact report format:

## ATS COMPATIBILITY SCORE: X/100

## MATCHED KEYWORDS
List all matching keywords found in both resume and JD

## MISSING KEYWORDS
List important JD keywords NOT in the resume

## FORMATTING ANALYSIS
Check ATS-friendly formatting issues

## SECTION-BY-SECTION ANALYSIS
Analyse: Summary, Experience, Skills, Education sections

## TOP 8 IMPROVEMENT SUGGESTIONS
Numbered, specific, actionable improvements

## KEYWORD DENSITY SCORE: X/10

## OVERALL VERDICT
2-3 sentences on chances and priority actions"""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ ATS Analysis complete!")
                    st.markdown(result)
                    st.download_button("⬇️ Download ATS Report", result,
                        file_name="ATS_Analysis_Report.txt", mime="text/plain")

# ═══════════════════════════════════════════
# TAB 4 — COVER LETTER
# ═══════════════════════════════════════════
with tab4:
    st.header("💌 Cover Letter Generator")
    st.markdown("Generate a personalised, professional cover letter in seconds.")

    c1, c2 = st.columns(2)
    with c1:
        cl_name    = st.text_input("Your Full Name *", key="cl_name", placeholder="Sravani Reddy")
        cl_role    = st.text_input("Role Applying For *", key="cl_role", placeholder="Backend Developer")
        cl_company = st.text_input("Company Name *", key="cl_company", placeholder="Google")
        cl_hiring  = st.text_input("Hiring Manager Name (if known)", placeholder="Mr. Rajan")
    with c2:
        cl_exp     = st.text_input("Years of Experience", placeholder="Fresher / 1 year / 3 years")
        cl_tone    = st.selectbox("Tone", ["Formal & Professional", "Enthusiastic", "Concise & Direct", "Creative"])
        cl_length  = st.selectbox("Length", ["Standard (300 words)", "Short (150 words)", "Detailed (450 words)"])

    cl_skills  = st.text_area("Your Key Skills & Experience", height=100, key="cl_skills",
                               placeholder="Python, FastAPI, REST APIs, 1 internship at XYZ...")
    cl_why     = st.text_area("Why this role / company?", height=80, key="cl_why",
                               placeholder="I admire Google's mission. I want to work on large-scale systems...")
    cl_achieve = st.text_area("Top Achievements to highlight", height=80, key="cl_ach",
                               placeholder="Built project used by 500+ users, Won hackathon, AWS Certified...")

    if st.button("✉️ Generate Cover Letter", key="gen_cl"):
        if not cl_name or not cl_role or not cl_company:
            st.error("Please fill in Name, Role, and Company.")
        else:
            with st.spinner("🤖 Writing your cover letter..."):
                prompt = f"""Write a compelling, personalised cover letter.

Applicant: {cl_name} | Role: {cl_role} | Company: {cl_company}
Hiring Manager: {cl_hiring if cl_hiring else "Hiring Manager"}
Experience: {cl_exp} | Tone: {cl_tone} | Length: {cl_length}
Skills: {cl_skills}
Motivation: {cl_why}
Achievements: {cl_achieve}

Format:
1. Date and contact header
2. Professional salutation
3. Strong opening — do NOT start with "I am writing to apply"
4. Body paragraph 1: skills + experience + achievements
5. Body paragraph 2: why this company specifically
6. Closing with confident call-to-action
7. Professional sign-off

Keep tone: {cl_tone}. Stay within: {cl_length}. Make it genuine, not generic."""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ Cover letter generated!")
                    st.text_area("Your Cover Letter:", result, height=450)
                    st.download_button("⬇️ Download Cover Letter", result,
                        file_name=f"Cover_Letter_{cl_company.replace(' ', '_')}.txt", mime="text/plain")

# ═══════════════════════════════════════════
# TAB 5 — LINKEDIN SUMMARY
# ═══════════════════════════════════════════
with tab5:
    st.header("🔗 LinkedIn Summary Generator")
    st.markdown("Create a magnetic LinkedIn profile that gets noticed by recruiters.")

    c1, c2 = st.columns(2)
    with c1:
        li_name   = st.text_input("Your Name *", key="li_name", placeholder="Sravani Reddy")
        li_role   = st.text_input("Current / Target Role *", key="li_role", placeholder="Software Developer")
        li_exp    = st.text_input("Experience Level", key="li_exp", placeholder="Fresher / 2 years")
        li_skills = st.text_input("Top Skills", key="li_skills", placeholder="Python, React, ML, Cloud")
    with c2:
        li_goal   = st.text_input("Career Goal", key="li_goal", placeholder="Build scalable backend systems")
        li_unique = st.text_input("What makes you unique?", key="li_unique",
                                   placeholder="Open source contributor, hackathon winner...")
        li_tone   = st.selectbox("Tone", ["Professional", "Conversational", "Bold & Confident"], key="li_tone")

    li_achievements = st.text_area("Key Achievements / Projects", height=100, key="li_ach",
                                    placeholder="Built X used by Y users, Certified in Z, Led team of N...")

    if st.button("🔗 Generate LinkedIn Summary", key="gen_li"):
        if not li_name or not li_role:
            st.error("Please enter your Name and Role.")
        else:
            with st.spinner("🤖 Crafting your LinkedIn summary..."):
                prompt = f"""You are a LinkedIn expert and personal branding specialist.

Create powerful LinkedIn profile content.

Name: {li_name} | Role: {li_role} | Experience: {li_exp}
Skills: {li_skills} | Goal: {li_goal} | Unique: {li_unique}
Achievements: {li_achievements} | Tone: {li_tone}

Generate:

1. LINKEDIN HEADLINE (120 chars max)
A punchy headline beyond just job title

2. LINKEDIN ABOUT SECTION (2000 chars max)
- Hook: Bold opening statement
- Story: Brief professional journey
- Skills: What you bring
- Achievements: 2-3 specific wins
- Goal: What opportunities you seek
- CTA: How to connect

3. TOP 10 FEATURED SKILLS to add to profile

4. 5 QUICK PROFILE OPTIMISATION TIPS

Tone: {li_tone}. Make it human, not robotic. Short paragraphs."""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ LinkedIn content generated!")
                    st.markdown(result)
                    st.download_button("⬇️ Download LinkedIn Content", result,
                        file_name=f"{li_name.replace(' ', '_')}_LinkedIn.txt", mime="text/plain")

# ═══════════════════════════════════════════
# TAB 6 — SKILLS GAP ANALYSER
# ═══════════════════════════════════════════
with tab6:
    st.header("📊 Skills Gap Analyser")
    st.markdown("Find exactly what skills you need for your dream job.")

    c1, c2 = st.columns(2)
    with c1:
        sg_role = st.text_input("Target Job Role *", key="sg_role", placeholder="Data Scientist at Google")
        sg_experience = st.selectbox("Your Experience Level", [
            "Fresher / Student", "0-1 years", "1-3 years", "3-5 years", "5+ years"
        ], key="sg_exp")
    with c2:
        sg_current_skills = st.text_area("Your Current Skills *", height=120, key="sg_skills",
                                          placeholder="Python, SQL, Basic ML, Pandas, NumPy, Statistics...")

    sg_jd = st.text_area("Paste Job Description (optional but recommended)", height=150, key="sg_jd",
                          placeholder="Paste the job description for the role you want...")

    if st.button("📊 Analyse My Skills Gap", key="gen_sg"):
        if not sg_role or not sg_current_skills:
            st.error("Please enter Target Role and Your Current Skills.")
        else:
            with st.spinner("🤖 Analysing your skills gap..."):
                prompt = f"""You are a senior tech career coach and skills strategist.

Perform a detailed skills gap analysis.

Target Role: {sg_role} | Experience: {sg_experience}
Current Skills: {sg_current_skills}
Job Description: {sg_jd if sg_jd else "Use industry standard requirements for " + sg_role}

Provide:

## TARGET ROLE OVERVIEW
Skills typically required for {sg_role}

## YOUR STRENGTHS
Skills you have that match the role

## CRITICAL GAPS (Must learn)
Top 5 must-learn skills — dealbreakers

## NICE-TO-HAVE GAPS
5 skills that strengthen your profile

## LEARNING ROADMAP
For each critical gap:
- Skill name
- Why it matters
- Best resource (course/platform)
- Time to learn

## 3-MONTH ACTION PLAN
Week-by-week learning plan

## READINESS SCORE: X/100

## FINAL RECOMMENDATION
Clear next steps to land the role in 3-6 months"""

                result = call_gemini(prompt)
                if result.startswith("❌") or result.startswith("⚠️"):
                    st.error(result)
                else:
                    st.success("✅ Skills Gap Analysis complete!")
                    st.markdown(result)
                    st.download_button("⬇️ Download Skills Gap Report", result,
                        file_name=f"Skills_Gap_{sg_role.replace(' ', '_')}.txt", mime="text/plain")

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; color:#888;'>Built with ❤️ using Streamlit & Google Gemini 2.0 Flash</p>",
    unsafe_allow_html=True
)
