import requests
from bs4 import BeautifulSoup
import os
import chardet  # Para detectar a codificação do arquivo
import re
import unicodedata

def remover_acentos(texto):
    """
    Remove acentos e caracteres especiais de uma string.
    """
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).replace(" ", "_").upper()

class WebScraper:
    def __init__(self, url_base, pasta_destino=r"D:\Documents\GitHub\bi-acidentes-rodovias\data"):
        """
        Classe para baixar arquivos CSV com nomes formatados corretamente.

        Parâmetros:
        - url_base (str): URL da página onde estão os arquivos CSV.
        - pasta_destino (str): Diretório onde os arquivos baixados serão salvos.
        """
        self.url_base = url_base
        self.pasta_destino = pasta_destino

        # Criar a pasta de destino se não existir
        if not os.path.exists(self.pasta_destino):
            os.makedirs(self.pasta_destino)

    def obter_links_e_nomes(self):
        """
        Obtém os links dos arquivos CSV e os respectivos nomes das rodovias.

        Retorna:
        - Uma lista de tuplas no formato (nome_rodovia, link_download).
        """
        response = requests.get(self.url_base)

        if response.status_code != 200:
            raise Exception(f"Erro ao acessar {self.url_base}: Status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        arquivos = []

        # Percorre todas as tags <a> que têm a classe "heading"
        for link_rodovia in soup.find_all("a", class_="heading"):
            titulo = link_rodovia.get("title", "").strip()
            if not titulo:
                titulo = link_rodovia.get_text(strip=True)

            # Extrai o nome da rodovia
            match = re.search(r"Demonstrativos de Acidentes\s*-\s*(.+)", titulo, re.IGNORECASE)
            if match:
                nome_rodovia = remover_acentos(match.group(1))
                link_recurso = link_rodovia["href"]
                url_recurso = f"https://dados.antt.gov.br{link_recurso}"
                
                # Acessar a página do recurso para encontrar o link de download do CSV
                response_recurso = requests.get(url_recurso)
                if response_recurso.status_code == 200:
                    soup_recurso = BeautifulSoup(response_recurso.text, "html.parser")
                    link_download_tag = soup_recurso.find("a", class_="resource-url-analytics", href=True)
                    if link_download_tag and link_download_tag["href"].endswith(".csv"):
                        arquivos.append((nome_rodovia, link_download_tag["href"]))

        if not arquivos:
            raise Exception("Nenhum arquivo CSV encontrado na página.")

        return arquivos

    def converter_para_utf8(self, caminho_arquivo):
        """
        Converte um arquivo CSV para UTF-8.
        """
        with open(caminho_arquivo, "rb") as f:
            raw_data = f.read()
            encoding_detectado = chardet.detect(raw_data)["encoding"]

        if encoding_detectado is None:
            print(f"⚠️ Não foi possível detectar a codificação de {caminho_arquivo}. Pulando conversão.")
            return

        if encoding_detectado.lower() != "utf-8":
            print(f"🔄 Convertendo {caminho_arquivo} de {encoding_detectado} para UTF-8...")
            with open(caminho_arquivo, "r", encoding=encoding_detectado, errors="ignore") as f:
                conteudo = f.read()

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)

            print(f"✅ Conversão para UTF-8 concluída: {caminho_arquivo}")

    def baixar_arquivos_csv(self):
        """
        Baixa todos os arquivos CSV encontrados e renomeia para o padrão definido.
        """
        arquivos = self.obter_links_e_nomes()

        for nome_rodovia, link in arquivos:
            nome_formatado = f"{nome_rodovia}.csv"
            caminho_arquivo = os.path.join(self.pasta_destino, nome_formatado)

            print(f"📥 Baixando: {nome_formatado} ...")
            response = requests.get(link)

            if response.status_code == 200:
                with open(caminho_arquivo, "wb") as file:
                    file.write(response.content)
                print(f"✅ Arquivo salvo em: {caminho_arquivo}")

                # Converter para UTF-8
                self.converter_para_utf8(caminho_arquivo)

            else:
                print(f"❌ Erro ao baixar {nome_formatado}: Status {response.status_code}")

# Uso da classe
if __name__ == "__main__":
    url_base = "https://dados.antt.gov.br/dataset/acidentes-rodovias"
    scraper = WebScraper(url_base)
    scraper.baixar_arquivos_csv()
