# Sergi Gallart Fanlo

def main():

  # Possibles moviments que pot fer l'usuari
  MOVEMENTS = [
      [1,0],      # Baixar
      [-1, 0],    # Pujar
      [0, 1],     # Dreta
      [0, -1]     # Esquerre
  ]

  # Matriu quadrada que determina com serà el camí
  MATRIX_1 = [
      ["x",     "x", "x", "x", "x", "GOAL"],
      ["R",     "R", "R", "x", "x", "R"],
      ["R",     "x", "R", "x", "x", "R"],
      ["R",     "x", "R", "R", "x", "R"],
      ["R",     "x", "x", "R", "x", "R"],
      ["START", "x", "x", "R", "R", "R"]
  ]

  matrix_size = len(MATRIX_1)

  # Trobem la posició inicial "START" sense utilitzar break
  pos = [-1, -1]
  i = 0
  while i < matrix_size:
    j = 0
    while j < matrix_size:
      if MATRIX_1[i][j] == "START":
        pos[0] = i
        pos[1] = j
        j = matrix_size
        i = matrix_size
      j += 1
    i += 1

  # Funció auxiliar per formatar la coordenada numèrica (fila, columna)
  def format_coordenada(r, c):
    return f"({r + 1}, {c + 1})"

  ruta = [format_coordenada(pos[0], pos[1])]
  moviment_anterior = [0, 0]

  # Bucle de cerca del camí fins a trobar "GOAL" sense break
  estat_actual = MATRIX_1[pos[0]][pos[1]]
  while estat_actual != "GOAL":
    idx = 0
    while idx < len(MOVEMENTS):
      mov = MOVEMENTS[idx]
      
      # Es passa MATRIX_1 com a argument, sense necessitat de declarar 'global'
      if pot_moure(pos[0], pos[1], matrix_size, mov, moviment_anterior, MATRIX_1):
        pos[0] += mov[0]
        pos[1] += mov[1]
        
        # Concatenació de llistes (sense .append())
        ruta = ruta + [format_coordenada(pos[0], pos[1])]
        
        moviment_anterior = mov
        estat_actual = MATRIX_1[pos[0]][pos[1]]
        idx = len(MOVEMENTS)
      
      idx += 1

  # Construcció manual de la cadena del camí (sense .join())
  cami_formatted = ""
  k = 0
  while k < len(ruta):
    cami_formatted += ruta[k]
    if k < len(ruta) - 1:
      cami_formatted += " > "
    k += 1

  # Mostrar el resultat final
  print("El camí per poder arribar a l'objectiu es:")
  print(cami_formatted)


def pot_moure(posicio_x: int, posicio_y: int, matrix_size: int, moviment: list[int], moviment_anterior: list[int], matrix_ref: list = None) -> bool:
  # 1. Comprovar si el moviment és l'invers exacte de l'anterior (per no retrocedir)
  if moviment[0] == -moviment_anterior[0] and moviment[1] == -moviment_anterior[1]:
    return False

  nx = posicio_x + moviment[0]
  ny = posicio_y + moviment[1]

  # 2. Comprovar límits de la matriu quadrada
  if not (0 <= nx < matrix_size and 0 <= ny < matrix_size):
    return False

  # 3. Comprovar si la cel·la destí està blocada ("x")
  matriu_actual = matrix_ref if matrix_ref is not None else []
  
  if matriu_actual[nx][ny] == "x":
    return False

  return True
main()