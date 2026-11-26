class Body:
    """A physical body that can receive or give heat."""

    def __init__(self, mass, heat_capacity, temperature):

        # check that the values make physical sense, otherwise use a safe default
        if mass <= 0:
            print("Mass must be greater than 0, using 1 kg")
            mass = 1
        if heat_capacity <= 0:
            print("Heat capacity must be greater than 0, using 1 J/kg°C")
            heat_capacity = 1
        if temperature < 0:
            print("Temperature must be 0 or higher, using 0 °C")
            temperature = 0

        self.mass = mass                    # [kg]
        self.heat_capacity = heat_capacity  # [J/kg°C]
        self.temperature = temperature      # [°C]

    def add_heat(self, heat):
        # heat in [J], can be negative (the body gives heat)
        delta_temperature = heat / (self.mass * self.heat_capacity)   # ΔT = Q / (m·c)
        self.temperature = self.temperature + delta_temperature       # new T = T + ΔT
        return self.temperature


if __name__ == "__main__":
    # runs only when this file is run directly, not when imported
    body = Body(100, 0.15, 200)
    print(body.add_heat(20))
    print(body.add_heat(-40))