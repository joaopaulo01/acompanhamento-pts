# configurar_credenciais.py
import os
import json
import getpass
import sys

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, is_password=False):
    """Solicita entrada do usuário, opcionalmente ocultando a entrada."""
    if is_password:
        return getpass.getpass(prompt)
    else:
        return input(prompt)

def save_credentials(credentials):
    """Salva as credenciais em um arquivo JSON."""
    try:
        with open('credentials.json', 'w') as f:
            json.dump(credentials, f)
        print("Credenciais salvas com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar credenciais: {str(e)}")

def load_credentials():
    """Carrega as credenciais de um arquivo JSON."""
    try:
        if os.path.exists('credentials.json'):
            with open('credentials.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar credenciais: {str(e)}")
    return {}

def main():
    """Função principal para configurar credenciais."""
    clear_screen()
    print("=== Configuração de Credenciais ===")
    print("\nEste script permite salvar suas credenciais para uso futuro.")
    print("AVISO: As credenciais serão salvas em texto simples no arquivo credentials.json.")
    print("       Isso é conveniente, mas menos seguro.")
    
    # Carrega credenciais existentes, se houver
    credentials = load_credentials()
    
    # Pergunta se deseja continuar
    choice = input("\nDeseja continuar? (s/n): ").lower()
    if choice != 's':
        print("Configuração cancelada.")
        return
    
    clear_screen()
    print("=== Configuração de Credenciais ===")
    
    # Solicita as credenciais
    credentials['usuario'] = get_input("\nUsuário: ")
    credentials['senha'] = get_input("Senha: ", is_password=True)
    
    # Solicita as configurações padrão
    print("\n=== Configurações Padrão ===")
    print("Estas configurações serão usadas como padrão ao iniciar o aplicativo.")
    
    credentials['empresa'] = get_input("\nEmpresa (padrão: PETROBRAS): ") or "PETROBRAS"
    
    area_options = ["GAS NATURAL&ENERGIA", "REFINO"]
    print("\nOpções de Área:")
    for i, option in enumerate(area_options, 1):
        print(f"{i}. {option}")
    
    area_choice = get_input("\nEscolha a área (1-2): ")
    try:
        area_index = int(area_choice) - 1
        if 0 <= area_index < len(area_options):
            credentials['area'] = area_options[area_index]
        else:
            credentials['area'] = "GAS NATURAL&ENERGIA"
    except ValueError:
        credentials['area'] = "GAS NATURAL&ENERGIA"
    
    # Solicita a unidade com base na área selecionada
    if credentials['area'] == "GAS NATURAL&ENERGIA":
        unidade_options = [
            "UTE-BF", "UTE-CAN", "UTE-CBT", "UTE-IBT", "UTE-JF", "UTE-NPI", "UTE-SRP",
            "UTE-TBA-TCA", "UTE-TCE", "UTE-TLG", "UTE-TMA", "UTE-TRI", "UTE-VLA",
            "UTGC e UTGSUL", "UTGCA", "UTGCAB", "UTGITB"
        ]
    else:  # REFINO
        unidade_options = [
            "FAFEN-BA", "FAFEN-SE", "LUBNOR", "PROTEGE+", "RECAP", "REDUC", "REFAP",
            "REGAP", "REMAN", "REPAR", "REPLAN", "REVAP", "RLAM", "RNEST", "RPBC", "SIX"
        ]
    
    print(f"\nOpções de Unidade para {credentials['area']}:")
    for i, option in enumerate(unidade_options, 1):
        print(f"{i}. {option}")
    
    unidade_choice = get_input(f"\nEscolha a unidade (1-{len(unidade_options)}): ")
    try:
        unidade_index = int(unidade_choice) - 1
        if 0 <= unidade_index < len(unidade_options):
            credentials['unidade'] = unidade_options[unidade_index]
        else:
            credentials['unidade'] = unidade_options[0]
    except ValueError:
        credentials['unidade'] = unidade_options[0]
    
    # Salva as credenciais
    save_credentials(credentials)
    
    print("\nConfiguração concluída!")
    print("As credenciais serão carregadas automaticamente ao iniciar o aplicativo.")
    print("\nPara iniciar o aplicativo, execute:")
    print("    python app.py")

if __name__ == "__main__":
    main()
