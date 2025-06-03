import streamlit as st

st.set_page_config(page_title="Rat Race + Bass Boosted Vibes", layout="wide")

st.title("🐭 Rat Race with Bass Boosted Vibes (YouTube Video)")

# Embed the YouTube video
youtube_url = "https://www.youtube.com/embed/i3XcYb2ZTO8?autoplay=0&mute=0"
st.video(youtube_url)

st.subheader("🐀 Live Rat Race GIFs")

rat_race_gifs = [
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHZteXUyNWllcnF3OG45dGdjb3Mzc3lyOWRsczJvdzU4YnE1MzhqdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nO5yKct2k5xCM/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnV6bHJpbm1lOGk4N2t1d2tmMDRjc25mbHozeXJtaDJ3ZDhnaDA5OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/CBdAAvsd63x5u/giphy.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmhxa2F4bnc3bW0wN2l2bWFsMXhxOTNjam0xaDdycG42b29ueWpxciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/n3buvz9Fa62Ri/giphy.gif",
]

cols = st.columns(len(rat_race_gifs))
for i, gif_url in enumerate(rat_race_gifs):
    with cols[i]:
        st.image(gif_url, use_container_width=True)
