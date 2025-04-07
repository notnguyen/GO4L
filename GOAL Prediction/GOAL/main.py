from controller.app_controller import AppController
from model.api_client import FootballAPIClient
from model.data_model import SerieAModel
from view.main_view import MainView

if __name__ == "__main__":
    view = MainView()
    client = FootballAPIClient()
    model = SerieAModel(client)
    controller = AppController(model, view)
    view.mainloop()
