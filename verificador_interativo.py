#!/usr/bin/env python3
"""
Verificador de Integridade de Arquivos - Versão Executável Interativa
Script que solicita parâmetros do usuário antes da execução
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from script import FileIntegrityChecker

class InteractiveFileChecker:
    """Classe para interface interativa do verificador"""
    
    def __init__(self):
        self.directories = []
        self.output_name = None
        self.recursive = True
        self.file_types = []
        self.auto_install_excel = False
        
    def print_header(self):
        """Exibir cabeçalho do programa"""
        print("=" * 60)
        print("🔍 VERIFICADOR DE INTEGRIDADE DE ARQUIVOS")
        print("=" * 60)
        print("Este programa verifica a integridade de arquivos em diretórios")
        print("detectando arquivos corrompidos, inacessíveis ou com problemas.")
        print("=" * 60)
        print()
    
    def validate_directory(self, path):
        """Validar se o diretório existe e é acessível"""
        if not path.strip():
            return False, "Caminho não pode estar vazio"
        
        if not os.path.exists(path):
            return False, f"Diretório não encontrado: {path}"
        
        if not os.path.isdir(path):
            return False, f"Caminho não é um diretório: {path}"
        
        if not os.access(path, os.R_OK):
            return False, f"Sem permissão de leitura: {path}"
        
        return True, "Diretório válido"
    
    def get_directories(self):
        """Solicitar diretórios para verificação"""
        print("📁 CONFIGURAÇÃO DE DIRETÓRIOS")
        print("-" * 30)
        
        while True:
            if not self.directories:
                print("Digite o caminho do diretório a ser verificado:")
                print("(Obrigatório - digite pelo menos um diretório)")
            else:
                print(f"\nDiretórios já adicionados: {len(self.directories)}")
                for i, d in enumerate(self.directories, 1):
                    print(f"  {i}. {d}")
                print("\nDeseja adicionar outro diretório? (s/n) ou digite o caminho:")
            
            user_input = input(">>> ").strip()
            
            if not user_input:
                if self.directories:
                    break
                else:
                    print("❌ Erro: Pelo menos um diretório deve ser especificado!")
                    continue
            
            if user_input.lower() in ['n', 'nao', 'não', 'no']:
                if self.directories:
                    break
                else:
                    print("❌ Erro: Pelo menos um diretório deve ser especificado!")
                    continue
            
            if user_input.lower() in ['s', 'sim', 'yes', 'y']:
                continue
            
            # Tratar como caminho de diretório
            valid, message = self.validate_directory(user_input)
            if valid:
                abs_path = os.path.abspath(user_input)
                if abs_path not in self.directories:
                    self.directories.append(abs_path)
                    print(f"✅ Diretório adicionado: {abs_path}")
                else:
                    print(f"⚠️  Diretório já foi adicionado: {abs_path}")
            else:
                print(f"❌ {message}")
                print("Tente novamente ou pressione Enter para continuar.")
        
        print(f"\n✅ {len(self.directories)} diretório(s) configurado(s) para verificação.")
    
    def get_output_settings(self):
        """Configurar opções de saída"""
        print("\n📄 CONFIGURAÇÃO DE SAÍDA")
        print("-" * 25)
        
        # Nome do arquivo de saída
        while True:
            print("Digite o nome base para os arquivos de relatório:")
            print("(Opcional - pressione Enter para usar nome automático)")
            output_input = input(">>> ").strip()
            
            if not output_input:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.output_name = f"relatorio_integridade_{timestamp}"
                print(f"✅ Nome automático: {self.output_name}")
                break
            
            # Validar nome do arquivo
            if any(char in output_input for char in '<>:"/\\|?*'):
                print("❌ Nome contém caracteres inválidos. Tente novamente.")
                continue
            
            self.output_name = output_input
            print(f"✅ Nome definido: {self.output_name}")
            break
    
    def get_filter_options(self):
        """Configurar filtros opcionais"""
        print("\n🎯 FILTROS OPCIONAIS")
        print("-" * 20)
        
        # Busca recursiva
        while True:
            recursive_input = input("Verificar subdiretórios recursivamente? (S/n): ").strip().lower()
            if recursive_input in ['', 's', 'sim', 'yes', 'y']:
                self.recursive = True
                print("✅ Busca recursiva ativada")
                break
            elif recursive_input in ['n', 'nao', 'não', 'no']:
                self.recursive = False
                print("✅ Busca apenas no diretório principal")
                break
            else:
                print("❌ Digite 's' para sim ou 'n' para não")
        
        # Filtro por tipos de arquivo
        print("\nFiltrar por tipos de arquivo específicos?")
        print("Exemplos: csv, json, xlsx, pdf, txt, py, sql")
        print("(Opcional - pressione Enter para verificar todos os tipos)")
        
        types_input = input(">>> ").strip()
        if types_input:
            self.file_types = [t.strip().lower() for t in types_input.split(',')]
            self.file_types = [t if t.startswith('.') else f'.{t}' for t in self.file_types]
            print(f"✅ Filtros configurados: {', '.join(self.file_types)}")
        else:
            print("✅ Verificando todos os tipos de arquivo")
        
        # Configuração para arquivos Excel
        self.get_excel_options()
    
    def get_excel_options(self):
        """Configurar opções avançadas para arquivos Excel"""
        # Verificar se há interesse em arquivos Excel
        has_excel = False
        
        if not self.file_types:  # Se verificando todos os tipos
            has_excel = True
        else:
            excel_types = ['.xlsx', '.xls']
            has_excel = any(ext in self.file_types for ext in excel_types)
        
        if not has_excel:
            return  # Não precisa configurar Excel
        
        print("\n📊 CONFIGURAÇÕES PARA ARQUIVOS EXCEL")
        print("-" * 35)
        print("Detectados arquivos Excel (.xlsx/.xls) para verificação.")
        print("Para análise completa é necessário o módulo 'pandas'.")
        print()
        print("Com pandas instalado você terá:")
        print("  • Contagem de planilhas e células")
        print("  • Análise de tipos de dados")
        print("  • Detecção de células vazias/corrompidas")
        print("  • Verificação estrutural completa")
        print()
        
        while True:
            excel_input = input("Instalar automaticamente dependências Excel se necessário? (S/n): ").strip().lower()
            if excel_input in ['', 's', 'sim', 'yes', 'y']:
                self.auto_install_excel = True
                print("✅ Instalação automática de dependências Excel ativada")
                break
            elif excel_input in ['n', 'nao', 'não', 'no']:
                self.auto_install_excel = False
                print("✅ Usando verificação básica de Excel (sem pandas)")
                break
            else:
                print("❌ Digite 's' para sim ou 'n' para não")
    
    def show_summary(self):
        """Exibir resumo das configurações"""
        print("\n📋 RESUMO DAS CONFIGURAÇÕES")
        print("=" * 30)
        print(f"Diretórios: {len(self.directories)}")
        for i, d in enumerate(self.directories, 1):
            print(f"  {i}. {d}")
        print(f"Arquivo de saída: {self.output_name}")
        print(f"Busca recursiva: {'Sim' if self.recursive else 'Não'}")
        if self.file_types:
            print(f"Filtros: {', '.join(self.file_types)}")
        else:
            print("Filtros: Nenhum (todos os arquivos)")
        print(f"Auto-instalar Excel: {'Sim' if self.auto_install_excel else 'Não'}")
        print("=" * 30)
    
    def confirm_execution(self):
        """Confirmar execução"""
        while True:
            confirm = input("\nDeseja prosseguir com a verificação? (S/n): ").strip().lower()
            if confirm in ['', 's', 'sim', 'yes', 'y']:
                return True
            elif confirm in ['n', 'nao', 'não', 'no']:
                return False
            else:
                print("❌ Digite 's' para sim ou 'n' para não")
    
    def execute_check(self):
        """Executar verificação de integridade"""
        print("\n🔍 EXECUTANDO VERIFICAÇÃO DE INTEGRIDADE")
        print("=" * 45)
        
        # Criar verificador customizado
        checker = CustomFileChecker(self.directories, self.recursive, self.file_types, self.auto_install_excel)
        
        try:
            # Executar verificação
            print("Iniciando verificação...")
            checker.scan_directories()
            
            # Gerar relatório em texto
            print("Gerando relatório...")
            checker.generate_text_report(self.output_name)
            
            # Mostrar resultados
            print("\n✅ VERIFICAÇÃO CONCLUÍDA!")
            print("=" * 25)
            print(f"Total de arquivos verificados: {checker.summary['total_files']}")
            print(f"Arquivos íntegros: {checker.summary['intact_files']}")
            print(f"Arquivos corrompidos: {checker.summary['corrupted_files']}")
            print(f"Arquivos inacessíveis: {checker.summary['inaccessible_files']}")
            
            if checker.summary['total_files'] > 0:
                intact_pct = (checker.summary['intact_files'] / checker.summary['total_files']) * 100
                print(f"Taxa de integridade: {intact_pct:.1f}%")
            
            print(f"\n📄 Relatório salvo em: {self.output_name}.txt")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERRO DURANTE A EXECUÇÃO!")
            print(f"Erro: {str(e)}")
            return False
    
    def run(self):
        """Executar interface interativa completa"""
        try:
            self.print_header()
            self.get_directories()
            self.get_output_settings()
            self.get_filter_options()
            self.show_summary()
            
            if self.confirm_execution():
                success = self.execute_check()
                
                if success:
                    print("\n🎉 Programa executado com sucesso!")
                    input("Pressione Enter para sair...")
                else:
                    print("\n💥 Ocorreu um erro durante a execução.")
                    input("Pressione Enter para sair...")
            else:
                print("\n❌ Operação cancelada pelo usuário.")
        
        except KeyboardInterrupt:
            print("\n\n❌ Operação cancelada pelo usuário (Ctrl+C)")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")


class CustomFileChecker(FileIntegrityChecker):
    """Versão customizada do verificador para interface interativa"""
    
    def __init__(self, directories, recursive=True, file_types=None, auto_install_excel=False):
        super().__init__(directories, output_format='txt', auto_install_excel=auto_install_excel)
        self.recursive = recursive
        self.file_types = file_types or []
    
    def should_check_file(self, file_path):
        """Verificar se arquivo deve ser processado baseado nos filtros"""
        if not self.file_types:
            return True
        
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.file_types
    
    def scan_directories(self):
        """Escanear diretórios com suporte a filtros"""
        print(f"Iniciando verificação de integridade em {len(self.directories)} diretórios")
        
        for directory in self.directories:
            print(f"Escaneando: {directory}")
            
            if not os.path.exists(directory):
                print(f"⚠️  Diretório não encontrado: {directory}")
                continue
            
            if self.recursive:
                # Percorrer recursivamente
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        if self.should_check_file(file_path):
                            self.process_file(file_path)
            else:
                # Apenas diretório principal
                try:
                    for item in os.listdir(directory):
                        file_path = os.path.join(directory, item)
                        
                        if os.path.isfile(file_path) and self.should_check_file(file_path):
                            self.process_file(file_path)
                except PermissionError:
                    print(f"⚠️  Sem permissão para ler diretório: {directory}")
        
        print(f"Verificação concluída. Total: {self.summary['total_files']} arquivos")
    
    def process_file(self, file_path):
        """Processar um arquivo individual"""
        try:
            result = self.check_file_integrity(file_path)
            self.results.append(result)
            
            # Atualizar sumário
            self.summary['total_files'] += 1
            
            if result['integrity_status'] == 'INTACT':
                self.summary['intact_files'] += 1
            elif result['integrity_status'] == 'CORRUPTED':
                self.summary['corrupted_files'] += 1
            elif result['integrity_status'] == 'INACCESSIBLE':
                self.summary['inaccessible_files'] += 1
                
            # Mostrar progresso a cada 100 arquivos
            if self.summary['total_files'] % 100 == 0:
                print(f"  Processados: {self.summary['total_files']} arquivos...")
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {e}")
    
    def generate_text_report(self, output_name):
        """Gerar relatório completo em formato texto"""
        report_file = f"{output_name}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("=" * 80 + "\n")
            f.write("                RELATÓRIO DE INTEGRIDADE DE ARQUIVOS\n")
            f.write("=" * 80 + "\n\n")
            
            # Informações gerais
            f.write(f"Data da verificação: {self.summary['scan_date']}\n")
            f.write(f"Diretórios verificados: {len(self.directories)}\n")
            for i, d in enumerate(self.directories, 1):
                f.write(f"  {i}. {d}\n")
            f.write(f"Busca recursiva: {'Sim' if self.recursive else 'Não'}\n")
            if self.file_types:
                f.write(f"Filtros aplicados: {', '.join(self.file_types)}\n")
            f.write("\n")
            
            # Resumo estatístico
            f.write("RESUMO ESTATÍSTICO\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total de arquivos verificados: {self.summary['total_files']:,}\n")
            f.write(f"Arquivos íntegros: {self.summary['intact_files']:,}\n")
            f.write(f"Arquivos corrompidos: {self.summary['corrupted_files']:,}\n")
            f.write(f"Arquivos inacessíveis: {self.summary['inaccessible_files']:,}\n")
            
            if self.summary['total_files'] > 0:
                intact_pct = (self.summary['intact_files'] / self.summary['total_files']) * 100
                corrupted_pct = (self.summary['corrupted_files'] / self.summary['total_files']) * 100
                inaccessible_pct = (self.summary['inaccessible_files'] / self.summary['total_files']) * 100
                
                f.write(f"\nPERCENTUAIS:\n")
                f.write(f"Taxa de integridade: {intact_pct:.1f}%\n")
                f.write(f"Taxa de corrupção: {corrupted_pct:.1f}%\n")
                f.write(f"Taxa de inacessibilidade: {inaccessible_pct:.1f}%\n")
            
            f.write("\n" + "=" * 80 + "\n\n")
            
            # Arquivos corrompidos
            corrupted_files = [r for r in self.results if r['integrity_status'] == 'CORRUPTED']
            if corrupted_files:
                f.write("ARQUIVOS CORROMPIDOS\n")
                f.write("-" * 20 + "\n")
                for i, result in enumerate(corrupted_files, 1):
                    f.write(f"{i:3d}. {result['file_path']}\n")
                    f.write(f"     Tamanho: {result['file_size']:,} bytes\n")
                    f.write(f"     Modificado: {result.get('last_modified', 'N/A')}\n")
                    if result.get('error'):
                        f.write(f"     Erro: {result['error']}\n")
                    if 'specific_checks' in result and 'error' in result['specific_checks']:
                        f.write(f"     Detalhes: {result['specific_checks']['error']}\n")
                    f.write("\n")
                f.write("\n")
            
            # Arquivos inacessíveis
            inaccessible_files = [r for r in self.results if r['integrity_status'] == 'INACCESSIBLE']
            if inaccessible_files:
                f.write("ARQUIVOS INACESSÍVEIS\n")
                f.write("-" * 21 + "\n")
                for i, result in enumerate(inaccessible_files, 1):
                    f.write(f"{i:3d}. {result['file_path']}\n")
                    if result.get('error'):
                        f.write(f"     Erro: {result['error']}\n")
                    f.write("\n")
                f.write("\n")
            
            # Lista completa de todos os arquivos
            f.write("LISTA COMPLETA DE ARQUIVOS VERIFICADOS\n")
            f.write("-" * 38 + "\n")
            f.write("Status | Tamanho    | Arquivo\n")
            f.write("-" * 60 + "\n")
            
            status_symbols = {
                'INTACT': '  ✅   ',
                'CORRUPTED': '  ❌   ',
                'INACCESSIBLE': '  🚫   ',
                'UNKNOWN': '  ❓   '
            }
            
            for result in sorted(self.results, key=lambda x: x['file_path']):
                status = result['integrity_status']
                symbol = status_symbols.get(status, '  ?   ')
                size = f"{result['file_size']:>10,}"
                file_path = result['file_path']
                
                f.write(f"{symbol} | {size} | {file_path}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("Relatório gerado pelo Verificador de Integridade de Arquivos\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")


def main():
    """Função principal do executável interativo"""
    try:
        interactive_checker = InteractiveFileChecker()
        interactive_checker.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()