import os

class ExportPlot:
    basePath: str

    def __init__(self, basePath) -> None:
        self.basePath = basePath

    def save(self, ax, file_name):
        file_path = os.path.join(self.basePath, file_name)

        ax.get_figure().savefig(file_path)