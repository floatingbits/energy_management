import pandas as pd
import lightgbm as lgb
class UncertaintyEstimatorPredictorWrapper:
    def __init__(self, needed_variables:list[str], model):
        self.needed_variables = needed_variables
        self.model = model

    def predict(self, input_values: dict[str,list[float]]):
        X = pd.DataFrame(input_values)
        if isinstance(self.model, lgb.basic.Booster):
            fitted_features = self.model.feature_name()
            X = X[fitted_features]

        return self.model.predict(X)

