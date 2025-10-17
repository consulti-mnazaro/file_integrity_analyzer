#!/usr/bin/env python3
"""
Script para verificar integridade de arquivos em diretórios
Verifica se arquivos estão corrompidos ou íntegros através de diferentes métodos
"""

import os
import sys
import hashlib
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse
import logging
import subprocess

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_integrity_check.log'),
        logging.StreamHandler()
    ]
)

class ExcelDependencyManager:
    """Gerenciador de dependências para arquivos Excel"""
    
    @staticmethod
    def check_pandas_available():
        """Verificar se pandas está disponível"""
        try:
            import pandas as pd
            import openpyxl  # Para xlsx
            return True, pd.__version__
        except ImportError as e:
            missing_modules = []
            if 'pandas' in str(e):
                missing_modules.append('pandas')
            if 'openpyxl' in str(e):
                missing_modules.append('openpyxl')
            return False, missing_modules
    
    @staticmethod
    def install_excel_dependencies(auto_install=False):
        """Instalar dependências do Excel"""
        available, info = ExcelDependencyManager.check_pandas_available()
        
        if available:
            return True, f"Pandas já instalado (versão {info})"
        
        if not auto_install:
            print("\n📊 SUPORTE EXCEL APRIMORADO DISPONÍVEL!")
            print("=" * 45)
            print("Para verificação completa de arquivos Excel (.xlsx/.xls):")
            print("- Análise de planilhas e dados")
            print("- Contagem de linhas e colunas") 
            print("- Verificação de integridade estrutural")
            print("- Detecção de células corrompidas")
            print()
            print("Módulos necessários:", info)
            print()
            
            resposta = input("Instalar automaticamente? (s/N): ").strip().lower()
            if resposta not in ['s', 'sim', 'y', 'yes']:
                return False, "Instalação cancelada pelo usuário"
        
        print("📦 Instalando dependências para Excel...")
        try:
            # Instalar pandas e openpyxl
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                'pandas>=1.3.0', 'openpyxl>=3.0.0'
            ])
            
            # Verificar instalação
            available, version = ExcelDependencyManager.check_pandas_available()
            if available:
                print(f"✅ Dependências instaladas com sucesso!")
                print(f"   Pandas versão: {version}")
                return True, "Instalação concluída"
            else:
                return False, "Erro na verificação pós-instalação"
                
        except subprocess.CalledProcessError as e:
            return False, f"Erro na instalação: {e}"
        except Exception as e:
            return False, f"Erro inesperado: {e}"

