# NFe XML to Excel Parser (`XMLtoXLSX`)

A lightweight, automated Python pipeline designed to extract structured metadata from Brazilian Electronic Invoices (NF-e) in XML format and compile them into an Excel (`.xlsx`) spreadsheet.

---

## Overview

Processing fiscal documents manually is repetitive and prone to error. **XMLtoXLSX** automates batch extraction from NF-e XML files, targeting essential operational and logistic records:

- **Invoice ID (`@Id`)**: The unique access key of the electronic invoice.
- **Issuer / Company (`xNome`)**: Legal business name of the issuer (`emit`).
- **Recipient / Customer (`xNome`)**: Legal business or client name of the destination (`dest`).
- **Delivery Address (`enderDest`)**: Recipient's destination address object/structure.
- **Gross Weight (`pesoB`)**: Logistic gross cargo weight if declared under transport (`transp`), with automatic fallback to `"Não Informado"`.

---

## Architecture & Workflow

```text
  XMLtoXLSX/nfs/
   ├── invoice_01.xml ──┐
   ├── invoice_02.xml ──┼──> [ xmltodict ] ──> [ Data Normalization ] ──> [ Pandas DataFrame ] ──> Nfs.xlsx
   └── ...            ──┘
```

1. **Batch Scan:** Reads all files located in the target directory (`XMLtoXLSX/nfs/`).
2. **Schema Adaptation:** Handles both standard NF-e structures (`<NFe>`) and processed authorization distributions (`<nfeProc><NFe>`).
3. **Defensive Extraction:** Validates optional logistics nodes (such as carrier freight volume / gross weight).
4. **Export:** Aggregates records into a structured tabular format and generates `Nfs.xlsx`.

---

## Prerequisites & Requirements

Ensure you have Python 3.8+ installed. Install the required dependencies via `pip`:

```bash
pip install pandas xmltodict openpyxl
```

*(Note: `openpyxl` is required by Pandas to write modern `.xlsx` files).*

---

## Project Structure

```text
.
├── XMLtoXLSX/
│   └── nfs/               # Directory containing raw .xml invoice files
├── main.py                # Extraction script
├── Nfs.xlsx               # Output generated Excel workbook
└── README.md
```

---

## Usage

1. Place your target `.xml` invoice files inside the folder:
   ```bash
   XMLtoXLSX/nfs/
   ```

2. Run the extraction script:
   ```bash
   python main.py
   ```

3. Open the generated `Nfs.xlsx` file in Microsoft Excel, LibreOffice Calc, or Google Sheets.

---

## Extracted Schema

| Column Name | Source XML Tag | Description | Sample Value |
|:---|:---|:---|:---|
| `File_ID` | `infNFe['@Id']` | Unique 44-digit Access Key | `NFe3524...` |
| `Company` | `emit/xNome` | Issuer Legal Name | `Empresa Exemplo LTDA` |
| `client_name` | `dest/xNome` | Recipient Name | `Cliente Final S/A` |
| `Address` | `dest/enderDest` | Full Destination Address | `{'xLgr': 'Av...', ...}` |
| `Weight` | `transp/vol/pesoB` | Cargo Gross Weight | `125.50` / `Não Informado` |

---

## Recommended Enhancements

- [ ] **Address Flattening:** Unpack nested address keys (`xLgr`, `nro`, `xBairro`, `xMun`, `UF`, `CEP`) into dedicated columns.
- [ ] **File Type Guard:** Add `if file_name.endswith('.xml'):` to skip temporary files or hidden files (like `.DS_Store`).
- [ ] **Value & Date Parsing:** Extract total invoice amount (`vNF`) and emission date (`dhEmi`).
