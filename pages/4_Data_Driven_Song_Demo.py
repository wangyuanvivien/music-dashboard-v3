import streamlit as st
import pandas as pd

# Set the page title and layout
st.set_page_config(layout="wide")
st.title("💡 A New Creative Workflow")

# --- NEW: Rewritten Chinese Summary (The "Pitch") ---
st.subheader("致 張信哲先生及創作團隊：")
st.header("一個由數據洞察與 AI 驅動的創作流程")

st.markdown(
    """
    這張儀表板不僅是數據的回顧，更是一個為未來創作而設計的「AI 輔助工具」。

    我們的目標是展示一個全新的工作流程：**如何利用您在作品中積累的數據資產，結合 AI (LLM) 來激發新歌的靈感，創作出能與聽眾產生更深刻共鳴的作品。**

    ---
    
    ### 這是一個可重複的創作流程：

    #### 1. 從數據中提取「成功配方」
    我們從您的數據中，利用模型分析出最受歡迎作品的關鍵特徵。
    * **(No. 1 特徵)** `高歌詞字數`：聽眾喜愛豐富、有敘事性的歌詞。
    * **(No. 2 特徵)** `D調 (Key of D)`：這個音調在您的熱門歌曲中佔有顯著地位。
    * **(No. 3/4 特徵)** `流行 + 古典`：融合「Pop」與「Classical」的編曲是您標誌性的成功風格。
    * **(No. 5 特徵)** `AI 情感主題`：歌詞中「憂鬱但堅定的釋懷」、「無條件的奉獻」等複雜情感主題最能引起共鳴。

    #### 2. 將「數據洞察」轉化為「AI 指令」
    我們將這些特徵轉化為一個具體的 AI 指令（如下方所示），用以指導 AI 產出符合您獨特風格的歌詞與旋律。

    #### 3. AI 產出「靈感原型」 (The Demo)
    下方的 Demo 歌曲 **(《D大調的無言(誓)》)** 就是這個流程的成果。

    它並非要取代創作，而是作為一個高質量的「靈感起點」。您可以從中挑選、修改、或純粹將其作為一個新方向的啟發。
    
    這個流程不只能複製「熱門公式」，更能透過分析「非典型熱門歌曲」(Outliers)，幫助您在保持經典風格的同時，不斷探索新的藝術可能性。
    """
)
# --- End of New Section ---

st.markdown("---")

# --- 1. The "Proof of Concept" Song ---
st.header("1. 靈感原型 (Case Study Demo)")
st.write("這首歌是上述流程的成果。請點擊播放，聆聽這首完全由數據驅動的歌曲。")

# --- THIS IS THE UPDATED LINE ---
audio_file_path = '無言_ai_song.mp3'
# --- END OF UPDATE ---

try:
    audio_file = open(audio_file_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mpeg')

except FileNotFoundError:
    st.error(
        f"**Error:** Could not find the audio file. "
        f"Please make sure you have uploaded the file as `無言_ai_song.mp3` "
        f"to the main (root) folder of your GitHub repository."
    )
except Exception as e:
    st.error(f"An error occurred while loading the audio file: {e}")


st.markdown("---")

# --- 2. The "Recipe" (Style Prompt) ---
st.header("2. 數據洞察轉化的 AI 指令 (The 'Recipe')")
st.write("這就是我們根據「特徵重要性」模型，提供給 AI 的具體指令：")
st.code(
    """A 1990s Mandopop ballad in the style of Jeff Chang. Emotional male tenor vocals, in Key of D-Major. The music is Pop, but with a strong Classical piano and string section. Lyrically dense and emotional.""",
    language="text"
)

st.markdown("---")

# --- 3. The Lyrics ---
st.header("3. 歌詞 (《D大調的無言(誓)》)")
st.subheader("Title: The Unspoken Vow in D-Major")

lyrics = """
(Verse 1)
城市的霓虹 閃爍又疏離
像我們昨晚 欲言又止的話題
你轉過身去 藏在陰影裡的嘆息
是我心中 最深的焦慮
我總在懷疑 幸福是否短暫
像手中握不住的沙 輕易飄散
我承認我害怕 那些流言 unha 
害怕這溫暖 只是夢的序曲

(Pre-Chorus)
直到你 昨夜為我 擦去眼角的淚滴
用你沉默的堅定 覆蓋了我的恐懼

(Chorus)
這就是我無言的承諾 用D大調的溫柔
從此我的世界 不再有憂鬱的漂流
你的愛是唯一的錨 穩住了我的飄搖
我願用我餘生 去交換你一秒的微笑
這就是我無言的承諾 是我唯一的祈求
所有焦慮不安 在你懷中化為烏有
我相信你 就像黑夜 相信黎明

(Verse 2)
我看過太多 虛假的承諾
在愛與不愛之間 殘酷地拉扯
他們不明白 我們經歷過的曲折
才讓這份愛 如此深刻
我不再去問 永遠到底有多遠
也不再去猜 命運的下一張牌
我只知道此刻 你的體溫是真的
我心中的空洞 被你填補了

(Pre-Chorus)
當你 輕輕撥開 我緊鎖的眉頭
我才發現我的世界 早已為你停留

(Chorus)
這就是我無言的承諾 用D大調的溫柔
從此我的世界 不再有憂鬱的漂流
你的愛是唯一的錨 穩住了我的飄搖
我願用我餘生 去交換你一秒的微笑
這就是我無言的承諾 是我唯一的祈求
所有焦慮不安 在你懷中化為烏有
我相信你 就像黑夜 相信黎明

(Bridge - C段)
讓時間去證明 這不是一時的衝動
我用我的全心 獻上我無條件的奉獻
就算世界崩塌 就算星辰殞落
我也會在你身邊 築起最後的窩

(Final Chorus)
這就是我無言的承諾 用D大調的溫柔
從此我的世界 不再有憂鬱的漂流
你的愛是唯一的錨 穩住了我的飄搖
我願用我餘生 去交換你一秒的微笑
這就是我無言的承諾 是我唯一的祈求
所有焦慮不安 在你懷中化為烏有
我相信你 就像黑夜 相信黎明
...我相信你 就像阿哲 相信情歌
"""
st.text(lyrics)
