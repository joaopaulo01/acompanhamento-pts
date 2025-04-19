# install.py
import subprocess
import sys
import os
import platform

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    if sys.version_info < (3, 8):
        print("Este script requer Python 3.8 ou superior.")
        sys.exit(1)

def install_requirements():
    """Instala as dependências necessárias."""
    requirements = [
        "selenium",
        "pandas",
        "flask",
        "webdriver-manager",
        "openpyxl",  # Para suporte a arquivos Excel
        "numpy"
    ]
    
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    for package in requirements:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Dependências instaladas com sucesso!")

def check_chrome():
    """Verifica se o Chrome está instalado."""
    system = platform.system()
    
    if system == "Windows":
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_path_alt = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path) or os.path.exists(chrome_path_alt):
            print("Chrome encontrado!")
            return True
    elif system == "Linux":
        try:
            subprocess.check_call(["which", "google-chrome"], stdout=subprocess.DEVNULL)
            print("Chrome encontrado!")
            return True
        except:
            pass
    elif system == "Darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            print("Chrome encontrado!")
            return True
    
    print("AVISO: Google Chrome não encontrado. Por favor, instale o Chrome para usar este aplicativo.")
    return False

def create_directories():
    """Cria os diretórios necessários."""
    directories = ["uploads", "screenshots", "templates", "static"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("Diretórios criados com sucesso!")

def main():
    """Função principal de instalação."""
    print("Iniciando instalação do Sistema de Acompanhamento de PTs...")
    
    check_python_version()
    install_requirements()
    check_chrome()
    create_directories()
    
    print("\nInstalação concluída com sucesso!")
    print("\nPara iniciar o aplicativo, execute:")
    print("    python app.py")

if __name__ == "__main__":
    main()
