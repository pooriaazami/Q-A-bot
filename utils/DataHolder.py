class DataHolder:
    __instance = None

    def __init__(self):
        if DataHolder.__instance is None:
            pass

    @staticmethod
    def get_instance():
        if DataHolder.__instance is None:
            DataHolder.__instance = DataHolder()

        return DataHolder.__instance
