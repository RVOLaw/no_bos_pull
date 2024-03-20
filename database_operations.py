import pyodbc

class DatabaseOperations:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_documents_for_file_number(self, file_number, requested_document_types):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        if not requested_document_types or not any(requested_document_types):
            # If no specific document types are requested or if the list contains only empty strings,
            # retrieve all document types for FILENO
            query = """
                SELECT D.DocumentPath, D.DocumentName, I.FILENO, I.CMT
                FROM IndexForm_CLS I JOIN Document D ON I.DocumentID = D.DocumentID
                WHERE I.FILENO = ?
            """
            documents = cursor.execute(query, file_number).fetchall()
        else:
            # Use placeholders for both file_number and document_types
            query = f"""
                SELECT D.DocumentPath, D.DocumentName, I.FILENO, I.CMT
                FROM IndexForm_CLS I JOIN Document D ON I.DocumentID = D.DocumentID
                WHERE I.FILENO = ? AND LOWER(I.CMT) IN ({', '.join(['?' for _ in requested_document_types])})
            """
            # Include both file_number and lowercase document_types in execute
            documents = cursor.execute(query, file_number, *requested_document_types).fetchall()

        conn.close()
        return documents
