import sys
import pygame
import random, time
from abc import ABC, abstractmethod

# Khởi tạo Pygame
pygame.init()

# 1. Cấu hình hằng số Giao diện
CELL_SIZE = 35  # Kích thước mỗi ô (pixels)
BOARD_SIZE = 20  # Bàn cờ 20x20
WIDTH = CELL_SIZE * BOARD_SIZE
HEIGHT = CELL_SIZE * BOARD_SIZE

# Màu sắc (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 64, 52)  # Quân X
BLUE = (52, 107, 235)  # Quân O

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro 20x20 AI Game")

#Pattern Score
patterns_scores = {
    # Tấn công (AI)
    'AI_5': 10000000,
    'AI_OPEN_4': 1000000,
    'AI_BLOCKED_4': 100000,
    'AI_OPEN_3': 10000,
    'AI_BLOCKED_3': 1000,
    'AI_OPEN_2': 100,
    # Phòng thủ (Ngăn đối thủ - Hệ số cao hơn để ưu tiên chặn)
    'PLAYER_5': 100000000,
    'PLAYER_OPEN_4': 10000000,  # Bắt buộc chặn ngay
    'PLAYER_BLOCKED_4': 1000000,
    'PLAYER_OPEN_3': 500000,
    'PLAYER_BLOCKED_3': 5000,
    'PLAYER_OPEN_2': 500,
}

DARK_BLUE = (30, 50, 100)
HOVER_COLOR = (100, 150, 240)
SELECTED_COLOR = (40, 200, 80)
#Heuristic function
def evaluate_board(board, ai_symbol):
    direction = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]
    ai_score = 0
    
    
    for r in range(board.size):
        for c in range(board.size):
            if board.board[r][c] == ' ':
                continue
            
            current_p = board.board[r][c]
            is_ai = current_p == ai_symbol
            
            for drow, dcol in direction:
                prev_r, prev_c = r - drow, c - dcol
                if 0 <= prev_r < board.size and 0 <= prev_c < board.size and board.board[prev_r][prev_c] == current_p:
                    continue
                
                length = 0
                curr_r, curr_c = r, c
                
                while (0 <= curr_r < board.size) and (0 <= curr_c < board.size) and board.board[curr_r][curr_c] == current_p:
                    length += 1 
                    curr_r += drow
                    curr_c += dcol
                
                open_ends = 0
                
                #Đầu trên
                if 0 <= prev_r < board.size and 0 <= prev_c < board.size and board.board[prev_r][prev_c] == ' ':
                    open_ends += 1
                    
                #Đầu dưới
                if (0 <= curr_r < board.size) and (0 <= curr_c < board.size) and board.board[curr_r][curr_c] == ' ':
                    open_ends += 1
                
                score = 0
                if length >= 5:
                    score = patterns_scores['AI_5'] if is_ai else patterns_scores['PLAYER_5']
                elif length == 4:
                    if open_ends == 2:
                        score = patterns_scores['AI_OPEN_4'] if is_ai else patterns_scores['PLAYER_OPEN_4']
                    elif open_ends == 1:
                        score = patterns_scores['AI_BLOCKED_4'] if is_ai else patterns_scores['PLAYER_BLOCKED_4']
                elif length == 3:
                    if open_ends == 2:
                        score = patterns_scores['AI_OPEN_3'] if is_ai else patterns_scores['PLAYER_OPEN_3']
                    elif open_ends == 1:
                        score = patterns_scores['AI_BLOCKED_3'] if is_ai else patterns_scores['PLAYER_BLOCKED_3']
                elif length == 2:
                    if open_ends == 2:
                        score = (
                            patterns_scores['AI_OPEN_2']
                            if is_ai
                            else patterns_scores['PLAYER_OPEN_2']
                        )

                if is_ai:
                    ai_score += score
                else:
                    ai_score -= score
    return ai_score

