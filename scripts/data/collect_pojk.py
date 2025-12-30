"""
POJK PDF Collection Script
Automatically download POJK (Peraturan OJK) documents from ojk.go.id

Target: 20+ PDF documents about insider trading and market regulation
"""

import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import time
import json
from typing import List, Dict
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class POJKCollector:
    """Collect POJK PDF documents from OJK website"""

    def __init__(self, output_dir: str = "data/raw/regulations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        self.metadata = []

    def search_pojk(self, keywords: List[str]) -> List[Dict]:
        """
        Search for POJK documents by keywords

        Args:
            keywords: List of search terms

        Returns:
            List of document metadata
        """
        # OJK regulation search URLs
        base_urls = [
            "https://www.ojk.go.id/id/regulasi/Pages/Default.aspx",
            "https://www.ojk.go.id/id/kanal/pasar-modal/regulasi/Default.aspx"
        ]

        found_docs = []

        for keyword in keywords:
            logger.info(f"Searching for: {keyword}")

            # Manual list of important POJK numbers
            # These are known relevant regulations
            important_pojk = [
                "POJK 30/2016",  # Transaksi Material
                "POJK 31/2016",  # Keterbukaan Informasi Transaksi Afiliasi
                "POJK 35/2015",  # Penyelenggaraan Usaha Perusahaan Pembiayaan
                "POJK 11/2020",  # Stimulus Penanganan Covid-19
                "POJK 32/2014",  # Rencana & Penyelenggaraan RUPS
                "POJK 33/2014",  # Direksi & Dewan Komisaris
                "POJK 34/2014",  # Komite Audit
                "POJK 35/2014",  # Sekretaris Perusahaan
                "POJK 13/2017",  # Penggunaan Jasa Konsultan Hukum, Akuntan, dan Penilai
            ]

            # Add to search list
            for pojk_num in important_pojk:
                found_docs.append({
                    'title': f"Peraturan OJK {pojk_num}",
                    'number': pojk_num,
                    'url': f"https://www.ojk.go.id/id/regulasi/{pojk_num.replace('/', '-').lower()}/",
                    'keywords': [keyword],
                    'source': 'ojk.go.id'
                })

        logger.info(f"Found {len(found_docs)} potential POJK documents")
        return found_docs

    def download_pdf(self, url: str, filename: str) -> bool:
        """
        Download PDF from URL

        Args:
            url: PDF URL
            filename: Local filename to save

        Returns:
            True if successful
        """
        try:
            logger.info(f"Downloading: {filename}")

            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Check if actually PDF
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' not in content_type.lower():
                logger.warning(f"Not a PDF: {content_type}")
                return False

            # Save file
            filepath = self.output_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)

            logger.info(f"✅ Downloaded: {filename} ({len(response.content) / 1024:.1f} KB)")
            return True

        except Exception as e:
            logger.error(f"❌ Download failed: {e}")
            return False

    def get_manual_pojk_list(self) -> List[Dict]:
        """
        Get manually curated list of important POJK documents
        Since web scraping OJK is complex, we use known important documents
        """
        # Based on research, these are critical POJK for insider trading detection
        pojk_list = [
            {
                'number': 'POJK 30/2016',
                'title': 'Transaksi Material dan Perubahan Kegiatan Usaha',
                'year': 2016,
                'category': 'Pasar Modal',
                'url': 'https://www.ojk.go.id/id/regulasi/Documents/Pages/Transaksi-Material-dan-Perubahan-Kegiatan-Usaha/POJK%2030%20-%202016.pdf',
                'relevance': 'HIGH'
            },
            {
                'number': 'POJK 31/2016',
                'title': 'Transaksi Afiliasi dan Benturan Kepentingan',
                'year': 2016,
                'category': 'Pasar Modal',
                'url': 'https://www.ojk.go.id/id/regulasi/Documents/Pages/Transaksi-Afiliasi-dan-Benturan-Kepentingan/POJK%2031%20-%202016.pdf',
                'relevance': 'HIGH'
            },
            {
                'number': 'POJK 33/2014',
                'title': 'Direksi dan Dewan Komisaris Emiten atau Perusahaan Publik',
                'year': 2014,
                'category': 'Pasar Modal',
                'url': 'https://www.ojk.go.id/id/regulasi/Documents/Pages/Direksi-dan-Dewan-Komisaris/POJK%2033-2014.pdf',
                'relevance': 'HIGH'
            },
            {
                'number': 'POJK 34/2014',
                'title': 'Komite Audit pada Emiten atau Perusahaan Publik',
                'year': 2014,
                'category': 'Pasar Modal',
                'url': 'https://www.ojk.go.id/id/regulasi/Documents/Pages/Komite-Audit/POJK%2034-2014.pdf',
                'relevance': 'MEDIUM'
            },
            {
                'number': 'POJK 35/2014',
                'title': 'Sekretaris Perusahaan pada Emiten atau Perusahaan Publik',
                'year': 2014,
                'category': 'Pasar Modal',
                'url': 'https://www.ojk.go.id/id/regulasi/Documents/Pages/Sekretaris-Perusahaan/POJK%2035-2014.pdf',
                'relevance': 'MEDIUM'
            },
        ]

        return pojk_list

    def collect_all(self, max_documents: int = 20) -> int:
        """
        Collect POJK documents

        Args:
            max_documents: Maximum number to download

        Returns:
            Number of successfully downloaded documents
        """
        logger.info("🚀 Starting POJK collection")
        logger.info(f"Target: {max_documents} documents")
        print()

        # Get document list
        pojk_list = self.get_manual_pojk_list()

        downloaded = 0
        failed = []

        for i, pojk in enumerate(pojk_list[:max_documents], 1):
            print(f"\n[{i}/{min(len(pojk_list), max_documents)}] {pojk['title']}")
            print("-" * 80)

            # Create filename
            filename = f"{pojk['number'].replace('/', '-')}.pdf"

            # Check if already downloaded
            if (self.output_dir / filename).exists():
                logger.info(f"⏭️  Skipping (already exists): {filename}")
                downloaded += 1
                continue

            # Download
            success = self.download_pdf(pojk['url'], filename)

            if success:
                downloaded += 1
                self.metadata.append(pojk)

                # Rate limiting - be respectful to OJK servers
                time.sleep(2)
            else:
                failed.append(pojk['number'])

            if downloaded >= max_documents:
                break

        # Save metadata
        self._save_metadata()

        # Summary
        print()
        print("=" * 80)
        print("📊 Collection Summary")
        print("=" * 80)
        print(f"✅ Successfully downloaded: {downloaded}")
        print(f"❌ Failed: {len(failed)}")
        if failed:
            print(f"   Failed documents: {', '.join(failed)}")
        print(f"📁 Saved to: {self.output_dir}")
        print()

        return downloaded

    def _save_metadata(self):
        """Save metadata to JSON"""
        metadata_file = self.output_dir / "metadata.json"

        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump({
                'collected_at': datetime.now().isoformat(),
                'total_documents': len(self.metadata),
                'documents': self.metadata
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"📝 Metadata saved: {metadata_file}")


def main():
    """Main execution"""
    print("=" * 80)
    print("📚 SENTINEL - POJK PDF Collector")
    print("=" * 80)
    print()

    collector = POJKCollector()

    # Collect documents
    downloaded = collector.collect_all(max_documents=20)

    if downloaded > 0:
        print("🎉 Collection complete!")
        print()
        print("Next steps:")
        print("  1. Review downloaded PDFs")
        print("  2. Extract text: python scripts/data/extract_pdf_text.py")
        print("  3. Build RAG: python scripts/demo_rag_quick.py")
    else:
        print("⚠️  No documents downloaded. Check URLs or internet connection.")


if __name__ == "__main__":
    main()
