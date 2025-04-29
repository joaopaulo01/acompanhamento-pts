# Dicionário de requisitantes
requisitantes = {
    "andaime": ["44583340", "47885986"],
    "eletrica": ["TQ25", "DTMZ", "DTO5", "E0FV"],
    "mecanica": ["TQ24", "E0E3", "F2IF", "CK13"],
    "instrumentacao": ["X7L1", "RSMU", "FIUU", "FIV0"],
    "civil": ["CV11", "ST22", "UV33", "WX44"]
}

# Exemplo de uso
for area, codigos in requisitantes.items():
    print(f"{area.capitalize()}: {', '.join(codigos)}")