#!/usr/bin/env python3
import sys
from enum import Enum

# =======================================
# 1. 手番を表す列挙型
class Color(Enum):
    Black = 0  # 先手
    White = 1  # 後手

def get_opponent_color(color: Color) -> Color:
    return Color.White if color == Color.Black else Color.Black

# =======================================
# 2. 駒の種類を表す列挙型
class Piece(Enum):
    NoPiece = 0                # 駒なし
    BlackPawn = 1              # 歩
    BlackLance = 2             # 香
    BlackKnight = 3            # 桂
    BlackSilver = 4            # 銀
    BlackGold = 5              # 金
    BlackBishop = 6            # 角
    BlackRook = 7              # 飛
    BlackKing = 8              # 王
    BlackPromotedPawn = 9      # と
    BlackPromotedLance = 10    # 杏
    BlackPromotedKnight = 11   # 圭
    BlackPromotedSilver = 12   # 全
    BlackHorse = 13            # 馬（角の成り）
    BlackDragon = 14           # 龍（飛の成り）
    WhitePawn = 15             # 歩↓
    WhiteLance = 16            # 香↓
    WhiteKnight = 17           # 桂↓
    WhiteSilver = 18           # 銀↓
    WhiteGold = 19             # 金↓
    WhiteBishop = 20           # 角↓
    WhiteRook = 21             # 飛↓
    WhiteKing = 22             # 王↓
    WhitePromotedPawn = 23     # と↓
    WhitePromotedLance = 24    # 杏↓
    WhitePromotedKnight = 25   # 圭↓
    WhitePromotedSilver = 26   # 全↓
    WhiteHorse = 27            # 馬↓
    WhiteDragon = 28           # 龍↓

# =======================================
# 3. 駒表示用のマッピング
PIECE_TO_USI_CHAR = {
    Piece.BlackPawn: 'P',
    Piece.BlackLance: 'L',
    Piece.BlackKnight: 'N',
    Piece.BlackSilver: 'S',
    Piece.BlackGold: 'G',
    Piece.BlackBishop: 'B',
    Piece.BlackRook: 'R',
    Piece.BlackKing: 'K',
    Piece.BlackPromotedPawn: 'P',
    Piece.BlackPromotedLance: 'L',
    Piece.BlackPromotedKnight: 'N',
    Piece.BlackPromotedSilver: 'S',
    Piece.BlackHorse: 'B',
    Piece.BlackDragon: 'R',
    Piece.WhitePawn: 'p',
    Piece.WhiteLance: 'l',
    Piece.WhiteKnight: 'n',
    Piece.WhiteSilver: 's',
    Piece.WhiteGold: 'g',
    Piece.WhiteBishop: 'b',
    Piece.WhiteRook: 'r',
    Piece.WhiteKing: 'k',
    Piece.WhitePromotedPawn: 'p',
    Piece.WhitePromotedLance: 'l',
    Piece.WhitePromotedKnight: 'n',
    Piece.WhitePromotedSilver: 's',
    Piece.WhiteHorse: 'b',
    Piece.WhiteDragon: 'r'
}

def get_usi_char_from_piece(piece: Piece) -> str:
    return PIECE_TO_USI_CHAR.get(piece)


PIECE_KANJIS = [
    "    ", "歩", "香", "桂", "銀", "金", "角", "飛", "王",
    "と", "杏", "圭", "全", "馬", "龍",
    "歩↓", "香↓", "桂↓", "銀↓", "金↓", "角↓", "飛↓", "王↓",
    "と↓", "杏↓", "圭↓", "全↓", "馬↓", "龍↓"
]

def get_kanji_from_piece(piece: Piece) -> str:
    return PIECE_KANJIS[piece.value]

# =======================================
# 4. SFENパース用のユーティリティ
CHAR_TO_PIECE = {}
NON_PROMOTED_TO_PROMOTED = {}

def initialize_types():
    global CHAR_TO_PIECE, NON_PROMOTED_TO_PROMOTED
    # --- 文字と駒の対応付け ---
    CHAR_TO_PIECE['K'] = Piece.BlackKing
    CHAR_TO_PIECE['k'] = Piece.WhiteKing
    CHAR_TO_PIECE['R'] = Piece.BlackRook
    CHAR_TO_PIECE['r'] = Piece.WhiteRook
    CHAR_TO_PIECE['B'] = Piece.BlackBishop
    CHAR_TO_PIECE['b'] = Piece.WhiteBishop
    CHAR_TO_PIECE['G'] = Piece.BlackGold
    CHAR_TO_PIECE['g'] = Piece.WhiteGold
    CHAR_TO_PIECE['S'] = Piece.BlackSilver
    CHAR_TO_PIECE['s'] = Piece.WhiteSilver
    CHAR_TO_PIECE['N'] = Piece.BlackKnight
    CHAR_TO_PIECE['n'] = Piece.WhiteKnight
    CHAR_TO_PIECE['L'] = Piece.BlackLance
    CHAR_TO_PIECE['l'] = Piece.WhiteLance
    CHAR_TO_PIECE['P'] = Piece.BlackPawn
    CHAR_TO_PIECE['p'] = Piece.WhitePawn
    # --- 成り駒の対応付け ---
    NON_PROMOTED_TO_PROMOTED[Piece.BlackPawn]   = Piece.BlackPromotedPawn
    NON_PROMOTED_TO_PROMOTED[Piece.BlackLance]  = Piece.BlackPromotedLance
    NON_PROMOTED_TO_PROMOTED[Piece.BlackKnight] = Piece.BlackPromotedKnight
    NON_PROMOTED_TO_PROMOTED[Piece.BlackSilver] = Piece.BlackPromotedSilver
    NON_PROMOTED_TO_PROMOTED[Piece.BlackBishop] = Piece.BlackHorse
    NON_PROMOTED_TO_PROMOTED[Piece.BlackRook]   = Piece.BlackDragon
    NON_PROMOTED_TO_PROMOTED[Piece.WhitePawn]   = Piece.WhitePromotedPawn
    NON_PROMOTED_TO_PROMOTED[Piece.WhiteLance]  = Piece.WhitePromotedLance
    NON_PROMOTED_TO_PROMOTED[Piece.WhiteKnight] = Piece.WhitePromotedKnight
    NON_PROMOTED_TO_PROMOTED[Piece.WhiteSilver] = Piece.WhitePromotedSilver
    NON_PROMOTED_TO_PROMOTED[Piece.WhiteBishop] = Piece.WhiteHorse
    NON_PROMOTED_TO_PROMOTED[Piece.WhiteRook]   = Piece.WhiteDragon

