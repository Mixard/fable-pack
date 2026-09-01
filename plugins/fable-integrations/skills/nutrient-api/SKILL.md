---
name: nutrient-api
description: Use when converting, OCRing, extracting, redacting, watermarking, signing, or form-filling documents with the Nutrient DWS API. Covers the /build endpoint, instructions JSON schemas, redaction presets, OCR language codes, and the MCP server config.
---

# Nutrient DWS Processor API

Commercial document-processing API. API key from https://dashboard.nutrient.io/sign_up/?product=processor (free tier available).

```bash
export NUTRIENT_API_KEY="pdf_live_..."
```

Every operation is a multipart POST to `https://api.nutrient.io/build` with:
- one or more file fields (field name referenced by the instructions), and
- an `instructions` JSON field: `{"parts": [...], "actions": [...], "output": {...}}`.

Supported inputs: PDF, DOCX, XLSX, PPTX, DOC, XLS, PPT, PPS, PPSX, ODT, RTF, HTML, JPG, PNG, TIFF, HEIC, GIF, WebP, SVG, TGA, EPS. Default output is PDF unless `output.type` says otherwise.

## Convert

```bash
# DOCX -> PDF
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.docx=@document.docx" \
  -F 'instructions={"parts":[{"file":"document.docx"}]}' \
  -o output.pdf

# PDF -> DOCX
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "document.pdf=@document.pdf" \
  -F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"docx"}}' \
  -o output.docx

# HTML -> PDF (note: parts entry uses "html", not "file")
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "index.html=@index.html" \
  -F 'instructions={"parts":[{"html":"index.html"}]}' \
  -o output.pdf
```

## Extract text and tables

```bash
# Plain text
-F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"text"}}'

# Tables as Excel
-F 'instructions={"parts":[{"file":"document.pdf"}],"output":{"type":"xlsx"}}'
```

## OCR

```bash
curl -X POST https://api.nutrient.io/build \
  -H "Authorization: Bearer $NUTRIENT_API_KEY" \
  -F "scanned.pdf=@scanned.pdf" \
  -F 'instructions={"parts":[{"file":"scanned.pdf"}],"actions":[{"type":"ocr","language":"english"}]}' \
  -o searchable.pdf
```

`language` accepts ISO 639-2 codes (`eng`, `deu`, `fra`, `spa`, `jpn`, `kor`, `chi_sim`, `chi_tra`, `ara`, `hin`, `rus`, ...) or full names (`english`, `german`). 100+ languages; full table: https://www.nutrient.io/guides/document-engine/ocr/language-support/

## Redact

Two strategies: `preset` and `regex`. Multiple redaction actions can be chained in one request.

```bash
# Preset-based (SSN + email)
-F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[
  {"type":"redaction","strategy":"preset","strategyOptions":{"preset":"social-security-number"}},
  {"type":"redaction","strategy":"preset","strategyOptions":{"preset":"email-address"}}]}'

# Regex-based
-F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[
  {"type":"redaction","strategy":"regex","strategyOptions":{"regex":"\\b[A-Z]{2}\\d{6}\\b"}}]}'
```

Presets: `social-security-number`, `email-address`, `credit-card-number`, `international-phone-number`, `north-american-phone-number`, `date`, `time`, `url`, `ipv4`, `ipv6`, `mac-address`, `us-zip-code`, `vin`.

## Watermark

```bash
-F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[
  {"type":"watermark","text":"CONFIDENTIAL","fontSize":72,"opacity":0.3,"rotation":-45}]}'
```

## Digital signature

```bash
# Self-signed CMS signature
-F 'instructions={"parts":[{"file":"document.pdf"}],"actions":[{"type":"sign","signatureType":"cms"}]}'
```

## Fill PDF forms

```bash
-F 'instructions={"parts":[{"file":"form.pdf"}],"actions":[
  {"type":"fillForm","formFields":{"name":"Jane Smith","email":"jane@example.com","date":"2026-02-06"}}]}'
```

Keys in `formFields` match the PDF form field names.

## MCP server

```json
{
  "mcpServers": {
    "nutrient-dws": {
      "command": "npx",
      "args": ["-y", "@nutrient-sdk/dws-mcp-server"],
      "env": {
        "NUTRIENT_DWS_API_KEY": "YOUR_API_KEY",
        "SANDBOX_PATH": "/path/to/working/directory"
      }
    }
  }
}
```

Note the different env var name: `NUTRIENT_DWS_API_KEY` for the MCP server vs `NUTRIENT_API_KEY` in the curl examples. `SANDBOX_PATH` restricts which files the server may read/write.

## Links

- API playground: https://dashboard.nutrient.io/processor-api/playground/
- Docs: https://www.nutrient.io/guides/dws-processor/
