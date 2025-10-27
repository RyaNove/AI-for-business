import streamlit as st
import os

# Set up page
st.set_page_config(page_title="SmartAd - AI Marketing Copy Generator", page_icon="💡")

# Check and import openai
try:
    from openai import OpenAI
    import openai
    st.sidebar.success("✅ OpenAI library loaded")
except ImportError:
    st.error("❌ OpenAI library not installed. Please ensure 'openai' is in requirements.txt")
    st.stop()

# Get API key from Streamlit Secrets
if 'OPENAI_API_KEY' in st.secrets:
    openai_api_key = st.secrets['OPENAI_API_KEY']
    client = OpenAI(api_key=openai_api_key)
else:
    st.error("""
    ## 🔑 OpenAI API Key Required
    
    Please follow these steps:
    
    1. **Get API Key**:
       - Visit https://platform.openai.com/api-keys
       - Click "Create new secret key"
       - Copy the generated key
    
    2. **Set up in Streamlit Cloud**:
       - Go to App Settings → Secrets
       - Add:
       ```toml
       OPENAI_API_KEY = "your-api-key-here"
       ```
    """)
    st.stop()

def generate_with_gpt(brand, product, audience, tone):
    """Generate ad copy using GPT"""
    try:
        prompt = f"""
        Create a {tone.lower()} Facebook ad copy for brand {brand}.
        
        Product Description: {product}
        Target Audience: {audience}
        
        Requirements:
        - 10-15 sentences long
        - Highlight product's key benefits and emotional appeal
        - End with a compelling call-to-action
        - Use {tone.lower()} tone of voice
        - Make it engaging and persuasive
        - Include relevant hashtags
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional marketing expert specializing in creating engaging social media ad copy."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8,
            top_p=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"❌ Generation failed: {str(e)}"

# Main application interface
st.title("💡 SmartAd - AI Marketing Copy Generator")
st.write("Generate catchy ad copy for your brand using GPT AI!")

# User input
col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("Brand Name", "EcoBottle", help="Enter your brand name")
    product = st.text_area(
        "Product Description", 
        "Eco-friendly reusable water bottle made from recycled materials.",
        help="Describe your product features and benefits"
    )

with col2:
    audience = st.text_input(
        "Target Audience", 
        "Young professionals who care about sustainability",
        help="Describe your target customer group"
    )
    tone = st.selectbox(
        "Tone of Voice", 
        ["Friendly", "Professional", "Humorous", "Inspirational", "Formal", "Casual"],
        help="Select the tone for your ad copy"
    )

# Advanced options
with st.expander("Advanced Options"):
    col3, col4 = st.columns(2)
    with col3:
        platform = st.selectbox(
            "Advertising Platform",
            ["Facebook", "Instagram", "Twitter", "LinkedIn", "General"]
        )
    with col4:
        language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German", "Multilingual"]
        )

# Generate button
if st.button("🚀 Generate Ad Copy", type="primary", use_container_width=True):
    if not all([brand, product, audience]):
        st.warning("Please fill in all required fields")
    else:
        with st.spinner("🤖 GPT is creating amazing ad copy..."):
            output = generate_with_gpt(brand, product, audience, tone)
            
            st.subheader("✨ AI-Generated Ad Copy:")
            
            # Beautify output
            st.success(output)
            
            # Add copy functionality
            st.code(output, language="markdown")
            
            # Download button
            st.download_button(
                label="📥 Download Copy",
                data=output,
                file_name=f"{brand}_ad_copy.txt",
                mime="text/plain"
            )

# Sidebar information
st.sidebar.title("ℹ️ Instructions")
st.sidebar.info("""
**Features:**
- Uses GPT-3.5 Turbo for high-quality copy
- Supports multiple tone styles
- Optimized for different platforms
- One-click download results

**Tips for best results:**
1. Describe product features in detail
2. Be specific about target audience
3. Choose appropriate tone
4. Generate multiple versions to choose the best
""")

# API status check
st.sidebar.markdown("---")
if st.sidebar.button("Check API Status"):
    try:
        client.models.list()
        st.sidebar.success("✅ API connection successful")
    except Exception as e:
        st.sidebar.error(f"❌ API connection failed: {str(e)}")

# Additional features
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Usage Tips")
st.sidebar.write("""
- **For eco-products**: Emphasize sustainability
- **For tech products**: Highlight innovation
- **For B2B**: Use professional tone
- **For B2C**: More friendly and engaging
""")
