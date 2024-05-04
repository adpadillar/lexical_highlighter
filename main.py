import re

operators = re.compile(r'\=\=|\!\=|\<\=|\>\=|\=|\+\=|\-\=|\<|\>|\+|\-|\*\*|\/\/|\*|\/|\%') # this regex is done
literals = re.compile(r'(\d+\.\d+|\d+|True|False|None|".*?"|\'.*?\')') # this regex is done
comments = re.compile(r'(#.*)') # this regex is done
keywords = re.compile(r'(def|if|else|elif|return|class|for|while|break|continue|and|or|not)') # this regex is done
identifiers = re.compile(r'([a-zA-Z_]\w*)') # this regex is done
data_structs = re.compile(r'(\[.*?\]|\(.*?,.*?\)|\{.*?\})')
# this should match lists [1, 2, 3] tuples (1, 2, 3) and dictionaries {1: 2, 3: 4}

def get_first_match(start: int, code: str):
  preceding_char = code[max(0, start - len("</span> ")):][0]
  code = code[start:]

  oper_match = operators.match(code)
  lit_match = literals.match(code)
  com_match = comments.match(code)
  key_match = keywords.match(code)
  id_match = identifiers.match(code)
  ds_match = data_structs.match(code)

  # check where is each of the matches, and return the first one
  matches = [oper_match, lit_match, com_match, key_match, id_match, ds_match]
  matches = [m for m in matches if m is not None]
  if len(matches) == 0:
    return None, None
  
  sorted_matches = sorted(matches, key=lambda x: x.start())
  first_match = sorted_matches[0]

  if first_match == oper_match:
    return first_match, "operator"
  elif first_match == lit_match:
    return first_match, "literal"
  elif first_match == com_match:
    return first_match, "comment"
  elif first_match == key_match:
    next_char = code[first_match.end()]
    # the next char cannot be a letter or a number or a _
    if next_char.isalnum() or next_char == "_":
      return None, None
    return first_match, "keyword"
  elif first_match == id_match:
    return first_match, "identifier"
  elif first_match == ds_match:
    if preceding_char.isalnum():
      return None, None
    return first_match, "data-structure"
  
def main():
  input_file = open('input.txt', 'r')
  template = open('template.html', 'r')
  out_html = open('output.html', 'w')

  code = input_file.read()

  i = 0
  while i < len(code):
    first_march, type_match = get_first_match(i, code)

    if first_march is None:
      i += 1
      continue
    
    code_before_match = code[:first_march.start() + i]
    code_after_match = code[first_march.end() + i:]
    new_middle = f'<span class="{type_match}">{first_march.group()}</span>'

    code = code_before_match + new_middle + code_after_match
    i = i + first_march.start() + len(new_middle)

  out_html_str = template.read().replace("{{CODE}}", code)
  out_html.write(out_html_str)

  input_file.close()
  template.close()
  out_html.close()

if __name__ == '__main__':
  main()
