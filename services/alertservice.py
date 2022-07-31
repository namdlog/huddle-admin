class CheckMaterialSingleton:
    instance = None

    def __init__(self):
        instance = self 
        
    def get_instance():
        if( instance is None):
            instance = CheckMaterialSingleton()
            return instance
        else:
            return instance