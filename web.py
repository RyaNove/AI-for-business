import streamlit as st
import requests

# 设置Hugging Face API token
HF_TOKEN = st.secrets.get("HF_TOKEN")  # 在Streamlit Cloud secrets中设置

def generate_with_hf(prompt, model="microsoft/DialoGPT-medium"):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 400,
            "temperature": 0.8,
            "top_p": 0.9,
            "do_sample": True
        },
        "options": {
            "wait_for_model": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        elif 'error' in result:
            st.error(f"Hugging Face API错误: {result['error']}")
            return None
        else:
            return str(result)
    except Exception as e:
        st.error(f"请求失败: {e}")
        return None

# 界面代码相同...
# 界面代码保持不变...
st.title("💡 SmartAd - AI Marketing Copy Generator")
st.write("Generate catchy ad copy for your brand using AI!")

brand = st.text_input("Brand Name", "EcoBottle")
product = st.text_area("Product Description", "Eco-friendly reusable water bottle made from recycled materials.")
audience = st.text_input("Target Audience", "Young professionals who care about sustainability")
tone = st.selectbox("Tone of Voice", ["Friendly", "Professional", "Funny", "Inspirational"])

if st.button("Generate Ad Copy"):
    with st.spinner("Creating your ad copy..."):
        prompt = f"Write a {tone.lower()} Facebook ad for {brand}. Product: {product}. Target audience: {audience}. Highlight benefits and include a call-to-action."
        
        output = generator(
            prompt,
            max_length=300,
            num_return_sequences=1,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.1,
            do_sample=True
        )[0]['generated_text']
        
        # 清理输出
        if output.startswith(prompt):
            output = output[len(prompt):].strip()
        
        st.subheader("✨ AI-Generated Ad Copy:")
        st.write(output)