from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

# Load the JSON data
with open('tags_data.json', 'r') as f:
    data = json.load(f)
    search_index = data['searchIndex']

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '').lower().strip()
    
    if not search_term:
        return ''  # Return empty string for empty search
        
    # Look up the term in our search index
    result = search_index.get(search_term)
    
    if result:
        # If we found an exact match
        html = f'''
        <tr>
            <td>{result['tag']}</td>
            <td>{result['category']}</td>
            <td>{result['postCount']}</td>
            <td>{''.join(f'<span class="alias-tag">{alias}</span>' for alias in result['aliases'])}</td>
        </tr>
        '''
        return html
    
    # If no exact match, search for partial matches
    matches = []
    search_terms = search_term.split()
    for term in search_terms:
        for key, value in search_index.items():
            if term in key.lower():
                if value not in matches:  # Avoid duplicates
                    matches.append(value)
    
    if matches:
        html = ''
        for match in matches[:5]:  # Limit to 5 results
            html += f'''
            <tr>
                <td>{match['tag']}</td>
                <td>{match['category']}</td>
                <td>{match['postCount']}</td>
                <td>{''.join(f'<span class="alias-tag">{alias}</span>' for alias in match['aliases'])}</td>
            </tr>
            '''
        return html
    
    return '<tr><td colspan="4">No matches found</td></tr>'

if __name__ == '__main__':
    app.run(debug=True)
