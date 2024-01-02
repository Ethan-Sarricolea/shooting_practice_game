"""
Description: Game initializer
Author: Sarricolea Cortés Ethan Yahel
"""
from modules import visualgame,logicgame

try:
    if __name__==("__main__"):
        running = True
        moduleLogicgame = logicgame()
        moduleVisualgame = visualgame(running,moduleLogicgame)
            
except Exception as e:
    # Captura el tipo de error
    print(f"Se ha producido un error: {type(e).__name__}")
    
finally:
    print("Fin de la ejecución")