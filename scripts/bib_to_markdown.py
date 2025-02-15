from pybtex.database.input import bibtex
from collections import defaultdict
from datetime import datetime

def bib_to_markdown(bib_file_path, highlight_author, output_file_path):
    """
    Convert a BibTeX file to a markdown format with specified author highlighted.
    """
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_file_path)
    
    entries_by_year = defaultdict(list)
    for key, entry in bib_data.entries.items():
        year = entry.fields.get('year', 'Unknown')
        entries_by_year[year].append(entry)
    
    sorted_years = sorted(entries_by_year.keys(), reverse=True)
    markdown_lines = [f"# Publications\n"]
    
    for year in sorted_years:
        #markdown_lines.append(f"\n## {year}")
        entries = sorted(entries_by_year[year], 
                        key=lambda x: x.fields.get('month', ''), 
                        reverse=True)
        
        for entry in entries:
            authors = []
            for author in entry.persons['author']:
                author_name = ' '.join(str(part) for part in author.rich_first_names + author.rich_last_names)
                if highlight_author.lower() in author_name.lower():
                    author_name = f"**{author_name}**"
                authors.append(author_name)
            
            author_string = ', '.join(authors)
            title = entry.fields.get('title', 'Untitled').strip('{}')
            venue = entry.fields.get('journal', 
                                   entry.fields.get('booktitle', 
                                                  'Unknown Venue')).strip('{}')
            
            volume = entry.fields.get('volume', '')
            number = entry.fields.get('number', '')
            pages = entry.fields.get('pages', '')
            
            extra_info = []
            if volume:
                extra_info.append(f"{volume}")
            if number:
                extra_info.append(f"({number})")
            if pages:
                extra_info.append(f": {pages}")
            
            extra_info_str = ' '.join(extra_info)
            
            markdown_lines.append(f"\n- {author_string}:  \n  _"{title}"_  \n  {venue} {extra_info_str} ({year})")
    
    markdown_content = '\n'.join(markdown_lines)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

if __name__ == "__main__":
    bib_to_markdown('publications.bib', 'Gabriele Scrivanti', 'publications.md')
