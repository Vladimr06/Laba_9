import random
import time

MAX_VERTICES = 100

# ==================== Ввод числа с проверкой ====================
def safe_int_input(prompt, min_value=None, max_value=None):
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Ошибка: нужно ввести целое число!\n")
            continue
        value = int(value)
        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}!\n")
            continue
        if max_value is not None and value > max_value:
            print(f"Ошибка: число должно быть не больше {max_value}!\n")
            continue
        return value

def safe_float_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = float(input(prompt).replace(',', '.').strip())
        except ValueError:
            print("Ошибка: нужно ввести число!\n")
            continue
        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}!\n")
            continue
        if max_value is not None and value > max_value:
            print(f"Ошибка: число должно быть не больше {max_value}!\n")
            continue
        return value

# ==================== Генерация графа ====================
def generate_graph_matrix(vertices, density=0.3):
    matrix = [[0]*vertices for _ in range(vertices)]
    for i in range(vertices):
        for j in range(i+1, vertices):
            if random.random() < density:
                matrix[i][j] = matrix[j][i] = 1
    return matrix

def input_graph_matrix():
    vertices = safe_int_input("Введите количество вершин графа: ", 1, MAX_VERTICES)
    print(f"Введите матрицу смежности ({vertices}x{vertices}): (0 - нет ребра, 1 - есть ребро)")
    matrix = []
    for i in range(vertices):
        row = []
        for j in range(vertices):
            value = safe_int_input(f"matrix[{i}][{j}] = ", 0, 1)
            row.append(value)
        matrix.append(row)
    # Проверка симметрии
    symmetric = all(matrix[i][j]==matrix[j][i] for i in range(vertices) for j in range(vertices))
    if not symmetric:
        print("Предупреждение: матрица не симметрична! Граф будет считаться ориентированным.")
    return matrix

# ==================== Очередь ====================
class Queue:
    def __init__(self):
        self.data=[]
    def enqueue(self,x):
        self.data.append(x)
    def dequeue(self):
        return self.data.pop(0) if self.data else None
    def empty(self):
        return len(self.data)==0

# ==================== BFS ====================
def bfs_matrix(matrix, start):
    visited=[False]*len(matrix)
    q=Queue()
    visited[start]=True
    q.enqueue(start)
    order=[]
    while not q.empty():
        v=q.dequeue()
        order.append(v)
        for i, val in enumerate(matrix[v]):
            if val==1 and not visited[i]:
                visited[i]=True
                q.enqueue(i)
    return order

# ==================== DFS ====================
def dfs_matrix(matrix):
    vertices=len(matrix)
    distances=[[-1]*vertices for _ in range(vertices)]
    def dfs(start, cur, dist, visited):
        visited[cur]=True
        if distances[start][cur]==-1 or dist<distances[start][cur]:
            distances[start][cur]=dist
        for i, val in enumerate(matrix[cur]):
            if val==1 and not visited[i]:
                dfs(start, i, dist+1, visited)
        visited[cur]=False
    for start in range(vertices):
        dfs(start,start,0,[False]*vertices)
    return distances

# ==================== Преобразование в списки смежности ====================
def matrix_to_list(matrix):
    n=len(matrix)
    lists=[[] for _ in range(n)]
    for i in range(n):
        for j,val in enumerate(matrix[i]):
            if val==1:
                lists[i].append(j)
    return lists

def bfs_list(lists,start):
    visited=[False]*len(lists)
    q=Queue()
    visited[start]=True
    q.enqueue(start)
    order=[]
    while not q.empty():
        v=q.dequeue()
        order.append(v)
        for neigh in lists[v]:
            if not visited[neigh]:
                visited[neigh]=True
                q.enqueue(neigh)
    return order

def dfs_list(lists):
    vertices=len(lists)
    distances=[[-1]*vertices for _ in range(vertices)]
    def dfs(start,cur,dist,visited):
        visited[cur]=True
        if distances[start][cur]==-1 or dist<distances[start][cur]:
            distances[start][cur]=dist
        for neigh in lists[cur]:
            if not visited[neigh]:
                dfs(start,neigh,dist+1,visited)
        visited[cur]=False
    for start in range(vertices):
        dfs(start,start,0,[False]*vertices)
    return distances

# ==================== Печать ====================
def print_matrix(matrix):
    n=len(matrix)
    print("  ", end="")
    for i in range(n):
        print(f"{i:2d}", end=" ")
    print()
    for i,row in enumerate(matrix):
        print(f"{i:2d}", end=" ")
        for val in row:
            print(f"{val:2d}",end=" ")
        print()

def print_distance_matrix(distances,name):
    print(f"\nМатрица расстояний ({name}):")
    n=len(distances)
    print("Из\\В ", end="")
    for j in range(n):
        print(f"{j:3d}", end=" ")
    print()
    for i,row in enumerate(distances):
        print(f"{i:3d} |", end="")
        for val in row:
            print(f"{'-' if val==-1 else val:3}", end=" ")
        print()

# ==================== MAIN ====================
def main():
    random.seed(time.time())
    print("=== СОЗДАНИЕ ГРАФА ===")
    choice = safe_int_input("1. Ввести вручную\n2. Сгенерировать случайно\nВыберите способ (1 или 2): ",1,2)
    if choice==1:
        matrix=input_graph_matrix()
    else:
        vertices=safe_int_input("Введите количество вершин: ",1,MAX_VERTICES)
        density=safe_float_input("Введите плотность графа (0.0-1.0): ",0.0,1.0)
        matrix=generate_graph_matrix(vertices,density)
    print("\nМатрица смежности:")
    print_matrix(matrix)
    start_vertex=safe_int_input(f"Введите начальную вершину (0-{len(matrix)-1}): ",0,len(matrix)-1)

    # BFS и DFS
    order_bfs_matrix=bfs_matrix(matrix,start_vertex)
    print(f"\nBFS (матрица) начиная с вершины {start_vertex}: {order_bfs_matrix}")

    order_bfs_list=bfs_list(matrix_to_list(matrix),start_vertex)
    print(f"BFS (списки) начиная с вершины {start_vertex}: {order_bfs_list}")

    distances_dfs_matrix=dfs_matrix(matrix)
    print_distance_matrix(distances_dfs_matrix,"DFS (матрица)")

    distances_dfs_list=dfs_list(matrix_to_list(matrix))
    print_distance_matrix(distances_dfs_list,"DFS (списки)")

if __name__=="__main__":
    main()

