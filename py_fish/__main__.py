from py_fish.models.engine import Engine, EngineApplication

engine = Engine(EngineApplication.PROPULSION, 170.0)

print(engine.calculate_consumption(60))