class FileIntegrityChecker:
    """Classe para verificar integridade de arquivos"""
    
    def __init__(self, directories: List[str], output_format: str = 'json', auto_install_excel=False):
        self.directories = directories
        self.output_format = output_format
        self.auto_install_excel = auto_install_excel
        self.results = []
        self.excel_enhancement_checked = False
        self.summary = {
            'total_files': 0,
            'intact_files': 0,
            'corrupted_files': 0,
            'inaccessible_files': 0,
            'excel_files': 0,
            'enhanced_excel_analysis': False,
            'scan_date': datetime.now().isoformat()
        }
        
        # Extensões de arquivos conhecidos e suas verificações específicas
        self.file_handlers = {
            '.csv': self._check_csv_file,
            '.json': self._check_json_file,
            '.xlsx': self._check_excel_file,
            '.xls': self._check_excel_file,
            '.pdf': self._check_pdf_file,
            '.txt': self._check_text_file,
            '.py': self._check_python_file,
            '.sql': self._check_sql_file,
            '.xml': self._check_xml_file,
            '.zip': self._check_zip_file,
            '.rar': self._check_rar_file
        }
    
    def calculate_file_hash(self, file_path: str, algorithm: str = 'md5') -> Optional[str]:
        """Calcula hash do arquivo para verificação de integridade"""
        try:
            hash_func = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            logging.error(f"Erro ao calcular hash do arquivo {file_path}: {e}")
            return None
    
    def _check_basic_accessibility(self, file_path: str) -> Dict:
        """Verificação básica de acessibilidade do arquivo"""
        result = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': 0,
            'is_accessible': False,
            'is_readable': False,
            'permissions': '',
            'last_modified': '',
            'error': None
        }
        
        try:
            # Verificar se arquivo existe
            if not os.path.exists(file_path):
                result['error'] = 'Arquivo não encontrado'
                return result
            
            # Obter informações do arquivo
            stat_info = os.stat(file_path)
            result['file_size'] = stat_info.st_size
            result['last_modified'] = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
            result['permissions'] = oct(stat_info.st_mode)[-3:]
            result['is_accessible'] = True
            
            # Verificar se é legível
            if os.access(file_path, os.R_OK):
                result['is_readable'] = True
            
        except Exception as e:
            result['error'] = str(e)
            logging.error(f"Erro ao acessar arquivo {file_path}: {e}")
        
        return result
    
    def _check_csv_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos CSV"""
        integrity_check = {'format_valid': False, 'rows_count': 0, 'columns_count': 0, 'encoding': 'unknown'}
        
        try:
            # Tentar diferentes encodings
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        # Detectar separador
                        sample = f.read(1024)
                        f.seek(0)
                        
                        separators = [',', ';', '\t', '|']
                        separator = ','
                        for sep in separators:
                            if sample.count(sep) > sample.count(separator):
                                separator = sep
                        
                        csv_reader = csv.reader(f, delimiter=separator)
                        rows = list(csv_reader)
                        
                        integrity_check['format_valid'] = True
                        integrity_check['rows_count'] = len(rows)
                        integrity_check['columns_count'] = len(rows[0]) if rows else 0
                        integrity_check['encoding'] = encoding
                        integrity_check['separator'] = separator
                        break
                        
                except UnicodeDecodeError:
                    continue
                    
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_json_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos JSON"""
        integrity_check = {'format_valid': False, 'json_valid': False}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                integrity_check['format_valid'] = True
                integrity_check['json_valid'] = True
                integrity_check['data_type'] = type(data).__name__
                
                if isinstance(data, dict):
                    integrity_check['keys_count'] = len(data.keys())
                elif isinstance(data, list):
                    integrity_check['items_count'] = len(data)
                    
        except json.JSONDecodeError as e:
            integrity_check['error'] = f"JSON inválido: {e}"
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_excel_file(self, file_path: str) -> Dict:
        """Verificação aprimorada para arquivos Excel"""
        integrity_check = {
            'format_valid': False, 
            'sheets_count': 0,
            'verification_level': 'basic'
        }
        
        # Verificação básica primeiro (sem pandas)
        try:
            file_ext = Path(file_path).suffix.lower()
            with open(file_path, 'rb') as f:
                header = f.read(8)
                
                if file_ext == '.xlsx':
                    # XLSX é baseado em ZIP
                    if header.startswith(b'PK\x03\x04'):
                        integrity_check['format_valid'] = True
                        integrity_check['file_type'] = 'xlsx'
                elif file_ext == '.xls':
                    # XLS formato binário da Microsoft
                    if header.startswith(b'\xd0\xcf\x11\xe0'):
                        integrity_check['format_valid'] = True
                        integrity_check['file_type'] = 'xls'
                        
        except Exception as e:
            integrity_check['error'] = f"Erro na verificação básica: {e}"
            return integrity_check
        
        # Verificação avançada com pandas
        try:
            import pandas as pd
            import openpyxl
            
            integrity_check['verification_level'] = 'advanced'
            integrity_check['pandas_version'] = pd.__version__
            
            # Verificar estrutura Excel
            try:
                excel_file = pd.ExcelFile(file_path)
                integrity_check['sheets_count'] = len(excel_file.sheet_names)
                integrity_check['sheet_names'] = excel_file.sheet_names
                
                # Analisar cada planilha
                sheets_info = {}
                total_cells = 0
                
                for sheet_name in excel_file.sheet_names[:5]:  # Limitar a 5 planilhas
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_name)
                        sheet_info = {
                            'rows': len(df),
                            'columns': len(df.columns),
                            'cells': len(df) * len(df.columns),
                            'has_data': not df.empty,
                            'column_names': list(df.columns) if len(df.columns) <= 20 else f"{len(df.columns)} colunas"
                        }
                        
                        # Verificar tipos de dados
                        dtypes = df.dtypes.value_counts()
                        sheet_info['data_types'] = {str(dtype): int(count) for dtype, count in dtypes.items()}
                        
                        # Verificar dados ausentes
                        missing_data = df.isnull().sum().sum()
                        sheet_info['missing_cells'] = int(missing_data)
                        sheet_info['missing_percentage'] = round((missing_data / sheet_info['cells'] * 100), 2) if sheet_info['cells'] > 0 else 0
                        
                        sheets_info[sheet_name] = sheet_info
                        total_cells += sheet_info['cells']
                        
                    except Exception as e:
                        sheets_info[sheet_name] = {'error': str(e)}
                
                integrity_check['sheets_info'] = sheets_info
                integrity_check['total_cells'] = total_cells
                
                # Verificação de integridade estrutural
                if integrity_check['sheets_count'] > 0:
                    integrity_check['structure_valid'] = True
                else:
                    integrity_check['structure_valid'] = False
                    integrity_check['warning'] = "Arquivo Excel sem planilhas válidas"
                    
            except pd.errors.EmptyDataError:
                integrity_check['error'] = "Arquivo Excel vazio"
            except Exception as e:
                error_msg = str(e).lower()
                if 'not a zip file' in error_msg or 'bad zipfile' in error_msg:
                    integrity_check['error'] = "Arquivo Excel corrompido ou formato inválido"
                elif 'permission' in error_msg:
                    integrity_check['error'] = "Sem permissão para acessar arquivo Excel"
                else:
                    integrity_check['error'] = f"Erro na análise Excel: {e}"
                
        except ImportError as e:
            # Pandas não disponível - oferecer instalação
            missing_modules = []
            if 'pandas' in str(e):
                missing_modules.append('pandas')
            if 'openpyxl' in str(e):
                missing_modules.append('openpyxl')
                
            integrity_check['verification_level'] = 'basic'
            integrity_check['warning'] = f"Verificação limitada - módulos ausentes: {', '.join(missing_modules)}"
            integrity_check['enhancement_available'] = True
            integrity_check['missing_modules'] = missing_modules
            
            # Se formato básico é válido, mas pandas ausente
            if integrity_check.get('format_valid'):
                integrity_check['suggestion'] = "Instale pandas e openpyxl para verificação completa de Excel"
        
        return integrity_check
    
    def _check_excel_enhancement(self):
        """Verificar e oferecer melhorias para Excel na primeira vez"""
        if self.excel_enhancement_checked:
            return
            
        self.excel_enhancement_checked = True
        available, info = ExcelDependencyManager.check_pandas_available()
        
        if not available:
            print(f"\n📊 Arquivo Excel detectado!")
            success, message = ExcelDependencyManager.install_excel_dependencies(self.auto_install_excel)
            if success:
                self.summary['enhanced_excel_analysis'] = True
                print("✅ Análise Excel aprimorada ativada!")
            else:
                print(f"⚠️  {message}")
                print("💡 Verificação básica de Excel será usada")
        else:
            self.summary['enhanced_excel_analysis'] = True
    
    def _check_pdf_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos PDF"""
        integrity_check = {'format_valid': False, 'pages_count': 0}
        
        try:
            # Verificação básica de header PDF
            with open(file_path, 'rb') as f:
                header = f.read(8)
                if header.startswith(b'%PDF-'):
                    integrity_check['format_valid'] = True
                    integrity_check['pdf_version'] = header.decode('ascii', errors='ignore')
                    
                # Procurar por trailer (indicativo de PDF bem formado)
                f.seek(-1024, 2)  # Últimos 1024 bytes
                tail = f.read()
                if b'%%EOF' in tail:
                    integrity_check['has_eof'] = True
                    
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_text_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos de texto"""
        integrity_check = {'format_valid': False, 'lines_count': 0, 'encoding': 'unknown'}
        
        try:
            encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                        integrity_check['format_valid'] = True
                        integrity_check['lines_count'] = len(lines)
                        integrity_check['encoding'] = encoding
                        integrity_check['char_count'] = sum(len(line) for line in lines)
                        break
                except UnicodeDecodeError:
                    continue
                    
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_python_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos Python"""
        integrity_check = {'format_valid': False, 'syntax_valid': False}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Compilar código Python para verificar sintaxe
            compile(content, file_path, 'exec')
            integrity_check['format_valid'] = True
            integrity_check['syntax_valid'] = True
            integrity_check['lines_count'] = len(content.splitlines())
            
        except SyntaxError as e:
            integrity_check['format_valid'] = True
            integrity_check['syntax_error'] = str(e)
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_sql_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos SQL"""
        integrity_check = {'format_valid': False, 'statements_count': 0}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            integrity_check['format_valid'] = True
            integrity_check['lines_count'] = len(content.splitlines())
            
            # Contar statements básicos
            statements = content.upper().count('SELECT') + content.upper().count('INSERT') + \
                        content.upper().count('UPDATE') + content.upper().count('DELETE') + \
                        content.upper().count('CREATE') + content.upper().count('DROP')
            integrity_check['statements_count'] = statements
            
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_xml_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos XML"""
        integrity_check = {'format_valid': False, 'well_formed': False}
        
        try:
            import xml.etree.ElementTree as ET
            
            tree = ET.parse(file_path)
            integrity_check['format_valid'] = True
            integrity_check['well_formed'] = True
            integrity_check['root_tag'] = tree.getroot().tag
            
        except ImportError:
            integrity_check['error'] = "xml.etree não disponível"
        except ET.ParseError as e:
            integrity_check['format_valid'] = True
            integrity_check['xml_error'] = str(e)
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_zip_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos ZIP"""
        integrity_check = {'format_valid': False, 'files_count': 0}
        
        try:
            import zipfile
            
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                # Testar integridade do ZIP
                bad_file = zip_file.testzip()
                integrity_check['format_valid'] = True
                integrity_check['is_corrupted'] = bad_file is not None
                integrity_check['files_count'] = len(zip_file.namelist())
                
                if bad_file:
                    integrity_check['corrupted_file'] = bad_file
                    
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def _check_rar_file(self, file_path: str) -> Dict:
        """Verificação específica para arquivos RAR"""
        integrity_check = {'format_valid': False}
        
        try:
            # Verificação básica de header RAR
            with open(file_path, 'rb') as f:
                header = f.read(7)
                if header.startswith(b'Rar!\x1a\x07\x00'):
                    integrity_check['format_valid'] = True
                    integrity_check['rar_signature'] = True
                    
        except Exception as e:
            integrity_check['error'] = str(e)
        
        return integrity_check
    
    def check_file_integrity(self, file_path: str) -> Dict:
        """Verificar integridade de um arquivo específico"""
        logging.info(f"Verificando arquivo: {file_path}")
        
        # Verificação básica
        result = self._check_basic_accessibility(file_path)
        
        # Se arquivo não está acessível, retornar resultado básico
        if not result['is_accessible']:
            result['integrity_status'] = 'INACCESSIBLE'
            return result
        
        # Calcular hash do arquivo
        result['md5_hash'] = self.calculate_file_hash(file_path, 'md5')
        result['sha256_hash'] = self.calculate_file_hash(file_path, 'sha256')
        
        # Verificação específica por tipo de arquivo
        file_ext = Path(file_path).suffix.lower()
        
        # Verificar se é arquivo Excel e ativar melhorias se necessário
        if file_ext in ['.xlsx', '.xls']:
            self._check_excel_enhancement()
            self.summary['excel_files'] += 1
        
        if file_ext in self.file_handlers:
            specific_check = self.file_handlers[file_ext](file_path)
            result['specific_checks'] = specific_check
        else:
            result['specific_checks'] = {'format': 'unknown', 'message': 'Tipo de arquivo não reconhecido'}
        
        # Determinar status de integridade
        if result['is_readable']:
            if result['file_size'] == 0:
                # Arquivos vazios são considerados suspeitos, mas não necessariamente corrompidos
                result['integrity_status'] = 'UNKNOWN'
                result['warning'] = 'Arquivo vazio'
            elif 'specific_checks' in result and 'error' not in result['specific_checks']:
                result['integrity_status'] = 'INTACT'
            elif 'specific_checks' in result and 'error' in result['specific_checks']:
                result['integrity_status'] = 'CORRUPTED'
            else:
                result['integrity_status'] = 'INTACT'  # Se é legível e tem conteúdo, assumir íntegro
        else:
            result['integrity_status'] = 'CORRUPTED'
        
        return result
    
    def scan_directories(self) -> None:
        """Escanear todos os diretórios especificados"""
        logging.info(f"Iniciando verificação de integridade em {len(self.directories)} diretórios")
        
        for directory in self.directories:
            logging.info(f"Escaneando diretório: {directory}")
            
            if not os.path.exists(directory):
                logging.warning(f"Diretório não encontrado: {directory}")
                continue
            
            # Percorrer recursivamente o diretório
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    
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
                            
                    except Exception as e:
                        logging.error(f"Erro ao processar arquivo {file_path}: {e}")
        
        logging.info(f"Verificação concluída. Total de arquivos: {self.summary['total_files']}")
    
    def generate_report(self, output_file: str = None) -> None:
        """Gerar relatório de integridade"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"integrity_report_{timestamp}"
        
        if self.output_format == 'json':
            report = {
                'summary': self.summary,
                'details': self.results
            }
            
            json_file = f"{output_file}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Relatório JSON gerado: {json_file}")
        
        elif self.output_format == 'csv':
            csv_file = f"{output_file}.csv"
            
            if self.results:
                # Flatten dos resultados para CSV
                flattened_results = []
                all_fields = set()
                
                # Primeira passada para coletar todos os campos possíveis
                for result in self.results:
                    flat_result = {
                        'file_path': result.get('file_path', ''),
                        'file_name': result.get('file_name', ''),
                        'file_size': result.get('file_size', 0),
                        'integrity_status': result.get('integrity_status', ''),
                        'is_accessible': result.get('is_accessible', False),
                        'is_readable': result.get('is_readable', False),
                        'last_modified': result.get('last_modified', ''),
                        'md5_hash': result.get('md5_hash', ''),
                        'error': result.get('error', ''),
                    }
                    
                    # Adicionar informações específicas se existirem
                    if 'specific_checks' in result:
                        for key, value in result['specific_checks'].items():
                            flat_result[f'specific_{key}'] = str(value) if value is not None else ''
                    
                    flattened_results.append(flat_result)
                    all_fields.update(flat_result.keys())
                
                # Garantir que todos os registros tenham todos os campos
                for flat_result in flattened_results:
                    for field in all_fields:
                        if field not in flat_result:
                            flat_result[field] = ''
                
                # Escrever CSV
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    if flattened_results:
                        writer = csv.DictWriter(f, fieldnames=sorted(all_fields))
                        writer.writeheader()
                        writer.writerows(flattened_results)
                
                logging.info(f"Relatório CSV gerado: {csv_file}")
        
        # Sempre gerar sumário em texto
        summary_file = f"{output_file}_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=== RELATÓRIO DE INTEGRIDADE DE ARQUIVOS ===\n\n")
            f.write(f"Data da verificação: {self.summary['scan_date']}\n")
            f.write(f"Total de arquivos verificados: {self.summary['total_files']}\n")
            f.write(f"Arquivos íntegros: {self.summary['intact_files']}\n")
            f.write(f"Arquivos corrompidos: {self.summary['corrupted_files']}\n")
            f.write(f"Arquivos inacessíveis: {self.summary['inaccessible_files']}\n\n")
            
            if self.summary['total_files'] > 0:
                intact_pct = (self.summary['intact_files'] / self.summary['total_files']) * 100
                corrupted_pct = (self.summary['corrupted_files'] / self.summary['total_files']) * 100
                f.write(f"Percentual de arquivos íntegros: {intact_pct:.1f}%\n")
                f.write(f"Percentual de arquivos corrompidos: {corrupted_pct:.1f}%\n\n")
            
            # Listar arquivos corrompidos
            if self.summary['corrupted_files'] > 0:
                f.write("=== ARQUIVOS CORROMPIDOS ===\n")
                for result in self.results:
                    if result['integrity_status'] == 'CORRUPTED':
                        f.write(f"- {result['file_path']}\n")
                        if result.get('error'):
                            f.write(f"  Erro: {result['error']}\n")
                f.write("\n")
        
        logging.info(f"Sumário gerado: {summary_file}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Verificador de Integridade de Arquivos')
    parser.add_argument('directories', nargs='+', help='Diretórios a serem verificados')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', 
                        help='Formato do relatório de saída (padrão: json)')
    parser.add_argument('--output', help='Nome base do arquivo de saída (sem extensão)')
    
    args = parser.parse_args()
    
    # Verificar se diretórios existem
    valid_directories = []
    for directory in args.directories:
        if os.path.exists(directory):
            valid_directories.append(directory)
        else:
            logging.warning(f"Diretório não encontrado: {directory}")
    
    if not valid_directories:
        logging.error("Nenhum diretório válido fornecido")
        sys.exit(1)
    
    # Criar verificador e executar
    checker = FileIntegrityChecker(valid_directories, args.format)
    checker.scan_directories()
    checker.generate_report(args.output)
    
    print("\n=== SUMÁRIO DA VERIFICAÇÃO ===")
    print(f"Total de arquivos: {checker.summary['total_files']}")
    print(f"Arquivos íntegros: {checker.summary['intact_files']}")
    print(f"Arquivos corrompidos: {checker.summary['corrupted_files']}")
    print(f"Arquivos inacessíveis: {checker.summary['inaccessible_files']}")


if __name__ == "__main__":
    main()