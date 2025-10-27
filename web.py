import streamlit as st
import openai
import os

# 设置页面
st.set_page_config(page_title="SmartAd - GPT营销文案生成器", page_icon="💡")

# 从Streamlit Secrets获取API密钥
if 'OPENAI_API_KEY' in st.secrets:
    openai.api_key = st.secrets['OPENAI_API_KEY']
else:
    # 如果没有设置secrets，显示设置指南
    st.error("""
    ## 🔑 需要设置OpenAI API密钥
    
    请按照以下步骤操作：
    
    1. **获取API密钥**：
       - 访问 https://platform.openai.com/api-keys
       - 登录/注册OpenAI账号
       - 点击"Create new secret key"
       - 复制生成的密钥
    
    2. **在Streamlit Cloud设置**：
       - 进入应用Settings → Secrets
       - 添加：
       ```toml
       OPENAI_API_KEY = "你的-api-key-here"
       ```
    """)
    st.stop()

def generate_with_gpt(brand, product, audience, tone):
    """使用GPT生成广告文案"""
    try:
        prompt = f"""
        为品牌 {brand} 创建一个{tone}风格的Facebook广告文案。
        
        产品描述: {product}
        目标受众: {audience}
        
        要求:
        - 10-15句话长度
        - 突出产品的主要优势和情感吸引力
        - 以鼓励行动的口号结束
        - 使用{tone}的语气
        - 内容要吸引人、有说服力
        - 包含相关的hashtag
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的市场营销专家，擅长创作吸引人的社交媒体广告文案。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.8,
            top_p=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except openai.error.AuthenticationError:
        return "❌ API密钥错误，请检查密钥是否正确"
    except openai.error.RateLimitError:
        return "❌ API调用频率超限，请稍后重试"
    except openai.error.APIError as e:
        return f"❌ OpenAI API错误: {str(e)}"
    except Exception as e:
        return f"❌ 生成失败: {str(e)}"

# 主应用界面
st.title("💡 SmartAd - AI Marketing Copy Generator")
st.write("使用GPT AI为你的品牌生成吸引人的广告文案！")

# 用户输入
col1, col2 = st.columns(2)

with col1:
    brand = st.text_input("品牌名称", "EcoBottle", help="输入你的品牌名称")
    product = st.text_area(
        "产品描述", 
        "Eco-friendly reusable water bottle made from recycled materials.",
        help="详细描述你的产品特点和优势"
    )

with col2:
    audience = st.text_input(
        "目标受众", 
        "Young professionals who care about sustainability",
        help="描述你的目标客户群体"
    )
    tone = st.selectbox(
        "语气风格", 
        ["友好", "专业", "幽默", "鼓舞人心", "正式", "轻松"],
        help="选择广告文案的语气风格"
    )

# 高级选项
with st.expander("高级选项"):
    col3, col4 = st.columns(2)
    with col3:
        platform = st.selectbox(
            "广告平台",
            ["Facebook", "Instagram", "Twitter", "LinkedIn", "通用"]
        )
    with col4:
        language = st.selectbox(
            "语言",
            ["中文", "English", "双语"]
        )

# 生成按钮
if st.button("🚀 生成广告文案", type="primary", use_container_width=True):
    if not all([brand, product, audience]):
        st.warning("请填写所有必填字段")
    else:
        with st.spinner("🤖 GPT正在创作精彩的广告文案..."):
            output = generate_with_gpt(brand, product, audience, tone)
            
            st.subheader("✨ AI生成的广告文案:")
            
            # 美化输出
            st.success(output)
            
            # 添加复制功能
            st.code(output, language="markdown")
            
            # 下载按钮
            st.download_button(
                label="📥 下载文案",
                data=output,
                file_name=f"{brand}_ad_copy.txt",
                mime="text/plain"
            )

# 侧边栏信息
st.sidebar.title("ℹ️ 使用说明")
st.sidebar.info("""
**功能特点：**
- 使用GPT-3.5 Turbo生成高质量文案
- 支持多种语气风格
- 针对不同平台优化
- 一键下载生成结果

**使用技巧：**
1. 详细描述产品特点
2. 明确目标受众
3. 选择合适的语气
4. 可多次生成选择最佳结果
""")

# API状态检查
st.sidebar.markdown("---")
if st.sidebar.button("检查API状态"):
    try:
        openai.Model.list()
        st.sidebar.success("✅ API连接正常")
    except:
        st.sidebar.error("❌ API连接失败")
