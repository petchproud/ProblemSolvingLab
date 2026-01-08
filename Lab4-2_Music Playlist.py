import streamlit as st

# --- Song Class ---
class Song:
    def __init__(self, title, artist, audio_data):
        self.title = title
        self.artist = artist
        self.audio_data = audio_data  # เก็บข้อมูลไฟล์เพลงแบบ binary
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_data):
        new_song = Song(title, artist, audio_data)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song
        self.length += 1
        st.sidebar.success(f"Added: {new_song}")

    def display_playlist(self):
        if self.head is None:
            return []

        playlist_songs = []
        current = self.head
        count = 1
        while current:
            # เพิ่มเครื่องหมาย ▶️ หน้าเพลงที่กำลังเลือกอยู่
            prefix = "▶️ " if current == self.current_song else "  "
            playlist_songs.append(f"{prefix}{count}. {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return playlist_songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            # แสดงเครื่องเล่นเพลง
            st.audio(self.current_song.audio_data, format='audio/mp3')
        else:
            st.warning("Playlist is empty or no song is selected.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        elif self.current_song and not self.current_song.next_song:
            st.warning("End of playlist.")
        else:
            st.warning("Playlist is empty.")

    def prev_song(self):
        if self.head is None or self.current_song == self.head:
            st.warning("Already at the beginning.")
            return
        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def get_length(self):
        return self.length

    def delete_song(self, title):
        if self.head is None:
            st.error(f"Cannot delete '{title}'. Playlist is empty.")
            return
        if self.head.title == title:
            if self.current_song == self.head:
                self.current_song = self.head.next_song
            self.head = self.head.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
            return
        current = self.head
        while current.next_song and current.next_song.title != title:
            current = current.next_song
        if current.next_song:
            if self.current_song == current.next_song:
                self.current_song = current.next_song.next_song or current
            current.next_song = current.next_song.next_song
            self.length -= 1
            st.success(f"Deleted: {title}")
        else:
            st.error(f"Song '{title}' not found.")

# --- Streamlit App Layout ---
st.title("🎶 Music Playlist Player (Linked List)")



if 'playlist' not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# Sidebar: เพิ่มเพลงพร้อมอัปโหลดไฟล์
st.sidebar.header("Upload New Song")
new_title = st.sidebar.text_input("Title")
new_artist = st.sidebar.text_input("Artist")
uploaded_file = st.sidebar.file_uploader("Choose an MP3 file", type=["mp3"])

if st.sidebar.button("Add Song to Playlist"):
    if new_title and new_artist and uploaded_file:
        # อ่านข้อมูลไฟล์เป็น bytes เพื่อเก็บลงใน Node
        audio_bytes = uploaded_file.read()
        st.session_state.playlist.add_song(new_title, new_artist, audio_bytes)
    else:
        st.sidebar.warning("Please fill all fields and upload a file.")

st.sidebar.markdown("---")
st.sidebar.header("Delete Song")
delete_title = st.sidebar.text_input("Title to Delete")
if st.sidebar.button("Delete Song"):
    if delete_title:
        st.session_state.playlist.delete_song(delete_title)
        st.rerun()

# แสดงรายการเพลง
st.header("Your Playlist")
playlist_content = st.session_state.playlist.display_playlist()
if playlist_content:
    for song_str in playlist_content:
        st.write(song_str)
else:
    st.write("Playlist is empty. Upload some songs!")

st.markdown("---")
st.header("Playback Controls")

# เรียกใช้ฟังก์ชันเล่นเพลงปัจจุบัน
st.session_state.playlist.play_current_song()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⏪ Previous"):
        st.session_state.playlist.prev_song()
        st.rerun()
with col2:
    if st.button("🔄 Refresh Player"):
        st.rerun()
with col3:
    if st.button("⏩ Next"):
        st.session_state.playlist.next_song()
        st.rerun()

st.write(f"Total songs: {st.session_state.playlist.get_length()}")