def transform_to_promoted_piece(piece: Piece) -> Piece:
    return NON_PROMOTED_TO_PROMOTED.get(piece, piece)

def transform_to_opponent_hand_piece(piece: Piece) -> Piece:
    if piece == Piece.NoPiece:
        return Piece.NoPiece
    # Black の駒を取ったら White の持ち駒に変換（その逆も）
    if 1 <= piece.value <= 14:
        return Piece(piece.value + 14)
    elif 15 <= piece.value <= 28:
        return Piece(piece.value - 14)
    return piece

# =======================================
# 5. 局面のデータ構造（Position クラス）
class Position:
    BOARD_SIZE = 9  # 将棋盤は9x9
    StartposSfen = "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1"

    def __init__(self):
        self.side_to_move = Color.Black
        self.board = [[Piece.NoPiece for _ in range(Position.BOARD_SIZE)] for _ in range(Position.BOARD_SIZE)]
        self.hand_pieces = [0] * len(PIECE_KANJIS)
        self.play = 0
        self.last_move = None

    # print(position)で、__str__がよばれ、盤面が文字列として出力される。
    def __str__(self):
        lines = []
        horizontal_line = "+----" * Position.BOARD_SIZE + "+"
        lines.append(horizontal_line)
        for rank in range(Position.BOARD_SIZE):
            line = "|"
        # line を構築するfor
            for file in range(Position.BOARD_SIZE - 1, -1, -1):
                piece_str = get_kanji_from_piece(self.board[file][rank])
                line += piece_str.center(3) + "|"
            lines.append(line)
            lines.append(horizontal_line)
        black_hand = ""
        white_hand = ""
        for piece in Piece:
            if 1 <= piece.value < 15:
                black_hand += get_kanji_from_piece(piece).strip() * self.hand_pieces[piece.value]
            elif 15 <= piece.value < len(PIECE_KANJIS):
                white_hand += get_kanji_from_piece(piece).strip() * self.hand_pieces[piece.value]
        lines.append("先手 持ち駒: " + black_hand + " , 後手 持ち駒: " + white_hand)
        side_str = "先手" if self.side_to_move == Color.Black else "後手"
        lines.append(f"手番 = {side_str}")
        lines.append(f"手数 = {self.play}")
        return "\n".join(lines)

    def set_board_from_sfen(self, sfen: str):
        #  初期化：盤面・持ち駒をクリアし、手数を1にリセット
        self.side_to_move = Color.Black
        for f in range(Position.BOARD_SIZE):
            for r in range(Position.BOARD_SIZE):
                self.board[f][r] = Piece.NoPiece
        self.hand_pieces = [0] * len(self.hand_pieces)
        self.play = 1

        file = Position.BOARD_SIZE - 1
        rank = 0
        index = 0
        promotion = False

        # 盤面パース（スペースまで読み込む）
        while index < len(sfen) and sfen[index] != ' ':
            ch = sfen[index]
            index += 1
            if ch == '/':   # / は段(rankの切り替わり)を意味する。行(rank)と列(列)について更新。
                rank += 1
                file = Position.BOARD_SIZE - 1
            elif ch == '+':             # 直後の駒の"成り"を表す記号
                promotion = True
            elif ch.isdigit():          # chが数字の時True。その数の分だけ空白マス。
                # 空のマスの数を数えて、その分だけ NoPiece を配置する
                empty = int(ch)
                for _ in range(empty):
                    self.board[file][rank] = Piece.NoPiece
                    file -= 1
            else:
                # 駒の文字の場合：CHAR_TO_PIECE を使って駒に変換
                piece = CHAR_TO_PIECE.get(ch)
                if piece is None:
                    raise ValueError(f"未知の駒文字: {ch}")
                if promotion:       # もし promotion フラグが立っていれば、成り変換する。
                    piece = transform_to_promoted_piece(piece)
                    promotion = False
                self.board[file][rank] = piece
                file -= 1

        while index < len(sfen) and sfen[index] == ' ':
            index += 1

        # 手番パース
        if index < len(sfen):
            side_char = sfen[index]
            index += 1
            self.side_to_move = Color.Black if side_char == 'b' else Color.White

        while index < len(sfen) and sfen[index] == ' ':
            index += 1

        # 持ち駒パース:'-'の場合は持ち駒なし、数字は枚数、文字は駒
            # 持ち駒については、先手後手のそれぞれの持ち駒の種類と、その枚数を表記します。枚数は、２枚以上であれば、駒の種類の前にその数字を表記します。
            # 先手側が銀１枚歩２枚、後手側が角１枚歩３枚であれば、S2Pb3pと表記されます。
        count = 0
        while index < len(sfen) and sfen[index] != ' ':
            ch = sfen[index]
            index += 1
            if ch == '-':
                continue
            if ch.isdigit():
                # 複数桁の数字を正しく数値に変換するため下記の計算になってる。
                    # (例)数字「1」と「0」が連続している場合、「1」を読むと count = 0 * 10 + 1 で count が 1 -> 次に「0」を読むと count = 1 * 10 + 0 で count が 10 になる！
                count = count * 10 + int(ch)
                continue
            piece = CHAR_TO_PIECE.get(ch)
            if piece is None:
                raise ValueError(f"未知の持ち駒文字: {ch}")
            # 数字(count)があればその枚数だけ記録、なければ1枚
            self.hand_pieces[piece.value] += count if count > 0 else 1
            count = 0

        while index < len(sfen) and sfen[index] == ' ':
            index += 1

        # 手数パース 最後に残った文字列を整数に変換して、手数としてセットする。
        if index < len(sfen):
            self.play = int(sfen[index:])

