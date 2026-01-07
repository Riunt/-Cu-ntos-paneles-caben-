from typing import List, Tuple, Dict
import json
from functools import lru_cache


def calculate_panels(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int) -> int:
    
    # EXPLICACIÓN DEL FLUJO DE DATOS:
    # 1. Esta función es llamada por 'run_tests' (abajo).
    #    Recibe las dimensiones iniciales completas del techo (roof_width, roof_height).
    #    Por ejemplo, en el Test 2, recibe: panel=1x2, roof=3x5.

    # Usamos @lru_cache para "recordar" resultados.
    @lru_cache(None)
    def solve(w: int, h: int) -> int:
        # ¿QUÉ SON w y h?
        # w (width): Es el ancho del pedazo de techo que nos queda por llenar.
        # h (height): Es el alto del pedazo de techo que nos queda por llenar.
        # Inicialmente son iguales al techo completo (3x5), pero a medida que
        # "cortamos" pedazos recursivamente, estos valores se van achicando.
        # Ejemplo: Si cortamos una franja de ancho 1, la siguiente llamada será solve(2, 5).

        # 1. Caso Base: Si el techo restante es más chico que el lado más corto del panel,
        # es imposible que quepa algo. Retornamos 0.
        if w * h < panel_width * panel_height: 
            return 0
            
        # 2. Estrategia Base: 
        # Calculamos cuántos caben si simplemente los alineamos como una cuadrícula.
        # Probamos alineación normal
        max_panels = (w // panel_width) * (h // panel_height)
        # Probamos alineación rotada (horizontal)
        max_panels = max(max_panels, (w // panel_height) * (h // panel_width))
        
        # 3. Estrategia Recursiva:
        # Intentamos "cortar" una franja del techo, llenarla, y resolver el resto recursivamente.
        # Probamos las 4 formas posibles de hacer el primer corte:
        
        # Opción A: Corte Vertical con panel Normal
        # Cortamos una franja de ancho 'panel_width'. En esa franja caben (h // panel_height) paneles.
        # Sumamos eso + lo que quepa en el resto del ancho (w - panel_width).
        if w >= panel_width:
            max_panels = max(max_panels, 
                           (h // panel_height) + solve(w - panel_width, h))
            
        # Opción B: Corte Vertical con panel Rotado
        # Cortamos una franja de ancho 'panel_height' (el panel acostado).
        if w >= panel_height:
            max_panels = max(max_panels, 
                           (h // panel_width) + solve(w - panel_height, h))
            
        # Opción C: Corte Horizontal con panel Normal
        # Cortamos una franja de alto 'panel_height'.
        if h >= panel_height:
            max_panels = max(max_panels, 
                           (w // panel_width) + solve(w, h - panel_height))

        # Opción D: Corte Horizontal con panel Rotado
        # Cortamos una franja de alto 'panel_width'.
        if h >= panel_width:
            max_panels = max(max_panels, 
                           (w // panel_height) + solve(w, h - panel_width))
                          
        return max_panels

    # INICIO DE LA RECURSIÓN:
    # Llamamos a la función interna 'solve' pasándole el techo completo.
    # El resultado final (el entero máximo) se retorna hacia 'run_tests'.
    return solve(roof_width, roof_height)


def run_tests() -> None:
    with open('test_cases.json', 'r') as f:
        data = json.load(f)
        test_cases: List[Dict[str, int]] = [
            {
                "panel_w": test["panelW"],
                "panel_h": test["panelH"],
                "roof_w": test["roofW"],
                "roof_h": test["roofH"],
                "expected": test["expected"]
            }
            for test in data["testCases"]
        ]
    
    print("Corriendo tests:")
    print("-------------------")
    
    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"], 
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]
        
        print(f"Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
              f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")
    
    run_tests()


if __name__ == "__main__":
    main()
