import os
from PyPDF2 import PdfReader, PdfWriter

def read_pdf_files(pwd):
    # Create unlocked_files directory if it doesn't exist
    unlock_dir = 'unlocked_files'
    if not os.path.exists(unlock_dir):
        os.makedirs(unlock_dir)
    
    # Get all PDF files recursively
    pdf_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    if not pdf_files:
        print("No PDF files found in the current directory and subdirectories.")
        return
    
    # Read each PDF file
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            print(f"\nReading: {pdf_file}")
            
            # Check if PDF is encrypted
            if reader.is_encrypted:
                print(f"{pdf_file} Status: Password Protected (Encrypted)")
                try:
                    # Try to decrypt with provided password
                    reader.decrypt(pwd)
                    print("Successfully decrypted!")
                    
                    # Create a new PDF writer
                    writer = PdfWriter()
                    
                    # Add all pages to the writer
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    # Preserve directory structure in output
                    rel_path = os.path.relpath(pdf_file, '.')
                    output_path = os.path.join(unlock_dir, os.path.dirname(rel_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                    
                    # Save the unlocked PDF
                    output_file = os.path.join(output_path, f"{os.path.basename(pdf_file)}")
                    with open(output_file, 'wb') as output:
                        writer.write(output)
                    print(f"Saved unlocked file to: {output_file}")
                    
                except Exception as e:
                    print(f"Failed to decrypt: {str(e)}")
                    continue
            else:
                print(f"{pdf_file} Status: Not Password Protected")
                continue
        except Exception as e:
            print(f"Error reading {pdf_file}: {str(e)}")

if __name__ == "__main__":
    print("Enter Common password for all pdf > ", end="")
    pwd = input()
    read_pdf_files(pwd)