# =======================================
# 6. 指し手（Move）データ構造
class Move:
    def __init__(self, file_from, rank_from, piece_from, file_to, rank_to, piece_to, drop, promotion, side_to_move):
        self.file_from = file_from
        self.rank_from = rank_from
        self.piece_from = piece_from
        self.file_to = file_to
        self.rank_to = rank_to
        self.piece_to = piece_to
        self.drop = drop
        self.promotion = promotion
        self.side_to_move = side_to_move

    def __str__(self):
        # 出力形式：先手は「▲」、後手は「△」
        RANK_TO_KANJI = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
        prefix = "▲" if self.side_to_move == Color.Black else "△"
        dest = f"{self.file_to + 1}{RANK_TO_KANJI[self.rank_to]}"
        piece_str = get_kanji_from_piece(self.piece_from).strip()
        return f"{prefix}{dest}{piece_str}"

# __eq__ と __hash__ は set や dict を使うと Python が自動で呼び出す ので、通常は明示的に呼び出すことはない。
    # Moveインスタンスの比較のための関数 : move1 == move2 は move1.__eq__(move2) という処理
    def __eq__(self, other):
        if not isinstance(other, Move): # Moveクラスのインスタンスでなければ False
            return False
        return (self.file_from, self.rank_from, self.piece_from, self.file_to, self.rank_to,
                self.piece_to, self.drop, self.promotion, self.side_to_move) == \
               (other.file_from, other.rank_from, other.piece_from, other.file_to, other.rank_to,
                other.piece_to, other.drop, other.promotion, other.side_to_move)
    # hash() を使ったときに、Moveオブジェクトのキーを返す
    def __hash__(self):
        return hash((self.file_from, self.rank_from, self.piece_from, self.file_to, self.rank_to,
                     self.piece_to, self.drop, self.promotion, self.side_to_move))
                     
    # インスタンスを使わない関数にするデコレータ @staticmethod
    # make_moveは Move クラスのインスタンスを使わず、単に USIの指し手文字列(move_str)から Move オブジェクトを作るだけなのでインスタンスが不要の関数。
    @staticmethod
    def make_move(position, move_str):
    # move_str: USI形式の指し手を表す文字列（例: "7g7f" や "G*5b"）
    # USI形式の文字列から Move オブジェクトを作る
        if move_str in {"resign", "win", "none"}:
            if move_str == "resign":
                return Move.RESIGN
            elif move_str == "win":
                return Move.WIN
            else:
                return Move.NONE
        #  持ち駒を打つとき("G*5b")　持ち駒を打つときは、最初に駒の種類を大文字で書き、それに*を追加し、さらに打った場所を追加します。金を５二に打つ場合は"G*5b"となります
        if move_str[1] == '*':
            piece = CHAR_TO_PIECE.get(move_str[0])
            file_to = ord(move_str[2]) - ord('1')
            rank_to = ord(move_str[3]) - ord('a')
            return Move(-1, -1, piece, file_to, rank_to, Piece.NoPiece,                     #Move オブジェクトを作成して返している！駒を「打つ」操作だから、drop=True となるよ。
                        drop=True, promotion=False, side_to_move=position.side_to_move)
        # 駒を移動する（移動手）処理("7g7f")
        else:
            file_from = ord(move_str[0]) - ord('1')
            rank_from = ord(move_str[1]) - ord('a')
            file_to = ord(move_str[2]) - ord('1')
            rank_to = ord(move_str[3]) - ord('a')
            promotion = (len(move_str) == 5 and move_str[4] == '+')  # 指し手について、駒が成るときは、最後に+を追加します。８八の駒が２二に移動して成るなら"8h2b+""
            piece_from = position.board[file_from][rank_from]           # piece_from は移動元の駒、piece_to は移動先の駒を盤面から取得している。
            piece_to = position.board[file_to][rank_to]
            return Move(file_from, rank_from, piece_from, file_to, rank_to, piece_to,           # Move オブジェクトを作成して返しているよ。駒を「移動」する場合は drop=False となる！
                        drop=False, promotion=promotion, side_to_move=position.side_to_move)

    # moveをUSIに変換する関数
    def transform_move_to_USI(self):
        if self == Move.RESIGN:
            return "resign"
        elif self == Move.WIN:
            return "win"
        # elif self == Move.NONE:
        #     return "none"

        usi_string = ""
        # 打ち手の場合
        if self.drop:
            usi_string += get_usi_char_from_piece(self.piece_from).upper()
            usi_string += "*"
        # 通常手の場合
        else:
            usi_string += chr(self.file_from + ord('1'))
            usi_string += chr(self.rank_from + ord('a'))

        usi_string += chr(self.file_to + ord('1'))
        usi_string += chr(self.rank_to + ord('a'))

        if self.promotion:
            usi_string += "+"
        
        return usi_string

