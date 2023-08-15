import sys
import os
import re

import json

from bs4 import BeautifulSoup
from bs4 import (Tag, NavigableString)

class ReadmeArticle():
	""" Converter of manual """
	def __init__(self, html_path):
		with open(html_path, 'r', encoding='utf-8') as fp:
			html = fp.read()
		self.soup = BeautifulSoup(html, 'lxml')
		self.h1 = None
		self.sections = None
		self.pages = []
		self.html_split()
		self.clear()

	def html_split(self):
		""" Split flat html-page to sections """

		self.sections = self.soup.new_tag('structure')
		section = self.soup.new_tag('section')
		self.sections.append(section)
		for element in self.soup.article.contents:
			if type(element) == Tag:
				if element.name == 'h1':
					self.h1 = element.text
				elif element.name == 'h2':
					section = self.soup.new_tag('section')
					self.sections.append(section)
					section.append(element)
					section['data-head'] = element.text
					anchor = element.find('a', {'class':'anchor'})
					anchor['id'] = ReadmeArticle.transliterate(element.text)
				else:
					section.append(element)

	def clear(self):
		for svg in self.sections.find_all('svg'):
			svg.decompose()
		for p in self.sections.find_all('p'):
			del p['dir']
			p['class'] = 'avs-article-p'
		for a in self.sections.find_all('a', {'class': 'anchor'}):
			del a['class']
			del a['href']
		for h in self.sections.find_all(re.compile(r'h\d+')):
			del h['dir']
			del h['tabindex']
			h['class'] = 'avs-article-h' + str(re.match(r'h(\d+)', h.name).group(1))
		for a in self.sections.find_all('a'):
			if 'href' in a.attrs:
				internal = re.match(r'https://github.com/AleksVersus/easy\.nrBD#', a['href'])
				if internal is not None:
					a['class'] = 'avs-page-internal-link'
					a['href'].replace('https://github.com/AleksVersus/easy.nrBD', '')
				else:
					a['class'] = 'avs-page-external-link'
		for div in self.sections.find_all('div', {'class': 'snippet-clipboard-content'}):
			div['class'] = 'Monokai-Code'
			div.pre.unwrap()
			div.find('div', {'class': 'zeroclipboard-container'}).decompose()
			new_soup = BeautifulSoup(ReadmeArticle.stilization_qsp_code(div.get_text()), 'lxml')
			div.clear()
			p = new_soup.html.body.find('p')
			ex = (p.contents if p is not None else new_soup.html.body.contents)
			div.extend(ex)
			vid = div.contents[:]
			vid.reverse()
			for element in vid:
				if type(element) == Tag and element.name == 'br':
					element.decompose()
				elif type(element) == NavigableString:
					match = re.match(r'^[\n\s]*$', element.text)
					if match is not None:
						element.extract()
					else:
						break
				else:
					break
		for div in self.sections.find_all('div', {'class': 'highlight-source-batchfile'}):
			div['class'] = 'Monokai-Code'
			div.pre.unwrap()
			new_soup = BeautifulSoup(ReadmeArticle.stilization_qsp_code(div.get_text()), 'lxml')
			div.clear()
			p = new_soup.html.body.find('p')
			ex = (p.contents if p is not None else new_soup.html.body.contents)
			div.extend(ex)
			vid = div.contents[:]
			vid.reverse()
			for element in vid:
				if type(element) == Tag and element.name == 'br':
					element.decompose()
				elif type(element) == NavigableString:
					match = re.match(r'^[\n\s]*$', element.text)
					if match is not None:
						element.extract()
					else:
						break
				else:
					break
		for tag in self.sections.find_all(dir='auto'):
			del tag['dir']
		for ul in self.sections.find_all('ul'):
			ul['class'] = "avs-articles-structure"

	def generate_pages(self, output_folder:str, project_json:str, template_path='./template.html'):
		with open(os.path.abspath(project_json), 'r', encoding='utf-8') as fp:
			project = json.load(fp)
		base_placing = {'sections': [], 'pages': []}
		for key, value in project['non_main_pages_sections'].items():
			for el in value:
				base_placing['sections'].append(el)
				base_placing['pages'].append(key)
		with open(os.path.abspath(template_path), 'r', encoding='utf-8') as fp:
			template_html = fp.read()
		pages = {}
		keys = list(project['non_main_pages_sections'].keys())
		keys.append('main')
		for key in keys:
			pages[key] = BeautifulSoup(template_html, 'lxml')
		for section in self.sections:
			if 'data-head' in section.attrs:
				if section['data-head'] in base_placing['sections']:
					i = base_placing['sections'].index(section['data-head'])
					key = base_placing['pages'][i]
					k = key
				else:
					k = 'main'
			else:
				k = 'main'
			article = pages[k].article
			article.append(section.extract())
		for key in pages:
			with open(f'{key}.html', 'w', encoding='utf-8') as fp:
				fp.write(pages[key].prettify())



	@staticmethod
	def append_tag(tag_name:str, target, soup, attrs=None):
		new_tag = soup.new_tag('tag_name')
		target.append(new_tag)
		if attrs is not None:
			for key, value in attrs.items():
				new_tag[key] = value
		return new_tag

	@staticmethod
	def transliterate(string):
		string=string.lower()
		sword={"а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"io","ж":"zh","з":"z","и":"i","й":"j","к":"k","л":"l","м":"m","н":"n"
		,"о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"h","ц":"ts","ч":"ch","ш":"sh","щ":"sch","ъ":"_","ы":"y","ь":"_",
		"э":"a","ю":"ju","я":"ja"," ":"_"}
		text=""
		for i in string:
			if not i in sword:
				text+=i
			else:
				text+=sword[i]
		return text

	@staticmethod
	def stilization_qsp_code(code_text:str):
		# convert code_text to css
		output_text = ""
		while len(code_text)>0:
			scope_type, prev_text, scope_regexp_obj, post_text = ReadmeArticle.find_overlap_qsp_scope(code_text)
			if scope_type=='comment':
				output_text += prev_text
				andamp = scope_regexp_obj.group(1)
				excmark = scope_regexp_obj.group(2)
				comment = scope_regexp_obj.group(3)
				output_text += f'<span class="Monokai-Operator">{andamp}</span>'
				output_text += f'<span class="Monokai-Comment">{excmark}{comment}</span>'
				code_text = post_text
			elif scope_type=='string':
				output_text += prev_text
				quot_opn = scope_regexp_obj.group(1)
				quot_cls = scope_regexp_obj.group(3)
				text = scope_regexp_obj.group(2)
				output_text += f'<span class="Monokai-String">{quot_opn}{text}{quot_cls}</span>'
				code_text = post_text
			elif scope_type=='markup':
				output_text += prev_text
				output_text += f'<span class="Monokai-Markup">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='location-start':
				output_text += prev_text
				output_text += f'<span class="Monokai-StartLoc">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='location-end':
				output_text += prev_text
				output_text += f'<span class="Monokai-EndLoc">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='operacion':
				output_text += prev_text
				output_text += f'<span class="Monokai-Operator">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='operator':
				output_text += prev_text
				output_text += f'<span class="Monokai-Operator">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='koperator':
				output_text += prev_text
				output_text += f'<span class="Monokai-Koperator">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='function':
				output_text += prev_text
				output_text += f'<span class="Monokai-Func">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='varname':
				output_text += prev_text
				output_text += f'<span class="Monokai-SysVar">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='hidefunc':
				output_text += prev_text
				output_text += f'<span class="Monokai-UnFunc">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type=='number':
				output_text += prev_text
				output_text += f'<span class="Monokai-Numeric">{scope_regexp_obj.group(0)}</span>'
				code_text = post_text
			elif scope_type in ('var', 'spaces'):
				output_text += prev_text
				output_text += f'{scope_regexp_obj.group(0)}'
				code_text = post_text
			else:
				output_text += code_text
				code_text = ''
		return ReadmeArticle.replace_spaces(output_text).replace('\n','<br/>\n')

	@staticmethod
	def find_overlap_qsp_scope(string_line:str):
		maximal = len(string_line)+1
		mini_data_base = {
			"scope-name": [
				'comment',
				'string',
				'markup',
				'location-start',
				'operacion',
				'operator',
				'koperator',
				'function',
				'varname',
				'hidefunc',
				'number',
				'location-end',
				'var'
			],
			"scope-regexp":
			[
				ReadmeArticle.search_comment(string_line),
				re.search(r'("|\')([\s\S]*?)(\1)', string_line, flags=re.MULTILINE),
				re.search(r'(^\s*)(:[^\s\'\"\{\}\&][^\s\'\"\{\}\&]*?)(?=\s*($|\&amp;))', string_line, flags=re.MULTILINE),
				re.search(r'^\s*#.*?$', string_line, flags=re.MULTILINE),
				re.search(
					r'\-\=|\+\=|\*\=|\/\=|&lt;\=|&gt;\=|\-|\=|\+|\*|\/|\[|\]|\{|\}|\(|\)|\:|\&amp;|,|&lt;|&gt;',
					string_line, flags=re.MULTILINE),
				re.search(r'(?i:(\bexec|\bset|\blet|\blocal|\bview|\binclib|\bfreelib|\baddqst|\bopenqst|\bopengame|\bsavegame|\bkillqst|\bcmdclr|\bcmdclear|\ball|\bclose|\bexit|\bplay|\bsettimer|\bmenu|\bunsel|\bunselect|\bjump|\bcopyarr|\bdelact|\bwait|\bkillall|\bdynamic|\bkillvar|\bdelobj|\baddobj|\bkillobj|\bcls|\bcla|\bgs|\bxgt|\bgt|\bgoto|\bgosub|\bxgoto|\brefint|\bshowobjs|\bshowstat|\bshowacts|\bshowinput|\bmsg|(?<!\w)\*?(pl?|nl|clr|clear)))\b', string_line, flags=re.MULTILINE),
				re.search(r'\b(?i:(act|if|elseif|else|loop|while|step|end))\b', string_line, flags=re.MULTILINE),
				re.search(r'(?i:(\bobj|\bisplay|\blen|\brgb|\bmsecscount|\bno|\band|\bmod|\bcountobj|\binstr|\bisnum|\bval|\bloc|\bor|\bra?nd|\barrsize|\barrpos|\barrcomp|\bstrcomp|\bstrpos|(?<!\w)\$?(input|user_text|usrtxt|desc|maintxt|stattxt|qspver|curloc|selobj|selact|curacts|mid|(u|l)case|trim|replace|getobj|str|strfind|iif|dyneval|func|max|min|arritem)))\b', string_line, flags=re.MULTILINE),
				re.search(r'(?i:(\bnosave|\bdisablescroll|\bdisablesubex|\bdebug|\busehtml|\b(b|f|l)color|\bfsize|(?<!\w)\$?(counter|ongload|ongsave|onnewloc|onactsel|onobjsel|onobjadd|onobjdel|usercom|fname|backimage|args|result)))\b', string_line, flags=re.MULTILINE),
				re.search(r'@[\w\.]+\b', string_line, flags=re.MULTILINE),
				re.search(r'\b\d+\b', string_line, flags=re.MULTILINE),
				re.search(r'(^\s*)(\-)(.*?$)', string_line, flags=re.MULTILINE),
				re.search(r'\b[A-Za-zА-Яа-я_0-9][\w\.]*?\b', string_line, flags=re.MULTILINE)
			],
			"scope-instring":
			[]
		}
		for i, string_id in enumerate(mini_data_base['scope-name']):
			match_in = mini_data_base['scope-regexp'][i]
			mini_data_base['scope-instring'].append(
				string_line.index(match_in.group(0)) if match_in is not None else maximal)
		minimal = min(mini_data_base['scope-instring'])
		if minimal!=maximal:
			i = mini_data_base['scope-instring'].index(minimal)
			scope_type = mini_data_base['scope-name'][i]
			scope_regexp_obj = mini_data_base['scope-regexp'][i]
			scope = scope_regexp_obj.group(0)
			q = string_line.index(scope)
			prev_line = string_line[0:q]
			post_line = string_line[q+len(scope):]
			return scope_type, prev_line, scope_regexp_obj, post_line
		else:
			return None, '', '', string_line

	@staticmethod
	def search_comment(string_line:str):
		temp_line = string_line
		comment = ""
		mode = {"comment-open": False}
		while len(temp_line)>0:
			comment_start = re.search(r'(^\s*|\&amp;\s*)(!)', temp_line, flags=re.MULTILINE)
			if comment_start is not None and not mode["comment-open"]:
				scope = comment_start.group(0)
				comment += scope
				q = temp_line.index(scope)
				temp_line = temp_line[q+len(scope):]
				mode["comment-open"]=True
			elif mode["comment-open"]:
				scope_type, prev_line, scope_regexp_obj, post_line = ReadmeArticle.find_overlap_comments_scope(temp_line)
				if scope_type in ('single-string', 'single-quotes', 'single-apostrophes', 'single-scobe'):
					scope = scope_regexp_obj.group(0)
					comment += prev_line + scope
					mode["comment-open"]=False
					break # comment is enough
				elif scope_type in ('quotes', 'apostrophes', 'scobe'):
					comment += scope_regexp_obj.group(0)
					temp_line = post_line
				else:
					#error
					print('[240] Error')
					return None
			else:
				# comment is not found
				return None
		if comment != "":
			return re.search(r'(^\s*|\&amp;\s*)(!)([\s\S]*)', comment, flags=re.MULTILINE)

	@staticmethod
	def find_overlap_comments_scope(string_line:str):
		# Get string. Return scope_type, prev_line, scope_regexp_obj, post_line
		maximal = len(string_line)+1
		mini_data_base = {
			"scope-name": [
				'single-quotes',
				'single-apostrophes',
				'single-scobe',
				'single-string',
				'quotes',
				'apostrophes',
				'scobe'
			],
			"scope-regexp":
			[
				re.search(r'^[^"\n]*?"[^"]*?"[^\'"\{\n]*?$', string_line, flags=re.MULTILINE),
				re.search(r'^[^\'\n]*?\'[^\']*?\'[^\'"\{\n]*?$', string_line, flags=re.MULTILINE),
				re.search(r'^[^\{\n]*?\{[^\}]*?\}[^\'"\{\n]*?$', string_line, flags=re.MULTILINE),
				re.search(r'(^[^"\'\{]*?$)', string_line, flags=re.MULTILINE),
				re.search(r'^[^"\n]*?"[^"]*?"[^"\n]*?', string_line, flags=re.MULTILINE),
				re.search(r'^[^\'\n]*?\'[^\']*?\'[^\'\n]*?', string_line, flags=re.MULTILINE),
				re.search(r'^[^\{]*?\{[^\}]*?\}[^\{\n]*?', string_line, flags=re.MULTILINE),
			],
			"scope-instring":
			[]
		}
		for string_id in mini_data_base['scope-name']:
			i = mini_data_base['scope-name'].index(string_id)
			match_in = mini_data_base['scope-regexp'][i]
			mini_data_base['scope-instring'].append(
				string_line.index(match_in.group(0)) if match_in is not None else maximal)
		minimal = min(mini_data_base['scope-instring'])
		if minimal!=maximal:
			i = mini_data_base['scope-instring'].index(minimal)
			scope_type = mini_data_base['scope-name'][i]
			scope_regexp_obj = mini_data_base['scope-regexp'][i]
			scope = scope_regexp_obj.group(0)
			q = string_line.index(scope)
			prev_line = string_line[0:q]
			post_line = string_line[q+len(scope):]
			return scope_type, prev_line, scope_regexp_obj, post_line
		else:
			return None, '', '', string_line

	@staticmethod
	def replace_spaces(html_text:str):
		# replace spaces on &nbsp; without tags
		output_text = ""
		while len(html_text)>0:
			tag = re.search(r'<.*?>', html_text)
			if tag is not None:
				q = html_text.index(tag.group(0))
				prev_text = html_text[:q]
				post_text = html_text[q+len(tag.group(0)):]
				output_text += prev_text.replace(' ', '&nbsp;')+tag.group(0)
				html_text = post_text
			else:
				output_text += html_text.replace(' ', '&nbsp;')
				html_text = ''
		return output_text
		

def main():
	ra = ReadmeArticle('[source].html')
	ra.generate_pages('../easy.database', './proj.json', template_path='./template.html')


if __name__ == "__main__":
	main()