import argparse
import os
from docling.document_converter import DocumentConverter
from guardrails.guardrails import Guardrails

def parse_document(file_path: str) -> str:
    """
    Parse a document (PDF/DOCX/TXT) using IBM Docling and return extracted text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    #Validate correct file path
    Guardrails.validate_file_type(file_path)

    #Validate size limit for the file
    Guardrails.validate_file_size(file_path)

    parser = DocumentConverter()
    doc = parser.convert(file_path).document

    # Extract raw text (Docling also supports structure extraction if needed)
    text_content = doc.export_to_text()

    return text_content


def main():
    # Step 1: Setup argparse for resume(s) and JD input
    parser = argparse.ArgumentParser(description="Resume + JD Processing Pipeline")

    parser.add_argument(
        "--resumes",
        nargs="+",#indicates more than 1 arguments processing
        required=True,
        help="Path(s) to resume file(s) (PDF/DOCX/TXT)",
    )
    parser.add_argument(
        "--jd",
        required=True,
        help="Path to Job Description file (PDF/DOCX/TXT)",
    )

    args = parser.parse_args()

    # Step 2: Parse resumes and JD using IBM Docling
    print("\nParsing Resumes...")
    for resume_path in args.resumes:
        try:
            resume_text = parse_document(resume_path)
            #Validate offensive language does not exist
            Guardrails.validate_prohibited_content(resume_text)
            print(f"\nParsed Resume: {resume_path}\n")
            print(resume_text[:500])  # print first 500 chars as preview
        except Exception as e:
            print(f"Failed to parse {resume_path}: {e}")

    print("\nParsing JD...")
    try:
        jd_text = parse_document(args.jd)
        # Validate offensive language does not exist
        Guardrails.validate_prohibited_content(jd_text)
        print(f"\nParsed JD: {args.jd}\n")
        print(jd_text[:500])
    except Exception as e:
        print(f"Failed to parse JD: {e}")


if __name__ == "__main__":
    main()