# 特別な指し手
Move.RESIGN = Move(2, 2, None, 2, 2, None, False, False, None)
Move.WIN = Move(3, 3, None, 3, 3, None, False, False, None)
Move.NONE = Move(4, 4, None, 4, 4, None, False, False, None)

# =======================================
# 7. 移動方向の定義
class Direction:
    def __init__(self, delta_file, delta_rank):
        self.delta_file = delta_file
        self.delta_rank = delta_rank

class MoveDirection:
    def __init__(self, direction, long=False):
        self.direction = direction
        self.long = long

UpLeft    = Direction(+1, -1)
Up        = Direction(0, -1)
UpRight   = Direction(-1, -1)
Left      = Direction(+1, 0)
Right     = Direction(-1, 0)
DownLeft  = Direction(+1, +1)
Down      = Direction(0, +1)
DownRight = Direction(-1, +1)

# 隣接リストのように、コマの値ごとの移動方法を管理。
MOVE_DIRECTIONS = [None] * (max(piece.value for piece in Piece) + 1)
MOVE_DIRECTIONS[0] = None
# Black 系
MOVE_DIRECTIONS[Piece.BlackPawn.value] = [MoveDirection(Up)]
MOVE_DIRECTIONS[Piece.BlackLance.value] = [MoveDirection(Up, long=True)]
MOVE_DIRECTIONS[Piece.BlackKnight.value] = [MoveDirection(Direction(+1, -2)), MoveDirection(Direction(-1, -2))]
MOVE_DIRECTIONS[Piece.BlackSilver.value] = [MoveDirection(UpLeft), MoveDirection(Up), MoveDirection(UpRight),
                                              MoveDirection(DownLeft), MoveDirection(DownRight)]
MOVE_DIRECTIONS[Piece.BlackGold.value] = [MoveDirection(UpLeft), MoveDirection(Up), MoveDirection(UpRight),
                                            MoveDirection(Left), MoveDirection(Right), MoveDirection(Down)]
MOVE_DIRECTIONS[Piece.BlackBishop.value] = [MoveDirection(UpLeft, long=True), MoveDirection(UpRight, long=True),
                                              MoveDirection(DownLeft, long=True), MoveDirection(DownRight, long=True)]
MOVE_DIRECTIONS[Piece.BlackRook.value] = [MoveDirection(Up, long=True), MoveDirection(Left, long=True),
                                            MoveDirection(Right, long=True), MoveDirection(Down, long=True)]
MOVE_DIRECTIONS[Piece.BlackKing.value] = [MoveDirection(UpLeft), MoveDirection(Up), MoveDirection(UpRight),
                                            MoveDirection(Left), MoveDirection(Right),
                                            MoveDirection(DownLeft), MoveDirection(Down), MoveDirection(DownRight)]
for p in [Piece.BlackPromotedPawn, Piece.BlackPromotedLance, Piece.BlackPromotedKnight, Piece.BlackPromotedSilver]:
    MOVE_DIRECTIONS[p.value] = MOVE_DIRECTIONS[Piece.BlackGold.value]
MOVE_DIRECTIONS[Piece.BlackHorse.value] = [MoveDirection(UpLeft, long=True), MoveDirection(Up), MoveDirection(UpRight, long=True),
                                             MoveDirection(Left), MoveDirection(Right),
                                             MoveDirection(DownLeft, long=True), MoveDirection(Down), MoveDirection(DownRight, long=True)]
MOVE_DIRECTIONS[Piece.BlackDragon.value] = [MoveDirection(UpLeft), MoveDirection(Up, long=True), MoveDirection(UpRight),
                                              MoveDirection(Left, long=True), MoveDirection(Right, long=True),
                                              MoveDirection(DownLeft), MoveDirection(Down, long=True), MoveDirection(DownRight)]
