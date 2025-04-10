from controller.app_controller import AppController
from model.api_client import FootballAPIClient
from model.data_model import SerieAModel
from view.main_view import MainView

if __name__ == "__main__":
        api_client = FootballAPIClient()
        model = SerieAModel(api_client)
        view = MainView()
        controller = AppController(model, view)
        view.controller = controller
        view.mainloop()

