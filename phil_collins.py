import streamlit as st
import random
import time

st.set_page_config(page_title="Rat Race + Bass Boosted Vibes", layout="wide")

st.markdown(
    """
    <style>
    .bass-boosted {
        animation: shake 0.5s;
        animation-iteration-count: infinite;
    }

    @keyframes shake {
      0% { transform: translate(1px, 1px) rotate(0deg); }
      10% { transform: translate(-1px, -2px) rotate(-1deg); }
      20% { transform: translate(-3px, 0px) rotate(1deg); }
      30% { transform: translate(3px, 2px) rotate(0deg); }
      40% { transform: translate(1px, -1px) rotate(1deg); }
      50% { transform: translate(-1px, 2px) rotate(-1deg); }
      60% { transform: translate(-3px, 1px) rotate(0deg); }
      70% { transform: translate(3px, 1px) rotate(-1deg); }
      80% { transform: translate(-1px, -1px) rotate(1deg); }
      90% { transform: translate(1px, 2px) rotate(0deg); }
      100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🐭 Rat Race with Bass Boosted Vibes")

# Embedded YouTube video with optional bass boost effect
with st.container():
    bass_level = st.slider("🎚️ Bass Level", 0, 10, 5)
    bass_class = "bass-boosted" if bass_level >= 8 else ""
    st.markdown(
        f'<div class="{bass_class}"><iframe width="100%" height="400" src="https://www.youtube.com/embed/i3XcYb2ZTO8?autoplay=0&mute=0" frameborder="0" allowfullscreen></iframe></div>',
        unsafe_allow_html=True,
    )

# Button to simulate "boost" and show random rat race GIFs
st.subheader("🐀 Live Rat Race GIFs")

rat_race_gifs = [
    "https://media1.giphy.com/media/nO5yKct2k5xCM/giphy.gif",
    "https://media3.giphy.com/media/CBdAAvsd63x5u/giphy.gif",
    "https://media4.giphy.com/media/n3buvz9Fa62Ri/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGY5NmltNnRyNm51bWx4YjVqeW4yZnF4ZXcyNmFpeTc5eDZwdGU5cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/N0nyPOrKptLMzzi6ym/giphy.gif",
    "https://media4.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif",
]

if st.button("💣 DROP THE BASS"):
    st.toast("🔥 Bass boosted! Rats going wild!")
    gifs_to_show = random.sample(rat_race_gifs, 3)
else:
    gifs_to_show = rat_race_gifs[:3]

cols = st.columns(len(gifs_to_show))
for i, gif_url in enumerate(gifs_to_show):
    with cols[i]:
        st.image(gif_url, use_container_width=True)