# White 系
MOVE_DIRECTIONS[Piece.WhitePawn.value] = [MoveDirection(Down)]
MOVE_DIRECTIONS[Piece.WhiteLance.value] = [MoveDirection(Down, long=True)]
MOVE_DIRECTIONS[Piece.WhiteKnight.value] = [MoveDirection(Direction(+1, 2)), MoveDirection(Direction(-1, 2))]
MOVE_DIRECTIONS[Piece.WhiteSilver.value] = [MoveDirection(UpLeft), MoveDirection(UpRight), MoveDirection(DownLeft),
                                              MoveDirection(Down), MoveDirection(DownRight)]
MOVE_DIRECTIONS[Piece.WhiteGold.value] = [MoveDirection(Up), MoveDirection(Left), MoveDirection(Right),
                                            MoveDirection(DownLeft), MoveDirection(Down), MoveDirection(DownRight)]
MOVE_DIRECTIONS[Piece.WhiteBishop.value] = [MoveDirection(UpLeft, long=True), MoveDirection(UpRight, long=True),
                                              MoveDirection(DownLeft, long=True), MoveDirection(DownRight, long=True)]
MOVE_DIRECTIONS[Piece.WhiteRook.value] = [MoveDirection(Up, long=True), MoveDirection(Left, long=True),
                                            MoveDirection(Right, long=True), MoveDirection(Down, long=True)]
MOVE_DIRECTIONS[Piece.WhiteKing.value] = [MoveDirection(UpLeft), MoveDirection(Up), MoveDirection(UpRight),
                                            MoveDirection(Left), MoveDirection(Right),
                                            MoveDirection(DownLeft), MoveDirection(Down), MoveDirection(DownRight)]
for p in [Piece.WhitePromotedPawn, Piece.WhitePromotedLance, Piece.WhitePromotedKnight, Piece.WhitePromotedSilver]:
    MOVE_DIRECTIONS[p.value] = MOVE_DIRECTIONS[Piece.WhiteGold.value]
MOVE_DIRECTIONS[Piece.WhiteHorse.value] = [MoveDirection(UpLeft, long=True), MoveDirection(Up), MoveDirection(UpRight, long=True),
                                             MoveDirection(Left), MoveDirection(Right),
                                             MoveDirection(DownLeft, long=True), MoveDirection(Down), MoveDirection(DownRight, long=True)]
MOVE_DIRECTIONS[Piece.WhiteDragon.value] = [MoveDirection(UpLeft), MoveDirection(Up, long=True), MoveDirection(UpRight),
                                              MoveDirection(Left, long=True), MoveDirection(Right, long=True),
                                              MoveDirection(DownLeft), MoveDirection(Down, long=True), MoveDirection(DownRight)]

# =======================================
# 8. ヘルパー関数群
def get_piece_color(piece: Piece):
    if piece == Piece.NoPiece:
        return None
    return Color.Black if 1 <= piece.value <= 14 else Color.White

def is_can_promote_piece(piece: Piece) -> bool:
    return piece in {Piece.BlackPawn, Piece.BlackLance, Piece.BlackKnight, Piece.BlackSilver,
                     Piece.BlackBishop, Piece.BlackRook,
                     Piece.WhitePawn, Piece.WhiteLance, Piece.WhiteKnight, Piece.WhiteSilver,
                     Piece.WhiteBishop, Piece.WhiteRook}


# 成らずに打てるか？の判定  (例)歩・香車 → 最終段（敵陣の最奥）には打てない
def is_can_put_without_promotion(piece: Piece, rank: int, side: Color) -> bool:
    if side == Color.Black:
        if piece == Piece.BlackPawn or piece == Piece.BlackLance:
            return rank > 0
        if piece == Piece.BlackKnight:
            return rank > 1
    elif side == Color.White:
        if piece == Piece.WhitePawn or piece == Piece.WhiteLance:
            return rank < Position.BOARD_SIZE - 1
        if piece == Piece.WhiteKnight:
            return rank < Position.BOARD_SIZE - 2
    return True

def is_pawn_exist(board, file: int, side: Color) -> bool:
    for r in range(Position.BOARD_SIZE):
        piece = board[file][r]
        if side == Color.Black and piece == Piece.BlackPawn:
            return True
        if side == Color.White and piece == Piece.WhitePawn:
            return True
    return False

