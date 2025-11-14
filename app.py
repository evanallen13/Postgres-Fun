from flask import Flask, request, jsonify
from src.post import POSTGRES_HOST
import json

app = Flask(__name__)

# Initialize database connection
pg_db = POSTGRES_HOST()

@app.route('/')
def home():
    """Home endpoint with API documentation"""
    return {
        "message": "PostgreSQL CRUD API",
        "endpoints": {
            "GET /": "This documentation",
            "POST /init": "Initialize database",
            "GET /documents": "Get all documents",
            "POST /documents": "Create a new document",
            "DELETE /documents": "Delete all documents",
            "DELETE /documents/<int:doc_id>": "Delete a specific document"
        }
    }

@app.route('/init', methods=['POST'])
def init_database():
    """Initialize the database tables"""
    try:
        pg_db.init_db()
        return jsonify({
            "status": "success",
            "message": "Database initialized successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get all documents from the database"""
    try:
        documents = pg_db.get_documents()
        # Convert to list of dictionaries for JSON response
        result = []
        for doc in documents:
            result.append({
                "id": doc[0],
                "content": doc[1]
            })
        
        return jsonify({
            "status": "success",
            "data": result,
            "count": len(result)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents', methods=['POST'])
def create_document():
    """Create a new document"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                "status": "error",
                "message": "Content field is required"
            }), 400
        
        content = data['content']
        pg_db.insert_document(content)
        
        return jsonify({
            "status": "success",
            "message": "Document created successfully",
            "data": {"content": content}
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents', methods=['DELETE'])
def delete_all_documents():
    """Delete all documents from the database"""
    try:
        pg_db.delete_documents()
        return jsonify({
            "status": "success",
            "message": "All documents deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a specific document by ID"""
    try:
        # Add a method to delete specific document by ID
        pg_db.cur.execute("DELETE FROM documents WHERE id = %s;", (doc_id,))
        
        if pg_db.cur.rowcount == 0:
            return jsonify({
                "status": "error",
                "message": f"Document with ID {doc_id} not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "message": f"Document {doc_id} deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document by ID"""
    try:
        pg_db.cur.execute("SELECT * FROM documents WHERE id = %s;", (doc_id,))
        doc = pg_db.cur.fetchone()
        
        if not doc:
            return jsonify({
                "status": "error",
                "message": f"Document with ID {doc_id} not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": {
                "id": doc[0],
                "content": doc[1]
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/documents/<int:doc_id>', methods=['PUT'])
def update_document(doc_id):
    """Update a specific document by ID"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                "status": "error",
                "message": "Content field is required"
            }), 400
        
        content = data['content']
        
        # Check if document exists
        pg_db.cur.execute("SELECT id FROM documents WHERE id = %s;", (doc_id,))
        if not pg_db.cur.fetchone():
            return jsonify({
                "status": "error",
                "message": f"Document with ID {doc_id} not found"
            }), 404
        
        # Update the document
        pg_db.cur.execute(
            "UPDATE documents SET content = %s WHERE id = %s;",
            (content, doc_id)
        )
        
        return jsonify({
            "status": "success",
            "message": f"Document {doc_id} updated successfully",
            "data": {
                "id": doc_id,
                "content": content
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Initialize database on startup
    try:
        pg_db.init_db()
        print("✅ Database initialized on startup")
    except Exception as e:
        print(f"❌ Error initializing database on startup: {e}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)