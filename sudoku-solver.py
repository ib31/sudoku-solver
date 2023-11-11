
grid = []
for i in range(9):
    grid+= [int(x) for x in input()]

# print(grid, file=sys.stderr, flush=True)
# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

def get_square(cell):
    line = cell // 9
    column = cell%9
    return line // 3 * 3 + column // 3 % 3

def get_line_array(grid, cell):
    line = cell // 9
    l = grid[line * 9 : cell] + grid[cell + 1 : (line + 1) * 9 :]
    return l

def get_column_array(grid, cell):
    column = cell%9
    c = grid[column:cell:9]+grid[cell+9::9]
    return c

def get_square_array(grid, cell):
    m = cell//9//3*3*9+cell%9//3*3
    # detect the po of the cell in the square
    square=[]
    if cell in range(m,m+3):
        square +=grid[m:cell]+grid[cell+1:m+3] + grid[m + 9 : m +12] + grid[m + 18 : m + 21]
    elif cell in range(m+9,m+12):
        square +=grid[m : m + 3] + grid[m+9:cell]+grid[cell+1:m+12] + grid[m + 18 : m + 21]
    else:
        square +=grid[m : m + 3]+ grid[m + 9 : m +12] + grid[m+18:cell]+grid[cell+1:m+21]
    return square

def check_cell(grid,cell):
    adjacent = get_line_array(grid, cell)+ get_column_array(grid, cell)+ get_square_array(grid, cell)
    return (grid[cell]==0) or (grid[cell] not in adjacent)

def check(grid):
    for cell in range(len(grid)):
        if not check_cell(grid,cell):
            return False
    return True

def get_neighborhood(cell):
    neighborhood = []
    neighborhood += [k for k in range(cell//9*9,cell)]+[k for k in range(cell+1,(cell//9+1)*9)]
    neighborhood += [k for k in range(cell%9,cell,9)]+[k for k in range(cell+1,9*9,9)]
    m = cell//9//3*3*9+cell%9//3*3
    if cell in range(m,m+3):
        neighborhood += [k for k in range(m,cell)]+[k for k in range(cell+1,m+3)]+[m+9,m+10,m+11]+[m+18,m+19,m+20]
    elif cell in range(m+9,m+12):
        neighborhood += [m+1,m+2,m+3]+[k for k in range(m+9,cell)]+[k for k in range(cell+1,m+11)]+[m+18,m+19,m+20]
    else:
        neighborhood += [m+1,m+2,m+3]+[m+9,m+10,m+11]+[k for k in range(m+18,cell)]+[k for k in range(cell+1,m+20)]
    return neighborhood

def curr_dom(grid, cell):
    if grid[cell] != 0:
        return [grid[cell]]
    d = []

    adjacent = get_line_array(grid, cell)+ get_column_array(grid, cell)+ get_square_array(grid, cell)
    for k in range(1, 10):
        if k not in adjacent:
            d.append(k)
    return d


def get_all_curr_doms(grid):
    current_doms = []
    for k in range(len(grid)):
        current_doms.append(curr_dom(grid, k))
    return current_doms


def fix_point1(grid, current_doms):
    s = 1
    while s > 0:
        for i, d in enumerate(current_doms):
            if len(d) == 1 and grid[i] == 0:
                grid[i] = d[0]
                s += 1
        current_doms = get_all_curr_doms(grid)
        s -= 1
    return grid, current_doms


def fix_point2(grid: list,current_doms):
    stack_cell = set()
    for i,d in enumerate(current_doms):
        if len(d)==1 and grid[i]==0:
            stack_cell.add(i)
    while len(stack_cell)>0:
        cell = stack_cell.pop()
        d = current_doms[cell]
        if len(d) >0:
            grid[cell] = d[0]
        else:
            return grid, current_doms
        adjacent_cells = get_neighborhood(cell)
        for i in adjacent_cells:
            d = curr_dom(grid,i)
            if len(d)==1 and grid[i]==0:
                stack_cell.add(i)
            current_doms[i] = d
    return grid, current_doms

def sort_tightest_domains(current_doms):
    return sorted(enumerate(current_doms), key=lambda x: len(x[1]),reverse=False)


def dfs(grid: list, current_doms: list):
    grid, current_doms = grid.copy(), current_doms.copy()
    # grid, current_doms = fix_point1(grid, current_doms)
    grid, current_doms = fix_point2(grid, current_doms)
    
    if [] in current_doms or not check(grid):
        return grid, False
    sorted = sort_tightest_domains(current_doms)
    branch_cell = -1
    for i, d in sorted:
        if grid[i] == 0:
            branch_cell = i
            break
    if branch_cell == -1:
        assert (branch_cell == -1) == (0 not in grid)
        return grid, True
    branch_dom = current_doms[branch_cell]
    for v in branch_dom:
        grid[branch_cell] = v
        new_curr_dom = get_all_curr_doms(grid)
        new_grid, is_solution = dfs(grid, new_curr_dom)
        if is_solution:
            return new_grid, is_solution
        else:
            pass

    return grid, False


current_doms = get_all_curr_doms(grid)
start = time.time()
grid,current_doms = dfs(grid,current_doms)
end = time.time()

print(end-start, file=sys.stderr, flush=True)

for k in range(9):
    line=""
    for i in range(9):
        line += str(grid[9*k+i])
    print(line)