# =======================================
# 9. 指し手生成(position から move を yield 出力する)
def generate_moves(position):
    side_to_move = position.side_to_move
    board = position.board
    hand_pieces = position.hand_pieces
    non_capture_promotion_moves = []    # 成り手のうち、駒を取らないもの
    non_capture_nonpromotion_moves = []     # 成らない手のうち、駒を取らないもの

    # 盤上の駒を動かす指し手の生成
    for file_from in range(Position.BOARD_SIZE):
        for rank_from in range(Position.BOARD_SIZE):
            piece_from = board[file_from][rank_from]
            if piece_from == Piece.NoPiece:
                continue
            if get_piece_color(piece_from) != side_to_move: # 相手の駒なら動かせないのでスキップ
                continue
            move_dirs = MOVE_DIRECTIONS[piece_from.value]
            if move_dirs is None:
                continue
            for move_direction in move_dirs:
                max_distance = 8 if move_direction.long else 1
                file_to = file_from
                rank_to = rank_from
            # 1地点の見方の駒の、ある1つの動かし方に注目して、long=Trueの場合、ループ
                for distance in range(max_distance):
                    file_to += move_direction.direction.delta_file
                    rank_to += move_direction.direction.delta_rank
                    if file_to < 0 or file_to >= Position.BOARD_SIZE or rank_to < 0 or rank_to >= Position.BOARD_SIZE:
                        break
                    piece_to = board[file_to][rank_to]      # 移動先にあるコマ
                    if piece_to != Piece.NoPiece and get_piece_color(piece_to) == side_to_move:  # 移動先の駒が仲間だと、進めないのでbreakで終了
                        break
                # 成り手の処理
                    if is_can_promote_piece(piece_from) and (
                        (side_to_move == Color.Black and (rank_to <= 2 or rank_from <= 2)) or
                        (side_to_move == Color.White and (rank_to >= Position.BOARD_SIZE - 3 or rank_from >= Position.BOARD_SIZE - 3))
                    ):
                        move = Move(file_from, rank_from, piece_from, file_to, rank_to, piece_to,       # 成れる駒なら promotion=True の手を作る
                                    drop=False, promotion=True, side_to_move=side_to_move)
                        if piece_to != Piece.NoPiece:                                                   # 駒を取る手なら即 yield
                            yield move
                        else:                                                                           # 非取りなら non_capture_promotion_moves に保存
                            non_capture_promotion_moves.append(move)
                # 成らない手の処理
                    if is_can_put_without_promotion(piece_from, rank_to, side_to_move):                 # 成らずで動けるなら promotion=False の手を作る
                        move = Move(file_from, rank_from, piece_from, file_to, rank_to, piece_to,
                                    drop=False, promotion=False, side_to_move=side_to_move)
                        if piece_to != Piece.NoPiece:                                                   # 駒を取る手なら即 yield
                            yield move
                        else:                                                                           # 非取りなら non_capture_nonpromotion_moves に保存
                            non_capture_nonpromotion_moves.append(move)
                    if piece_to != Piece.NoPiece:                                           # 敵の駒を取ったらそれ以上先進ませずに、そこでストップ（飛車や角もここで止まる）
                        break
    # 非取りの手は最後に yieldする。成り手 → 成らない手の順番で生成！
    for move in non_capture_promotion_moves:
        yield move
    for move in non_capture_nonpromotion_moves:
        yield move

    # 「持ち駒(drop)を打つ手」の処理
        # 持ち駒を「歩」から「飛車」までループでチェック するための範囲指定
    min_piece = Piece.BlackPawn if side_to_move == Color.Black else Piece.WhitePawn
    max_piece = Piece.BlackRook if side_to_move == Color.Black else Piece.WhiteRook
    for p_val in range(min_piece.value, max_piece.value + 1):
        piece_from = Piece(p_val)   # これから打とうとしている持ち駒
        if hand_pieces[piece_from.value] == 0:  # 指定した種類の持ち駒なしの場合
            continue
        for file_to in range(Position.BOARD_SIZE):
            for rank_to in range(Position.BOARD_SIZE):
                if board[file_to][rank_to] != Piece.NoPiece:    # すでに駒がある場所は 打てない
                    continue
                if not is_can_put_without_promotion(piece_from, rank_to, side_to_move):    # 桂馬・香車・歩は 打てる場所に制限ありなのでチェック
                    continue
                if piece_from in {Piece.BlackPawn, Piece.WhitePawn} and is_pawn_exist(board, file_to, side_to_move):  #二歩を防ぐ処理もここで行う！
                    continue
                yield Move(-1, -1, piece_from, file_to, rank_to, Piece.NoPiece,
                           drop=True, promotion=False, side_to_move=side_to_move)

# yieldとは? : 普通の return とは違い、一度 yield で値を返しても関数の状態を保持したままで、次の続きの処理を続ける のが特徴。

# =======================================
# 10. 局面操作：指し手の適用と取り消し(positionに対して、moveオブジェクトを読み込んで変化を加える)
# 駒を動かすための補助関数
    # 盤面に駒を置く関数
def put_piece(board, file, rank, piece):
    assert board[file][rank] == Piece.NoPiece, "配置先に駒がある！"
    board[file][rank] = piece

    # 盤面から駒を取り除く関数
def remove_piece(board, file, rank):
    assert board[file][rank] != Piece.NoPiece, "そこには駒がない！"
    board[file][rank] = Piece.NoPiece

# position に move を適用して実際に局面を変更する関数
def do_move(position, move):
    assert position.side_to_move == move.side_to_move, "手番が合わない！"
    if move.piece_to != Piece.NoPiece:                                      # 取った駒（move.piece_to）があった場合、その駒を盤面から取り除く
        remove_piece(position.board, move.file_to, move.rank_to)
        position.hand_pieces[transform_to_opponent_hand_piece(move.piece_to).value] += 1  # 敵味方(black or white)を変換して、手持ちのコマとして追加する。
    if move.drop:                                                                   # 手駒から選んでコマを打つ場合の処理
        assert position.hand_pieces[move.piece_from.value] > 0, "持ち駒がない！"
        position.hand_pieces[move.piece_from.value] -= 1
    else:                                                                           # すでに盤面にある駒を移動する場合は、移動元の駒を盤面から取り除いて、次に進む。
        remove_piece(position.board, move.file_from, move.rank_from)
    new_piece = transform_to_promoted_piece(move.piece_from) if move.promotion else move.piece_from     # 成りがある場合、成った後のコマに更新
    put_piece(position.board, move.file_to, move.rank_to, new_piece)                    # 移動先のマスに新しい駒（または昇格した駒）を配置して、盤面boardを更新する！
    position.side_to_move = get_opponent_color(position.side_to_move)                          # 最後に、次の手番を相手に渡すために、手番を切り替えたり、手数を増やしたりする。
    position.play += 1
    position.last_move = move                                                           # それと、今回の指し手を記録しておくよ。これでゲームが進んだことを記録できる！

