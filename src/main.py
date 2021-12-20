import pathlib
import heapq
import copy

SIZE = 8


def init_board():
    board = []

    for _ in range(0, SIZE):
        row = []
        for _ in range(0, SIZE):
            row.append(0)
        board.append(row)

    return copy.deepcopy(board)


def draw_board(
        list_queens=[],
        board=init_board()
):
    _board = copy.deepcopy(board)

    for queen in list_queens:
        pos_i = queen[0]
        pos_j = queen[1]

        _board[pos_i][pos_j] = _board[pos_i][pos_j] + SIZE + 1

        for i in range(0, SIZE):
            for j in range(0, SIZE):
                if i == pos_i and j == pos_j:
                    continue

                if i == pos_i or j == pos_j or pos_i + pos_j == i + j or pos_i - pos_j == i - j:
                    _board[i][j] = _board[i][j] + 1

    return copy.deepcopy(_board)


def decode_board(board=init_board()):
    result = ""
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            result = result + str(board[i][j] == 9 and 'x' or '_') + " "
        result = result + "\n"

    return result


def cal_h(board=init_board()):
    h = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (board[i][j] == 0):
                h = h + 1

    return h


def check_if_can_place(queen_pos, board):
    pos_i = queen_pos[0]
    pos_j = queen_pos[1]

    return board[pos_i][pos_j] == 0


def place_queens(initial_queens=[]):
    list_result = []
    for queens in initial_queens:
        list_result.append(queens)

    queue = []
    init_board = draw_board(list_queens=list_result)
    init_h = cal_h(init_board)
    heapq.heappush(
        queue, (init_h, list_result, init_board))

    decoded_board = decode_board(board=init_board)
    visited_states = [decode_board]

    tree_board = {}

    while (len(queue) != 0):
        (current_h, current_list, current_board) = heapq.heappop(queue)


        if (len(current_list) > len(list_result)):
            list_result = copy.deepcopy(current_list)
            if len(list_result) >= SIZE:
                break

        for i in range(0, SIZE):
            for j in range(0, SIZE):
                if check_if_can_place(queen_pos=(i, j), board=current_board):

                    next_board = draw_board(
                        list_queens=[(i, j)],
                        board=copy.deepcopy(current_board)
                    )
                    next_list = copy.deepcopy(current_list)
                    next_list.append((i, j))

                    # skip if have visited this state before
                    decoded_next_board = decode_board(board=next_board)
                    if decoded_next_board in visited_states:
                        continue

                    visited_states.append(decoded_next_board)
                    decoded_current_board = decode_board(board=current_board)
                    if not decoded_current_board in tree_board:
                        tree_board[decoded_current_board] = []
                    
                    tree_board[decoded_current_board].append(decoded_next_board)



                    heapq.heappush(
                        queue, (cal_h(next_board), next_list, next_board))

    return (list_result, tree_board)


list_queens = []
rootDir = str(pathlib.Path().resolve())

f = open(rootDir + '/input.txt', 'r')
m = int(f.readline())
for _ in range(0, m):
    [x, y] = [(int)(num) for num in f.readline().split()]
    list_queens.append((x, y))
f.close()

(list_place_queens, tree_placed_board) = place_queens(initial_queens=list_queens)
print(len(list_place_queens))
print(list_place_queens)

placed_board = draw_board(list_queens=list_place_queens)

# draw initial board

# print(decode_board(placed_board))

init_state =  decode_board(draw_board(list_queens=list_queens))

TAB = "          "

def print_state(state, tree, tab, file=None, depth=0):
    file.write(tab + "depth: " + str(depth) + ')\n')

    for row in state.split('\n'):
        file.write(tab + row + '\n')
    
    if not state in tree:
        return
    
    for next_state in tree[state]:
        print_state(
            state=next_state,
            tree=tree,
            tab=tab + TAB,
            file=file,
            depth=depth + 1
        )

    file.write('\n')

f = open(rootDir + '/output.txt', 'w')
print_state(
    state=init_state, 
    tree=tree_placed_board, 
    tab="",
    file=f
)
f.close()

