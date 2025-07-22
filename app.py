import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Salary Prediction", page_icon="💰", layout="wide")

# Simple CSS for better look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main app styling with premium dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
        animation: backgroundShift 8s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); }
        50% { background: linear-gradient(135deg, #16213e 0%, #0f0f23 50%, #1a1a2e 100%); }
    }
    
    /* Premium gradient title */
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.8rem;
        font-weight: 800;
        margin-bottom: 1rem;
        letter-spacing: -2px;
        animation: titlePulse 3s ease-in-out infinite, titleFloat 4s ease-in-out infinite, titleGradientShift 6s ease-in-out infinite;
        position: relative;
        background-size: 200% 200%;
    }
    
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    @keyframes titleGradientShift {
        0% { 
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        33% { 
            background: linear-gradient(135deg, #4ecdc4 0%, #45b7d1 50%, #96ceb4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        66% { 
            background: linear-gradient(135deg, #45b7d1 0%, #96ceb4 50%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        100% { 
            background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    }
    
   
    
    
    .input-container:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border-color: #667eea;
    }
    
    @keyframes containerBreathe {
        0%, 100% { box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
        50% { box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.15); }
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 25px;
        text-align: center;
        color: white;
        margin: 2rem 0;
        box-shadow: 
            0 25px 50px rgba(102, 126, 234, 0.4),
            0 10px 20px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        animation: predictionPulse 3s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .prediction-box:hover {
        animation-play-state: paused;
        transform: rotateX(5deg) rotateY(5deg);
        box-shadow: 
            0 35px 70px rgba(102, 126, 234, 0.6),
            0 15px 30px rgba(102, 126, 234, 0.4);
    }
    
    @keyframes predictionPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4), 0 10px 20px rgba(102, 126, 234, 0.2);
        }
        50% { 
            transform: scale(1.02);
            box-shadow: 0 30px 60px rgba(102, 126, 234, 0.5), 0 15px 30px rgba(102, 126, 234, 0.3);
        }
    }
    
    .prediction-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Premium button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.4),
            0 5px 15px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
        transform: translateY(0);
        border: 2px solid transparent;
        background-clip: padding-box;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 20px 50px rgba(102, 126, 234, 0.6),
            0 10px 25px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        background: linear-gradient(135deg, #7c8fee 0%, #8a5bb8 100%);
        border-color: rgba(255, 255, 255, 0.3);
        letter-spacing: 1px;
        color: #ffff00;
        text-shadow: 0 2px 8px rgba(255, 255, 0, 0.4), 0 0 20px rgba(255, 255, 0, 0.3);
        animation: buttonPulse 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes buttonPulse {
        0% { filter: brightness(1); }
        100% { filter: brightness(1.1); }
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button:active {
        transform: translateY(-2px) scale(1.02);
        transition: all 0.1s ease;
    }
    
    /* Premium input fields */
    .stNumberInput input {
        background: #2d2d2d;
        border: 2px solid #444;
        border-radius: 12px;
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        padding: 0.8rem;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stNumberInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), 0 0 20px rgba(102, 126, 234, 0.3);
        outline: none;
        transform: translateY(-1px);
        background: #333;
    }
    
    .stNumberInput input:hover {
        border-color: #555;
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Premium select boxes */
    .stSelectbox > div > div {
        background: #2d2d2d;
        border: 2px solid #444;
        border-radius: 12px;
        color: white;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), 0 0 20px rgba(102, 126, 234, 0.3);
        transform: translateY(-1px);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #555;
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: #2d2d2d;
        color: white;
        transition: all 0.3s ease;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: #2d2d2d;
        color: white;
        border-color: #444;
    }
    
    /* Section headers */
    h3 {
        color: #e0e0e0 !important;
        font-weight: 600;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        animation: headerGlow 4s ease-in-out infinite;
        position: relative;
    }
    
    @keyframes headerGlow {
        0%, 100% { text-shadow: 0 0 10px rgba(102, 126, 234, 0.3); }
        50% { text-shadow: 0 0 20px rgba(102, 126, 234, 0.6), 0 0 30px rgba(102, 126, 234, 0.4); }
    }
    
    /* Description text */
    .description-text {
        color: #b0b0b0;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        line-height: 1.6;
        animation: textPulse 5s ease-in-out infinite;
    }
    
    @keyframes textPulse {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 1; }
    }
    
    /* Premium metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1e1e1e 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 0.5rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        animation: cardFloat 6s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: cardRotate 8s linear infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) rotateY(5deg);
        box-shadow: 
            0 25px 50px rgba(102, 126, 234, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: #667eea;
    }
    
    @keyframes cardFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }
    
    @keyframes cardRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        border: 1px solid #333;
        border-radius: 15px;
        color: white;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data for visualization
@st.cache_data
def create_sample_data():
    np.random.seed(42)
    years = np.random.randint(0, 25, 200)
    job_rates = np.random.uniform(1, 5, 200)
    
    # Education levels with salary multipliers
    education_levels = ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Professional Certification"]
    education_multipliers = [0.8, 1.0, 1.3, 1.6, 1.2]
    education_data = np.random.choice(education_levels, 200)
    
    # Job levels with salary multipliers
    job_levels = ["Entry Level", "Junior", "Mid-Level", "Senior", "Lead", "Manager", "Director", "Executive"]
    job_multipliers = [0.7, 0.9, 1.0, 1.4, 1.6, 1.8, 2.2, 2.8]
    job_level_data = np.random.choice(job_levels, 200)
    
    # Calculate salaries with new factors
    salaries_usd = []
    for i in range(200):
        base_salary = 35000 + (years[i] * 2500) + (job_rates[i] * 8000)
        
        # Apply education multiplier
        edu_idx = education_levels.index(education_data[i])
        base_salary *= education_multipliers[edu_idx]
        
        # Apply job level multiplier
        job_idx = job_levels.index(job_level_data[i])
        base_salary *= job_multipliers[job_idx]
        
        # Add some randomness
        base_salary += np.random.normal(0, 5000)
        salaries_usd.append(max(base_salary, 25000))  # Minimum salary
    
    salaries_inr = [salary * 83.5 for salary in salaries_usd]
    
    return pd.DataFrame({
        'Years': years,
        'Job_Rating': job_rates,
        'Education': education_data,
        'Job_Level': job_level_data,
        'Salary_USD': salaries_usd,
        'Salary_INR': salaries_inr
    })

# Load model safely
@st.cache_resource
def load_model():
    try:
        return joblib.load("linearmodel.pkl")
    except:
        st.error("Model file not found. Using sample prediction.")
        return None

# Page title
st.markdown('<h1 class="main-title">💰 Salary Prediction Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="description-text">Get accurate salary predictions powered by advanced analytics and machine learning</p>', unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.markdown("### 📝 Enter Your Details")
    
    # Input fields with better styling
    years = st.number_input("🗓️ Years of Experience", value=5, step=1, min_value=0, max_value=50, help="Enter your total years of work experience")
    jobrate = st.number_input("⭐ Job Performance Rating", value=3.5, step=0.1, min_value=0.0, max_value=5.0, help="Rate your job performance from 1.0 to 5.0")
    
    # Education Level
    education = st.selectbox("🎓 Education Level", 
                           ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Professional Certification"],
                           index=1,
                           help="Select your highest level of education")
    
    # Job Level/Position
    job_level = st.selectbox("💼 Job Level", 
                           ["Entry Level", "Junior", "Mid-Level", "Senior", "Lead", "Manager", "Director", "Executive"],
                           index=2,
                           help="Select your current job level or position")
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Prediction button
    predict = st.button("🚀 Predict My Salary")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Load model and sample data
    model = load_model()
    sample_data = create_sample_data()

    if predict:
        st.balloons()
        
        # Education multipliers
        education_multipliers = {
            "High School": 0.8,
            "Bachelor's Degree": 1.0,
            "Master's Degree": 1.3,
            "PhD": 1.6,
            "Professional Certification": 1.2
        }
        
        # Job level multipliers
        job_multipliers = {
            "Entry Level": 0.7,
            "Junior": 0.9,
            "Mid-Level": 1.0,
            "Senior": 1.4,
            "Lead": 1.6,
            "Manager": 1.8,
            "Director": 2.2,
            "Executive": 2.8
        }
        
        if model:
            # Use actual model if available (would need to be retrained with new features)
            x = np.array([[years, jobrate]])
            prediction = model.predict(x)
            predicted_usd = prediction[0]
            # Apply education and job level adjustments
            predicted_usd *= education_multipliers[education]
            predicted_usd *= job_multipliers[job_level]
        else:
            # Enhanced formula with new factors
            base_salary = 35000 + (years * 2500) + (jobrate * 8000)
            predicted_usd = base_salary * education_multipliers[education] * job_multipliers[job_level]
        
        # Convert to INR
        predicted_inr = predicted_usd * 83.5
        
        # Display results in a premium box
        st.markdown(f"""
        <div class="prediction-box">
            <h2 style="margin: 0; font-size: 1.4rem; font-weight: 600; opacity: 0.9;">🎉 Your Predicted Annual Salary</h2>
            <h1 style="margin: 1rem 0; font-size: 3rem; font-weight: 800; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">₹{predicted_inr:,.0f}</h1>
            <p style="margin: 0; font-size: 1.2rem; opacity: 0.9; font-weight: 500;">${predicted_usd:,.0f} USD</p>
            <p style="margin-top: 1.5rem; font-size: 1rem; opacity: 0.8;">Based on {years} years experience, {jobrate}/5.0 rating, {education}, {job_level}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show comparison with average
        avg_salary = sample_data['Salary_INR'].mean()
        diff = predicted_inr - avg_salary
        
        if diff > 0:
            st.success(f"📈 Excellent! Your predicted salary is ₹{diff:,.0f} above the market average")
        else:
            st.info(f"📊 Your predicted salary is ₹{abs(diff):,.0f} below the market average")

with col2:
    st.markdown("### 📊 Live Market Analytics")
    
    # Chart 1: Enhanced scatter plot
    fig1 = px.scatter(sample_data, 
                     x='Years', 
                     y='Salary_INR',
                     color='Job_Rating',
                     title='💰 Market Salary Analysis',
                     color_continuous_scale='viridis',
                     labels={'Salary_INR': 'Annual Salary (₹)', 'Years': 'Years of Experience'},
                     template='plotly_dark',
                     opacity=0.7)
    
    # Add prediction point if button was clicked
    if predict:
        fig1.add_scatter(x=[years], y=[predicted_inr], 
                        mode='markers+text', 
                        marker=dict(size=25, color='#667eea', symbol='star', 
                                  line=dict(width=3, color='white')),
                        name='Your Position',
                        text=['⭐ YOU'],
                        textposition="top center",
                        textfont=dict(size=16, color='white', family="Inter"))
    
    fig1.update_layout(
        height=380,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        title=dict(font=dict(size=18, color='#e0e0e0', family='Inter')),
        showlegend=True,
        legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1)
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Enhanced trend line
    trend_data = sample_data.groupby('Years')['Salary_INR'].mean().reset_index()
    fig2 = px.line(trend_data, x='Years', y='Salary_INR',
                  title='📈 Salary Growth Trajectory',
                  markers=True,
                  template='plotly_dark')
    
    fig2.update_traces(
        line=dict(color='#667eea', width=4),
        marker=dict(size=10, color='#764ba2', line=dict(width=2, color='white'))
    )
    
    fig2.update_layout(
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        title=dict(font=dict(size=18, color='#e0e0e0', family='Inter'))
    )
    st.plotly_chart(fig2, use_container_width=True)

# Add some statistics at the bottom
st.markdown("---")
st.markdown("### 📈 Salary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: white; margin: 0;">💰 Average Salary</h4>
        <h2 style="color: #4ECDC4; margin: 0.5rem 0;">₹{sample_data['Salary_INR'].mean():,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: white; margin: 0;">📊 Max Salary</h4>
        <h2 style="color: #FF6B6B; margin: 0.5rem 0;">₹{sample_data['Salary_INR'].max():,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: white; margin: 0;">📉 Min Salary</h4>
        <h2 style="color: #96CEB4; margin: 0.5rem 0;">₹{sample_data['Salary_INR'].min():,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="color: white; margin: 0;">👥 Sample Size</h4>
        <h2 style="color: #45B7D1; margin: 0.5rem 0;">{len(sample_data):,}</h2>
    </div>
    """, unsafe_allow_html=True)