# 指し手を元に戻す関数 : 探索時などで指し手を適用・元に戻す処理が必要になるため、局面を一手戻す関数も実装
def undo_move(position, move):
    position.play -= 1                                              # まず最初に、手数（position.play）を1つ減らして、手番を元に戻すよ。これで「戻す」動作ができる。
    position.side_to_move = get_opponent_color(position.side_to_move)
    remove_piece(position.board, move.file_to, move.rank_to)        # 盤面から、元々移動先に置いた駒を取り除いて、戻す。
    if move.drop:                                                   # もし駒を「打つ」手だった場合、その駒を持ち駒に戻す！これで、駒を打った時に戻してあげる処理をしている。
        position.hand_pieces[move.piece_from.value] += 1
    else:                                                           # 駒を「移動」した場合、その駒を元の位置に戻すよ。
        put_piece(position.board, move.file_from, move.rank_from, move.piece_from)
    if move.piece_to != Piece.NoPiece:                                                  # 最後に、もし相手の駒を取った場合、その駒を持ち駒から取り除き、元の位置に戻す。
        position.hand_pieces[transform_to_opponent_hand_piece(move.piece_to).value] -= 1
        put_piece(position.board, move.file_to, move.rank_to, move.piece_to)


# =======================================
# 11. 評価関数
class Evaluator:
    # PieceValues の配列。インデックスは Piece.value に対応している。各駒に割り当てた値は一般的に使われる駒価値に準拠しています。
    PIECE_VALUES = [
        0,     # NoPiece
        90,    # BlackPawn（歩）
        315,   # BlackLance（香）
        405,   # BlackKnight（桂）
        495,   # BlackSilver（銀）
        540,   # BlackGold（金）
        855,   # BlackBishop（角）
        945,   # BlackRook（飛）
        15000, # BlackKing（王）
        540,   # BlackPromotedPawn（と）
        540,   # BlackPromotedLance（成香）
        540,   # BlackPromotedKnight（成桂）
        540,   # BlackPromotedSilver（成銀）
        945,   # BlackHorse（馬）
        1395,  # BlackDragon（龍）
        -90,   # WhitePawn（歩↓）
        -315,  # WhiteLance（香↓）
        -405,  # WhiteKnight（桂↓）
        -495,  # WhiteSilver（銀↓）
        -540,  # WhiteGold（金↓）
        -855,  # WhiteBishop（角↓）
        -945,  # WhiteRook（飛↓）
        -15000,     # WhiteKing（王↓）
        -540,  # WhitePromotedPawn（と↓）
        -540,  # WhitePromotedLance（成香↓）
        -540,  # WhitePromotedKnight（成桂↓）
        -540,  # WhitePromotedSilver（成銀↓）
        -945,  # WhiteHorse（馬↓）
        -1395  # WhiteDragon（龍↓）
    ]

    @staticmethod
    def evaluate(position):  # 評価値を出力する関数：盤面と持ち駒の駒価値の合計を計算する
        value = 0
        # 盤面上の駒の評価値の合計を求める
        for file in range(Position.BOARD_SIZE):
            for rank in range(Position.BOARD_SIZE):
                piece = position.board[file][rank]
                value += Evaluator.PIECE_VALUES[piece.value]
        # 持ち駒の評価値の合計を求める
        for i in range(len(position.hand_pieces)):
            value += Evaluator.PIECE_VALUES[i] * position.hand_pieces[i]
        # 後手の場合は評価値を反転
        if position.side_to_move == Color.White:
            value = -value
        return value

# =======================================
# 12. ミニマックス法を用いた最善手の探索部(11. の評価関数を利用)
import time

class BestMove:
    def __init__(self, move, value):
        self.move = move
        self.value = value

