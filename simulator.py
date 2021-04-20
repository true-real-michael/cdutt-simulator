import wexpect


# ---------------------- CONSTANTS ---------------------- #
"""
MOVE_LIMIT    - преел ходов, по правилам игры - 150
TEAM_X_FILE   - путь к файлу команды X
HOUSE PATTERN - расстановка домов 
TEAM_X_MANUAL - если True, ввод и вывод для этой команды будет перенаправлен в консоль 
"""

MOVE_LIMIT = 150
TEAM_0_FILE = 'team0.exe'
TEAM_1_FILE = 'team1.exe'
HOUSE_PATTERN = 'F4 G2 G8 H3 H6 I1 I9 J5 K3 K7 L1 L6 L9'
TEAM_O_MANUAL = False
TEAM_1_MANUAL = False

# ------------------------- MAP ------------------------- #

"""
A  - акробат
C  - клоун
S  - силач
M  - фокусник
T  - дрессировщик

0  - команда 0
1  - команда 1

H_ - пустой дом
H0 - дом команды 0
H1 - дом команды 1

__ - пустое поле
"""

g = [
    ['A1', 'C1', 'S1', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 9 0
    ['C1', 'M1', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 8 1
    ['S1', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 7 2
    ['T1', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 6 3
    ['__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 5 4
    ['T0', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 4 5
    ['S0', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 3 6
    ['C0', 'M0', '__', '__', '__', '__', '__', '__', '__', '__', '__', '__'],  # 2 7
    ['A0', 'C0', 'S0', '__', '__', '__', '__', '__', '__', '__', '__', '__']  # _1 8
]  # _ A     B     C     D     E     F     G     H     I     J     K     L


#      0     1     2     3     4     5     6     7     8     9    10    11


def get_coord(notation: str) -> [int, int]:
    c1 = notation[0]
    c2 = notation[1]
    row = 9 - int(c2)
    col = 'ABCDEFGHIJKL'.index(c1)
    return [row, col]


def get_notation(crd: [int, int]) -> str:
    row = crd[0]
    col = crd[1]
    c1 = 'ABCDEFGHIJKL'[col]
    c2 = str(9 - row)
    return c1 + c2


def print_map():
    t0_houses = t1_houses = 0
    for l in g:
        t0_houses += l.count('H0')
        t1_houses += l.count('H1')
    print('9  ' + ' '.join(g[0]))
    print('8  ' + ' '.join(g[1]))
    print('7  ' + ' '.join(g[2]))
    print('6  ' + ' '.join(g[3]))
    print('5  ' + ' '.join(g[4]))
    print('4  ' + ' '.join(g[5]))
    print('3  ' + ' '.join(g[6]))
    print('2  ' + ' '.join(g[7]))
    print('1  ' + ' '.join(g[8]))
    print('\n    A  B  C  D  E  F  G  H  I  J  K  L')
    print(f'Team0: {t0_houses} houses\nTeam1: {t1_houses} houses\n')


# ------------------ MOVE FUNCTION ------------------#


def check_and_execute(move: str, team: int) -> bool:
    global g

    def commit_if_free(befor_crd, after_crd):
        if g[after_crd[0]][after_crd[1]] == 'H_':
            g[after_crd[0]][after_crd[1]] = f'H{g[befor_crd[0]][befor_crd[1]][1]}'
            g[befor_crd[0]][befor_crd[1]] = f'__'
            return True
        elif g[after_crd[0]][after_crd[1]] == '__':
            g[after_crd[0]][after_crd[1]] = g[befor_crd[0]][befor_crd[1]]
            g[befor_crd[0]][befor_crd[1]] = f'__'
            return True
        else:
            print(f'ERROR: Team{team} invalid move {move}\n       Cell {after} is not empty')
            return False

    def dangerous(crd: [int, int], team: int) -> bool:
        return crd[0] > 0 and g[crd[0] - 1][crd[1]] == f'T{1 - team}' \
               or crd[1] > 0 and g[crd[0]][crd[1] - 1] == f'T{1 - team}' \
               or crd[0] < 8 and g[crd[0] + 1][crd[1]] == f'T{1 - team}' \
               or crd[1] < 11 and g[crd[0]][crd[1] + 1] == f'T{1 - team}' \
               or crd[0] > 0 and crd[1] > 0 and g[crd[0] - 1][crd[1] - 1] == f'T{1 - team}' \
               or crd[0] > 0 and crd[1] < 11 and g[crd[0] - 1][crd[1] + 1] == f'T{1 - team}' \
               or crd[0] < 8 and crd[1] > 0 and g[crd[0] + 1][crd[1] - 1] == f'T{1 - team}' \
               or crd[0] < 8 and crd[1] < 11 and g[crd[0] + 1][crd[1] + 1] == f'T{1 - team}'

    if move == 'Z0-Z0': return True

    befor, after = move[:2], move[3:]
    befor_crd, after_crd = get_coord(befor), get_coord(after)
    if not (0 <= befor_crd[0] <= 8 and 0 <= befor_crd[1] <= 11
            and 0 <= after_crd[0] <= 8 and 0 <= after_crd[1] <= 11):
        return False
    if dangerous(befor_crd, team):
        print(f'ERROR: Team{team} invalid move {move}\n       Cannot move while in danger')
        return False
    if dangerous(after_crd, team):
        print(f'ERROR: Team{team} invalid move {move}\n       Cannot move to dangerous cell')
        return False

    delta_row = abs(after_crd[0] - befor_crd[0])
    delta_col = abs(after_crd[1] - befor_crd[1])
    if delta_row == 0 and delta_col == 0:
        print(f'ERROR: Team{team} invalid move {move}\n       If Team does not move, the move should be Z0-Z0')
        return False

    figure = g[befor_crd[0]][befor_crd[1]]
    if figure[0] not in 'ASTCM' or int(figure[1]) != team:
        print(f'ERROR: Team{team} invalid move {move}\n       Team does not own the figure {figure}')
        return False

    #

    if figure[0] == 'A':
        if not (delta_row, delta_col) in ((0, 1), (1, 0), (0, 2), (2, 0), (1, 1), (2, 2)):
            print(f'ERROR: Team{team} invalid move {move}\n       Invalid move for {figure}')
            return False
        return commit_if_free(befor_crd, after_crd)

    elif figure[0] in ('C', 'T'):
        if not (delta_row <= 1 and delta_col <= 1):
            print(f'ERROR: Team{team} invalid move {move}\n       Invalid move for {figure}')
            return False

        return commit_if_free(befor_crd, after_crd)

    elif figure[0] == 'S':
        if not (delta_row <= 1 and delta_col <= 1):
            print(f'ERROR: Team{team} invalid move {move}\n       Invalid move for {figure}')
            return False

        if g[after_crd[0]][after_crd[1]] in ('__', 'H_'):
            return commit_if_free(befor_crd, after_crd)
        after2_crd = [after_crd[0] * 2 - befor_crd[0], after_crd[1] * 2 - befor_crd[1]]
        if g[after_crd[0]][after_crd[1]] in (f'A{team}', f'C{team}', f'S{team}', f'M{team}', f'T{team}'):
            if dangerous(after2_crd, team):
                print(f'ERROR: Team{team} invalid move {move}\n       Cannot move allies to danger')
                return False
            return commit_if_free(after_crd, after2_crd) and commit_if_free(befor_crd, after_crd)

        if g[after_crd[0]][after_crd[1]] in (
                f'A{1 - team}', f'C{1 - team}', f'S{1 - team}', f'M{1 - team}', f'T{1 - team}'):
            return commit_if_free(after_crd, after2_crd) and commit_if_free(befor_crd, after_crd)

    elif figure[0] == 'M':
        if g[after_crd[0]][after_crd[1]] in (
                f'A{team}', f'C{team}', f'S{team}', f'M{team}', f'T{team}', f'A{1 - team}', f'C{1 - team}',
                f'S{1 - team}'):
            g[after_crd[0]][after_crd[1]], g[befor_crd[0]][befor_crd[1]] = g[befor_crd[0]][befor_crd[1]], \
                                                                           g[after_crd[0]][after_crd[1]]
            return True
        if not (delta_row <= 1 and delta_col <= 1) or g[after_crd[0]][after_crd[1]] in (f'M{1 - team}', f'T{1 - team}'):
            print(f'ERROR: Team{team} invalid move {move}\n       Cannot swap with enemy Trainers and Magicians')
            return False
        return commit_if_free(befor_crd, after_crd)


# ----------------- HOUSE GENERATION ----------------- #
houses_notatoins = HOUSE_PATTERN.split()
houses_coords = [get_coord(nt) for nt in houses_notatoins]

for h_crd in houses_coords:
    g[h_crd[0]][h_crd[1]] = 'H_'

# TODO: IMPLEMENT HOUSE GENERATION


# ---------------- TEAMs & COMMs INITIALIZATION ---------------- #

if not TEAM_O_MANUAL:
    t0 = wexpect.spawn(TEAM_0_FILE)
if not TEAM_1_MANUAL:
    t1 = wexpect.spawn(TEAM_1_FILE)
print_map()


def send_man(team: int, move: str) -> None:
    print(f'Team{1 - team} made a move: {move}')


def get_man(team: int) -> str:
    return input(f'Team{team}\'s turn\n')


def send_auto(team_pipe, move: str) -> None:
    team_pipe.sendline(move)
    team_pipe.expect('.*')


def get_auto(team_pipe) -> str:
    return team_pipe.after.split()[-1]


def communicate_auto(team_pipe, move: str) -> str:
    team_pipe.sendline(move)
    team_pipe.expect('.*')
    return team_pipe.after.split()[-1]


def communicate_manual(team: int, move: str) -> str:
    mov = input(f'output for Team{team}:\n{move}\nExpecting Team{team} move: ')
    return mov


# ----------------------- GAME ----------------------- #

for i in range(150):
    if TEAM_O_MANUAL:
        if i == 0:
            mov0 = communicate_manual(0, f'{HOUSE_PATTERN}\r\n0')
        else:
            mov0 = communicate_manual(0, mov1)
    else:
        if i == 0:
            mov0 = communicate_auto(t0, f'{HOUSE_PATTERN}\r\n0')
        else:
            mov0 = communicate_auto(t0, mov1)
        print(mov0)

    # print_map()
    res0 = check_and_execute(mov0, 0)
    if not res0:
        print('Team1 wins!')
        break
    print_map()

    if TEAM_1_MANUAL:
        if i == 0:
            mov1 = communicate_manual(1, f'{HOUSE_PATTERN}\r\n1\r\n{mov0}')
        else:
            mov1 = communicate_manual(1, mov0)
    else:
        if i == 0:
            mov1 = communicate_auto(t1, f'{HOUSE_PATTERN}\r\n1\r\n{mov0}')
        else:
            mov1 = communicate_auto(t1, mov0)
        print(mov1)

    # print_map()
    res1 = check_and_execute(mov1, 1)
    if not res1:
        print('Team0 wins!')
        break
    print_map()

# ---------------- FINISHING PROGRAM ---------------- #

if not TEAM_O_MANUAL:
    t0.close()
if not TEAM_1_MANUAL:
    t1.close()