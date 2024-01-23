
from models.pedagogical.prototype import Prototype_pedagogical_model
from users.schemas import User

class Model_manager():
    """Since the ITS should be a research platform that incorporates different methods for feedback and task selection, the model manager
    aims to simplify the use of varying implementations of the pedagogical, domain and learner model. 
    """
    
    def __init__(self):
        """In the constructor all variants of models should be registered (and instantiated) for later selection.
        """
        self.prototype = Prototype_pedagogical_model()

    def pedagogical_model(self, user: User):
        return self.prototype
    
    #TODO: Maybe that is not necesessary
    def domain_model(self):
        raise Exception("Not implemented!")
    
    def learner_model(self):
        raise Exception("Not implemented!")