class Searcher:
    # ある頂点(盤面)視点から、複数生えている辺(指し手)の中から、1つだけ最適な辺(最善の指し手 と 最善と判断したエビデンスに該当する評価値)を返す関数  (DFSの探索挙動)
        # 頂点: 盤面(positionのイメージ), 複数の辺 : たくさんある指し手(moveのイメージ)
        # この視点が、親ノード->子ノードの遷移で、敵/味方 が切り替わるのが重要ポイント。
        # つまり、子ノードから返されるの最善手(1個)は、敵にとっての最善手になっている。
    @staticmethod
    def search(position, depth, nodes):

        # 基底条件 : ある頂点に到達したとき、再帰深さが0だったら、再帰を終了する。
            # この局面では指し手は選択せずに、盤面の評価値だけを行う。
            # これらの葉ノードの「値」がボトムアップで、味方・敵の視点の真逆の基準で選択されながら(値に-1をかけ算しながら)、根に向かって候補値が絞られるイメージ。
        if depth == 0:
            return BestMove(Move.NONE, Evaluator.evaluate(position))
        
        # 初期値のセット
        best_move = Move.RESIGN  # 最善手の初期値としては投了を設定しておく
        best_value = -float('inf')
        
        moves = list(generate_moves(position))
        # moveを1つ取り出して、盤面に適用すると、敵盤面へ遷移
        for move in moves:
            # 相手の王を取れるなら最善手として即採用する
            if move.piece_to == Piece.BlackKing or move.piece_to == Piece.WhiteKing:
                return BestMove(move, float('inf'))
        
            nodes[0] += 1  # 探索ノード数を管理
            do_move(position, move)  # move適用すると、敵の盤面になる
            child_best_move = Searcher.search(position, depth - 1, nodes)  # 子ノード(1つ)から返される最善手(1つ) (<- 敵視点での(評価値に基づく)最善手)
            undo_move(position, move)  # 自分の盤面に戻す

            # ネガマックス法: ミニマックスの簡略化バージョン
            value = - child_best_move.value  # 子ノード(1つ)から返される最善手(1つ)は、敵にとっての最善手。従って複数子ノードから返る複数の指し手の中で、価値が最小(-1をかけた時には最大)のものを選べば良い。(悪あがきのイメージ)
            if value > best_value:
                best_value = value
                best_move = move

        # 手下全員の言い分をforで訊き終えてから return するタイプの再帰。(ただし、手下とは犬猿の仲で、真逆のことを互いに主張しているイメージ。)
        return BestMove(best_move, best_value)  # 最善の指し手 と 最善と判断したエビデンスに該当する評価値 をセットにして返す。


# =======================================
# 13. USIプロトコルに対応したメイン処理

# import random

def main():
    initialize_types()
    position = Position()

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue

        parts = line.split()
        if len(parts) == 0:
            continue

        command = parts[0]

        if command == "usi":
            print("id name My Shogi Engine")
            print("id author YourName")
            print("option name USI_Ponder type check default true")
            print("option name USI_Hash type spin default 256")
            print("usiok")
        elif command == "isready":
            print("readyok")
        elif command == "position":
            if parts[1] == "startpos":
                position.set_board_from_sfen(Position.StartposSfen)
                next_index = 2
            elif parts[1] == "sfen":
                sfen = " ".join(parts[2:6])
                position.set_board_from_sfen(sfen)
                next_index = 6
            else:
                print(f"info string 不正なpositionコマンド: {line}")
                continue
            # 指し手があれば適用する
            for token in parts[next_index:]:
                if token == "moves":
                    continue
                move = Move.make_move(position, token)  # move 生成
                do_move(position, move)                 # positionに対して、moveを適用
        elif command == "d":
            print(position)
        elif command == "generatemove":
            moves = list(generate_moves(position))
            if moves:
                for move in moves:
                    print(move, end=" ")
                print()  #  最後に改行を入れる : エンジンがコマンドの行を送信する場合、最後に必ず改行コード（\n）を追加する必要がある。改行コードがないと、GUIは行の終わりを認識できない。
            else:
                print("no moves")
        elif command == "go":
            # ランダム指し手生成
            # moves = list(generate_moves(position))
            # if not moves:
            #     print("bestmove resign")
            # else:
            #     move = random.choice(moves)
            #     print("bestmove " + move.transform_move_to_USI())

            depth = 3  # 探索深さ（必要に応じて調整可能）
            begin_time = time.time()
            nodes = [0] # 探索ノード数を管理
            best_move = Searcher.search(position, depth, nodes)
            end_time = time.time()
            delta_time = int((end_time - begin_time) * 1000)  #　探索時間をmsに変換
            nps = int(nodes[0] / (end_time - begin_time)) if (end_time - begin_time) > 0 else 0
            best_move_string = best_move.move.transform_move_to_USI()
            score_CP = best_move.value
            # info コマンドで探索情報を出力
            print(f"info depth {depth} seldepth {depth} time {delta_time} nodes {nodes[0]} score cp {score_CP} nps {nps} pv {best_move_string}")

            if best_move.value < -30000:
                print("bestmove resign")
            else:
                print("bestmove " + best_move_string)

        elif command == "eval":
            print(Evaluator.evaluate(position))
        elif command == "quit":
            break
        elif command in ["usinewgame", "setoption", "stop", "ponderhit", "gameover"]:
            pass    # もし pass を削除すると、Python は elif のブロックに何も処理がないとエラーを出してしまう。
        else:
            print(f"info string Unsupported command: {command}")

        sys.stdout.flush()

if __name__ == "__main__":
    main()

# Python のすべてのモジュール（←つまりPythonファイル）には特殊な変数 __name__ があり、スクリプトが直接実行された場合は "__main__" というモジュール名の値が設定される。
# プログラムを実行したときに、「このコードはメインプログラム（他のファイルからインポートされず、直接実行されているもの）として動いているか？」を確認している
# つまりは、このコードが直接実行される場合のみmain()が動くようにしてる

# USIプロトコルは、標準入出力（stdin/stdout）を用いたテキストベースのプロトコルであり、シンプルに、print() と sys.stdout.flush() を使うだけで通信できる。