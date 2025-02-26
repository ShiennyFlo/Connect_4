import streamlit as st
import random

ROWS = 6
COLUMNS = 7
EMPTY = " "
PLAYER_COLORS = ["red", "yellow"]

# Daftar pertanyaan (pertanyaan, pilihan, jawaban benar)
QUESTIONS = [
    ("Apa nama perusahaan dari sistem operasi Windows?", ["Microsoft", "Microscope"], 1),
    ("Yang manakah merupakan salah satu jenis ancaman siber?", ["Fishing", "Phishing"], 2),
    ("Apa itu kepanjangan dari AI?", ["Artificial Intercity", "Artificial Intelligence"], 2),
    ("Alat komunikasi yang sering digunakan rakyat +62 adalah?", ["Line", "Whatsapp"], 2),
    ("Apa kerugian dari keamanan siber yang kurang baik?", ["Dompet mudah dicuri", "Data privasi tersebar"], 2),
    ("Bahasa komputer biasanya juga disebut dengan?", ["Coding", "Compute"], 1),
    ("Apa salah satu pencegahan bahaya siber?", ["Password yang kuat", "Enkripsi data"], 1),
    ("Apa nama sistem operasi yang dikembangkan dari Google?", ["IOS", "Android"], 2),
    ("Apa kegunaan anti virus?", ["Mencegah virus berbahaya masuk ke dalam komputer", "Mencegah bakteri berbahaya masuk ke dalam komputer"], 1),
    ("Apa yang dilindungi oleh keamanan siber?", ["Data dan Sistem", "Laptop di rumah"], 1),
    ("Apa yang dapat dilakukan untuk mencegah gadget kita dibobol?", ["Simpan di tempat yang aman", "Buatkan password"], 2),
    ("Apa itu keamanan siber?", ["Upaya untuk melindungi sistem komputer jaringan, hardware, aplikasi, layanan, dan data dari ancaman berbahaya", "Upaya untuk menurunkan kasus korupsi di Indonesia"], 1),
    ("Apa itu Phishing?", ["Membuat layanan online tidak dapat diakses", "Menyamar sebagai entitas terpecaya untuk mencuri data"], 2),
    ("Aplikasi microsoft yang digunakan untuk mempuat slide presentasi?", ["Power Ranger", "Power Point"], 2)
]

def create_board():
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if all(board[r][c + i] == piece for i in range(4)):
                return True
    # Vertikal
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True
    # Diagonal positif
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True
    # Diagonal negatif
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True
    return False

def is_board_full(board):
    return all(board[0][c] != EMPTY for c in range(COLUMNS))

def ask_question():
    if "current_question" not in st.session_state:
        question, choices, correct = random.choice(QUESTIONS)
        st.session_state.current_question = (question, choices, correct)

    question, choices, correct = st.session_state.current_question
    st.subheader(f"📝 Pertanyaan: {question}")
    answer = st.radio("Pilih jawaban:", choices, index=None, key="question_answer")

    if answer:
        is_correct = (choices.index(answer) + 1 == correct)
        if is_correct:
            st.success("✅ Jawaban benar! Pilih kolom untuk meletakkan bola.")
        else:
            st.error("❌ Jawaban salah! Giliran dilewati.")
        del st.session_state.current_question  # Hapus pertanyaan setelah dijawab
        return is_correct
    return None

def render_board(board):
    with st.container():
        for row in board:
            cols = st.columns(COLUMNS, gap="small")
            for i, cell in enumerate(row):
                color = cell if cell in PLAYER_COLORS else "lightgrey"
                cols[i].markdown(
                    f"""
                    <div style='width:60px;height:60px;background-color:{color};border-radius:50%;border:2px solid #333;margin:auto;'></div>
                    """, unsafe_allow_html=True
                )

def play_game():
    st.set_page_config(page_title="Connect 4", layout="centered")
    st.title("🎮 Connect 4!")
    st.write("💡 Jawab pertanyaan untuk mendapatkan kesempatan meletakkan bola!")

    if "board" not in st.session_state:
        st.session_state.board = create_board()
        st.session_state.turn = 0
        st.session_state.game_over = False
        st.session_state.awaiting_move = False

    current_player = st.session_state.turn % 2

    if st.session_state.game_over:
        if "winner" in st.session_state:
            st.success(f"🏆 Pemain {st.session_state.winner + 1} ({PLAYER_COLORS[st.session_state.winner]}) menang!")
        else:
            st.info("🤝 Permainan seri!")
        if st.button("🔄 Mulai Ulang"):
            st.session_state.board = create_board()
            st.session_state.turn = 0
            st.session_state.game_over = False
            st.session_state.awaiting_move = False
            if "winner" in st.session_state:
                del st.session_state.winner
        return

    st.markdown(f"### 🎲 Giliran Pemain {current_player + 1} ({PLAYER_COLORS[current_player]})")

    if not st.session_state.awaiting_move:
        question_answered = ask_question()
        if question_answered is not None:
            if question_answered:
                st.session_state.awaiting_move = True
            else:
                st.session_state.turn += 1  # Giliran berikutnya jika salah
    else:
        st.write("⬇️ Pilih kolom untuk meletakkan bola:")
        cols = st.columns(COLUMNS)
        for col_index, col in enumerate(cols):
            if col.button(f"⬇️", key=f"col_{col_index}") and is_valid_location(st.session_state.board, col_index):
                row = get_next_open_row(st.session_state.board, col_index)
                drop_piece(st.session_state.board, row, col_index, PLAYER_COLORS[current_player])
                st.session_state.awaiting_move = False

                # Cek kemenangan
                if winning_move(st.session_state.board, PLAYER_COLORS[current_player]):
                    st.session_state.winner = current_player
                    st.session_state.game_over = True
                # Cek seri jika papan penuh dan belum ada pemenang
                elif is_board_full(st.session_state.board):
                    st.session_state.game_over = True
                else:
                    st.session_state.turn += 1
                break

    st.markdown("---")
    render_board(st.session_state.board)

if __name__ == "__main__":
    play_game()