def draw_winner_overlay(screen, text_message):
    """Vẽ bảng thông báo chiến thắng đè lên màn hình bàn cờ."""
    # 1. Tạo một bề mặt (Surface) bán trong suốt màu đen
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)  # Độ trong suốt (0-255)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # 2. Cấu hình Font chữ thông báo
    font_large = pygame.font.SysFont('Arial', 48, bold=True)
    font_small = pygame.font.SysFont('Arial', 24)

    # 3. Tạo chữ Thông báo thắng
    text_surface = font_large.render(text_message, True, (255, 215, 0))  # Màu vàng
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

    # 4. Tạo chữ Hướng dẫn chơi lại / Thoát
    sub_surface = font_small.render("R-Replay | Q-Quit | M-Menu", True, WHITE)
    sub_rect = sub_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))

    # 5. Vẽ lên màn hình
    screen.blit(text_surface, text_rect)
    screen.blit(sub_surface, sub_rect)

def draw_menu(screen, selected_symbol):
    screen.fill((25, 35, 60))  # Nền xanh tối hiện đại hơn

    font_title = pygame.font.SysFont('Arial', 46, bold=True)
    font_section = pygame.font.SysFont('Arial', 20, bold=True)
    font_btn = pygame.font.SysFont('Arial', 24, bold=True)
    font_info = pygame.font.SysFont('Arial', 18)

    # 1. TIÊU ĐỀ
    title_surface = font_title.render("CARO 20x20", True, (255, 215, 0))
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 80)))

    # 2. KHU VỰC CHỌN QUÂN CỜ (Giữa top)
    sec1_surface = font_section.render(
        "1. CHỌN QUÂN CỜ (X ĐI TRƯỚC):", True, (200, 220, 255)
    )
    screen.blit(sec1_surface, sec1_surface.get_rect(center=(WIDTH // 2, 160)))

    btn_x = pygame.Rect(WIDTH // 2 - 140, 190, 130, 50)
    btn_o = pygame.Rect(WIDTH // 2 + 10, 190, 130, 50)

    # Màu nút X / O khi được chọn
    color_x = RED if selected_symbol == 'X' else (80, 90, 110)
    color_o = BLUE if selected_symbol == 'O' else (80, 90, 110)

    # Viền sáng nếu được chọn
    border_x = 4 if selected_symbol == 'X' else 0
    border_o = 4 if selected_symbol == 'O' else 0

    pygame.draw.rect(screen, color_x, btn_x, border_radius=10)
    pygame.draw.rect(screen, color_o, btn_o, border_radius=10)

    if border_x:
        pygame.draw.rect(
            screen, WHITE, btn_x, width=border_x, border_radius=10
        )
    if border_o:
        pygame.draw.rect(
            screen, WHITE, btn_o, width=border_o, border_radius=10
        )

    text_x = font_btn.render("Quân X", True, WHITE)
    text_o = font_btn.render("Quân O", True, WHITE)
    screen.blit(text_x, text_x.get_rect(center=btn_x.center))
    screen.blit(text_o, text_o.get_rect(center=btn_o.center))

    # 3. KHU VỰC CHỌN MỨC ĐỘ (Giữa màn hình)
    sec2_surface = font_section.render(
        "2. CHỌN MỨC ĐỘ AI:", True, (200, 220, 255)
    )
    screen.blit(sec2_surface, sec2_surface.get_rect(center=(WIDTH // 2, 280)))

    buttons = [
        {
            "text": "EASY",
            "mode": "easy",
            "rect": pygame.Rect(WIDTH // 2 - 150, 315, 300, 50),
        },
        {
            "text": "MEDIUM",
            "mode": "medium",
            "rect": pygame.Rect(WIDTH // 2 - 150, 380, 300, 50),
        },
        {
            "text": "HARD",
            "mode": "hard",
            "rect": pygame.Rect(WIDTH // 2 - 150, 445, 300, 50),
        },
    ]

    mouse_pos = pygame.mouse.get_pos()

    for btn in buttons:
        is_hover = btn["rect"].collidepoint(mouse_pos)
        color = HOVER_COLOR if is_hover else WHITE
        text_color = WHITE if is_hover else BLACK

        pygame.draw.rect(screen, color, btn["rect"], border_radius=12)
        text_surf = font_btn.render(btn["text"], True, text_color)
        screen.blit(text_surf, text_surf.get_rect(center=btn["rect"].center))

    # 4. KHU VỰC HƯỚNG DẪN BẮT PHÍM (Tận dụng vùng trống phía dưới)
    guide_box = pygame.Rect(WIDTH // 2 - 200, 530, 400, 120)
    pygame.draw.rect(screen, (35, 48, 80), guide_box, border_radius=10)
    pygame.draw.rect(screen, (70, 90, 130), guide_box, width=2, border_radius=10)

    g_title = font_section.render("Phím tắt trong game:", True, (255, 215, 0))
    g_line1 = font_info.render("- Phím R: Chơi lại ván mới", True, WHITE)
    g_line2 = font_info.render("- Phím M: Quay về Menu chính", True, WHITE)
    g_line3 = font_info.render("- Phím Q: Thoát game", True, WHITE)

    screen.blit(g_title, (guide_box.x + 20, guide_box.y + 12))
    screen.blit(g_line1, (guide_box.x + 20, guide_box.y + 40))
    screen.blit(g_line2, (guide_box.x + 20, guide_box.y + 65))
    screen.blit(g_line3, (guide_box.x + 20, guide_box.y + 90))

    return btn_x, btn_o, buttons
    
#Board class
class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

    def is_valid_move(self, row, col):
        return 0 <= row < 20 and 0 <= col < 20 and self.board[row][col] == ' '

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def check_win(self, r, c, player):
        direction = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]
        
        for drow, dcol in direction:
            count = 1
            
            i = 1
            while True:
                nrow = r + drow * i
                ncol = c + dcol * i
                
                if (0 <= nrow < self.size) and (0 <= ncol < self.size) and (self.board[nrow][ncol] == player):
                    count += 1
                    i += 1
                else:
                    break
            
            j = 1
            while True:
                nrow = r - drow * j
                ncol = c - dcol * j
                
                if (0 <= nrow < self.size) and (0 <= ncol < self.size) and (self.board[nrow][ncol] == player):
                    count += 1
                    j += 1
                else:
                    break
                    
            if count >= 5:
                return True
        return False
             
    def get_empty_cell(self):
        empty_cell = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c] == ' ':
                    empty_cell.append((r, c))
        return empty_cell
    
    def undo_move(self, r, c):
        self.board[r][c] = ' '
        
class BaseAI:
    def __init__(self, symbol):
        self.symbol = symbol
        self.symbol_of_opponent = 'O' #if symbol == 'X' else 'X'
    @abstractmethod
    def get_move(self, board):
        pass   

class RandomAI(BaseAI): #Random AI --very weak
    def __init__(self, symbol):
        super().__init__(symbol)
    def get_move(self, board):
        empty_cell = Board.get_empty_cell(board)   
        ai_row, ai_col = random.choice(empty_cell)
        
        return ai_row, ai_col

class AlphaBetaAI(BaseAI):
    def __init__(self, symbol, depth):
        super().__init__(symbol)
        self.depth = depth
        
    def get_move(self, board):
        candidate_moves = self.get_candidate_move(board)
        
        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol)
            if board.check_win(r, c, self.symbol):
                board.undo_move(r, c)
                return (r, c)
            board.undo_move(r, c)

        # 2. ƯU TIÊN 2: Bắt buộc CHẶN NGAY nếu người chơi chuẩn bị thắng (3 hoặc 4 quân)
        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol_of_opponent)
            if board.check_win(r, c, self.symbol_of_opponent):
                board.undo_move(r, c)
                return (r, c)  # Chặn ngay lập tức!
            board.undo_move(r, c)
            
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol)
            
            score = self._alpha_beta(board, self.depth - 1, alpha, beta, False, (r, c), self.symbol)
            board.undo_move(r, c)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            
        return best_move
    
    def get_candidate_move(self, board, distance = 1):
        candidates = set()
        
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != ' ':
                   
                    for drow in range(-distance, distance + 1):
                        for dcol in range(-distance, distance + 1):
                            if drow == 0 and dcol == 0:
                                continue
                            nrow = r + drow
                            ncol = c + dcol
                            
                            if 0 <= ncol < board.size and 0 <= nrow < board.size and board.board[nrow][ncol] == ' ':
                                candidates.add((nrow, ncol))
        if not candidates:
            return [(board.size // 2, board.size // 2)]
        return list(candidates)
    
    def _alpha_beta(self, board, depth, alpha, beta, is_maximizing, last_move, player_symbol):
        if last_move is not None:
            if board.check_win(last_move[0], last_move[1], player_symbol):
                if player_symbol == self.symbol:
                    return patterns_scores["PLAYER_5"]
                else:
                    return patterns_scores["AI_5"]
                
        if depth == 0 or len(board.get_empty_cell()) == 0:
            return evaluate_board(board, self.symbol)

        candidates_move = self.get_candidate_move(board)
        
        if is_maximizing:
            max_eval = -100000000000
            
            for r, c in candidates_move:
                board.make_move(r, c, self.symbol)
                
                eval = self._alpha_beta(board, depth - 1, alpha, beta, False, (r, c), player_symbol)
                board.undo_move(r, c)
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = +100000000000
            
            for r, c in candidates_move:
                board.make_move(r, c, player_symbol)
                
                eval = self._alpha_beta(board, depth - 1, alpha, beta, True, (r, c), player_symbol)
                board.undo_move(r, c)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                
                if beta <= alpha:
                    break
            return min_eval

class GreedyBFS_AI(BaseAI):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_candidate_move(self, board, distance = 1):
        candidates = set()
        
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != ' ':
                    
                    for drow in range(-distance, distance + 1):
                        for dcol in range(-distance, distance + 1):
                            if drow == 0 and dcol == 0:
                                continue
                            nrow = r + drow
                            ncol = c + dcol
                            
                            if 0 <= ncol < board.size and 0 <= nrow < board.size and board.board[nrow][ncol] == ' ':
                                candidates.add((nrow, ncol))
        if not candidates:
            return [(board.size // 2, board.size // 2)]
        return list(candidates)
        
    def get_move(self, board):
        candidate_moves = self.get_candidate_move(board)
                
        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol)
            if board.check_win(r, c, self.symbol):
                board.undo_move(r, c)
                return (r, c)
            board.undo_move(r, c)

        # 2. ƯU TIÊN 2: Bắt buộc CHẶN NGAY nếu người chơi chuẩn bị thắng (3 hoặc 4 quân)
        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol_of_opponent)
            if board.check_win(r, c, self.symbol_of_opponent):
                board.undo_move(r, c)
                return (r, c)  # Chặn ngay lập tức!
            board.undo_move(r, c)
            
        best_score = float('-inf')
        best_move = None

        for r, c in candidate_moves:
            board.make_move(r, c, self.symbol)
            
            score = evaluate_board(board, self.symbol)
            
            if score > best_score:
                best_score = score
                best_move = (r, c)  
            board.undo_move(r, c)
        return best_move
    
def draw_board(screen, board_obj):
    """Hàm View: Đảm nhận vẽ lưới và quân cờ từ dữ liệu của class Board."""
    screen.fill(WHITE)

    # 1. Vẽ các đường lưới
    for i in range(BOARD_SIZE):
        pygame.draw.line(
            screen,
            BLACK,
            (0, i * CELL_SIZE),
            (WIDTH, i * CELL_SIZE),
            1,
        )
        pygame.draw.line(
            screen,
            BLACK,
            (i * CELL_SIZE, 0),
            (i * CELL_SIZE, HEIGHT),
            1,
        )

    # 2. Vẽ quân cờ 'X' và 'O' dựa trên board_obj.board
    font = pygame.font.SysFont('Arial', int(CELL_SIZE * 0.8), bold=True)

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            symbol = board_obj.board[r][c]
            if symbol != ' ':
                color = RED if symbol == 'X' else BLUE
                text = font.render(symbol, True, color)
                # Căn giữa chữ vào ô
                text_rect = text.get_rect(
                    center=(
                        c * CELL_SIZE + CELL_SIZE // 2,
                        r * CELL_SIZE + CELL_SIZE // 2,
                    )
                )
                screen.blit(text, text_rect)

# ==========================================
# LUỒNG CHẠY CHÍNH (GAME LOOP)
# ==========================================
def main():
    game_board = None
    player_symbol = 'X'
    ai_symbol = 'O'
    current_player = 'X'
    running = True
    game_over = False
    winner_text = ""
    clock = pygame.time.Clock()
    game_state = "Menu"
    ai_player = None
    
    while running:
        if game_state == "Menu":
            btn_x, btn_o, buttons = draw_menu(screen, player_symbol)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Chọn quân cờ
                    if btn_x.collidepoint(pos):
                        player_symbol = 'X'
                        ai_symbol = 'O'
                    elif btn_o.collidepoint(pos):
                        player_symbol = 'O'
                        ai_symbol = 'X'
                    
                    for btn in buttons:
                        if btn["rect"].collidepoint(pos):
                            mode = btn["mode"]
                            if mode == "easy":
                                ai_player = RandomAI(symbol=ai_symbol)
                            elif mode == "medium":
                                ai_player = GreedyBFS_AI(symbol=ai_symbol)
                            elif mode == "hard":
                                ai_player = AlphaBetaAI(symbol=ai_symbol, depth=1)

                            # Khởi tạo ván mới
                            game_board = Board(size=20)
                            current_player = 'X'
                            game_over = False
                            winner_text = ""
                            game_state = "Playing"
                        
        elif game_state == "Playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Bấm 'Q' để thoát
                    if event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()
                    # Bấm 'R' để Reset chơi lại từ đầu
                    if event.key == pygame.K_r:
                        game_board = Board(size=20)
                        current_player = 'X'
                        game_over = False
                        winner_text = ""
                    if event.key == pygame.K_m:
                        game_state = "Menu"
                        
                # Bắt sự kiện Click chuột người chơi
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_over and current_player == player_symbol:
                        pos = pygame.mouse.get_pos()
                        # Chuyển đổi từ Pixel sang tọa độ Hàng - Cột
                        col = pos[0] // CELL_SIZE
                        row = pos[1] // CELL_SIZE
                    
                        # Gọi hàm của class Board
                        if game_board.make_move(row, col, current_player):
                            if game_board.check_win(row, col, current_player):
                                winner_text = "Player thắng"
                                game_over = True
                            else:
                        # Đổi lượt sang AI
                                current_player = ai_symbol

            # Lượt của AI (Tự động đánh khi đến lượt)
            if not game_over and current_player == ai_symbol:
                ai_row, ai_col = ai_player.get_move(game_board)
                    
                if game_board.make_move(ai_row, ai_col, ai_symbol):
                    if game_board.check_win(ai_row, ai_col, ai_symbol):
                        winner_text = "AI THẮNG!"
                        game_over = True
                    else:
                        current_player = player_symbol
            draw_board(screen, game_board)
                    
            if game_over == True:
                draw_winner_overlay(screen, winner_text)
                
            pygame.display.flip()
            
        clock.tick(45)
if __name__ == '__main__':
    main()