from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    # Create or fetch CarMake records (no duplicates)
    car_make_instances = []
    for data in car_make_data:
        make_obj, _ = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]},
        )
        # If it already existed but description is blank/different, you can optionally update it:
        if make_obj.description != data["description"]:
            make_obj.description = data["description"]
            make_obj.save()
        car_make_instances.append(make_obj)

    dealer_id_default = 1

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_id_default},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_id_default},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "car_make": car_make_instances[0], "dealer_id": dealer_id_default},

        {"name": "A-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_id_default},
        {"name": "C-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_id_default},
        {"name": "E-Class", "type": "SUV", "year": 2023, "car_make": car_make_instances[1], "dealer_id": dealer_id_default},

        {"name": "A4", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_id_default},
        {"name": "A5", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_id_default},
        {"name": "A6", "type": "SUV", "year": 2023, "car_make": car_make_instances[2], "dealer_id": dealer_id_default},

        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_id_default},
        {"name": "Carnival", "type": "SUV", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_id_default},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "car_make": car_make_instances[3], "dealer_id": dealer_id_default},

        {"name": "Corolla", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_id_default},
        {"name": "Camry", "type": "Sedan", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_id_default},
        {"name": "Kluger", "type": "SUV", "year": 2023, "car_make": car_make_instances[4], "dealer_id": dealer_id_default},
    ]

    # Create or fetch CarModel records (no duplicates)
    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=data["car_make"],
            defaults={
                "dealer_id": data["dealer_id"],
                "type": data["type"],
                "year": data["year"],
            },
        )
